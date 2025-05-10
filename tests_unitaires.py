import unittest

from objects import Vehicule, Reservation, User, Reservation_DSL

class TestUser(unittest.TestCase):
    def test_user_creation_valide(self):
        u = User("123456789", "Durand", "Paul", "paul@gmail.com", "0612345678", "C", "motdepasse")
        self.assertEqual(u.nom, "Durand")

    #def test_user_id_invalide(self):
        #with self.assertRaises(ValueError):
            #User("abc123", "Durand", "Paul", "paul@gmail.com", "0612345678", "C", "motdepasse")


class TestReservationDSL(unittest.TestCase):
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
            vehicule.set_valeur("type_moteur","gaz")   # Ce type de moteur n'est pas valide.

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
