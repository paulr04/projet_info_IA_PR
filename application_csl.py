import csv
from datetime import datetime

USER_FILE = 'users.csv'  # Fichier unique pour clients et vendeurs
VEHICULES_FILE = 'vehicules.csv'
RESERVATIONS_FILE = 'reservations.csv'

def generer_id_unique():
    # Fonction pour générer un ID unique (par exemple, un ID numérique ou aléatoire)
    return str(100000000 + len(open(USER_FILE).readlines()))  # Exemple basique pour générer un ID unique

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
    try:
        # Vérifier que la date de fin est supérieure ou égale à la date de début
        date_debut = convertir_date(date_debut)
        date_fin = convertir_date(date_fin)

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
            return difference.days
        else:
            print("La date de fin ne peut pas être antérieure à la date de début.")
            return None
    except ValueError:
        print("Format de date incorrect. Assurez-vous que les dates sont au format MM-DD-YYYY.")
        return None

class Application:
    def __init__(self):
        self.utilisateur_connecte = None  # L'utilisateur connecté (client ou vendeur)
        self.choisir_action()

    def choisir_action(self):
        # Menu principal
        while True:
            print("\nMenu principal :")
            print("1. Se connecter")
            print("2. Créer un compte client")
            print("3. Quitter")

            choix = input("Choisissez une action (1-3): ")
            if choix == "1":
                self.se_connecter()
            elif choix == "2":
                self.creer_compte_client()
            elif choix == "3":
                print("Au revoir!")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

    def se_connecter(self):
        print("\nSe connecter :")
        user_id = input("ID (9 chiffres) : ")
        mot_de_passe = input("Mot de passe : ")

        # Vérification des identifiants dans le fichier unique USER_FILE
        utilisateur = self.verifier_identifiants(user_id, mot_de_passe)

        if utilisateur:
            # Message de bienvenue avec le prénom de l'utilisateur
            print(
                f"Bonjour, {utilisateur['prenom']} ! Vous êtes connecté en tant que {'client' if utilisateur['role'] == 'C' else 'vendeur'}.")

            self.utilisateur_connecte = utilisateur
            self.afficher_menu(utilisateur['role'])
        else:
            print("ID ou mot de passe incorrect.")

    def verifier_identifiants(self, user_id, mot_de_passe):
        # Recherche dans le fichier USER_FILE pour vérifier l'ID et récupérer le rôle
        with open(USER_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == user_id and row['mot_de_passe'] == mot_de_passe:
                    return row  # Retourne les informations de l'utilisateur (client ou vendeur)
        return None  # Si aucun utilisateur n'est trouvé ou mot de passe incorrect

    def afficher_menu(self, role):
        if role == "C":
            self.menu_client()
        elif role == "V":
            self.menu_vendeur()

    def menu_client(self):
        while True:
            print("\nMenu Client :")
            print("1. Consulter le catalogue de véhicules")
            print("2. Faire une réservation")
            print("3. Quitter")

            choix = input("Choisissez une action (1-3): ")
            if choix == "1":
                self.consulter_catalogue()
            elif choix == "2":
                self.reserver_vehicule()
            elif choix == "3":
                self.supprimer_compte_client()
            elif choix == "4":
                print("Déconnexion...")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

    def menu_vendeur(self):
        while True:
            print("\nMenu Vendeur :")
            print("1. Consulter le catalogue de véhicules")
            print("2. Ajouter un véhicule")
            print("3. Supprimer un véhicule")
            print("4. Faire une réservation")
            print("5. Créer un compte client")
            print("6. Supprimer un compte client")
            print("7. Quitter")

            choix = input("Choisissez une action (1-7): ")
            if choix == "1":
                self.consulter_catalogue()
            elif choix == "2":
                self.ajouter_vehicule()
            elif choix == "3":
                self.supprimer_vehicule()
            elif choix == "4":
                self.reserver_vehicule()
            elif choix == "5":
                self.creer_compte_client()
            elif choix == "6":
                self.creer_compte_client()
            elif choix == "7":
                print("Déconnexion...")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

    def consulter_catalogue(self):
        print("\nCatalogue des véhicules :")
        # Afficher les véhicules disponibles
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"ID: {row['id']}, Marque: {row['marque']}, Modèle: {row['modele']}, Prix/jour: {row['prix_jour']}")

    def reserver_vehicule(self):
        print("\nFaire une réservation :")
        vehicule_id = input("ID du véhicule à réserver : ")
        # Recherche du véhicule
        vehicule = self.rechercher_vehicule_par_id(vehicule_id)
        if vehicule:
            date_debut = input("Date de début (YYYY-MM-DD) : ")
            date_fin = input("Date de fin (YYYY-MM-DD) : ")
            print(f"Réservation confirmée pour le véhicule {vehicule['marque']} {vehicule['modele']} du {date_debut} au {date_fin}.")
        else:
            print("Véhicule non trouvé.")

    def rechercher_vehicule_par_id(self, vehicule_id):
        # Recherche du véhicule par ID dans le fichier des véhicules
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == vehicule_id:
                    return row
        return None

    def creer_compte_client(self):
        print("\nCréer un compte client :")
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        email = input("Email : ")
        telephone = input("Téléphone : ")
        mot_de_passe = input("Mot de passe : ")

        client_id = generer_id_unique()  # Assure-toi d'avoir une fonction pour générer un ID unique
        client = {'id': client_id, 'nom': nom, 'prenom': prenom, 'email': email, 'telephone': telephone, 'role': 'C', 'mot_de_passe': mot_de_passe}

        self.ajouter_user_to_csv(client)
        print(f"Compte client créé avec succès! Votre ID est {client_id}.")

    def supprimer_compte_client(self):
        print("\nSupprimer un compte client :")
        # Code pour supprimer un compte client (en fonction du role V ou C interface différent)

    def ajouter_user_to_csv(self, user):
        with open(USER_FILE, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=user.keys())
            writer.writerow(user)

    def ajouter_vehicule(self):
        print("\nAjouter un véhicule :")
        # Code pour ajouter un véhicule (option réservée au vendeur)
        pass

    def supprimer_vehicule(self):
        print("\nSupprimer un véhicule :")
        # Code pour supprimer un véhicule (option réservée au vendeur)
        pass


if __name__ == "__main__":
    # Création d'une instance de l'application et lancement du menu principal
    app = Application()
