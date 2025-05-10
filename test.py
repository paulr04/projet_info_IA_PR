import re

TYPES_VEHICULE = ["berline", "citadine", "avion", "bateau", "SUV", "special", "camion", "utilitaire", "militaire", "4x4", "supercar", "monospace", "pick-up"]
TYPES_MOTEUR = ["essence", "diesel", "electrique", "hybride", 'kerosene', 'hydrogene', 'fioul']
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
    - dispo : bool disponibilité du véhicule (True ou False) en cas de maintenance
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
            if not isinstance(prix_jour, (float, int)) or prix_jour <= 0:
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
            if not isinstance(vitesse_max, (float, int)) or vitesse_max <= 0:
                raise ValueError("La vitesse maximale doit être un nombre positif.")
        except ValueError as e: 
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(puissance, (float, int)) or puissance <= 0:
                raise ValueError("La puissance doit être un nombre positif.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise
        try:
            if not isinstance(volume_utile, (float, int)) or volume_utile <= 0:
                raise ValueError("Le volume utile doit être un nombre positif.")
        except ValueError as e:
            print(f"Erreur lors de l'initialisation du véhicule : {e}")
            raise   
        try:
            if not isinstance(nb_places, int) or nb_places <= 0:
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
            if not isinstance(value, (float, int)) or value <= 0:
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
            if not isinstance(value, (float, int)) or value <= 0:
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
            if not isinstance(value, (float, int)) or value <= 0:
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
            if not isinstance(value, (float, int)) or value <= 0:
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
            if not isinstance(value, int) or value <= 0:
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


class Vehicule:
    """
    Auteur : Paul Renaud

    Représente un véhicule disponible à la location.

    Attributs :
        id_vehicule (str)     : Identifiant unique du véhicule (généré automatiquement).
        marque (str)          : Marque du véhicule.
        modele (str)          : Modèle du véhicule.
        prix_jour (float)     : Prix de la location par jour en euros.
        masse (float)         : Masse du véhicule en kg.
        vitesse_max (float)   : Vitesse maximale du véhicule en km/h.
        puissance (float)     : Puissance du véhicule en chevaux.
        volume_utile (float)  : Volume utile du véhicule en m³.
        nb_places (int)       : Nombre de places assises dans le véhicule.
        type_moteur (str)     : Type de moteur du véhicule (ex : "essence", "diesel", "électrique",...).
        hauteur (float)       : Hauteur du véhicule en m.
        type_vehicule (str)   : Type du véhicule (ex : "berline", "citadine", "avion", "tank").
        boite_vitesse (str)   : Type de boîte de vitesse du véhicule ("manuelle" ou "automatique").
        entretien_annuel (float) : Prix en euros de l'entretien annuel du véhicule.
        dispo (bool)          : Disponibilité du véhicule (True si disponible, False sinon).
        description (str)     : Description textuelle du véhicule.

    Méthodes :
        to_dict()           : Renvoie une représentation dictionnaire du véhicule.
        save_to_file()      : Enregistre le véhicule dans le fichier CSV s'il n'existe pas déjà.
    """

    def __init__(self, id_vehicule, marque, modele, prix_jour, masse, vitesse_max, puissance,
        volume_utile, nb_places, type_moteur, hauteur, type_vehicule,
        boite_vitesse, entretien_annuel, dispo, description):
        self.id_vehicule = id_vehicule
        self.marque = marque
        self.modele = modele
        self.prix_jour = float(prix_jour)
        self.masse = masse
        self.vitesse_max = vitesse_max
        self.puissance = puissance
        self.volume_utile = volume_utile
        self.nb_places = nb_places
        self.type_moteur = type_moteur
        self.hauteur = hauteur
        self.type_vehicule = type_vehicule
        self.boite_vitesse = boite_vitesse
        self.entretien_annuel = entretien_annuel
        self.dispo = bool(dispo)
        self.description = description

    def to_dict(self):
        """
        Convertit l'objet Véhicule en dictionnaire pour une utilisation dans la base de données.

        Retour :
            dict : Représentation de l'objet sous forme de dictionnaire.
        """
        return self.__dict__

    def __str__(self):
        """
        Retourne une chaîne de caractères représentant le véhicule.

        Retour :
            str : Quelques caractéristiques du véhicule.
        """
        return (f"{self.marque} {self.modele} ({self.type_vehicule}) - {self.id_vehicule} - "
                f"{self.prix_jour:.2f}€/jour - {self.nb_places} places - {self.dispo}")
