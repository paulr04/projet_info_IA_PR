import csv
import re
import ast

def recherche_vehicules_flexible(fichier_csv):
    champs_recherche = [
        "marque", "modele", "prix_jour", "masse", "vitesse_max", "puissance",
        "volume_utile", "nb_places", "type_moteur", "dimensions",
        "type_vehicule", "boite_vitesse"
    ]

    # Chargement du fichier
    with open(fichier_csv, newline='', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)
        vehicules = []
        for ligne in lecteur:
            for champ in ligne:
                if champ in ['prix_jour', 'masse', 'vitesse_max', 'puissance', 'volume_utile', 'entretien_annuel']:
                    ligne[champ] = float(ligne[champ])
                elif champ == 'nb_places':
                    ligne[champ] = int(ligne[champ])
                elif champ == 'dispo':
                    ligne[champ] = ligne[champ] == 'True'
                elif champ == 'dimensions':
                    ligne[champ] = ast.literal_eval(ligne[champ])
            vehicules.append(ligne)

    print("\nChamps disponibles pour la recherche (ex: prix_jour <= 50):\n")
    print(", ".join(champs_recherche))
    print("\nTapez 'ok' quand vous avez fini d'entrer vos critères.\n")

    criteres = []
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
                elif isinstance(val_csv, tuple):
                    val = ast.literal_eval(val)
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
                f"{v['description']}"
            ]
            for champ, _, _ in criteres:
                if champ not in ['prix_jour', 'marque', 'modele']:
                    infos.append(f"{champ}: {v[champ]}")
            print(" - " + ", ".join(infos))
    else:
        print("\n Aucun véhicule ne correspond aux critères.")

recherche_vehicules_flexible("data/vehicules.csv")