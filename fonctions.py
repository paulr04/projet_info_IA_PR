from datetime import *
import re
import csv
import os
import random
from objects import *

USER_FILE = 'data/users.csv'
VEHICULES_FILE = 'data/vehicules.csv'
RESERVATIONS_FILE = 'data/reservations.csv'
TYPES_VEHICULE = ["berline", "citadine", "avion", "bateau", "SUV", "tank", "artillerie", "APC"]
TYPES_MOTEUR = ["essence", "diesel", "electrique", "hybride"]
BOITES_VITESSE = ["manuelle", "automatique"]

def generer_id_unique(FILE, champ_id):
    """
    Génère un ID unique à 9 chiffres aléatoires qui n'existe pas déjà dans le fichier CSV.
    """
    ids_existants = set()

    # Lecture des IDs existants
    if os.path.exists(FILE):
        with open(FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for ligne in reader:
                if champ_id in ligne and ligne[champ_id].isdigit():
                    ids_existants.add(ligne[champ_id])
    else:
        print("fichier introuvable")

    # Génération aléatoire jusqu'à trouver un ID non utilisé
    while True:
        nouvel_id = str(random.randint(100000000, 999999999))
        if nouvel_id not in ids_existants:
            return nouvel_id
            break


def convertir_date(date):
    """
    Convertit une date sous forme de chaîne (MM-DD-YYYY) en objet datetime.
    """
    format_date = "%m-%d-%Y"  # Format MM-DD-YYYY
    return datetime.strptime(date, format_date)

def verifier_dates(date_debut, date_fin):
    """
    Vérifie si les dates sont valides (format et ordre) et renvoie True si tout est correct.
    """
    # conversion des dates
    date_debut = convertir_date(date_debut)
    date_fin = convertir_date(date_fin)
    try:
        if date_fin >= date_debut:
            return True, date_debut, date_fin
        else:
            print("La date de fin ne peut pas être antérieure à la date de début.")
            return False, None, None
    except ValueError:
        print("Format de date incorrect. Assurez-vous que les dates sont au format MM-DD-YYYY.")
        return False, None, None

def calculer_jours_reservation(date_debut, date_fin):
    """
    Calcule le nombre de jours entre deux dates après vérification de leur validité.
    La date doit être au format MM-DD-YYYY.
    """
    try:
        # Conversion des dates en objets datetime
        format_date = "%m-%d-%Y"
        date_debut_obj = datetime.strptime(date_debut, format_date)
        date_fin_obj = datetime.strptime(date_fin, format_date)

        # Vérifier que la date de fin est après ou égale à la date de début
        if date_fin_obj >= date_debut_obj:
            # Calculer la différence en jours
            difference = date_fin_obj - date_debut_obj
            return (difference.days + 1) # On ajoute 1 jour car intervalle de date fermé
        else:
            print("La date de fin ne peut pas être antérieure à la date de début.")
            return None
    except ValueError:
        print("Format de date incorrect. Assurez-vous que les dates sont au format MM-DD-YYYY.")
        return None

def demander_input_float(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre décimal.")

def demander_input_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Entrée invalide. Veuillez entrer un entier.")

def demander_input_choix(message, options):
    print(f"{message} Options : {options}")
    while True:
        choix = input("> ").strip().lower()
        if choix in options:
            return choix
        else:
            print("Choix invalide. Veuillez choisir parmi les options données.")

def demander_input_dimensions():
    while True:
        try:
            dims = input("Dimensions (L l h) en mètres, séparées par des espaces : ").strip().split()
            if len(dims) != 3:
                raise ValueError
            return tuple(float(x) for x in dims)
        except ValueError:
            print("Format invalide. Entrez 3 nombres décimaux séparés par des espaces.")

def demander_input_bool(message):
    while True:
        val = input(f"{message} (oui/non) : ").strip().lower()
        if val in ["oui", "non"]:
            return val == "oui"
        else:
            print("Veuillez répondre par 'oui' ou 'non'.")

def demander_plaque_ajout(message,FILE,champ_id='id_vehicule'):
    ids_existants = set()

    # Lecture des IDs existants
    if os.path.exists(FILE):
        with open(FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for ligne in reader:
                if champ_id in ligne:
                    ids_existants.add(ligne[champ_id])
    else:
        print("fichier introuvable")

    while True:
        plaque = input(message).strip().upper()
        if re.match(r"^[A-Z]{2}-\d{3}-[A-Z]{2}$", plaque) and plaque not in ids_existants:
            return plaque
        else:
            print("Format invalide ou plaque existante. Utilisez le format AA-000-AA.")

def demander_plaque(message):
    """
        Demande une plaque au format AB-123-CD et vérifie qu'elle n'existe pas déjà.
        """
    while True:
        plaque = input(message).strip().upper()

        if not re.match(r"^[A-Z]{2}-\d{3}-[A-Z]{2}$", plaque):
            print("Format invalide. Utilisez le format AB-123-CD.")
            continue
        # Vérification de l'existence de la plaque
        if os.path.exists(VEHICULES_FILE):
            with open(VEHICULES_FILE, mode="r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames and "id_vehicule" in reader.fieldnames:
                    if any(row["id_vehicule"] == plaque for row in reader):
                        print("Véhicule trouvé ! ")
                        return plaque
                        continue
                    else:
                        print("Véhicule introuvable ! ")
                else:
                    print(" PROBLEME ")
                    continue

def demander_date_valide(message="Date (MM-DD-YYYY) : "):
    while True:
        date_str = input(message).strip()
        try:
            date_obj = datetime.strptime(date_str, "%m-%d-%Y").date()
            if date_obj < datetime.today().date():
                print("La date ne peut pas être antérieure à aujourd’hui.")
            else:
                return date_str
        except ValueError:
            print("Format de date invalide. Utilisez le format MM-DD-YYYY.")

def demander_id(message,FILE,id_name):
    while True:
        id_ver = input(message).strip()

        # Vérifie que l'ID est au bon format (9 chiffres)
        if not re.match(r"^\d{9}$", id_ver):
            print("Format d'ID invalide. L'ID doit contenir exactement 9 chiffres.")
            continue

        # Vérifie si l'ID existe dans le fichier CSV
        if not os.path.exists(FILE):
            print("Fichier introuvable.")
            return None

        with open(FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if any(row[id_name] == id_ver for row in reader):
                return id_ver
            else:
                print("ID introuvable.")
                break

def supprimer_ligne_par_id(fichier_csv, key, id_recherche):
    temp_file = "temp.csv"
    ligne_supprimee = False

    with open(fichier_csv, mode="r", encoding="utf-8", newline="") as fichier_in, \
         open(temp_file, mode="w", encoding="utf-8", newline="") as fichier_out:

        reader = csv.DictReader(fichier_in)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(fichier_out, fieldnames=fieldnames)
        writer.writeheader()

        for ligne in reader:
            if ligne[key] != id_recherche:
                writer.writerow(ligne)
            else:
                ligne_supprimee = True

    if ligne_supprimee:
        os.replace(temp_file, fichier_csv)
        print(f"Ligne avec l’ID {id_recherche} supprimée avec succès.")
    else:
        os.remove(temp_file)
        print(f"Aucune ligne avec l’ID {id_recherche} trouvée.")


def modifier_champ_csv_par_id(fichier_csv, id_recherche, champ_id, champ_a_modifier, nouvelle_valeur):
    temp_file = "temp.csv"
    trouve = False

    with open(fichier_csv, mode="r", encoding="utf-8", newline="") as fichier_in, \
         open(temp_file, mode="w", encoding="utf-8", newline="") as fichier_out:

        reader = csv.DictReader(fichier_in)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(fichier_out, fieldnames=fieldnames)
        writer.writeheader()

        for ligne in reader:
            if ligne[champ_id] == id_recherche:
                if champ_a_modifier in ligne:
                    ligne[champ_a_modifier] = nouvelle_valeur
                    trouve = True
                else:
                    print(f" Champ '{champ_a_modifier}' introuvable.")
                    return
            writer.writerow(ligne)

    if trouve:
        os.replace(temp_file, fichier_csv)
        print(f"Le champ {champ_a_modifier} a été mis à jour pour l'ID {id_recherche}.")
    else:
        os.remove(temp_file)
        print(f"Aucune entrée avec l'ID {id_recherche} trouvée dans le fichier.")

def trouver_value(FILE, id_recherche, champ_id, champ_id_return):
    if not os.path.exists(FILE):
        print("Fichier introuvable.")
        return None

    with open(FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if champ_id not in row or champ_id_return not in row:
                print(f"Champs '{champ_id}' ou '{champ_id_return}' introuvables dans le fichier.")
                return None
            if row[champ_id] == id_recherche:
                return row[champ_id_return]

    print(f"Valeur avec {champ_id} = {id_recherche} non trouvée.")
    return None
def info_user(id_user):
    """
    Récupère les informations d'un utilisateur à partir de son ID.
    """
    if not os.path.exists(USER_FILE):
        print("Fichier introuvable.")
        return None

    with open(USER_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["id_user"] == id_user:
                user_id = row['id_user']
                nom = row['nom']
                prenom = row['prenom']
                email = row['email']
                telephone = row['telephone']
                role = row['role']
                mot_de_passe = row['mot_de_passe']
                return User(user_id, nom, prenom, email, telephone, role, mot_de_passe)
            else:
                pass
def info_vehicule(id_vehicule):
    """
    Récupère les informations d'un véhicule à partir de son ID.
    """
    if not os.path.exists(VEHICULES_FILE):
        print("Fichier introuvable.")
        return None

    with open(VEHICULES_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["id_vehicule"] == id_vehicule:
                id_vehicule = row['id_vehicule']
                marque = row['marque']
                modele = row['modele']
                prix_jour = float(row['prix_jour'])
                masse = float(row['masse'])
                vitesse_max = float(row['vitesse_max'])
                puissance = float(row['puissance'])
                volume_utile = float(row['volume_utile'])
                nb_places = int(row['nb_places'])
                type_moteur = row['type_moteur'] 
                dimension = tuple(row['dimensions'])
                type_vehicule = row['type_vehicule']
                boite_vitesse = row['boite_vitesse']
                entretien_annuel = float(row['entretien_annuel'])
                dispo = row['dispo']
                description = row['description']
                return Vehicule(
                    id_vehicule, marque, modele, prix_jour, masse, vitesse_max, puissance,
                    volume_utile, nb_places, type_moteur, dimension, type_vehicule,
                    boite_vitesse, entretien_annuel, dispo, description
                )
            else:
                pass

def verifier_reservation(date_debut, date_fin, id_vehicule):
    lst_date_debut = []
    lst_date_fin = []
    with open(RESERVATIONS_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id_vehicule'] == id_vehicule and convertir_date(row['date_fin']).date() >= datetime.today().date():
                lst_date_debut.append(row['date_debut'])
                lst_date_fin.append(row['date_fin'])
        if lst_date_fin == [] and lst_date_debut == [] :
            print("OK RESERVATION")
        for element in lst_date_debut:
            for k in lst_date_fin:
                if convertir_date(date_debut).date() <= convertir_date(k).date() and convertir_date(date_fin).date() >= convertir_date(element).date() and lst_date_fin.index(k) == lst_date_debut.index(element):
                    print("CONFLIT DE RESERVATION")
                    return True
                    break
                else:
                    print("OK RESERVATION")
                    pass
def supprimer_facture(id_resa):
    """
    Supprime la facture associée à une réservation donnée.
    """
    fichier_pdf = f"facture_{id_resa}.pdf"
    path_save = os.path.join(os.path.abspath("factures_pdf"), fichier_pdf)

    if os.path.exists(path_save):
        os.remove(path_save)
        print(f"Facture {fichier_pdf} supprimée avec succès.")
    else:
        print(f"Aucune facture trouvée pour l'ID de réservation {id_resa}.")


def modifier_champ_csv(fichier_csv, champ_id, id_val, champs_interdits):
    # Lecture du fichier
    with open(fichier_csv, mode='r', newline='', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)
        lignes = list(lecteur)
        champs = lecteur.fieldnames

    if champ_id not in champs:
        print(f"Erreur : le champ ID '{champ_id}' n'existe pas.")
        return

    ligne_modifiee = False
    for ligne in lignes:
        if ligne[champ_id] == id_val:
            champs_modifiables = [c for c in champs if c not in champs_interdits]
            print("Champs modifiables :", champs_modifiables)

            champ_a_modifier = input("Quel champ voulez-vous modifier ? ")
            if champ_a_modifier not in champs_modifiables:
                print("Erreur : champ interdit ou inexistant.")
                return

            nouvelle_valeur = input(f"Nouvelle valeur pour '{champ_a_modifier}' : ")
            ligne[champ_a_modifier] = nouvelle_valeur
            ligne_modifiee = True
            break

    if not ligne_modifiee:
        print(f"Aucune ligne trouvée avec {champ_id} = {id_val}.")
        return

    with open(fichier_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(lignes)

    print("Modification effectuée avec succès.")