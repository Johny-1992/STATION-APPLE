from config import PRICES, BECS

def calcul_litres(index_debut, index_fin):
    """Calcule le nombre de litres vendus"""
    return index_fin - index_debut

def calcul_montant(bec, litres):
    """Calcule le montant pour un bec donné"""
    carburant = BECS.get(bec, "essence")  # default essence
    prix = PRICES[carburant]
    return litres * prix

def calcul_station(index_dict):
    """
    index_dict = {
        "1a": (6666000, 6666100),
        "1b": (5555000, 5555100),
        ...
    }
    Retourne un dictionnaire avec litres et montant par bec
    """
    result = {}
    total_global = 0
    for bec, (debut, fin) in index_dict.items():
        litres = calcul_litres(debut, fin)
        montant = calcul_montant(bec, litres)
        result[bec] = {"litres": litres, "montant": montant}
        total_global += montant
    result["total"] = total_global
    return result
