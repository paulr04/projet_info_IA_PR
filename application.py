import csv
import os
import datetime
from fonctions import *
from objects import *
from facture import *
from fonctions import plot_reservations_par_mois

USER_FILE = 'data/users.csv'
VEHICULES_FILE = 'data/vehicules.csv'
RESERVATIONS_FILE = 'data/reservations.csv'
CHAMPS_INTERDITS = ['id_user', 'id_resa', 'id_vehicule', 'role', 'mot_de_passe', 'type_moteur', 'type_vehicule', 'boite_vitesse']
NO_SURCLASSEMENT_TYPES = ["avion", "bateau", "militaire", "special"]

class Application:
    '''
    Auteur : 
        Paul Renaud 
        Ilyann Aragon
        
    La classe Application représente le coeur du système de gestion de la location de véhicules.
    Elle centralise la gestion des utilisateurs (client et vendeur), des résevations et du parc de véhicules.
    Elle fournit toutes les fonctionnalités nécessaires à l'utilisation de la plateforme, quece soit du côté client (réservation, gestion du compte) ou du côté vendeur (gestion du catalogue et des clients).
    Elle intègre également des outils d'analyse et de génération de rapports comme les factures et les bilans de ventes.
    Attributs :
        - utilisateur_connecte (bool) : L'utilisateur actuellement connecté (client ou vendeur).
        - criteres_resa (bool): Les critères de recherche pour le catalogue de véhicules.
    Méthodes :
        - choisir_action() : Affiche le menu principal et gère les choix de l'utilisateur.
        - se_connecter() : Gère la connexion de l'utilisateur.
        - verifier_identifiants() : Vérifie les identifiants de l'utilisateur dans le fichier USER_FILE.
        - afficher_menu() : Affiche le menu en fonction du rôle de l'utilisateur (client ou vendeur).
        - menu_client() : Affiche le menu pour le client et gère ses choix.
        - menu_vendeur() : Affiche le menu pour le vendeur et gère ses choix.
        - menu_analyse_ventes() : Affiche le menu pour l'analyse des ventes et gère les choix de l'utilisateur.
        - consulter_catalogue() : Affiche le catalogue des véhicules disponibles.
        - consulter_user() : Affiche la liste des utilisateurs.
        - consulter_reservations() : Affiche la liste des réservations.
        - rechercher_vehicule_par_id() : Recherche un véhicule par son ID.
        - reserver_vehicule() : Gère la réservation d'un véhicule.
        - trouver_vehicule_disponible() : Trouve les véhicules disponibles pour réservation.
        - surclassement() : Gère le surclassement d'un véhicule c.a.d propose un véhicule de catégorie supérieur à un client, lorsque c'est possible tout en conservant le prix initial du véhicule réservé.
        - annuler_reservation() : Gère l'annulation d'une réservation.
        - creer_compte_client() : Gère la création d'un compte client.
        - ajouter_vehicule() : Gère l'ajout d'un véhicule au catalogue en fonction des paramètres fixés par le programme list(types_véhicule),list(boites_vitesse) ... .
        - supprimer_vehicule() : Gère la suppression d'un véhicule du catalogue.
        - changer_de_mdp() : Gère le changement de mot de passe de l'utilisateur.
        - changer_caracteristique_vehicule() : Gère la modification d'une caractéristique d'un véhicule.
        - changer_caracteristique_compte() : Gère la modification d'une caractéristique du compte utilisateur.
        - consulter_reservations_prochaines_vehicule() : Gère la consultation des réservations prochaines en fonction de la plaque d'immatriculation du véhicule.
        - recherche_de_véhicule_pour_reservation() : Gère la recherche de véhicule pour réservation.
    '''
    def __init__(self):
        self.utilisateur_connecte = None  # L'utilisateur connecté (client ou vendeur)
        self.criteres_resa = None  # Critères de recherche pour le catalogue de véhicules
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
            print("2. Faire une recherche de véhicule et le réserver")
            print("3. Consulter vos réservations")
            print("4. Faire une réservation")
            print("5. Supprimer le compte")
            print("6. Annuler une réservation")
            print("7. Changer de mot de passse")
            print("8. Modifier une caractéristique sur votre compte")
            print("9. Quitter")

            choix = input("Choisissez une action (1-9): ")
            if choix == "1":
                self.consulter_catalogue()
            elif choix == "2":
                self.recherche_de_véhicule_pour_reservation()
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
                self.changer_caracteristique_compte()
            elif choix == "9":
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
            print("12. Modifier une caractéristique sur un véhicule")
            print("13. Modifier une caractéristique sur votre compte")
            print("14. Consulter les réservations prochaines d'un véhicule")
            print("15. Consulter un véhicule")
            print("16. Quitter")

            choix = input("Choisissez une action (1-16): ")
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
                self.menu_analyse_ventes()
            elif choix == "12":
                self.changer_caracteristique_vehicule()
            elif choix == "13":
                self.changer_caracteristique_compte()
            elif choix == "14":
                self.consulter_reservations_prochaines_vehicule()
            elif choix == "15":
                self.consulter_vehicule()
            elif choix == "16":
                print("Déconnexion...")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

    def menu_analyse_ventes(self): 
        while True:
            print("\nMenu Analyse des ventes :")
            print("1. Consulter le nombre de reservations passées par mois")#fait
            print("2. Consulter le nombre de reservations passées par ans")#fait
            print("3. Calculer le bénéfice sur l'année")#fait
            print("4. Consulter le bénéfice par année")#fait
            print("5. Consulter le bénéfice total")#fait
            print("6. Consulter le nombre de réservation par véhicule par année")#fait
            print("7. Consulter le nombre de réservation par véhicule")#fait
            print("8. Consulter la rentabilité par véhicule")#fait
            print("9. Consulter Le type de réservation par véhicule (surclassement ou classique)")#fait
            print("10. Quitter")
            choix = input("Choisissez une action (1-10): ")
            if choix == "1":
                plot_reservations_par_mois()   
            elif choix == "2":                   
                plot_reservations_par_annee()
            elif choix == "3":
                print("\nChoisir l'année :")
                annee = demander_input_int("Année : ")
                benefice_pour_annee(annee)
                input("ENTER pour continuer")
            elif choix == "4":
                benefice_par_annee_histogramme()
            elif choix == "5":
                afficher_benefice_total()
                input("ENTER pour continuer")
            elif choix == "6":
                print("\nChoisir l'année :")
                annee = demander_input_int("Année : ")
                reservations_par_vehicule_par_an(annee=annee)
            elif choix == "7":
                plot_reservations_par_vehicule()
            elif choix == "8":
                plot_rentabilite_depuis_csv(RESERVATIONS_FILE, VEHICULES_FILE)
            elif choix == "9":
                plot_reservations_histogram(RESERVATIONS_FILE)
            elif choix == "10":
                print("Retour...")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

    def consulter_catalogue(self):
        print("\nCatalogue des véhicules :\n")
        # Afficher les véhicules disponibles
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"ID : {row['id_vehicule']}, Marque : {row['marque']}, Modèle : {row['modele']}, Prix/jour : {row['prix_jour']} €, Disponibilité : {row['dispo']}, Description : {row['description']}")
        print("\n--- FIN ---\n")
        input("ENTER pour continuer")

    def consulter_user(self):
        print("\nUtilisateurs :\n")
        with open(USER_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"ID : {row['id_user']}, Prenom : {row['prenom']}, Nom : {row['nom']}, Email : {row['email']}, Telephone : {row['telephone']}, Role: {row['role']}")
        print("\n--- FIN ---\n")
        input("ENTER pour continuer")

    def consulter_reservations(self):
        user = self.utilisateur_connecte
        if user.role == "V":
            print("\nRéservations :\n")
            with open(RESERVATIONS_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if convertir_date(row['date_fin']).date() >= datetime.today().date():    
                        print(f"ID réservation : {row['id_resa']}, ID client : {row['id_user']}, ID véhicule : {row['id_vehicule']}, date de début : {row['date_debut']}, date de fin : {row['date_fin']}, prix : {row['prix_total']}")
            print("\n--- FIN ---\n")
            input("ENTER pour continuer")
        
        else:
            print("\nVos réservations :\n")
            with open(RESERVATIONS_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['id_user'] == user.id_user and convertir_date(row['date_fin']).date() >= datetime.today().date():
                        print(f"ID réservation : {row['id_resa']}, ID client : {row['id_user']}, ID véhicule : {row['id_vehicule']}, date de début : {row['date_debut']}, date de fin : {row['date_fin']}, prix : {row['prix_total']}")
                    else:
                        pass
            print("\n--- FIN ---\n")
            input("ENTER pour continuer")

    def rechercher_vehicule_par_id(self, vehicule_id):
        # Recherche du véhicule par ID dans le fichier des véhicules
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id_vehicule'] == vehicule_id and row['dispo'] == 'True':
                    return Vehicule(row['id_vehicule'], row['marque'], row['modele'], row['prix_jour'], row['masse'], row['vitesse_max'], row['puissance'], row['volume_utile'], row['nb_places'], row['type_moteur'], row['hauteur'], row['type_vehicule'], row['boite_vitesse'], row['entretien_annuel'], row['dispo'], row['description'])
        return None

    def reserver_vehicule(self):
        print("\nFaire une réservation :\n")
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
            jours_res = calculer_jours_reservation(date_debut, date_fin)
            prix_vehicule = vehicule.prix_jour
            prix = jours_res * prix_vehicule
            indispo = verifier_reservation(date_debut, date_fin, id_vehicule)

            if indispo:
                type_v = vehicule.type_vehicule
                print("Le véhicule n'est pas disponible aux dates demandées :( .") # SURCLASSEMENT
                surcl_choix = demander_input_bool("Souhaitez-vous surclasser la réservation ? (oui/non): ")
                self.surclassement(vehicule, self.trouver_vehicule_disponible(date_debut, date_fin),date_debut, date_fin, id_user, jours_res, prix, type_v,surcl_choix)
            else:
                id_resa = generer_id_unique(RESERVATIONS_FILE, 'id_resa')
                surclassement = False
                string = string = f"RESERVATION {id_resa} CLIENT {id_user} VEHICULE {id_vehicule} DU {date_debut} AU {date_fin} JOURS {jours_res} PRIX {prix} SURCLASSEMENT {surclassement}"
                reservation = Reservation_DSL.from_dsl(string)
                facture(reservation,info_user(id_user),info_vehicule(id_vehicule))
                Reservation_DSL.enregistrer(reservation, RESERVATIONS_FILE)
                print(f"Réservation n° {id_resa} confirmée pour {id_user} pour le véhicule {vehicule.marque} {vehicule.modele} du {date_debut} au {date_fin} total de {jours_res} jour(s), coût : {prix} €.")
        else:
            print("Véhicule non disponible (maintenance, entretient...)")

    def trouver_vehicule_disponible(self, date_debut, date_fin):
        # Recherche des véhicules disponibles dans le fichier des véhicules
        vehicules_disponibles = []
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['dispo'] == 'True' and not verifier_reservation(date_debut, date_fin, row['id_vehicule']):
                    # Vérification de la disponibilité du véhicule
                    vehicule = load_vehicule_POO(row)
                    vehicules_disponibles.append(vehicule)
        return vehicules_disponibles

    def surclassement(self, Vehicule, vehicules_disponibles,date_debut, date_fin, id_user, jours, prix,type_vehicule,surclassement_choix):
        
        if self.criteres_resa:
            pass
        else:
            print("le type de véhicule n'est pas pris en compte dans la recherche suivante :\n")
            self.criteres_resa = criteres(VEHICULES_FILE)

        if surclassement_choix and self.criteres_resa:
            if Vehicule.type_vehicule not in NO_SURCLASSEMENT_TYPES:
                print("La réservation peut être surclassé.") 
                for element in self.criteres_resa:
                    if element[0] == 'prix_jour':
                        self.criteres_resa.remove(element)
                    if element[0] == 'type_vehicule': #surclassement avec meme type de vehicule si aucun surclassement trouvé on surclasse avec le type donné par le client 
                        self.criteres_resa.remove(element)
                        self.criteres_resa.append(("type_vehicule", "=", type_vehicule))
                for vehicules in vehicules_disponibles:
                    if vehicules.prix_jour >= Vehicule.prix_jour:
                        vehicules.prix_jour = Vehicule.prix_jour
                    else:
                        vehicules.prix_jour = vehicules.prix_jour
                recherche_vehicule = recherche(vehicules_disponibles, self.criteres_resa)
                if recherche_vehicule:
                    while True:
                        choix = demander_input_bool("Souhaitez-vous réserver un véhicule ? (oui/non): ")
                        vehicule_choisi = demander_plaque("Plaque d'immatriculation du véhicule à réserver (format AA-000-AA):")
                        if vehicule_choisi in [v.id_vehicule for v in recherche_vehicule] and choix:
                            id_resa = generer_id_unique(RESERVATIONS_FILE, 'id_resa')
                            if float(trouver_value(VEHICULES_FILE, vehicule_choisi,'id_vehicule','prix_jour')) >= Vehicule.prix_jour:
                                surclassement = True
                            else:
                                surclassement = False 
                            obj_vehicule = info_vehicule(vehicule_choisi)
                            if obj_vehicule.prix_jour >= Vehicule.prix_jour:
                                obj_vehicule.prix_jour = Vehicule.prix_jour
                            prix = obj_vehicule.prix_jour * jours
                            string = string = f"RESERVATION {id_resa} CLIENT {id_user} VEHICULE {obj_vehicule.id_vehicule} DU {date_debut} AU {date_fin} JOURS {jours} PRIX {prix} SURCLASSEMENT {surclassement}"
                            reservation = Reservation_DSL.from_dsl(string)
                            facture(reservation,info_user(id_user),obj_vehicule)
                            Reservation_DSL.enregistrer(reservation, RESERVATIONS_FILE)
                            print(f"Réservation n° {id_resa} confirmée pour {id_user} pour le véhicule {obj_vehicule.marque} {obj_vehicule.modele} du {date_debut} au {date_fin} total de {jours} jour(s), coût : {prix} €.")
                            self.criteres_resa = None
                            break
                        else:
                            print("plaque non valide ou réservation annulée.")
                            self.criteres_resa = None
                            break
                                    
                else:
                    self.criteres_resa = None
                    print("Aucun véhicule trouvé avec les critères spécifiés pour le surclassement.")
                    surclassement_bis = demander_input_bool("Souhaitez-vous un autre surclassement ? (oui/non): ")
                    if surclassement_bis:   
                        print("Veuillez choisir un autre type de véhicule pour nouveau surclassement :")
                        type_vehicule_failed = demander_input_choix("Type de véhicule : ", TYPES_VEHICULE)
                        self.surclassement(Vehicule, vehicules_disponibles,date_debut, date_fin, id_user, jours, prix, type_vehicule_failed, surclassement_bis)
                    else:
                        print("Réservation annulée.")
                        self.criteres_resa = None
            else:
                print("Le véhicule ne peut pas être surclassé ou type de véhicule impossible à surclasser.")
        else:
            print("réservation annulée")

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
            if id_reservation:
                date_debut = trouver_value(RESERVATIONS_FILE, id_reservation, 'id_resa', 'date_debut')
                if user.role == "V" and convertir_date(date_debut).date() >= datetime.today().date():
                    supprimer_ligne_par_id(RESERVATIONS_FILE, "id_resa",id_reservation)
                    supprimer_facture(id_reservation)
                    print(f"Réservation n° {id_reservation} annulée avec succès.")
                if user.role == "C" and convertir_date(date_debut).date() >= datetime.today().date():
                    id_test = trouver_value(RESERVATIONS_FILE, id_reservation, 'id_resa', 'id_user')
                    if user.id_user == id_test:
                        supprimer_ligne_par_id(RESERVATIONS_FILE, "id_resa",id_reservation)
                        supprimer_facture(id_reservation)
                        print(f"Réservation n° {id_reservation} annulée avec succès.")
                    else:
                        print("Vous pouvez supprimer uniquement vos réservations")
                else:
                    print("Vous ne pouvez pas annuler cette réservation.")   
            else:
                print("Aucune réservation trouvée avec cet ID.") 
        else:
            print("ID ou mot de passe incorrect.")

    def creer_compte_client(self):
        print("\nCréer un compte client :\n")
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
        print("\n--- AJOUT D'UN VÉHICULE ---\n")

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
        hauteur = demander_input_float("Hauteur (m) : ")
        type_vehicule = demander_input_choix("Type de véhicule : ", TYPES_VEHICULE)
        boite_vitesse = demander_input_choix("Boîte de vitesse : ", BOITES_VITESSE)
        entretien_annuel = demander_input_float("Entretien annuel (€) : ")
        dispo = demander_input_bool("Le véhicule est-il disponible ? (True/False) : ")
        description = input("Description du véhicule : ").strip()

        vehicule = Vehicule(id_vehicule, marque, modele, prix_jour, masse, vitesse_max, puissance,volume_utile, nb_places, type_moteur, hauteur, type_vehicule, boite_vitesse, entretien_annuel, dispo, description )

        file_exists = os.path.exists(VEHICULES_FILE)
        with open(VEHICULES_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=vehicule.to_dict().keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(vehicule.to_dict())

        print(f"\nVéhicule ajouté avec succès ! ID : {vehicule.id_vehicule}")

    def supprimer_vehicule(self):
        print("\nSupprimer un véhicule :\n")
        user_id = self.utilisateur_connecte.id_user
        mot_de_passe = input("Mot de passe : ")
        user = self.verifier_identifiants(user_id, mot_de_passe)
        if user:
            id_vehicule = demander_plaque("Plaque d'immatriculation du véhicule à supprimer (format AA-000-AA) : ")
            supprimer_ligne_par_id(VEHICULES_FILE, "id_vehicule",id_vehicule)
        else:
            print("ID ou mot de passe incorrect.")

    def supprimer_compte_client(self):
        print("\nSupprimer un compte client :\n")
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
        print("\nChanger de mot de passe :\n")
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

    def changer_caracteristique_vehicule(self):
        print("\nModifier une caractéristique sur un véhicule :\n")
        user_id = self.utilisateur_connecte.id_user
        mot_de_passe = input("Mot de passe : ")
        user = self.verifier_identifiants(user_id, mot_de_passe)
        if user:
            id_vehicule = demander_plaque("Plaque d'immatriculation du véhicule à modifier (format AA-000-AA) : ")
            modifier_champ_csv(VEHICULES_FILE, "id_vehicule", id_vehicule, CHAMPS_INTERDITS)
        else:
            print("ID ou mot de passe incorrect.")

    def changer_caracteristique_compte(self):
        print("\nModifier une caractéristique sur votre compte :\n")
        user_id = self.utilisateur_connecte.id_user
        mot_de_passe = input("Mot de passe : ")
        user = self.verifier_identifiants(user_id, mot_de_passe)
        if user:
            id_user = self.utilisateur_connecte.id_user
            modifier_champ_csv(USER_FILE, "id_user", id_user, CHAMPS_INTERDITS)
        else:
            print("ID ou mot de passe incorrect.")

    def consulter_vehicule(self):
        print("\nConsulter un véhicule :\n")
        id_vehicule = demander_plaque("Plaque d'immatriculation du véhicule à consulter (format AA-000-AA) : ")
        vehicule = self.rechercher_vehicule_par_id(id_vehicule)
        if vehicule:
            Vehicule_1 = info_vehicule(id_vehicule) 
            vdict = Vehicule_1.to_dict()
            print(f"\n--- {id_vehicule} ---\n")   
            for cle, valeur in vdict.items():
                print(f"{cle} : {valeur}")
            print("\n--- FIN ---\n")
            input("ENTER pour continuer")
        else:
            print("Véhicule non trouvé.")

    def consulter_reservations_prochaines_vehicule(self):
        print("\nConsulter les réservations prochaines d'un véhicule :\n")
        id_vehicule = demander_plaque("Plaque d'immatriculation du véhicule (format AA-000-AA) : ")
        print(f"\n--- Réservations du {id_vehicule} --- \n")
        with open(RESERVATIONS_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id_vehicule'] == id_vehicule and convertir_date(row['date_fin']).date() >= datetime.today().date():
                    print(f"ID réservation : {row['id_resa']}, ID client : {row['id_user']}, date de début : {row['date_debut']}, date de fin : {row['date_fin']}, prix : {row['prix_total']}")
        print("\n--- FIN ---\n")
        input("ENTER pour continuer")

    def recherche_de_véhicule_pour_reservation(self):
        vehicules_search = load_vehicules(VEHICULES_FILE)
        print("\nRecherche de véhicule :\n")
        crit = criteres(VEHICULES_FILE)
        resultats = recherche(vehicules_search, crit)
        self.criteres_resa = crit
        if resultats:
            ok_resa = demander_input_bool("Souhaitez-vous réserver un véhicule ? (oui/non): ")
            if ok_resa:    
                self.reserver_vehicule()
        else:
            print("Aucun véhicule trouvé avec les critères spécifiés.")
    
if __name__ == "__main__":
    # Création d'une instance de l'application et lancement du menu principal
    app = Application()
