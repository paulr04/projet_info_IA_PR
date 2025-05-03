
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
        dimensions (tuple)    : Dimensions du véhicule sous forme de tuple (longueur, largeur, hauteur) en m.
        type_vehicule (str)   : Type du véhicule (ex : "berline", "citadine", "avion", "tank").
        boite_vitesse (str)   : Type de boîte de vitesse du véhicule ("manuelle" ou "automatique").
        entretien_annuel (float) : Prix en euros de l'entretien annuel du véhicule.
        dispo (bool)          : Disponibilité du véhicule (True si disponible, False sinon).
        description (str)     : Description textuelle du véhicule.

    Méthodes :
        to_dict()           : Renvoie une représentation dictionnaire du véhicule.
        save_to_file()      : Enregistre le véhicule dans le fichier CSV s'il n'existe pas déjà.
    """

    def __init__(
        self, id_vehicule, marque, modele, prix_jour, masse, vitesse_max, puissance,
        volume_utile, nb_places, type_moteur, dimensions, type_vehicule,
        boite_vitesse, entretien_annuel, dispo, description
    ):
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
        self.dimensions = str(dimensions)
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

class Reservation:
    """
    Auteur : Paul Renaud

    Représente une réservation de véhicule effectuée par un client.

    Attributs :
        id_resa (str)         : Identifiant unique de la réservation.
        id_user (str)         : Identifiant de l'utilisateur.
        id_vehicule (str)     : Identifiant du véhicule réservé.
        date_debut (str)      : Date de début de la location (format YYYY-MM-DD).
        date_fin (str)        : Date de fin de la location (format YYYY-MM-DD).
        jours (int)           : Nombre de jour(s) (durée de la réservation)
        prix_total (str)      : Prix total de la réservation en EUR €

    Méthodes :
        to_dict()             : Renvoie une représentation dictionnaire de la réservation.
        save_to_file()        : Enregistre la réservation dans le fichier CSV.
    """

    def __init__(self, id_resa, id_user, id_vehicule, date_debut, date_fin, jours, prix_total):
        self.id_resa = id_resa
        self.id_user = id_user
        self.id_vehicule = id_vehicule
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.jours = jours
        self.prix_total = prix_total

    def to_dict(self):
        """
        Convertit l'objet Reservation en dictionnaire pour une utilisation dans la base de données.

        Retour :
            dict : Représentation de l'objet sous forme de dictionnaire.
        """
        return self.__dict__

    def __str__(self):
        """
        Retourne une chaîne de caractères représentant la réservation.

        Retour :
            str : Détails de la réservation incluant l'ID du client, l'ID du véhicule,
                  les dates de début et de fin, et le prix total.
        """
        return (f"Réservation ID {self.id_resa} - Client {self.id_user} - "
                f"Véhicule {self.id_vehicule} - Du {self.date_debut} au {self.date_fin} - ({self.jours} jour(s)) - "
                f"Prix total : {self.prix_total:.2f}€")

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


    def __init__(self, id_user, nom, prenom, email, telephone, role, mot_de_passe):
        self.id_user = id_user
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone
        self.role = role
        self.mot_de_passe = mot_de_passe

    def to_dict(self):
        """
        Convertit l'objet User en dictionnaire pour une utilisation dans la base de données.

        Retour :
            dict : Représentation de l'objet sous forme de dictionnaire.
        """
        return self.__dict__

    def __str__(self):
        """
        Retourne une chaîne de caractères représentant l'utilisateur'.

        Retour :
            str : Prénom, Nom et rôle de l'utilisateur.
        """
        return f"{self.prenom} {self.nom} - {self.role}"
