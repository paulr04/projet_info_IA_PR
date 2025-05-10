
TYPES_VEHICULE = ["berline", "citadine", "avion", "bateau", "SUV", "special", "camion", "utilitaire", "militaire", "4x4", "supercar", "monospace", "pick-up"]
TYPES_MOTEUR = ["essence", "diesel", "electrique", "hybride", 'kerosene', 'hydrogene', 'fioul']
BOITES_VITESSE = ["manuelle", "automatique"]

class Vehicule:
    """
    Auteur : Paul Renaud

    Représente un véhicule disponible à la location.
    """

    def __init__(self, id_vehicule, marque, modele, prix_jour, masse, vitesse_max, puissance,
                 volume_utile, nb_places, type_moteur, hauteur, type_vehicule,
                 boite_vitesse, entretien_annuel, dispo, description):
        self._id_vehicule = id_vehicule
        self._marque = marque
        self._modele = modele
        self._prix_jour = float(prix_jour)
        self._masse = masse
        self._vitesse_max = vitesse_max
        self._puissance = puissance
        self._volume_utile = volume_utile
        self._nb_places = nb_places
        self._type_moteur = type_moteur
        self._hauteur = hauteur
        self._type_vehicule = type_vehicule
        self._boite_vitesse = boite_vitesse
        self._entretien_annuel = entretien_annuel
        self._dispo = bool(dispo)
        self._description = description

    # Properties and setters with validation
    @property
    def id_vehicule(self):
        return self._id_vehicule

    @property
    def marque(self):
        return self._marque

    @marque.setter
    def marque(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError("La marque doit être une chaîne de caractères.")
            self._marque = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def modele(self):
        return self._modele

    @modele.setter
    def modele(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError("Le modèle doit être une chaîne de caractères.")
            self._modele = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def prix_jour(self):
        return self._prix_jour

    @prix_jour.setter
    def prix_jour(self, value):
        try:
            if not isinstance(value, (float, int)) or value <= 0:
                raise ValueError("Le prix par jour doit être un nombre positif.")
            self._prix_jour = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def masse(self):
        return self._masse

    @masse.setter
    def masse(self, value):
        try:
            if not isinstance(value, (float, int)) or value <= 0:
                raise ValueError("La masse doit être un nombre positif.")
            self._masse = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def vitesse_max(self):
        return self._vitesse_max

    @vitesse_max.setter
    def vitesse_max(self, value):
        try:
            if not isinstance(value, (float, int)) or value <= 0:
                raise ValueError("La vitesse maximale doit être un nombre positif.")
            self._vitesse_max = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def puissance(self):
        return self._puissance

    @puissance.setter
    def puissance(self, value):
        try:
            if not isinstance(value, (float, int)) or value <= 0:
                raise ValueError("La puissance doit être un nombre positif.")
            self._puissance = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def volume_utile(self):
        return self._volume_utile

    @volume_utile.setter
    def volume_utile(self, value):
        try:
            if not isinstance(value, (float, int)) or value <= 0:
                raise ValueError("Le volume utile doit être un nombre positif.")
            self._volume_utile = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def nb_places(self):
        return self._nb_places

    @nb_places.setter
    def nb_places(self, value):
        try:
            if not isinstance(value, int) or value <= 0:
                raise ValueError("Le nombre de places doit être un entier positif.")
            self._nb_places = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def type_moteur(self):
        return self._type_moteur

    @type_moteur.setter
    def type_moteur(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError("Le type de moteur doit être une chaîne de caractères.")
            self._type_moteur = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def hauteur(self):
        return self._hauteur

    @hauteur.setter
    def hauteur(self, value):
        try:
            if not isinstance(value, (float, int)) or value <= 0:
                raise ValueError("La hauteur doit être un nombre positif.")
            self._hauteur = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def type_vehicule(self):
        return self._type_vehicule

    @type_vehicule.setter
    def type_vehicule(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError("Le type de véhicule doit être une chaîne de caractères.")
            self._type_vehicule = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def boite_vitesse(self):
        return self._boite_vitesse

    @boite_vitesse.setter
    def boite_vitesse(self, value):
        try:
            if value not in ["manuelle", "automatique"]:
                raise ValueError("La boîte de vitesse doit être 'manuelle' ou 'automatique'.")
            self._boite_vitesse = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def entretien_annuel(self):
        return self._entretien_annuel

    @entretien_annuel.setter
    def entretien_annuel(self, value):
        try:
            if not isinstance(value, (float, int)) or value < 0:
                raise ValueError("L'entretien annuel doit être un nombre positif ou nul.")
            self._entretien_annuel = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def dispo(self):
        return self._dispo

    @dispo.setter
    def dispo(self, value):
        try:
            if not isinstance(value, bool):
                raise ValueError("La disponibilité doit être un booléen.")
            self._dispo = value
        except ValueError as e:
            print(f"Erreur : {e}")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError("La description doit être une chaîne de caractères.")
            self._description = value
        except ValueError as e:
            print(f"Erreur : {e}")

    def to_dict(self):
        """Convertit l'objet Véhicule en dictionnaire pour une utilisation dans la base de données."""
        return self.__dict__

    def __str__(self):
        """Retourne une chaîne de caractères représentant le véhicule."""
        return (f"{self.marque} {self.modele} ({self.type_vehicule}) - {self.id_vehicule} - "
                f"{self.prix_jour:.2f}€/jour - {self.nb_places} places - {self.dispo}")

    # Method to set a value to any instance variable
    def set_valeur(self, attribut, valeur):
        try:
            if hasattr(self, attribut):
                setattr(self, attribut, valeur)
            else:
                raise AttributeError(f"L'attribut {attribut} n'existe pas.")
        except Exception as e:
            print(f"Erreur : {e}")
