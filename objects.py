import re
import os
import csv

USER_FILE = 'data/users.csv'
VEHICULES_FILE = 'data/vehicules.csv'
RESERVATIONS_FILE = 'data/reservations.csv'

CHAMPS_INTERDITS = ['id_user', 'id_resa', 'id_vehicule', 'role', 'mot_de_passe', 'type_moteur', 'type_vehicule', 'boite_vitesse']
NO_SURCLASSEMENT_TYPES = ["avion", "bateau", "militaire", "special",'autre', 'chantier', 'helicoptere', 'formule 1', 'rally']
TYPES_VEHICULE = ["berline", "citadine", "avion", "bateau", "SUV", "special", "camion", "utilitaire", "militaire", "4x4", "supercar", "monospace", "pick-up", "velo", "moto", "quad", "trottinette", "camionette", "bus", "minibus", "cabriolet", "roadster", "coupe", "break", "limousine", "formule 1", "rallye", "helicoptere", "chantier",'autre']
TYPES_MOTEUR = ["essence", "diesel", "electrique", "hybride", 'kerosene', 'hydrogene', 'fioul', 'nucleaire', 'gaz', 'propergol', 'autre']
BOITES_VITESSE = ["manuelle", "automatique"]


class Vehicule:
    """
    ---
    Auteur : Paul Renaud
    ---
    Représente un véhicule disponible à la location.
    ---
    attributs :
    - id_vehicule : str place au format 'AA-123-AA'
    - marque : str marque du véhicule
    - modele : str modèle du véhicule
    - prix_jour : float prix par jour de location en euros
    - masse : float masse du véhicule en kg
    - vitesse_max : float vitesse maximale en km/h
    - puissance : float puissance du moteur en chevaux
    - volume_utile : float volume utile en m3
    - nb_places : int nombre de places assises
    - type_moteur : str type de moteur (essence, diesel, électrique, hybride, etc.)
    - hauteur : float hauteur du véhicule en m
    - type_vehicule : str type de véhicule (berline, citadine, SUV, etc.)
    - boite_vitesse : str type de boîte de vitesse (manuelle, automatique)
    - entretien_annuel : float coût d'entretien annuel en euros
    - dispo : bool disponibilité True ou False) en cas de maintenance
    - description : str description du véhicule
    ---
    méthodes :
    - __init__ : constructeur de la classe
    - to_dict : convertit l'objet Véhicule en dictionnaire pour une utilisation dans la base de données
    - __str__ : retourne une chaîne de caractères représentant le véhicule
    - set_valeur : méthode pour définir une valeur à n'importe quel attribut de l'objet
    - getters et setters pour chaque attribut avec validation
    ---
    """
    def __init__(self, id_vehicule, marque, modele, prix_jour, masse, vitesse_max, puissance,
                 volume_utile, nb_places, type_moteur, hauteur, type_vehicule,
                 boite_vitesse, entretien_annuel, dispo, description):
        self._id_vehicule = str(id_vehicule)
        self._marque = str(marque)
        self._modele = str(modele)
        self._prix_jour = float(prix_jour)
        self._masse = float(masse)
        self._vitesse_max = float(vitesse_max)
        self._puissance = float(puissance)
        self._volume_utile = float(volume_utile)
        self._nb_places = int(nb_places)
        self._type_moteur = str(type_moteur)
        self._hauteur = float(hauteur)
        self._type_vehicule = str(type_vehicule)
        self._boite_vitesse = str(boite_vitesse)
        self._entretien_annuel = float(entretien_annuel)
        self._dispo = bool(dispo)
        self._description = str(description)
        # Validation des attributs sur l'initialisation
        try:
            if not re.match(r"^[A-Z]{2}-\d{3}-[A-Z]{2}$", id_vehicule) or not isinstance(id_vehicule, str):
                raise ValueError("L'ID du véhicule doit être au format 'AA-123-AA' et en str.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise   
        try:
            if not isinstance(marque, str):
                raise ValueError("La marque doit être une chaîne de caractères.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(modele, str):
                raise ValueError("Le modèle doit être une chaîne de caractères.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(prix_jour, (float, int)) or prix_jour < 0:
                raise ValueError("Le prix par jour doit être un nombre positif.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(masse, (float, int)) or masse <= 0:
                raise ValueError("La masse doit être un nombre positif.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(vitesse_max, (float, int)) or vitesse_max < 0:
                raise ValueError("La vitesse maximale doit être un nombre positif.")
        except ValueError as e: 
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(puissance, (float, int)) or puissance < 0:
                raise ValueError("La puissance doit être un nombre positif.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(volume_utile, (float, int)) or volume_utile < 0:
                raise ValueError("Le volume utile doit être un nombre positif.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise   
        try:
            if not isinstance(nb_places, int) or nb_places < 0:
                raise ValueError("Le nombre de places doit être un entier positif.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise   
        try:
            if not isinstance(type_moteur, str) or type_moteur not in TYPES_MOTEUR:
                raise ValueError(f"Le type de moteur doit être l'un des suivants : {', '.join(TYPES_MOTEUR)}.") 
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(hauteur, (float, int)) or hauteur <= 0:
                raise ValueError("La hauteur doit être un nombre positif.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(type_vehicule, str) or type_vehicule not in TYPES_VEHICULE:
                raise ValueError(f"Le type de véhicule doit être l'un des suivants : {', '.join(TYPES_VEHICULE)}.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(boite_vitesse, str) or boite_vitesse not in BOITES_VITESSE:
                raise ValueError(f"La boîte de vitesse doit être l'une des suivantes : {', '.join(BOITES_VITESSE)}.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(entretien_annuel, (float, int)) or entretien_annuel < 0:
                raise ValueError("L'entretien annuel doit être un nombre positif ou nul.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(dispo, bool):
                raise ValueError("La disponibilité doit être un booléen.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(description, str):
                raise ValueError("La description doit être une chaîne de caractères.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise

    # propriétés pour chaque attribut avec validation
    @property
    def id_vehicule(self):
        return self._id_vehicule

    @id_vehicule.setter
    def id_vehicule(self, value):
        if not re.match(self.ID_VEHICULE_REGEX, value):
            raise ValueError("L'ID du véhicule doit être au format 'AA-123-AA'.")
        self._id_vehicule = value

    @property
    def marque(self):
        return self._marque

    @marque.setter
    def marque(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError("La marque doit être une chaîne de caractères.")
            self._marque = value
        except ValueError:
            raise ValueError("Erreur : La marque doit être une chaîne de caractères.")

    @property
    def modele(self):
        return self._modele

    @modele.setter
    def modele(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError("Le modèle doit être une chaîne de caractères.")
            self._modele = value
        except ValueError:
            raise ValueError("Erreur : Le modèle doit être une chaîne de caractères.")

    @property
    def prix_jour(self):
        return self._prix_jour

    @prix_jour.setter
    def prix_jour(self, value):
        try:
            if not isinstance(value, (float, int)) or value < 0:
                raise ValueError("Le prix par jour doit être un nombre positif.")
            self._prix_jour = value
        except ValueError:
            raise ValueError("Erreur : Le prix par jour doit être un nombre positif.")

    @property
    def masse(self):
        return self._masse

    @masse.setter
    def masse(self, value):
        try:
            if not isinstance(value, (float, int)) or value <= 0:
                raise ValueError("La masse doit être un nombre positif.")
            self._masse = value
        except ValueError:
            raise ValueError("Erreur : La masse doit être un nombre positif.")

    @property
    def vitesse_max(self):
        return self._vitesse_max

    @vitesse_max.setter
    def vitesse_max(self, value):
        try:
            if not isinstance(value, (float, int)) or value < 0:
                raise ValueError("La vitesse maximale doit être un nombre positif.")
            self._vitesse_max = value
        except ValueError:
            raise ValueError("Erreur : La vitesse maximale doit être un nombre positif.")

    @property
    def puissance(self):
        return self._puissance

    @puissance.setter
    def puissance(self, value):
        try:
            if not isinstance(value, (float, int)) or value < 0:
                raise ValueError("La puissance doit être un nombre positif.")
            self._puissance = value
        except ValueError:
            raise ValueError("Erreur : La puissance doit être un nombre positif.")

    @property
    def volume_utile(self):
        return self._volume_utile

    @volume_utile.setter
    def volume_utile(self, value):
        try:
            if not isinstance(value, (float, int)) or value < 0:
                raise ValueError("Le volume utile doit être un nombre positif.")
            self._volume_utile = value
        except ValueError:
            raise ValueError("Erreur : Le volume utile doit être un nombre positif.")

    @property
    def nb_places(self):
        return self._nb_places

    @nb_places.setter
    def nb_places(self, value):
        try:
            if not isinstance(value, int) or value < 0:
                raise ValueError("Le nombre de places doit être un entier positif.")
            self._nb_places = value
        except ValueError:
            raise ValueError("Erreur : Le nombre de places doit être un entier positif.")

    @property
    def type_moteur(self):
        return self._type_moteur

    @type_moteur.setter
    def type_moteur(self, value):
        try:
            if value not in TYPES_MOTEUR:
                raise ValueError(f"Le type de moteur doit être l'un des suivants : {', '.join(TYPES_MOTEUR)}.")
            self._type_moteur = value
        except ValueError:
            raise ValueError(f"Erreur : Le type de moteur doit être l'un des suivants : {', '.join(TYPES_MOTEUR)}.")

    @property
    def hauteur(self):
        return self._hauteur

    @hauteur.setter
    def hauteur(self, value):
        try:
            if not isinstance(value, (float, int)) or value <= 0:
                raise ValueError("La hauteur doit être un nombre positif.")
            self._hauteur = value
        except ValueError:
            raise ValueError("Erreur : La hauteur doit être un nombre positif.")

    @property
    def type_vehicule(self):
        return self._type_vehicule

    @type_vehicule.setter
    def type_vehicule(self, value):
        try:
            if value not in TYPES_VEHICULE:
                raise ValueError(f"Le type de véhicule doit être l'un des suivants : {', '.join(TYPES_VEHICULE)}.")
            self._type_vehicule = value
        except ValueError:
            raise ValueError(f"Erreur : Le type de véhicule doit être l'un des suivants : {', '.join(TYPES_VEHICULE)}.")

    @property
    def boite_vitesse(self):
        return self._boite_vitesse

    @boite_vitesse.setter
    def boite_vitesse(self, value):
        try:
            if value not in BOITES_VITESSE:
                raise ValueError(f"La boîte de vitesse doit être l'une des suivantes : {', '.join(BOITES_VITESSE)}.")
            self._boite_vitesse = value
        except ValueError:
            raise ValueError(f"Erreur : La boîte de vitesse doit être l'une des suivantes : {', '.join(BOITES_VITESSE)}.")

    @property
    def entretien_annuel(self):
        return self._entretien_annuel

    @entretien_annuel.setter
    def entretien_annuel(self, value):
        try:
            if not isinstance(value, (float, int)) or value < 0:
                raise ValueError("L'entretien annuel doit être un nombre positif ou nul.")
            self._entretien_annuel = value
        except ValueError:
            raise ValueError("Erreur : L'entretien annuel doit être un nombre positif ou nul.")

    @property
    def dispo(self):
        return self._dispo

    @dispo.setter
    def dispo(self, value):
        try:
            if not isinstance(value, bool):
                raise ValueError("La disponibilité doit être un booléen.")
            self._dispo = value
        except ValueError:
            raise ValueError("Erreur : La disponibilité doit être un booléen.")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError("La description doit être une chaîne de caractères.")
            self._description = value
        except ValueError:
            raise ValueError("Erreur : La description doit être une chaîne de caractères.")

    def to_dict(self):
        """Convertit l'objet Véhicule en dictionnaire pour une utilisation dans la base de données."""
        return self.__dict__

    def __str__(self):
        """Retourne une chaîne de caractères représentant le véhicule."""
        return (f"{self.marque} {self.modele} ({self.type_vehicule}) - {self.id_vehicule} - "
                f"{self.prix_jour:.2f}€/jour - {self.nb_places} places - {self.dispo}")

    # Méthode pour définir une valeur à n'importe quel attribut de l'objet
    # en vérifiant si l'attribut existe et en respectant les types
    def set_valeur(self, attribut, valeur):
        try:
            if hasattr(self, attribut):
                setattr(self, attribut, valeur)
            else:
                raise AttributeError(f"L'attribut {attribut} n'existe pas.")
        except AttributeError:
            raise AttributeError(f"Erreur : L'attribut {attribut} n'existe pas.")


class User:
    """
    Auteur : Paul Renaud

    Représente un utilisateur de l'application de gestion de location de véhicules.

    Un utilisateur peut être un client ('C') ou un vendeur ('V').

    Attributs :
        id_user (int)     : Identifiant unique de l'utilisateur.
        nom (str)           : Nom de l'utilisateur.
        prenom (str)        : Prénom de l'utilisateur.
        email (str)         : Adresse e-mail.
        telephone (str)     : Numéro de téléphone.
        mot_de_passe (str)  : Mot de passe (stocké en clair dans le CSV).
        role (str)          : Rôle de l'utilisateur ('C' pour client, 'V' pour vendeur).

    Méthodes :
        to_dict()           : Renvoie une représentation dictionnaire de l'utilisateur.
        save_to_file()      : Enregistre l'utilisateur dans le fichier CSV s'il n'existe pas déjà.
    """

    def __init__(self, id_user, nom, prenom, email, telephone, role, mot_de_passe, app):
        self.id_user = id_user
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone
        self.role = role
        self.mot_de_passe = mot_de_passe
        self.app = app
        try:
            if not re.match(r"^\d{9}$", id_user) or not isinstance(id_user, str):
                raise ValueError("L'ID de l'utilisateur doit être au format '123456789' et en str.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du client : {e}")
            raise
        try:
            if not isinstance(nom, str):
                raise ValueError("Le nom doit être une chaîne de caractères.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du client : {e}")
            raise
        try:
            if not isinstance(prenom, str):
                raise ValueError("Le prénom doit être une chaîne de caractères.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du client : {e}")
            raise
        try:
            if not isinstance(email, str):
                raise ValueError("L'email doit être une chaîne de caractères.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du client : {e}")
            raise
        try:
            if not re.match(r"^\d{10}$", telephone) or not isinstance(telephone, str):
                raise ValueError("Le téléphone doit être au format '0123456789' et en str.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du client : {e}")
            raise
        try:
            if not isinstance(mot_de_passe, str):
                raise ValueError("Le mot de passe doit être une chaîne de caractères.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du client : {e}")
            raise
    def to_dict(self):
        """
        Convertit l'objet User en dictionnaire pour une utilisation dans la base de données.

        Retour :
            d: Représentation de l'objet sous forme de dictionnaire.
        """
        d = self.__dict__.copy()
        d.pop('app', None)  
        return d

    def __str__(self):
        """
        Retourne une chaîne de caractères représentant l'utilisateur'.

        Retour :
            str : Prénom, Nom et rôle de l'utilisateur.
        """
        return f"{self.prenom} {self.nom} - {self.role}"

class Client(User):
    """
    Auteur : Paul Renaud

    Représente un client de l'application de gestion de location de véhicules.

    Attributs :
        id_user (int)     : Identifiant unique de l'utilisateur.
        nom (str)           : Nom de l'utilisateur.
        prenom (str)        : Prénom de l'utilisateur.
        email (str)         : Adresse e-mail.
        telephone (str)     : Numéro de téléphone.
        mot_de_passe (str)  : Mot de passe (stocké en clair dans le CSV).
        role (str)          : Rôle de l'utilisateur ('C' pour client, 'V' pour vendeur, 'A' pour admin).
    """
    def __init__(self, id_user, nom, prenom, email, telephone, role, mot_de_passe, app):
        super().__init__(id_user, nom, prenom, email, telephone, "C", mot_de_passe, app)
         # Vérification que le rôle est 'C' pour client
        try:
            if role != "C":
                raise ValueError("Le rôle doit être 'C' pour client.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du vendeur : {e}")
            raise 
    def menu(self):
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
                self.app.consulter_catalogue()
            elif choix == "2":
                self.app.recherche_de_véhicule_pour_reservation()
            elif choix == "3":
                self.app.consulter_reservations()
            elif choix == "4":
                self.app.reserver_vehicule()
            elif choix == "5":
                self.app.supprimer_compte_client()
                break
            elif choix == "6":
                self.app.annuler_reservation()
            elif choix == "7":
                self.app.changer_de_mdp()
                break
            elif choix == "8":
                self.app.changer_caracteristique_compte()
            elif choix == "9":
                print("Déconnexion...")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")
    @property
    def reduction_coef(self):
        return 1.0 # Coefficient de réduction pour les clients, pas de réduction

class Vendeur(User):
    """
    Auteur : Paul Renaud

    Représente un vendeur de l'application de gestion de location de véhicules.

    Attributs :
        id_user (int)     : Identifiant unique de l'utilisateur.
        nom (str)           : Nom de l'utilisateur.
        prenom (str)        : Prénom de l'utilisateur.
        email (str)         : Adresse e-mail.
        telephone (str)     : Numéro de téléphone.
        mot_de_passe (str)  : Mot de passe (stocké en clair dans le CSV).
        role (str)          : Rôle de l'utilisateur ('C' pour client, 'V' pour vendeur, 'A' pour admin).
    """
    def __init__(self, id_user, nom, prenom, email, telephone, role, mot_de_passe, app):
        super().__init__(id_user, nom, prenom, email, telephone, "V", mot_de_passe, app)
        # Vérification que le rôle est 'V' pour vendeur
        try:
            if role != "V":
                raise ValueError("Le rôle doit être 'V' pour vendeur.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du vendeur : {e}")
            raise 

    def menu(self):
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
                self.app.consulter_catalogue()
            elif choix == "2":
                self.app.consulter_user()
            elif choix == "3":
                self.app.consulter_reservations()
            elif choix == "4":
                self.app.ajouter_vehicule()
            elif choix == "5":
                self.app.supprimer_vehicule()
            elif choix == "6":
                self.app.reserver_vehicule()
            elif choix == "7":
                self.app.annuler_reservation()
            elif choix == "8":
                self.app.creer_compte_client()
            elif choix == "9":
                self.app.supprimer_compte_client()
            elif choix == "10":
                self.app.changer_de_mdp()
                break 
            elif choix == "11":
                self.menu_analyse_ventes()
            elif choix == "12":
                self.app.changer_caracteristique_vehicule()
            elif choix == "13":
                self.app.changer_caracteristique_compte()
            elif choix == "14":
                self.app.consulter_reservations_prochaines_vehicule()
            elif choix == "15":
                self.app.consulter_vehicule()
            elif choix == "16":
                print("Déconnexion...")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")
    def menu_analyse_ventes(self):
        """
        Analyse les ventes du vendeur.
        """
        import fonctions as f
        USER_FILE = 'data/users.csv'
        VEHICULES_FILE = 'data/vehicules.csv'
        RESERVATIONS_FILE = 'data/reservations.csv'
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
                f.plot_reservations_par_mois()   
            elif choix == "2":                   
                f.plot_reservations_par_annee()
            elif choix == "3":
                print("\nChoisir l'année :")
                annee = f.demander_input_int("Année : ")
                f.benefice_pour_annee(annee)
                input("ENTER pour continuer")
            elif choix == "4":
                f.benefice_par_annee_histogramme()
            elif choix == "5":
                f.afficher_benefice_total()
                input("ENTER pour continuer")
            elif choix == "6":
                print("\nChoisir l'année :")
                annee = f.demander_input_int("Année : ")
                f.reservations_par_vehicule_par_an(annee=annee)
            elif choix == "7":
                f.plot_reservations_par_vehicule()
            elif choix == "8":
                f.plot_rentabilite_depuis_csv(RESERVATIONS_FILE, VEHICULES_FILE)
            elif choix == "9":
                f.plot_reservations_histogram(RESERVATIONS_FILE)
            elif choix == "10":
                print("Retour...")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")
    @property
    def reduction_coef(self):
        return 0.8  # Coefficient de réduction pour les vendeurs   
    
class Admin(User):
    """
    Auteur : Paul Renaud

    Représente un administrateur de l'application de gestion de location de véhicules.

    Attributs :
        id_user (int)     : Identifiant unique de l'utilisateur.
        nom (str)           : Nom de l'utilisateur.
        prenom (str)        : Prénom de l'utilisateur.
        email (str)         : Adresse e-mail.
        telephone (str)     : Numéro de téléphone.
        mot_de_passe (str)  : Mot de passe (stocké en clair dans le CSV).
        role (str)          : Rôle de l'utilisateur ('C' pour client, 'V' pour vendeur, 'A' pour admin).
    """
    def __init__(self, id_user, nom, prenom, email, telephone, role, mot_de_passe, app):
        super().__init__(id_user, nom, prenom, email, telephone, "A", mot_de_passe, app)
         # Vérification que le rôle est 'A' pour admin
        try:
            if role != "A":
                raise ValueError("Le rôle doit être 'A' pour admin.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation de l'administrateur : {e}")
            raise
    @property
    def reduction_coef(self):
        return 0  # Coefficient de réduction pour les administrateurs

    def menu(self):
        """
        Affiche le menu de l'administrateur et gère les actions.
        
        Le rôle d'administrateur n'existait pas initialement dans l'application console, 
        mais il est ajouté pour la gestion des utilisateurs (vendeurs) et des véhicules.
        le menu est donc vide car l'application texte est obsolète et elle n'est plus utilisée.
        """
        pass
class Reservation_DSL:
    """
    Auteur : Paul Renaud

    Représente une réservation de véhicule effectuée par un client.

    Attributs :
        id_resa (str)         : Identifiant unique de la réservation (9 chiffres entre 1 et 9).
        id_user (str)         : Identifiant de l'utilisateur (9 chiffres entre 1 et 9).
        id_vehicule (str)     : Identifiant du véhicule (format AA-123-AA).
        date_debut (str)      : Date de début de location (format MM-DD-YYYY).
        date_fin (str)        : Date de fin de location (format MM-DD-YYYY).
        jours (int)           : Durée de la réservation.
        prix_total (float)    : Prix total.
        surclassement (bool) : True si surclassement.
    Méthodes :
        from_dsl(dsl: str)    : Crée une instance de Reservation à partir d'une chaîne DSL.
        enregistrer(chemin_fichier : str)       : Enregistre la réservation dans un fichier CSV.
    """

    def __init__(self, id_resa, id_user, id_vehicule, date_debut, date_fin, jours, prix_total, surclassement=False):
        self.id_resa = id_resa
        self.id_user = id_user
        self.id_vehicule = id_vehicule
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.jours = jours
        self.prix_total = prix_total
        self.surclassement = surclassement
        # Validation des attributs sur l'initialisation
        try:
            if not re.match(r"^\d{9}$", id_resa) or not isinstance(id_resa, str):
                raise ValueError("L'ID de réservation doit être au format '123456789' et en str.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation de la réservation : {e}")
            raise
        try:
            if not re.match(r"^\d{9}$", id_user) or not isinstance(id_user, str):
                raise ValueError("L'ID de l'utilisateur doit être au format '123456789' et en str.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation de la réservation : {e}")
            raise
        try:
            if not re.match(r"^[A-Z]{2}-\d{3}-[A-Z]{2}$", id_vehicule) or not isinstance(id_vehicule, str):
                raise ValueError("L'ID du véhicule doit être au format 'AA-123-AA' et en str.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation de la réservation : {e}")
            raise
        try:
            if not re.match(r"^\d{2}-\d{2}-\d{4}$", date_debut) or not isinstance(date_debut, str):
                raise ValueError("La date de début doit être au format 'MM-DD-YYYY' et en str.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation de la réservation : {e}")
            raise
        try:
            if not re.match(r"^\d{2}-\d{2}-\d{4}$", date_fin) or not isinstance(date_fin, str):
                raise ValueError("La date de fin doit être au format 'MM-DD-YYYY' et en str.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation de la réservation : {e}")
            raise
        try:
            if not isinstance(jours, int) or jours <= 0:
                raise ValueError("Le nombre de jours doit être un entier positif.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation de la réservation : {e}")
            raise
        try:
            if not isinstance(prix_total, (float, int)) or prix_total < 0:
                raise ValueError("Le prix total doit être un nombre positif.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation de la réservation : {e}")
            raise
        try:
            if not isinstance(surclassement, bool):
                raise ValueError("Le surclassement doit être un booléen.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation de la réservation : {e}")
            raise

    @classmethod
    def from_dsl(cls, dsl: str):
        """
        DSL attendu :
        "RESERVATION[123456789] CLIENT[987654321] VEHICULE[AB-123-CD] DU[05-01-2025] AU[05-05-2025] JOURS[3] PRIX[400.00] SURCLASSEMENT[True]"

        """
        import re

        pattern = r"RESERVATION (\d{9}) CLIENT (\d{9}) VEHICULE ([A-Z]{2}-\d{3}-[A-Z]{2}) DU (\d{2}-\d{2}-\d{4}) AU (\d{2}-\d{2}-\d{4}) JOURS (\d+) PRIX ([\d\.]+) SURCLASSEMENT (True|False)"
        try:
            match = re.match(pattern, dsl)
            if match:
                id_resa, id_user, id_vehicule, date_debut, date_fin, jours, prix_total , surclassement_str = match.groups()
                # Conversion des types
                jours = int(jours)
                prix_total = float(prix_total)
                surclassement = surclassement_str == "True" if surclassement_str else False
                # verification des valeurs
                try:
                    if not re.match(r"^\d{9}$", id_resa) or not isinstance(id_resa, str):
                        raise ValueError("L'ID de réservation doit être au format '123456789' et en str.")
                except ValueError as e:
                    print(f"Erreur lors de l'initialisation de la réservation : {e}")
                    raise
                try:
                    if not re.match(r"^\d{9}$", id_user) or not isinstance(id_user, str):
                        raise ValueError("L'ID de l'utilisateur doit être au format '123456789' et en str.")
                except ValueError as e:
                    print(f"Erreur lors de l'initialisation de la réservation : {e}")
                    raise
                try:
                    if not re.match(r"^[A-Z]{2}-\d{3}-[A-Z]{2}$", id_vehicule) or not isinstance(id_vehicule, str):
                        raise ValueError("L'ID du véhicule doit être au format 'AA-123-AA' et en str.")
                except ValueError as e:
                    print(f"Erreur lors de l'initialisation de la réservation : {e}")
                    raise
                try:
                    if not re.match(r"^\d{2}-\d{2}-\d{4}$", date_debut) or not isinstance(date_debut, str):
                        raise ValueError("La date de début doit être au format 'MM-DD-YYYY' et en str.")
                except ValueError as e:
                    print(f"Erreur lors de l'initialisation de la réservation : {e}")
                    raise   
                try:
                    if not re.match(r"^\d{2}-\d{2}-\d{4}$", date_fin) or not isinstance(date_fin, str):
                        raise ValueError("La date de fin doit être au format 'MM-DD-YYYY' et en str.")
                except ValueError as e:
                    print(f"Erreur lors de l'initialisation de la réservation : {e}")
                    raise
                try:
                    if not isinstance(jours, int) or jours <= 0:
                        raise ValueError("Le nombre de jours doit être un entier positif.")
                except ValueError as e:
                    print(f"Erreur lors de l'initialisation de la réservation : {e}")
                    raise
                try:
                    if not isinstance(prix_total, (float, int)) or prix_total < 0:
                        raise ValueError("Le prix total doit être un nombre positif.")
                except ValueError as e:
                    print(f"Erreur lors de l'initialisation de la réservation : {e}")
                    raise
                try:
                    if not isinstance(surclassement_str, str) or surclassement_str not in ["True", "False"]:
                        raise ValueError("Le surclassement doit être 'True' ou 'False'.")
                except ValueError as e:
                    print(f"Erreur lors de l'initialisation de la réservation : {e}")
                    raise
                surclassement = surclassement_str == "True" if surclassement_str else False
                return cls(id_resa, id_user, id_vehicule, date_debut, date_fin, int(jours), float(prix_total), bool(surclassement))
            if not match:
                raise ValueError("DSL invalide. Format attendu : ""RESERVATION 578878064 CLIENT 000000230 VEHICULE FR-416-FR DU 08-08-2025 AU 08-09-2025 JOURS 2 PRIX 30000.0 SURCLASSEMENT False")
        except ValueError:
            raise  ValueError("DSL invalide. Format attendu : ""RESERVATION 578878064 CLIENT 000000230 VEHICULE FR-416-FR DU 08-08-2025 AU 08-09-2025 JOURS 2 PRIX 30000.0 SURCLASSEMENT False")
    def enregistrer(self, chemin_fichier="data/reservations.csv"):
        """
        Enregistre la réservation actuelle dans un fichier CSV.
        Si le fichier n'existe pas, l'en-tête est ajoutée.
        """
        file_exists = os.path.exists(chemin_fichier)
        with open(chemin_fichier, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "id_resa", "id_user", "id_vehicule",
                "date_debut", "date_fin", "jours",
                "prix_total", "surclassement"
            ])
            if not file_exists:
                writer.writeheader()
            writer.writerow(self.to_dict())

    def to_dict(self):
        return {
            "id_resa": self.id_resa,
            "id_user": self.id_user,
            "id_vehicule": self.id_vehicule,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "jours": self.jours,
            "prix_total": self.prix_total,
            "surclassement": self.surclassement
        }

    def __str__(self):
        return (
            f"Réservation {self.id_resa} | Client {self.id_user} | Véhicule {self.id_vehicule} | "
            f"Du {self.date_debut} au {self.date_fin} ({self.jours} jours) | "
            f"Prix : {self.prix_total:.2f}€ | Surclassement : {'Oui' if self.surclassement else 'Non'}"
        )

