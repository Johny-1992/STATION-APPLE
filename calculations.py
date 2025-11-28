# calculations.py
from config import PRICES, PUMPS

def calculate_litres_amounts(index_start: dict, index_end: dict):
    """
    index_start et index_end sont des dictionnaires {bec: valeur_index}
    Retourne un dictionnaire {bec: {'litres': X, 'montant': Y}}
    """
    results = {}
    total_litres = 0
    total_amount = 0

    for bec, fuel in PUMPS.items():
        start = index_start.get(bec, 0)
        end = index_end.get(bec, 0)
        litres = max(0, end - start)
        montant = litres * PRICES[fuel]

        results[bec] = {
            "fuel": fuel,
            "litres": litres,
            "montant": montant
        }
        total_litres += litres
        total_amount += montant

    results["total"] = {
        "litres": total_litres,
        "montant": total_amount
    }
    return results
