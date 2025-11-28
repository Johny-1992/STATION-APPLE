# app.py
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from calculations import calculate_litres_amounts
from fpdf import FPDF
import pandas as pd

kivy.require("2.1.0")

class StationAppleApp(App):

    def build(self):
        self.index_start_inputs = {}
        self.index_end_inputs = {}

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Créer les champs pour chaque bec
        for bec in ["1a","1b","2a","2b","3a","3b"]:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            row.add_widget(Label(text=f"{bec} Start:"))
            start_input = TextInput(multiline=False, input_filter='int')
            row.add_widget(start_input)
            self.index_start_inputs[bec] = start_input

            row.add_widget(Label(text=f"{bec} End:"))
            end_input = TextInput(multiline=False, input_filter='int')
            row.add_widget(end_input)
            self.index_end_inputs[bec] = end_input

            layout.add_widget(row)

        # Bouton calcul
        btn = Button(text="Calculer litres / montant", size_hint_y=None, height=50)
        btn.bind(on_press=self.calculate)
        layout.add_widget(btn)

        # Zone d'affichage
        self.result_label = Label(text="", halign='left', valign='top')
        layout.add_widget(self.result_label)

        return layout

    def calculate(self, instance):
        index_start = {bec: int(inp.text or 0) for bec, inp in self.index_start_inputs.items()}
        index_end = {bec: int(inp.text or 0) for bec, inp in self.index_end_inputs.items()}

        results = calculate_litres_amounts(index_start, index_end)
        text = ""
        for bec, data in results.items():
            if bec != "total":
                text += f"{bec} ({data['fuel']}): {data['litres']} L x {data['montant']/max(data['litres'],1):.0f} FC = {data['montant']} FC\n"
        text += f"\nTOTAL: {results['total']['litres']} L, Montant: {results['total']['montant']} FC"
        self.result_label.text = text

        # Générer PDF
        self.generate_pdf(results)

        # Générer Excel
        self.generate_excel(results)

    def generate_pdf(self, results):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Rapport Station Apple", ln=1)
        for bec, data in results.items():
            if bec != "total":
                pdf.cell(0, 8, f"{bec} ({data['fuel']}): {data['litres']} L, Montant: {data['montant']} FC", ln=1)
        pdf.cell(0, 8, f"TOTAL: {results['total']['litres']} L, Montant: {results['total']['montant']} FC", ln=1)
        pdf.output("rapport_station_apple.pdf")

    def generate_excel(self, results):
        df = pd.DataFrame.from_dict(results, orient='index')
        df.to_excel("rapport_station_apple.xlsx")

if __name__ == "__main__":
    StationAppleApp().run()
