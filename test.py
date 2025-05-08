import csv
import re

TYPES_VEHICULE = ["berline", "citadine", "avion", "bateau", "SUV", "special", "camion", "fourgon", "militaire"]
TYPES_MOTEUR = ["essence", "diesel", "electrique", "hybride"]
BOITES_VITESSE = ["manuelle", "automatique"]

def load_vehicules(fichier_csv):
    with open(fichier_csv, newline='', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)
        vehicules = []
        for ligne in lecteur:
            for champ in ligne:
                if champ in ['prix_jour', 'masse', 'vitesse_max', 'puissance', 'volume_utile', 'entretien_annuel', 'hauteur']:
                    ligne[champ] = float(ligne[champ])
                elif champ == 'nb_places':
                    ligne[champ] = int(ligne[champ])
                elif champ == 'dispo':
                    ligne[champ] = ligne[champ] == 'True'
            vehicules.append(ligne)
    return vehicules

def criteres(fichier_csv):
    # Liste prédéfinie des types de véhicules

    champs_recherche = [
        "marque", "modele", "prix_jour", "masse", "vitesse_max", "puissance",
        "volume_utile", "nb_places", "type_moteur", "hauteur", "boite_vitesse"
    ]
    
    # Demander à l'utilisateur de spécifier un type de véhicule parmi la liste prédéfinie
    print("\nType de véhicule obligatoire. Veuillez entrer un type de véhicule.")
    print("Types disponibles : " + ", ".join(TYPES_VEHICULE))
    type_vehicule = input("> ").strip().lower()

    if type_vehicule not in TYPES_VEHICULE:
        print(f"Type de véhicule '{type_vehicule}' non valide. La recherche ne marchera pas.")
        return []
    
    criteres = [("type_vehicule", "=", type_vehicule)]  # Ajouter le type de véhicule aux critères

    print("\nREMARQUE : Les champs texte ne peuvent pas être comparés avec <, >, <= ou >=.")
    print("REMARQUE : Les champs texte sont en minuscule sans accent...")
    print(f"OPTIONS type de moteur : {TYPES_MOTEUR}")
    print(f"OPTIONS type de véhicule : {TYPES_VEHICULE}")
    print(f"OPTIONS boîte de vitesse : {BOITES_VITESSE}")
    print("\nrespectez les OPTIONS sinon la recherche ne marchera pas\n")
    print("\nChamps disponibles pour la recherche (ex: prix_jour <= 50, marque = renault):\n")
    print(", ".join(champs_recherche))
    print("\nTapez 'ok' quand vous avez fini d'entrer vos critères.\n")


    while True:
        entree = input("> ").strip()
        if entree.lower() == "ok":
            break
        match = re.match(r"(\w+)\s*(<=|>=|=|<|>)\s*(.+)", entree)
        if not match:
            print("Format invalide. Exemple : prix_jour <= 50 , marque = toyota")
            continue
        champ, op, val = match.groups()
        if champ not in champs_recherche:
            print(f"Champ '{champ}' non valide.")
            continue
        if op in [">", "<", ">=", "<="] and champ in ["marque", "modele", "type_moteur", "type_vehicule", "boite_vitesse"]:
            print(f"Opérateur '{op}' non valide pour le champ texte '{champ}'.")
            continue
        criteres.append((champ, op, val))
    return criteres


def recherche(vehicules, criteres):

    op_map = {
        "=": lambda a, b: a == b,
        "<": lambda a, b: a < b,
        ">": lambda a, b: a > b,
        "<=": lambda a, b: a <= b,
        ">=": lambda a, b: a >= b,
    }

    resultats = []
    for v in vehicules:
        if not v.get("dispo", False):
            continue
        
        match_all = True
        for champ, op, val in criteres:
            val_csv = v[champ]
            try:
                if isinstance(val_csv, float):
                    val = float(val)
                elif isinstance(val_csv, int):
                    val = int(val)
                elif isinstance(val_csv, bool):
                    val = val.lower() == 'true'
            except Exception:
                match_all = False
                break
            if not op_map[op](val_csv, val):
                match_all = False
                break

        if match_all:
            resultats.append(v)

    if resultats:
        print(f"\n {len(resultats)} véhicule(s) trouvé(s) :\n")
        for v in resultats:
            infos = [
                f"ID : {v['id_vehicule']}",
                f"Prix/jour : {v['prix_jour']} €",
                f"Type : {v['type_vehicule']}",
                f"Marque : {v['marque']}",
                f"Modèle : {v['modele']}",
                f"{v['description']}\n"
            ]
            for champ, _, _ in criteres:
                if champ not in ['prix_jour', 'marque', 'modele', 'description', 'type_vehicule']:
                    infos.append(f"{champ}: {v[champ]}")
            print(" - " + ", ".join(infos))
            return resultats
    else:
        print("\nAucun véhicule ne correspond aux critères.\n")
        print("Essayez d'etre plus souple dans vos critères de recherche.\n")
        print("Vous pouvez consulter le catalogue des véhicules pour plus d'information.\n")

if __name__ == "__main__":
    vehicules = load_vehicules("data/vehicules.csv")
    criteres = criteres("data/vehicules.csv")
    resultats = recherche(vehicules, criteres)
    print("res" , resultats)