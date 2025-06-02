import unittest
import fonctions as f
from objects import Vehicule, User, Reservation_DSL, Vendeur, Client, Admin

USER_FILE = 'data/users.csv'
VEHICULES_FILE = 'data/vehicules.csv'
RESERVATIONS_FILE = 'data/reservations.csv'
CHAMPS_INTERDITS = ['id_user', 'id_resa', 'id_vehicule', 'role', 'mot_de_passe', 'type_moteur', 'type_vehicule', 'boite_vitesse']
CHAMPS_INTERDITS = ['id_user', 'id_resa', 'id_vehicule', 'role', 'mot_de_passe', 'type_moteur', 'type_vehicule', 'boite_vitesse']
NO_SURCLASSEMENT_TYPES = ["avion", "bateau", "militaire", "special",'autre', 'chantier', 'helicoptere', 'formule 1', 'rally']
TYPES_VEHICULE = ["berline", "citadine", "avion", "bateau", "SUV", "special", "camion", "utilitaire", "militaire", "4x4", "supercar", "monospace", "pick-up", "velo", "moto", "quad", "trottinette", "camionette", "bus", "minibus", "cabriolet", "roadster", "coupe", "break", "limousine", "formule 1", "rally", "helicoptere", "chantier",'autre']
TYPES_MOTEUR = ["essence", "diesel", "electrique", "hybride", 'kerosene', 'hydrogene', 'fioul', 'nucleaire', 'gaz', 'propergol', 'autre']
BOITES_VITESSE = ["manuelle", "automatique"]

class TestUser(unittest.TestCase):
    """
    
    Classe de test pour la classe User et ses sous-classes (héritage) Vendeur et Client.
    
    """
    def test_user_creation_valide(self):
        """Tester la création d'un utilisateur avec des valeurs valides."""
        u = User("123456789", "Durand", "Paul", "paul@gmail.com", "0612345678", "C", "motdepasse", app=None)
        self.assertEqual(u.nom, "Durand")
    
    def test_role_vendeur(self):
        """Teste l'erreur si un utilisateur avec le rôle 'V' est créé en tant que Client."""
        with self.assertRaises(ValueError):
            Vendeur("123456789", "Durand", "Paul", "paul@gmail.com", "0612345678", "C", "motdepasse", app=None)
    
    def test_role_client(self):
        """Teste l'erreur si un utilisateur avec le rôle 'C' est créé en tant que Vendeur."""
        with self.assertRaises(ValueError):
            Client("123456789", "Durand", "Paul", "paul@gmail.com", "0612345678", "V", "motdepasse", app=None)
    
    def test_reduction_role(self):
        """Tester la réduction du rôle d'un utilisateur."""
        client = Client("123456789", "Durand", "Paul", "paul@gmail.com", "0612345678", "C", "motdepasse", app=None)
        vendeur = Vendeur("123456789", "Durand", "Paul", "paul@gmail.com", "0612345678", "V", "motdepasse", app=None)
        admin = Admin("123456789", "Durand", "Paul", "paul@gmail.com", "0612345678", "A", "motdepasse", app=None)
        self.assertEqual(client.role, "C")
        self.assertEqual(vendeur.role, "V")
        self.assertEqual(admin.role, "A")
        self.assertIsInstance(client, Client)
        self.assertIsInstance(vendeur, Vendeur)
        self.assertIsInstance(admin, Admin)
        self.assertEqual(client.reduction_coef, 1)
        self.assertEqual(vendeur.reduction_coef, 0.8)
        self.assertEqual(admin.reduction_coef, 0)

class Testfonctions(unittest.TestCase):
    """

    Classe de test pour les fonctions de chargement des données.
    
    """
    def test_load_vehicule_POO(self):
        """Tester le chargement des véhicules depuis un fichier CSV."""
        vehicules = f.load_vehicules(VEHICULES_FILE)
        self.assertIsInstance(vehicules, list)
        for vehicule in vehicules:
            self.assertIsInstance(vehicule, Vehicule)
    
    def test_load_users_POO(self):
        """Tester le chargement des utilisateurs depuis un fichier CSV."""
        users = f.load_users_POO(USER_FILE)
        self.assertIsInstance(users, list)
        for user in users:
            self.assertIsInstance(user, User)
        for user in users:
            if user.role == 'V':
                self.assertIsInstance(user, Vendeur)
            elif user.role == 'C':
                self.assertIsInstance(user, Client)
            elif user.role == 'A':
                self.assertIsInstance(user, Admin)
            else:
                self.fail(f"Rôle inconnu pour l'utilisateur {user.id_user}: {user.role}")

class TestReservationDSL(unittest.TestCase):
    """

    Classe de test pour la classe Reservation_DSL.

    """
    def test_parsing_valide(self):
        dsl = "RESERVATION 578878064 CLIENT 000000230 VEHICULE FR-416-FR DU 08-08-2025 AU 08-09-2025 JOURS 2 PRIX 120.0 SURCLASSEMENT False"
        resa_dsl = Reservation_DSL.from_dsl(dsl)
        self.assertIsInstance(resa_dsl, Reservation_DSL)
        self.assertEqual(resa_dsl.id_resa, "578878064")
        self.assertEqual(resa_dsl.id_user, "000000230")
        self.assertEqual(resa_dsl.id_vehicule, "FR-416-FR")
        self.assertEqual(resa_dsl.date_debut, "08-08-2025")
        self.assertEqual(resa_dsl.date_fin, "08-09-2025")
        self.assertEqual(resa_dsl.jours, 2)
        self.assertEqual(resa_dsl.surclassement, False)
        self.assertEqual(resa_dsl.prix_total, 120.0)

    def test_parsing_invalide(self):
        bad_dsl = "RESERVATION 123 CLIENT 456 VEHICULE 123 DU 01-01-2025 AU 02-01-2025 JOURS 2 PRIX 50 SURCLASSEMENT False"
        with self.assertRaises(ValueError):
            Reservation_DSL.from_dsl(bad_dsl)


class TestVehicule(unittest.TestCase):
    """Classe de test pour la classe Vehicule."""
    def test_creation_valide(self):
        """Tester la création d'un objet Vehicule avec des valeurs valides."""
        vehicule = Vehicule(
            id_vehicule="AA-123-AA", marque="toyota", modele="corolla", prix_jour=50.0,
            masse=1500.0, vitesse_max=180.0, puissance=120.0, volume_utile=0.5,
            nb_places=5, type_moteur="essence", hauteur=1.5, type_vehicule="berline",
            boite_vitesse="manuelle", entretien_annuel=200.0, dispo=True, description="voiture familiale"
        )
        self.assertEqual(vehicule.marque, "toyota")
        self.assertEqual(vehicule.modele, "corolla")
        self.assertEqual(vehicule.prix_jour, 50.0)
        self.assertEqual(vehicule.type_moteur, "essence")
        self.assertEqual(vehicule.type_vehicule, "berline")
        self.assertEqual(vehicule.description, "voiture familiale")
        self.assertIsInstance(vehicule, Vehicule)
        
    def test_creation_invalide_id_vehicule(self):
        """Tester la création avec un ID véhicule invalide."""
        with self.assertRaises(ValueError):
            Vehicule(
                id_vehicule="123-456", marque="toyota", modele="corolla", prix_jour=50.0,
                masse=1500.0, vitesse_max=180.0, puissance=120.0, volume_utile=0.5,
                nb_places=5, type_moteur="essence", hauteur=1.5, type_vehicule="berline",
                boite_vitesse="manuelle", entretien_annuel=200.0, dispo=True, description="voiture familiale"
            )

    def test_creation_invalide_prix_jour(self):
        """Tester la création avec un prix par jour invalide (négatif)."""
        with self.assertRaises(ValueError):
            Vehicule(
                id_vehicule="AA-123-AA", marque="toyota", modele="corolla", prix_jour=-50.0,
                masse=1500.0, vitesse_max=180.0, puissance=120.0, volume_utile=0.5,
                nb_places=5, type_moteur="essence", hauteur=1.5, type_vehicule="berline",
                boite_vitesse="manuelle", entretien_annuel=200.0, dispo=True, description="voiture familiale"
            )

    def test_creation_invalide_type_moteur(self):
        """Tester la création avec un type de moteur invalide."""
        with self.assertRaises(ValueError):
            Vehicule(
                id_vehicule="AA-123-AA", marque="toyota", modele="corolla", prix_jour=50.0,
                masse=1500.0, vitesse_max=180.0, puissance=120.0, volume_utile=0.5,
                nb_places=5, type_moteur="poudre_de_perlimpinpin", hauteur=1.5, type_vehicule="berline",
                boite_vitesse="manuelle", entretien_annuel=200.0, dispo=True, description="voiture familiale"
            )

    def test_creation_invalide_type_vehicule(self):
        """Tester la création avec un type de véhicule invalide."""
        with self.assertRaises(ValueError):
            Vehicule(
                id_vehicule="AA-123-AA", marque="toyota", modele="corolla", prix_jour=50.0,
                masse=1500.0, vitesse_max=180.0, puissance=120.0, volume_utile=0.5,
                nb_places=5, type_moteur="essence", hauteur=1.5, type_vehicule="avion de chasse",
                boite_vitesse="manuelle", entretien_annuel=200.0, dispo=True, description="voiture familiale"
            )

    def test_set_marque_valide(self):
        """Tester le setter de la marque avec une valeur valide."""
        vehicule = Vehicule(
            id_vehicule="AA-123-AA", marque="toyota", modele="corolla", prix_jour=50.0,
            masse=1500.0, vitesse_max=180.0, puissance=120.0, volume_utile=0.5,
            nb_places=5, type_moteur="essence", hauteur=1.5, type_vehicule="berline",
            boite_vitesse="manuelle", entretien_annuel=200.0, dispo=True, description="voiture familiale"
        )
        vehicule.marque = "honda"
        self.assertEqual(vehicule.marque, "honda")

    def test_set_marque_invalide(self):
        """Tester le setter de la marque avec une valeur invalide."""
        vehicule = Vehicule(
            id_vehicule="AA-123-AA", marque="toyota", modele="corolla", prix_jour=50.0,
            masse=1500.0, vitesse_max=180.0, puissance=120.0, volume_utile=0.5,
            nb_places=5, type_moteur="essence", hauteur=1.5, type_vehicule="berline",
            boite_vitesse="manuelle", entretien_annuel=200.0, dispo=True, description="voiture familiale"
        )
        with self.assertRaises(ValueError):
            vehicule.marque = 1234  # Doit être une chaîne de caractères.

    def test_set_type_moteur_invalide(self):
        """Tester le setter du type de moteur avec une valeur invalide."""
        vehicule = Vehicule(
            id_vehicule="AA-123-AA", marque="toyota", modele="corolla", prix_jour=50.0,
            masse=1500.0, vitesse_max=180.0, puissance=120.0, volume_utile=0.5,
            nb_places=5, type_moteur="essence", hauteur=1.5, type_vehicule="berline",
            boite_vitesse="manuelle", entretien_annuel=200.0, dispo=True, description="voiture familiale"
        )
        with self.assertRaises(ValueError):
            vehicule.set_valeur("type_moteur","eau")   # Ce type de moteur n'est pas valide.

    def test_set_type_vehicule_invalide(self):
        """Tester le setter du type de véhicule avec une valeur invalide."""
        vehicule = Vehicule(
            id_vehicule="AA-123-AA", marque="toyota", modele="corolla", prix_jour=50.0,
            masse=1500.0, vitesse_max=180.0, puissance=120.0, volume_utile=0.5,
            nb_places=5, type_moteur="essence", hauteur=1.5, type_vehicule="berline",
            boite_vitesse="manuelle", entretien_annuel=200.0, dispo=True, description="voiture familiale"
        )
        with self.assertRaises(ValueError):
            vehicule.type_vehicule = "vélo"  # Ce type de véhicule n'est pas valide.

    def test_set_valeur_attribut_inexistant(self):
        """Tester la méthode set_valeur avec un attribut inexistant."""
        vehicule = Vehicule(
            id_vehicule="AA-123-AA", marque="toyota", modele="corolla", prix_jour=50.0,
            masse=1500.0, vitesse_max=180.0, puissance=120.0, volume_utile=0.5,
            nb_places=5, type_moteur="essence", hauteur=1.5, type_vehicule="berline",
            boite_vitesse="manuelle", entretien_annuel=200.0, dispo=True, description="voiture familiale"
        )
        with self.assertRaises(AttributeError):
            vehicule.set_valeur("non_existant", "test")  # Attribut inexistant. 

if __name__ == "__main__":
    unittest.main()
