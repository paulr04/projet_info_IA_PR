import csv
import os
from fonctions import *
from objects import Vehicule, Reservation, User
from facture import facture

USER_FILE = 'data/users.csv'
VEHICULES_FILE = 'data/vehicules.csv'
RESERVATIONS_FILE = 'data/reservations.csv'

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
        user = self.verifier_identifiants(user_id, mot_de_passe)

        if user:
            # Message de bienvenue avec le prénom de l'utilisateur
            print(
                f"Bonjour, {user.prenom} ! Vous êtes connecté en tant que {'client' if user.role == 'C' else 'vendeur'}.")

            self.utilisateur_connecte = user
            self.afficher_menu(user.role)
        else:
            print("ID ou mot de passe incorrect.")

    def verifier_identifiants(self, user_id, mot_de_passe):
        # Recherche dans le fichier USER_FILE pour vérifier l'ID et récupérer le rôle
        with open(USER_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id_user'] == user_id and row['mot_de_passe'] == mot_de_passe:
                    user_id = row['id_user']
                    nom = row['nom']
                    prenom = row['prenom']
                    email = row['email']
                    telephone = row['telephone']
                    role = row['role']
                    mot_de_passe = row['mot_de_passe']
                    return User(user_id, nom, prenom, email, telephone, role, mot_de_passe)  # Retourne les informations de l'utilisateur (client ou vendeur)
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
            print("2. Faire une recherche de véhicule")
            print("3. Consulter vos réservations")
            print("4. Faire une réservation")
            print("5. Supprimer le compte")
            print("6. Annuler une réservation")
            print("7. Changer de mot de passse")
            print("8. Quitter")

            choix = input("Choisissez une action (1-8): ")
            if choix == "1":
                self.consulter_catalogue()
            elif choix == "2":
                print("en cour de développement")
            elif choix == "3":
                self.consulter_reservations()
            elif choix == "4":
                self.reserver_vehicule()
            elif choix == "5":
                self.supprimer_compte_client()
                break
            elif choix == "6":
                self.annuler_reservation()
            elif choix == "7":
                self.changer_de_mdp()
                break
            elif choix == "8":
                print("Déconnexion...")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

    def menu_vendeur(self):
        while True:
            print("\nMenu Vendeur :")
            print("1. Consulter le catalogue de véhicules")
            print("2. Consulter les utilisateurs")
            print("3. Consulter les réservations")
            print("4. Ajouter un véhicule")
            print("5. Supprimer un véhicule")
            print("6. Faire une réservation")
            print("7. Annuler une réservation")
            print("8. Créer un compte client")
            print("9. Supprimer un compte client")
            print("10. Changer de mot de passe")
            print("11. Analyse des ventes")
            print("12. Quitter")

            choix = input("Choisissez une action (1-12): ")
            if choix == "1":
                self.consulter_catalogue()
            elif choix == "2":
                self.consulter_user()
            elif choix == "3":
                self.consulter_reservations()
            elif choix == "4":
                self.ajouter_vehicule()
            elif choix == "5":
                self.supprimer_vehicule()
            elif choix == "6":
                self.reserver_vehicule()
            elif choix == "7":
                self.annuler_reservation()
            elif choix == "8":
                self.creer_compte_client()
            elif choix == "9":
                self.supprimer_compte_client()
            elif choix == "10":
                self.changer_de_mdp()
                break
            elif choix == "11":
                print("en cour de développement")
            elif choix == "12":
                print("Déconnexion...")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

    def menu_analyse_ventes(self):
        pass


    def consulter_catalogue(self):
        print("\nCatalogue des véhicules :")
        # Afficher les véhicules disponibles
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"ID : {row['id_vehicule']}, Marque : {row['marque']}, Modèle : {row['modele']}, Prix/jour : {row['prix_jour']}")

    def consulter_user(self):
        print("\nUtilisateurs :")
        with open(USER_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"ID : {row['id_user']}, Prenom : {row['prenom']}, Nom : {row['nom']}, Email : {row['email']}, Telephone : {row['telephone']}, Role: {row['role']}")

    def consulter_reservations(self):
        user = self.utilisateur_connecte
        if user.role == "V":
            print("\nRéservations :")
            with open(RESERVATIONS_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    print(f"ID réservation : {row['id_resa']}, ID client : {row['id_user']}, ID véhicule : {row['id_vehicule']}, date de début : {row['date_debut']}, date de fin : {row['date_fin']}, prix : {row['prix_total']}")
        else:
            print("\nVos réservations :")
            with open(RESERVATIONS_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['id_user'] == user.id_user:
                        print(f"ID réservation : {row['id_resa']}, ID client : {row['id_user']}, ID véhicule : {row['id_vehicule']}, date de début : {row['date_debut']}, date de fin : {row['date_fin']}, prix : {row['prix_total']}")
                    else:
                        pass

    def rechercher_vehicule_par_id(self, vehicule_id):
        # Recherche du véhicule par ID dans le fichier des véhicules
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id_vehicule'] == vehicule_id:
                    return row
        return None

    def reserver_vehicule(self):
        print("\nFaire une réservation :")
        if self.utilisateur_connecte.role == "C":
            id_user = self.utilisateur_connecte.id_user
        else:
            id_user = demander_id("ID du client :",USER_FILE,'id_user')
        id_vehicule = demander_plaque("Plaque du véhicule à réserver (format AA-000-AA) :")
        vehicule = self.rechercher_vehicule_par_id(id_vehicule)
        if vehicule:
            date_debut = demander_date_valide("Date de début (inclus) (format MM-DD-YYYY) : ")
            date_fin = demander_date_valide("Date de fin (inclus) (format MM-DD-YYYY) : ")
            verifier_dates(date_debut, date_fin)
            indispo = verifier_reservation(date_debut, date_fin, id_vehicule)
            if indispo:
                print("Le véhicule n'est pas disponible aux dates demandées.") # SURCLASSEMENT
            else:
                jours_res = calculer_jours_reservation(date_debut, date_fin)
                prix_vehicule = float(trouver_value(VEHICULES_FILE, id_vehicule, 'id_vehicule', 'prix_jour'))
                prix = jours_res * prix_vehicule
                id_resa = generer_id_unique(RESERVATIONS_FILE, 'id_resa')
                reservation = Reservation(id_resa, id_user, id_vehicule, date_debut, date_fin, jours_res, prix)
                facture(reservation,info_user(id_user),info_vehicule(id_vehicule))
                file_exists = os.path.exists(RESERVATIONS_FILE)
                with open(RESERVATIONS_FILE, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=reservation.to_dict().keys())
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(reservation.to_dict())
                print(f"Réservation n° {id_resa} confirmée pour {id_user} pour le véhicule {vehicule['marque']} {vehicule['modele']} du {date_debut} au {date_fin} total de {jours_res} jour(s), coût : {prix} €.")
        else:
            print("Véhicule non trouvé.")

    def annuler_reservation(self):
        user = self.utilisateur_connecte
        user_id = user.id_user
        if user.role == "C":
            Application.consulter_reservations(self)
        else:
            pass
        mot_de_passe = input("Mot de passe : ")
        user = self.verifier_identifiants(user_id, mot_de_passe)
        if user:
            id_reservation = demander_id("ID réservation à annuler (entrez 9 chiffres): ", RESERVATIONS_FILE, 'id_resa')
            supprimer_ligne_par_id(RESERVATIONS_FILE, "id_resa",id_reservation)
        else:
            print("ID ou mot de passe incorrect.")

    def creer_compte_client(self):
        print("\nCréer un compte client :")
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        email = input("Email : ")
        telephone = input("Téléphone : ")
        mot_de_passe = input("Mot de passe : ")
        client_id = generer_id_unique(USER_FILE,'id_user')
        role = 'C'

        user = User(client_id, nom, prenom, email, telephone, role, mot_de_passe)

        file_exists = os.path.exists(USER_FILE)
        with open(USER_FILE, mode='a', newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=user.to_dict().keys())
            if not file_exists :
                writer.writeheader()
            writer.writerow(user.to_dict())

        print(f"Compte client créé avec succès! ID : {user.id_user} Nom : {user.nom} Prenom : {user.prenom}.")

    def ajouter_vehicule(self):
        print("\n--- AJOUT D'UN VÉHICULE ---")

        id_vehicule = demander_plaque_ajout("Plaque d'immatriculation (format AA-000-AA) : ",VEHICULES_FILE)
        marque = input("Marque : ").strip()
        modele = input("Modèle : ").strip()
        prix_jour = demander_input_float("Prix par jour (€) : ")
        masse = demander_input_float("Masse (kg) : ")
        vitesse_max = demander_input_float("Vitesse maximale (km/h) : ")
        puissance = demander_input_float("Puissance (ch) : ")
        volume_utile = demander_input_float("Volume utile (m³) : ")
        nb_places = demander_input_int("Nombre de places : ")
        type_moteur = demander_input_choix("Type de moteur : ", TYPES_MOTEUR)
        dimensions = demander_input_dimensions()
        type_vehicule = demander_input_choix("Type de véhicule : ", TYPES_VEHICULE)
        boite_vitesse = demander_input_choix("Boîte de vitesse : ", BOITES_VITESSE)
        entretien_annuel = demander_input_float("Entretien annuel (€) : ")
        dispo = demander_input_bool("Le véhicule est-il disponible ? (True/False) : ")
        description = input("Description du véhicule : ").strip()

        vehicule = Vehicule(id_vehicule, marque, modele, prix_jour, masse, vitesse_max, puissance,volume_utile, nb_places, type_moteur, dimensions, type_vehicule, boite_vitesse, entretien_annuel, dispo, description )

        file_exists = os.path.exists(VEHICULES_FILE)
        with open(VEHICULES_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=vehicule.to_dict().keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(vehicule.to_dict())

        print(f"\nVéhicule ajouté avec succès ! ID : {vehicule.id_vehicule}")

    def supprimer_vehicule(self):
        print("\nSupprimer un véhicule :")
        user_id = self.utilisateur_connecte.id_user
        mot_de_passe = input("Mot de passe : ")
        user = self.verifier_identifiants(user_id, mot_de_passe)
        if user:
            id_vehicule = demander_plaque("Plaque d'immatriculation du véhicule à supprimer (format AA-000-AA) : ")
            supprimer_ligne_par_id(VEHICULES_FILE, "id_vehicule",id_vehicule)
        else:
            print("ID ou mot de passe incorrect.")

    def supprimer_compte_client(self):
        print("\nSupprimer un compte client :")
        user_id = self.utilisateur_connecte.id_user
        mot_de_passe = input("Mot de passe : ")
        user = self.verifier_identifiants(user_id, mot_de_passe)
        if user:
            if user.role == "C":
                id_supp = self.utilisateur_connecte.id_user
            elif user.role == "V":
                id_supp = demander_id("ID d'utilisateur à supprimer : ",USER_FILE,'id_user')
            else:
                print("PROBLEME")
            supprimer_ligne_par_id(USER_FILE, "id_user",id_supp)
        else:
            print("ID ou mot de passe incorrect.")

    def changer_de_mdp(self):
        print("\nChanger de mot de passe :")
        user_id = self.utilisateur_connecte.id_user
        mot_de_passe = input("Mot de passe : ")
        user = self.verifier_identifiants(user_id, mot_de_passe)
        if user:
            while True:
                nouv_mdp = input("Nouveau mot de passe : ")
                conf_mdp = input("Confirmation mot de passe : ")
                if nouv_mdp == conf_mdp:
                    print("Mot de passe changé avec succès !")
                    modifier_champ_csv_par_id(USER_FILE, user_id,"id_user","mot_de_passe",nouv_mdp)
                    break
                else:
                    print(" Les mots de passes ne sont pas identiques")
        else:
            print("ID ou mot de passe incorrect.")

if __name__ == "__main__":
    # Création d'une instance de l'application et lancement du menu principal
    app = Application()
