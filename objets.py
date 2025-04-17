
class Vehicule:
    """
    Auteur : Paul Renaud

    Représente un véhicule disponible à la location.

    Attributs :
        id (str)            : Identifiant unique du véhicule.
        marque (str)        : Marque du véhicule.
        modele (str)        : Modèle du véhicule.
        annee (int)         : Année de mise en circulation.
        kilometrage (int)   : Kilométrage du véhicule.
        prix_par_jour (float) : Tarif de location par jour en euros.
        disponible (bool)   : Indique si le véhicule est disponible à la location.

    Méthodes :
        to_dict()           : Renvoie une représentation dictionnaire du véhicule.
        save_to_file()      : Enregistre le véhicule dans le fichier CSV s'il n'existe pas déjà.
    """

    def __init__(
        self, id, marque, modele, prix_jour, masse, vitesse_max, puissance,
        volume_utile, nb_places, type_moteur, dimensions, type_vehicule,
        boite_vitesse, entretien_annuel, dispo, description
    ):
        self.id = id
        self.marque = marque
        self.modele = modele
        self.prix_jour = float(prix_jour)
        self.masse = masse
        self.vitesse_max = vitesse_max
        self.puissance = puissance
        self.volume_utile = volume_utile
        self.nb_places = nb_places
        self.type_moteur = type_moteur
        self.dimensions = dimensions
        self.type_vehicule = type_vehicule
        self.boite_vitesse = boite_vitesse
        self.entretien_annuel = entretien_annuel
        self.dispo = dispo
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
        return (f"{self.marque} {self.modele} ({self.type_vehicule}) - {self.id} - "
                f"{self.prix_jour:.2f}€/jour - {self.nb_places} places - {self.dispo}")

class Reservation:
    """
    Auteur : Paul Renaud

    Représente une réservation de véhicule effectuée par un client.

    Attributs :
        id (str)              : Identifiant unique de la réservation.
        id_client (str)       : Identifiant de l'utilisateur client.
        id_vehicule (str)     : Identifiant du véhicule réservé.
        date_debut (str)      : Date de début de la location (format YYYY-MM-DD).
        date_fin (str)        : Date de fin de la location (format YYYY-MM-DD).
        statut (str)          : Statut de la réservation (ex. : 'en attente', 'validée', 'annulée').

    Méthodes :
        to_dict()             : Renvoie une représentation dictionnaire de la réservation.
        save_to_file()        : Enregistre la réservation dans le fichier CSV.
    """

    def __init__(self, id_resa, client_id, vehicule_id, debut, fin, prix_total):
        self.id_resa = id_resa
        self.client_id = client_id
        self.vehicule_id = vehicule_id
        self.debut = debut
        self.fin = fin
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
        return (f"Réservation ID {self.id_resa} - Client {self.client_id} - "
                f"Véhicule {self.vehicule_id} - Du {self.debut} au {self.fin} - "
                f"Prix total : {self.prix_total:.2f}€")

class User:
    """
    Auteur : Paul Renaud

    Représente un utilisateur de l'application de gestion de location de véhicules.

    Un utilisateur peut être un client ('C') ou un vendeur ('V').

    Attributs :
        id (str)            : Identifiant unique de l'utilisateur.
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


    def __init__(self, id, nom, prenom, email, telephone, role, mot_de_passe):
        self.id = id
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
