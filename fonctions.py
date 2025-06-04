'''
    Auteur :
        Paul Renaud
        Ilyann Aragon
    
    Ce fichier ne conttient pas de classes, il contient seulement des méthodes qui premettent de soulager les classees application,user,vehicule,reservation ...

    Méthodes :
        - generer_id_unique : génère un ID unique à 9 chiffres aléatoires qui n'existe pas déjà dansun fichier CSV.
        - convertir_date : convertit une date sous forme de chaîne (MM-DD-YYYY) en objet datetime.
        - verifier_dates : vérifie si les dates sont valides (format et ordre) et renvoie True si tout est correct.
        - calculer_jours_reservation : calcule le nombre de jours entre deux dates après vérification de leur validité.
        - demander_input_float : demande à l'utilisateur d'entrer un nombre décimal et gère les erreurs de saisie.
        - demander_input_int : demande à l'utilisateur d'entrer un entier et gère les erreurs de saisie.
        - demander_input_choix : demande à l'utilisateur de choisir parmi une liste d'options.
        - demander_input_bool : demande à l'utilisateur de répondre par 'oui' ou 'non' et renvoie un booléen.
        - demander_plaque_ajout : demande une plaque au format AA-000-AA et vérifie qu'elle n'existe pas déjà dans le fichier CSV (vehicule ou reservation) et l'ajoute dans ce dernier.
        - demander_plaque : demande une plaque au format AB-123-CD et vérifie qu'elle existe.
        - demander_date_valide : demande à l'utilisateur d'entrer une date au format MM-DD-YYYY et vérifie qu'elle n'est pas antérieure à la date actuelle.
        - demander_id : demande à l'utilisateur d'entrer un ID et vérifie qu'il existe dans le fichier CSV.
        - supprimer_ligne_par_id : supprime une ligne d'un fichier CSV en fonction d'un ID donné.
        - modifier_champ_csv_par_id : modifie un champ d'un fichier CSV en fonction d'un ID donné.
        - trouver_value : trouve une valeur dans un fichier CSV en fonction d'un ID donné.
        - info_user : récupère les informations d'un utilisateur à partir de son ID.
        - info_vehicule : récupère les informations d'un véhicule à partir de son ID.
        - verifier_reservation : vérifie si une réservation est possible en fonction des dates et de l'ID du véhicule.
        - supprimer_facture : supprime la facture associée à une réservation donnée.
        - modifier_champ_csv : modifie un champ d'un fichier CSV en fonction d'un ID donné avec une liste de champs interdits.
        - load_vehicules : charge les véhicules à partir d'un fichier CSV.
        - criteres : demande à l'utilisateur de spécifier des critères de recherche pour les véhicules.
        - recherche : effectue une recherche de véhicules en fonction des critères spécifiés par l'utilisateur.
        - load_vehicule_POO : charge un véhicule à partir d'une ligne de CSV.
        - load_vehicule_POO_id : charge un véhicule à partir d'une ligne de CSV en fonction de son ID.
        - lire_donnees_reservations : lit les données de réservations à partir d'un fichier CSV.
        - plot_reservations_par_mois : génère un histogramme du nombre de réservations par mois.
        - plot_reservations_par_annee : génère un histogramme du nombre de réservations par année.
        - benefice_par_annee_histogramme : génère un histogramme des bénéfices par année à partir des réservations et des véhicules.
        - benefice_par_annee : calcule le bénéfice total pour une année à choisir.
        - lire_csv : lit un fichier CSV et retourne son contenu sous forme de liste de dictionnaires.
        - reservation_vehicule_par_an : génere un histogramme du nombre de reservations pout chaque vehicule pour une année donnée.
        - plot_reservations_par_vehicule : génère un histogramme du nombre de réservations par véhicule.
        - plot_reservations_histogramme : Affiche un histogramme comparant les réservations classiques et les surclassements pour chaque véhicule à partir d'un fichier CSV.
        - plot_rentabilite_depuis_csv : Génère un graphique comparant les revenus et les coûts d'entretien annuels des véhicules, calculés à partir de deux fichiers CSV, et affiche un indice de rentabilité pour chaque véhicule.
        - load_users_POO : charge les utilisateurs à partir d'un fichier CSV et convertit les champs en types appropriés.
    '''

from datetime import *
import re
import csv
import os
import random
from objects import Client, Vehicule, Vendeur, User, Admin
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import defaultdict
from collections import Counter


USER_FILE = 'data/users.csv'
VEHICULES_FILE = 'data/vehicules.csv'
RESERVATIONS_FILE = 'data/reservations.csv'
CHAMPS_INTERDITS = ['id_user', 'id_resa', 'id_vehicule', 'role', 'mot_de_passe', 'type_moteur', 'type_vehicule', 'boite_vitesse']
NO_SURCLASSEMENT_TYPES = ["avion", "bateau", "militaire", "special",'autre', 'chantier', 'helicoptere', 'formule 1', 'rally']
TYPES_VEHICULE = ["berline", "citadine", "avion", "bateau", "SUV", "special", "camion", "utilitaire", "militaire", "4x4", "supercar", "monospace", "pick-up", "velo", "moto", "quad", "trottinette", "camionette", "bus", "minibus", "cabriolet", "roadster", "coupe", "break", "limousine", "formule 1", "rally", "helicoptere", "chantier",'autre']
TYPES_MOTEUR = ["essence", "diesel", "electrique", "hybride", 'kerosene', 'hydrogene', 'fioul', 'nucleaire', 'gaz', 'propergol', 'autre']
BOITES_VITESSE = ["manuelle", "automatique"]

def generer_id_unique(FILE, champ_id):
    """
    génère un ID unique à 9 chiffres aléatoires qui n'existe pas déjà dans un fichier CSV.
    input:
        FILE : str : chemin du fichier CSV où vérifier l'unicité de l'ID
        champ_id : str : nom de la colonne contenant les IDs (par défaut 'id_vehicule')
    output:
        str : nouvel ID unique à 9 chiffres
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
    input:
        date : str : Date au format MM-DD-YYYY
    output:
        datetime : Objet datetime correspondant à la date fournie.
    """
    format_date = "%m-%d-%Y"  # Format MM-DD-YYYY
    return datetime.strptime(date, format_date)

def verifier_dates(date_debut, date_fin):
    """
    Vérifie si les dates sont valides (format et ordre) et renvoie True si tout est correct.
    
    input:
        date_debut : str : Date de début de la réservation au format MM-DD-YYYY
        date_fin : str : Date de fin de la réservation au format MM-DD-YYYY
    output:
        tuple : (bool, date_debut, date_fin) où bool est True si les dates sont valides, False sinon.

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
    input:
        date_debut : str : Date de début de la réservation au format MM-DD-YYYY
        date_fin : str : Date de fin de la réservation au format MM-DD-YYYY
    output:
        int : Nombre de jours de réservation, ou None si les dates sont invalides ou dans le mauvais ordre.
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
    """
    Demande à l'utilisateur d'entrer un nombre décimal et gère les erreurs de saisie.
    input:
        message : str : message à afficher à l'utilisateur
    output:
        float : nombre décimal valide entré par l'utilisateur    
    """
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre décimal.")

def demander_input_int(message):
    """
    Demande à l'utilisateur d'entrer un entier et gère les erreurs de saisie.
    input:
        message : str : message à afficher à l'utilisateur
    output:
        int : entier valide entré par l'utilisateur
    """
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Entrée invalide. Veuillez entrer un entier.")

def demander_input_choix(message, options):
    """
    Demande à l'utilisateur de choisir parmi une liste d'options.
    input:
        message : str : message à afficher à l'utilisateur
        options : list : liste des options disponibles
    output:
        str : l'option choisie par l'utilisateur, ou None si l'utilisateur ne fait pas de choix valide
    """
    print(f"{message} Options : {options}")
    while True:
        choix = input("> ").strip().lower()
        if choix in options:
            return choix
        else:
            print("Choix invalide. Veuillez choisir parmi les options données.")

def demander_input_bool(message):
    """
    Demande à l'utilisateur de répondre par 'oui' ou 'non' et renvoie un booléen.

    input:
        message : str : message à afficher à l'utilisateur
    output:
        bool : True si l'utilisateur répond 'oui', False s'il répond 'non'
    """
    while True:
        val = input(f"{message} (oui/non) : ").strip().lower()
        if val in ["oui", "non"]:
            return val == "oui"
        else:
            print("Veuillez répondre par 'oui' ou 'non'.")

def demander_plaque_ajout(message,FILE,champ_id='id_vehicule'):
    """
    Demande une plaque au format AA-000-AA et vérifie qu'elle n'existe pas déjà dans le fichier CSV.
    
    input:
        message : str : message à afficher à l'utilisateur
        FILE : str : chemin du fichier CSV où vérifier l'unicité de la plaque
        champ_id : str : nom de la colonne contenant les IDs (par défaut 'id_vehicule')
    output:
        str : plaque valide au format AA-000-AA qui n'existe pas déjà dans le fichier CSV
    
    """
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
    Demande une plaque au format AB-123-CD et vérifie qu'elle existe.
    input:
        message : str : message à afficher à l'utilisateur
    output:
        str : plaque valide ou None si la plaque n'existe pas
    """
    plaque = input(message).strip().upper()

    if not re.match(r"^[A-Z]{2}-\d{3}-[A-Z]{2}$", plaque):
        print("Format invalide. Utilisez le format AB-123-CD.")
 
    # Vérification de l'existence de la plaque
    if os.path.exists(VEHICULES_FILE):
        with open(VEHICULES_FILE, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames and "id_vehicule" in reader.fieldnames:
                if any(row["id_vehicule"] == plaque for row in reader):
                    print("Véhicule trouvé ! ")
                    return plaque
                else:
                    print("Véhicule introuvable ! ")
            else:
                print(" PROBLEME ")


def demander_date_valide(message="Date (MM-DD-YYYY) : "):
    """
    Demande à l'utilisateur d'entrer une date au format MM-DD-YYYY et vérifie qu'elle n'est pas antérieure à aujourd'hui.
    input:
        message : str : message à afficher à l'utilisateur
    output:
        str : date valide au format MM-DD-YYYY
    """
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
    """
    input : 
            message : str : message à afficher à l'utilisateur
            FILE : str : chemin du fichier CSV
            id_name : str : nom de la colonne contenant les ID
    output : 
            str : ID valide entré par l'utilisateur

    Demande à l'utilisateur d'entrer un ID et vérifie qu'il existe dans le fichier CSV.
    """
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
    """
    Supprime une ligne d'un fichier CSV en fonction d'un ID donné.
    input:
        fichier_csv : str : Chemin du fichier CSV à modifier
        key : str : Nom de la colonne contenant l'ID
        id_recherche : str : ID de la ligne à supprimer
    output:
        None
    """
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
    """
    Modifie un champ d'un fichier CSV en fonction d'un ID donné.

    input:
        fichier_csv : str : Chemin du fichier CSV à modifier
        id_recherche : str : ID de la ligne à modifier
        champ_id : str : Nom de la colonne contenant l'ID
        champ_a_modifier : str : Nom du champ à modifier
        nouvelle_valeur : str : Nouvelle valeur à attribuer au champ
    output:
        None
    """
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
    """
    trouve une valeur dans un fichier CSV en fonction d'un ID donné.
    input:
        FILE : str : chemin du fichier CSV
        id_recherche : str : ID à rechercher
        champ_id : str : nom de la colonne contenant l'ID
        champ_id_return : str : nom de la colonne dont on veut récupérer la valeur
    output:
        str : valeur trouvée ou None si non trouvée
    """
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
    input:
        id_user : str : ID de l'utilisateur à rechercher
    output:
        User : instance de la classe User (Client ou Vendeur) ou None si l'utilisateur n'est pas trouvé
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
                from application import Application as app
                if role == 'C':
                    return Client(user_id, nom, prenom, email, telephone, role, mot_de_passe, app=app)
                if role == 'V':
                    return Vendeur(user_id, nom, prenom, email, telephone, role, mot_de_passe, app=app)
                if role == 'A':
                    return Admin(user_id, nom, prenom, email, telephone, role, mot_de_passe, app=app)
            else:
                pass
def info_vehicule(id_vehicule):
    """
    Récupère les informations d'un véhicule à partir de son ID.
    input:
        id_vehicule : str : ID du véhicule à rechercher
    output:
        Vehicule : instance de la classe Vehicule ou None si le véhicule n'est pas trouvé
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
                hauteur = float(row['hauteur'])
                type_vehicule = row['type_vehicule']
                boite_vitesse = row['boite_vitesse']
                entretien_annuel = float(row['entretien_annuel'])
                dispo = bool(row['dispo'])
                description = row['description']
                return Vehicule(
                    id_vehicule, marque, modele, prix_jour, masse, vitesse_max, puissance,
                    volume_utile, nb_places, type_moteur, hauteur, type_vehicule,
                    boite_vitesse, entretien_annuel, dispo, description
                )
            else:
                pass

def verifier_reservation(date_debut, date_fin, id_vehicule):
    """
    Vérifie si une réservation est possible en fonction des dates et de l'ID du véhicule.
    
    input:
        date_debut : str : Date de début de la réservation au format MM-DD-YYYY
        date_fin : str : Date de fin de la réservation au format MM-DD-YYYY
        id_vehicule : str : ID du véhicule à vérifier
    output:
        bool : True si la réservation est possible, False si un conflit de réservation est détecté.
    """
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
    input:
        id_resa : str : ID de la réservation dont on veut supprimer la facture
    output:
        None
    """
    fichier_pdf = f"facture_{id_resa}.pdf"
    path_save = os.path.join(os.path.abspath("factures_pdf"), fichier_pdf)

    if os.path.exists(path_save):
        os.remove(path_save)
        print(f"Facture {fichier_pdf} supprimée avec succès.")
    else:
        print(f"Aucune facture trouvée pour l'ID de réservation {id_resa}.")

def load_users_POO(file):
    """
    Charge les utilisateurs à partir d'un fichier CSV et convertit les champs en types appropriés.
    
    Paramètres :
        csv (str) : Chemin vers le fichier CSV contenant les données des utilisateurs.
    Retour :
        list : Liste d'objets User (Client ou Vendeur) chargés à partir du fichier CSV.
    """
    with open(file, newline='', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)
        users = []
        for ligne in lecteur:
            if ligne['role'] == 'C':
                users.append(Client(
                    ligne['id_user'], ligne['nom'], ligne['prenom'], ligne['email'],
                    ligne['telephone'], ligne['role'], ligne['mot_de_passe'], app=None
                ))
            elif ligne['role'] == 'V':
                users.append(Vendeur(
                    ligne['id_user'], ligne['nom'], ligne['prenom'], ligne['email'],
                    ligne['telephone'], ligne['role'], ligne['mot_de_passe'], app=None
                ))
            elif ligne['role'] == 'A':
                users.append(Admin(
                    ligne['id_user'], ligne['nom'], ligne['prenom'], ligne['email'],
                    ligne['telephone'], ligne['role'], ligne['mot_de_passe'], app=None
                ))
    return users


def modifier_champ_csv(fichier_csv, champ_id, id_val, champs_interdits):
    """
    modifie un champ d'un fichier CSV en fonction d'un ID donné.
    
    input:
        fichier_csv : str : Chemin du fichier CSV à modifier
        champ_id : str : Nom de la colonne contenant l'ID
        id_val : str : Valeur de l'ID à rechercher
        champs_interdits : list : Liste des champs interdits à modifier
    output:
        None

    """
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

def load_vehicules(fichier_csv):
    """
    Charge les véhicules à partir d'un fichier CSV et convertit les champs en types appropriés.
    
    Paramètres :
        fichier_csv (str) : Chemin vers le fichier CSV contenant les données des véhicules.
    Retour :
    
        list : Liste d'objets Vehicule chargés à partir du fichier CSV.
    """
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
            vehicules.append(load_vehicule_POO(ligne))
    return vehicules

def criteres():
    """
    Demande à l'utilisateur de spécifier des critères de recherche pour les véhicules.
    
    input:
        None
    output:
        list : Liste de tuples contenant les critères de recherche (champ, opérateur, valeur).
    """

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
    print("REMARQUE : Les champs texte sont en minuscule sans accents...")
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
    """
    
    Effectue une recherche de véhicules en fonction des critères spécifiés par l'utilisateur.
    input:
        vehicules : list : Liste d'objets Vehicule à filtrer
        criteres : list : Liste de tuples contenant les critères de recherche (champ, opérateur, valeur)
    output:
        list : Liste d'objets Vehicule correspondant aux critères de recherche, ou un message si aucun véhicule n'est trouvé.
    """
    op_map = {
        "=": lambda a, b: a == b,
        "<": lambda a, b: a < b,
        ">": lambda a, b: a > b,
        "<=": lambda a, b: a <= b,
        ">=": lambda a, b: a >= b,
    }
   
    resultats = []
    for v in vehicules:
        if not getattr(v, "dispo", False):
            continue

        match_all = True
        for champ, op, val in criteres:
            val_obj = getattr(v, champ, None)
            if val_obj is None:
                match_all = False
                break
            try:
                if isinstance(val_obj, float):
                    val = float(val)
                elif isinstance(val_obj, int):
                    val = int(val)
                elif isinstance(val_obj, bool):
                    val = val.lower() == 'true'
            except Exception:
                match_all = False
                break
            if not op_map[op](val_obj, val):
                match_all = False
                break

        if match_all:
            resultats.append(v)

    if resultats:
        print(f"\n {len(resultats)} véhicule(s) trouvé(s) :\n")
        for v in resultats:
            infos = [
                f"ID : {v.id_vehicule}",
                f"Prix/jour : {v.prix_jour} €",
                f"Type : {v.type_vehicule}",
                f"Marque : {v.marque}",
                f"Modèle : {v.modele}",
                f"{v.description}"
            ]
            for champ, _, _ in criteres:
                if champ not in ['prix_jour', 'marque', 'modele', 'description', 'type_vehicule']:
                    infos.append(f"{champ}: {getattr(v, champ)}")
            print(" - " + ", ".join(infos))
        return resultats
    else:
        print("\nAucun véhicule ne correspond aux critères.\n")
        print("Essayez d'etre plus souple dans vos critères de recherche.\n")
        print("Vous pouvez consulter le catalogue des véhicules pour plus d'information.\n")

def load_vehicule_POO(row):
    """
    Charge un véhicule à partir d'une ligne de CSV.
    input:
        row : dict : Dictionnaire représentant une ligne du fichier CSV des véhicules
    output:
        Vehicule : instance de la classe Vehicule initialisée avec les données de la ligne
    """
    return Vehicule(
        row['id_vehicule'], row['marque'], row['modele'], float(row['prix_jour']),
        float(row['masse']), float(row['vitesse_max']), float(row['puissance']),
        float(row['volume_utile']), int(row['nb_places']), row['type_moteur'],
        float(row['hauteur']), row['type_vehicule'], row['boite_vitesse'],
        float(row['entretien_annuel']), bool(row['dispo']), row['description']
    )

def load_vehicule_POO_id(csv,id_vehicule):
    """
    Recherche un véhicule par son identifiant dans un fichier CSV et renvoie une instance
    d'objet véhicule via la fonction load_vehicule_POO.

    Paramètres :
        csv (str) : Chemin vers le fichier CSV contenant les données des véhicules.
        id_vehicule (str) : Identifiant du véhicule à rechercher.

    Retour :
        objet : L'objet véhicule correspondant si trouvé, sinon None.
    """
    with open(csv, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id_vehicule'] == id_vehicule:
                return load_vehicule_POO(row)
            else:
                print("Véhicule introuvable !")

def lire_donnees_reservations(fichier_reservations='reservations.csv'):
    """
    Lit un fichier CSV de réservations et convertit certaines colonnes en types appropriés.

    Cette fonction lit les réservations à partir d'un fichier CSV situé dans le dossier 'data'
    relatif au script. Elle convertit les champs 'date_debut' en objets datetime et 'prix_total'
    en float. Les lignes invalides sont ignorées avec un message d'erreur.

    Paramètres :
        fichier_reservations (str) : Nom du fichier CSV des réservations (par défaut 'reservations.csv').

    Retour :
        list : Liste de dictionnaires représentant les réservations avec types convertis.
    """
    chemin_repertoire = str(os.path.dirname(os.path.realpath(__file__)))
    chemin_data = str(os.path.join(chemin_repertoire, 'data'))
    chemin_reservations = os.path.join(chemin_data, fichier_reservations)
    donnees = []
    with open(chemin_reservations, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row['date_debut'] = datetime.strptime(row['date_debut'], "%m-%d-%Y")
                row['prix_total'] = float(row['prix_total'])
                donnees.append(row)
            except Exception as e:
                print(f"Erreur sur une ligne : {e}")
    return donnees

def plot_reservations_par_mois(donnees=lire_donnees_reservations('reservations.csv')):
    """
    Affiche un histogramme du nombre de réservations par mois.

    La fonction extrait la date de début de chaque réservation, l'agrège par mois (au format YYYY-MM),
    puis affiche un histogramme montrant l'évolution mensuelle du nombre de réservations.

    Paramètres :
        donnees (list) : Liste de dictionnaires représentant les réservations, chaque élément contenant
                         au moins une clé 'date_debut' de type datetime.

    Retour :
        None
    """
    stats = defaultdict(int)
    for r in donnees:
        mois = r['date_debut'].strftime("%Y-%m")
        stats[mois] += 1

    mois_tries = sorted(stats)
    valeurs = [stats[m] for m in mois_tries]

    plt.figure(figsize=(10, 5))
    plt.bar(mois_tries, valeurs, color='teal')
    plt.title("Nombre de réservations par mois")
    plt.xlabel("Mois")
    plt.ylabel("Nombre de réservations")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_reservations_par_annee(fichier_reservations=lire_donnees_reservations('reservations.csv')):
    """
    Affiche un histogramme du nombre de réservations par année.

    La fonction parcourt les données de réservation, extrait l'année de début de chaque réservation, 
    puis compte combien de réservations ont eu lieu chaque année. Elle génère ensuite un histogramme 
    pour visualiser l'évolution du nombre de réservations dans le temps.

    Paramètres :
        donnees (list) : Liste de dictionnaires représentant les réservations, chaque élément contenant 
                         au moins une clé 'date_debut' de type datetime.

    Retour :
        None
    """
    stats = defaultdict(int)
    for r in fichier_reservations:
        annee = r['date_debut'].year
        stats[annee] += 1

    annees = sorted(stats)
    valeurs = [stats[a] for a in annees]
 
    plt.figure(figsize=(6, 5))
    plt.bar(annees, valeurs, color='coral')
    plt.title("Nombre de réservations par année")
    plt.xlabel("Année")
    plt.ylabel("Nombre de réservations")
    plt.tight_layout()
    plt.show()

def benefice_par_annee_histogramme(fichier_reservations='reservations.csv', fichier_vehicules='vehicules.csv'):
    """
    Calcule le bénéfice net annuel et affiche un histogramme des bénéfices par année.

    Pour chaque réservation, le bénéfice est calculé comme la différence entre le prix total 
    payé et le coût d'entretien journalier (entretien annuel divisé par 365 jours multiplié 
    par le nombre de jours de la réservation). Seules les dates de début des réservations 
    sont prises en compte pour déterminer l'année.

    Paramètres :
        fichier_reservations (str) : Nom du fichier CSV contenant les réservations, utilisation des colonnes 'id_vehicule', 'date_debut', 'date_fin', 'prix_total'.
        fichier_vehicules (str) : Nom du fichier CSV contenant les véhicules, utilisation des colonnes 'id_vehicule' et 'entretien_annuel'.

    Retour :
        dict : Dictionnaire associant chaque année (int) à son bénéfice net (float) en euros.
    """
    chemin_script = os.path.dirname(os.path.realpath(__file__))
    chemin_data = os.path.join(chemin_script, 'data')
    chemin_reservations = os.path.join(chemin_data, fichier_reservations)
    chemin_vehicules = os.path.join(chemin_data, fichier_vehicules)

    reservations = lire_csv(chemin_reservations)
    vehicules = lire_csv(chemin_vehicules)

    # Dictionnaire pour stocker le coût d'entretien par véhicule
    dico_entretien_annuel = {
        v['id_vehicule']: float(v['entretien_annuel']) for v in vehicules
    }

    # Stocke les bénéfices par année
    benefices_par_annee = defaultdict(float)

    for resa in reservations:
        try:
            date_debut = datetime.strptime(resa['date_debut'], '%m-%d-%Y')
            date_fin = datetime.strptime(resa['date_fin'], '%m-%d-%Y')
            annee = date_debut.year

            id_vehicule = resa['id_vehicule']
            prix_total = float(resa['prix_total'])
            nb_jours = (date_fin - date_debut).days + 1

            entretien_annuel = dico_entretien_annuel.get(id_vehicule, 0.0)
            cout_entretien = (entretien_annuel / 365) * nb_jours

            benefice = prix_total - cout_entretien
            benefices_par_annee[annee] += benefice

        except Exception as e:
            print(f"Erreur dans la ligne {resa} : {e}")

    # Trie les années pour l'affichage
    annees = sorted(benefices_par_annee.keys())
    benefices = [round(benefices_par_annee[a], 2) for a in annees]

    # Histogramme
    plt.figure(figsize=(10, 6))
    plt.bar(benefices_par_annee.keys(), benefices_par_annee.values())
    plt.xlabel('Année')
    plt.ylabel('Bénéfice (€)')
    plt.title('Bénéfice par année')

    # Forcer l'affichage des années comme entiers
    plt.xticks(sorted(benefices_par_annee.keys()))  # assure aussi l’ordre chronologique

    plt.tight_layout()
    plt.show()
    return dict(benefices_par_annee)


def benefice_pour_annee(annee_voulue, fichier_reservations='reservations.csv', fichier_vehicules='vehicules.csv'):
    """
    Calcule et affiche le bénéfice net généré par les réservations pour une année donnée.

    Le bénéfice est obtenu en soustrayant les coûts d'entretien (proportionnels au nombre de jours 
    de réservation) du prix total payé pour chaque réservation commencée dans l'année spécifiée.
    Le coût d'entretien annuel est réparti sur 365 jours.

    Paramètres :
        annee_voulue (int) : Année pour laquelle calculer le bénéfice (ex : 2023).
        fichier_reservations (str) : Nom du fichier CSV contenant les réservations, utilisation des colonnes 'id_vehicule', 'date_debut', 'date_fin' et 'prix_total'.
        fichier_vehicules (str) : Nom du fichier CSV contenant les véhicules, utilisation des colonnes 'id_vehicule' et 'entretien_annuel'.

    Retour :
        float : Bénéfice net total pour l'année spécifiée (en euros).
    """
    
    chemin_script = os.path.dirname(os.path.realpath(__file__))
    chemin_data = os.path.join(chemin_script, 'data')
    chemin_reservations = os.path.join(chemin_data, fichier_reservations)
    chemin_vehicules = os.path.join(chemin_data, fichier_vehicules)

    reservations = lire_csv(chemin_reservations)
    vehicules = lire_csv(chemin_vehicules)

    dico_entretien_annuel = {
        v['id_vehicule']: float(v['entretien_annuel']) for v in vehicules
    }
    total_net = 0.0

    for resa in reservations:
        try:
            date_debut = datetime.strptime(resa['date_debut'], '%m-%d-%Y')
            date_fin = datetime.strptime(resa['date_fin'], '%m-%d-%Y')
            if date_debut.year != annee_voulue:
                continue

            id_vehicule = resa['id_vehicule']
            prix_total = float(resa['prix_total'])
            nb_jours = (date_fin - date_debut).days + 1

            entretien_annuel = dico_entretien_annuel.get(id_vehicule, 0.0)
            cout_entretien = (entretien_annuel / 365) * nb_jours

            total_net += prix_total - cout_entretien

        except Exception as e:
            print(f"Erreur dans la ligne {resa} : {e}")

    print(f"Bénéfice net pour {annee_voulue} : {round(total_net, 2)} €")
    return total_net

def afficher_benefice_total(fichier_reservations='reservations.csv', fichier_vehicules='vehicules.csv'):
    
    """
    Calcule et affiche le bénéfice total généré par tous les véhicules, toutes années confondues.

    Le bénéfice est calculé en soustrayant le coût d'entretien (proportionnel au nombre de jours 
    de réservation) du prix total payé pour chaque réservation. Le coût d'entretien annuel est 
    réparti sur 365 jours.

    Paramètres :
        fichier_reservations (str) : Nom du fichier CSV contenant les réservations, utilisation des colonnes 'id_vehicule', 'prix_total' et 'jours'.
        fichier_vehicules (str) : Nom du fichier CSV contenant les véhicules, utilisation des colonnes 'id_vehicule' et 'entretien_annuel'.

    Retour :
        float : Le bénéfice total cumulé (en euros).
    """
    # Chemins vers les fichiers
    dossier = os.path.join(os.path.dirname(__file__), 'data')
    reservations = lire_csv(os.path.join(dossier, fichier_reservations))
    vehicules = lire_csv(os.path.join(dossier, fichier_vehicules))

    # Récupération du coût d'entretien annuel par véhicule
    couts_entretien = {v['id_vehicule']: float(v['entretien_annuel']) for v in vehicules}

    benefice_total = 0.0

    for resa in reservations:
        id_veh = resa['id_vehicule']
        prix = float(resa['prix_total'])
        jours = int(resa['jours'])
        entretien_par_jour = couts_entretien.get(id_veh, 0.0) / 365
        cout_entretien = entretien_par_jour * jours
        benefice_total += prix - cout_entretien

    print(f"Bénéfice total toutes années confondues : {round(benefice_total, 2)} €")
    return benefice_total

def lire_csv(fichier):
    """
    Lit un fichier CSV et retourne une liste de dictionnaires, 
    où chaque dictionnaire représente une ligne du fichier avec des paires clé-valeur.

    Paramètres :
        fichier (str) : Chemin vers le fichier CSV à lire.

    Retour :
        list[dict] : Liste de lignes du fichier, chaque ligne étant représentée sous forme de dictionnaire.
    """
    with open(fichier, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
    


def reservations_par_vehicule_par_an(annee, fichier_vehicules='vehicules.csv', fichier_reservations='reservations.csv'):
    """
    Affiche un histogramme du nombre de réservations par véhicule pour une année donnée, 
    à partir de deux fichiers CSV contenant les informations sur les véhicules et les réservations.
    
    Paramètres :
        annee (int) : Année pour laquelle on souhaite filtrer les réservations (ex : 2024).
        fichier_vehicules (str) : Nom du fichier CSV contenant les données des véhicules. 
                                  Doit contenir les colonnes 'id_vehicule', 'marque' et 'modele'.
        fichier_reservations (str) : Nom du fichier CSV contenant les données de réservation.
                                     Doit contenir les colonnes 'id_vehicule' et 'date_debut' (au format '%m-%d-%Y').

    Affiche :
        - Un graphique en barres indiquant le nombre de réservations effectuées pour chaque véhicule 
          (nommé par sa marque et son modèle) durant l'année spécifiée.

    Retour :
        None
    """
    # Définition des chemins
    chemin_repertoire = os.path.dirname(os.path.realpath(__file__))
    chemin_data = os.path.join(chemin_repertoire, 'data') 
    chemin_vehicules = os.path.join(chemin_data, fichier_vehicules)  
    chemin_reservations = os.path.join(chemin_data, fichier_reservations)  

    # Chargement des données
    vehicules = lire_csv(chemin_vehicules)
    reservations = lire_csv(chemin_reservations)
    
    # Filtrage des réservations pour l'année donnée
    reservations_annee = [
        resa for resa in reservations 
        if datetime.strptime(resa['date_debut'], '%m-%d-%Y').year == annee
    ]
    
    compteur_reservations = Counter(resa['id_vehicule'] for resa in reservations_annee)
    vehicules_dict = {vehicule['id_vehicule']: f"{vehicule['marque']} {vehicule['modele']}" for vehicule in vehicules}
    vehicules_noms = [vehicules_dict.get(id_vehicule, "Inconnu") for id_vehicule in compteur_reservations.keys()]
    nb_reservations = list(compteur_reservations.values())
    
    
    plt.figure(figsize=(10, 6))
    plt.bar(vehicules_noms, nb_reservations)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Véhicule')
    plt.ylabel('Nombre de réservations')
    plt.title(f'Nombre de réservations par véhicule pour l\'année {annee}')
    plt.tight_layout()

    # Enregistrer le graphique en PNG dans le dossier 'bilan'
    plt.show()
    return plt

def plot_reservations_par_vehicule(fichier_reservations='reservations.csv'):
    """
        Affiche un histogramme du nombre de réservations par véhicule à partir d'un fichier CSV.

        Le graphique montre, pour chaque identifiant de véhicule, le nombre total de réservations 
        enregistrées dans le fichier CSV.

        Paramètres :
            fichier_reservations (str) : Nom du fichier CSV contenant les réservations. 
                                        Le fichier doit être situé dans un dossier 'data' 
                                        à la racine du script, et contenir une colonne 'id_vehicule'.

        Affiche :
            - Un graphique en barres montrant le nombre de réservations pour chaque véhicule.

        Retour :
            None
    """
    chemin_script = os.path.dirname(os.path.realpath(__file__))
    chemin_data = os.path.join(chemin_script, 'data')
    chemin_resa = os.path.join(chemin_data, fichier_reservations)

    with open(chemin_resa, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        reservations = [row for row in reader]

    compteur = Counter(resa['id_vehicule'] for resa in reservations)

    vehicules = list(compteur.keys())
    nb_reservations = list(compteur.values())

    plt.figure(figsize=(10, 6))
    plt.bar(vehicules, nb_reservations, color='skyblue')
    plt.xlabel('ID Véhicule')
    plt.ylabel('Nombre de réservations')
    plt.title('Nombre de réservations par véhicule')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    #dossier_bilan = os.path.join(chemin_script, 'bilan')
    #chemin_sauvegarde = os.path.join(dossier_bilan,'reservations_par_vehicule.png')
    #plt.savefig(chemin_sauvegarde)
    #print(f"Le graphique a été enregistré dans le dossier 'bilan' sous : {chemin_sauvegarde}")
    

def plot_reservations_histogram(csv_path='data/reservations.csv'):
    """
        Affiche un histogramme des réservations par véhicule, en distinguant les réservations classiques 
    des surclassements, à partir d'un fichier CSV.

    Le graphique présente pour chaque véhicule deux barres côte à côte :
    - une pour les réservations classiques (surclassement = False),
    - une pour les surclassements (surclassement = True),
    ainsi que le total de réservations annoté au-dessus des barres.

    Paramètres :
        csv_path (str) : Chemin vers le fichier CSV contenant les données de réservation ('id_vehicule' et 'surclassement').

    Affiche :
        - Un graphique matplotlib avec le nombre de réservations par véhicule,
          différenciant classiques et surclassements.
        - Le total des réservations au-dessus des barres pour chaque véhicule.

    Retour :
        None
    """
    # Chargement des données
    df = pd.read_csv(csv_path)

    # Regrouper par véhicule et surclassement
    grouped = df.groupby(['id_vehicule', 'surclassement']).size().unstack(fill_value=0)

    # Forcer l'existence des colonnes True et False
    if True not in grouped.columns:
        grouped[True] = 0
    if False not in grouped.columns:
        grouped[False] = 0

    # Total par véhicule
    grouped['total'] = grouped[True] + grouped[False]

    # Tracé
    x = np.arange(len(grouped))
    width = 0.35

    fig, ax = plt.subplots(figsize=(16, 9)) 

    bars_false = ax.bar(x - width/2, grouped[False], width, label='Classique', color='green')
    bars_true = ax.bar(x + width/2, grouped[True], width, label='Surclassement', color='red')

    for i, total in enumerate(grouped['total']):
        ax.text(i, total + 0.5, str(total), ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Mise en forme
    ax.set_xlabel('ID Véhicule')
    ax.set_ylabel('Nombre de réservations')
    ax.set_title('Réservations par véhicule : Classiques (vert) vs Surclassements (rouge)')
    ax.set_xticks(x)
    ax.set_xticklabels(grouped.index, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

def plot_rentabilite_depuis_csv(fichier_resa=RESERVATIONS_FILE, fichier_vehicules=VEHICULES_FILE):
    """    
    Génère un graphique comparant les revenus et les coûts d'entretien annuels des véhicules,
    calculés à partir de deux fichiers CSV, et affiche un indice de rentabilité pour chaque véhicule.

    L'indice de rentabilité est défini comme : revenu total / coût d'entretien annuel.

    Paramètres :
        fichier_resa (str) : Chemin vers le fichier CSV des réservations ('id_vehicule' et 'prix_total').
        fichier_vehicules (str) : Chemin vers le fichier CSV des véhicules ('id_vehicule' et 'entretien_annuel').

    Affiche :
        - Un graphique en barres montrant les revenus et les coûts d'entretien (en k€) pour chaque véhicule, indices de rentabilité directement au-dessus des barres.
        - Affiche les indices dans la console.

    Retour :
        None
    """
    
    revenus = defaultdict(float)
    entretiens = {}

    # Lecture des revenus depuis le fichier des réservations 
    with open(fichier_resa, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_vehicule = row["id_vehicule"]
            prix = float(row["prix_total"])
            revenus[id_vehicule] += prix

    #Lecture des coûts d'entretien depuis le fichier des véhicules
    with open(fichier_vehicules, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_vehicule = row["id_vehicule"]
            entretien = float(row["entretien_annuel"])
            entretiens[id_vehicule] = entretien

    #Fusion des véhicules présents dans les deux fichiers
    ids_vehicules = sorted(list(set(revenus.keys()) & set(entretiens.keys())))
    liste_revenus = [revenus[v] for v in ids_vehicules]
    liste_entretiens = [entretiens[v] for v in ids_vehicules]

    #Calcul des indices de rentabilité
    indices = []
    for i in range(len(ids_vehicules)):
        revenu = liste_revenus[i]
        cout = liste_entretiens[i]
        indice = revenu / cout if cout != 0 else float('inf')
        indices.append(indice)
        print(f"Véhicule {ids_vehicules[i]}  Indice de rentabilité : {indice:.2f}")

    #Affichage du graphique
    x = range(len(ids_vehicules))
    width = 0.35
    fig, ax = plt.subplots(figsize=(14, 8))
    #Diviser les valeurs par 1000 pour affichage en k€
    bar1 = ax.bar([i - width/2 for i in x], [r / 1000 for r in liste_revenus], width, label="Revenus (k€)", color='green')
    bar2 = ax.bar([i + width/2 for i in x], [e / 1000 for e in liste_entretiens], width, label="Entretien (k€)", color='red')

    #Ajout des indices de rentabilité au-dessus des barres
    for i in range(len(x)):
        pos = max(liste_revenus[i], liste_entretiens[i]) / 1000 + 0.05
        ax.text(i, pos, f"{indices[i]:.2f}", ha='center', fontsize=11, fontweight='bold')

    ax.set_xlabel("ID Véhicule")
    ax.set_ylabel("Montant (k€)")
    ax.set_title("Revenus vs Entretien (en k€) avec Indice de Rentabilité")
    ax.set_xticks(x)
    ax.set_xticklabels(x, rotation=45, ha='right')
    ax.set_xticklabels(ids_vehicules)
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

