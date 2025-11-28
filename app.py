from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import pandas as pd
from fpdf import FPDF

POMPES = {
    "1a": {"carburant": "Essence", "prix": 3830},
    "1b": {"carburant": "Mazout", "prix": 3200},
    "2a": {"carburant": "Essence", "prix": 3830},
    "2b": {"carburant": "Mazout", "prix": 3200},
    "3a": {"carburant": "Essence", "prix": 3830},
    "3b": {"carburant": "Mazout", "prix": 3200}
}

class StationAppleApp(App):
    def build(self):
        self.title = "STATION APPLE"
        self.inputs = {}
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        layout.add_widget(Label(text="STATION APPLE", font_size=22))

        grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        for bec, info in POMPES.items():
            grid.add_widget(Label(text=f"{bec} ({info['carburant']})"))
            self.inputs[f"{bec}_start"] = TextInput(hint_text="Index début", multiline=False)
            grid.add_widget(self.inputs[f"{bec}_start"])
            self.inputs[f"{bec}_end"] = TextInput(hint_text="Index fin", multiline=False)
            grid.add_widget(self.inputs[f"{bec}_end"])

        layout.add_widget(grid)

        layout.add_widget(Label(text="Prix par litre"))

        self.price_inputs = {}
        price_grid = GridLayout(cols=2)
        for bec, info in POMPES.items():
            price_grid.add_widget(Label(text=f"{bec}"))
            self.price_inputs[bec] = TextInput(text=str(info["prix"]), multiline=False)
            price_grid.add_widget(self.price_inputs[bec])

        layout.add_widget(price_grid)

        btn = Button(text="CALCULER")
        btn.bind(on_press=self.calculer)
        layout.add_widget(btn)

        self.result_label = Label(text="")
        layout.add_widget(self.result_label)

        return layout

    def calculer(self, instance):
        total_general = 0
        lignes = []

        for bec, info in POMPES.items():
            try:
                debut = int(self.inputs[f"{bec}_start"].text)
                fin = int(self.inputs[f"{bec}_end"].text)
                prix = float(self.price_inputs[bec].text)
                litres = fin - debut
                total = litres * prix
                total_general += total

                lignes.append({
                    "Bec": bec,
                    "Carburant": info["carburant"],
                    "Litres": litres,
                    "Prix": prix,
                    "Total": total
                })
            except:
                pass

        texte = ""
        for l in lignes:
            texte += f"{l['Bec']} : {l['Litres']} L x {l['Prix']} = {l['Total']} FC\n"

        texte += f"\nTOTAL GÉNÉRAL = {total_general} FC"
        self.result_label.text = texte

        self.export_pdf(lignes)
        self.export_excel(lignes)

    def export_pdf(self, data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="RAPPORT - STATION APPLE", ln=True)
        pdf.ln(10)

        for d in data:
            pdf.cell(200, 10, txt=f"{d['Bec']} {d['Carburant']} : {d['Litres']} L = {d['Total']} FC", ln=True)

        pdf.output("rapport_station.pdf")

    def export_excel(self, data):
        df = pd.DataFrame(data)
        df.to_excel("rapport_station.xlsx", index=False)

if __name__ == "__main__":
    StationAppleApp().run()
