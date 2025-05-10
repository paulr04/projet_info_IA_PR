import unittest

from objects import Vehicule, Reservation, User, Reservation_DSL

class TestVehicule(unittest.TestCase):
    def test_vehicule_creation_valide(self):
        v = Vehicule(
            id_vehicule="AB-123-CD", marque="Peugeot", modele="208",
            prix_jour=45.0, masse=1200, vitesse_max=180, puissance=110,
            volume_utile=300, nb_places=5, type_moteur="Essence", hauteur=1.45,
            type_vehicule="Citadine", boite_vitesse="Manuelle", entretien_annuel=200,
            dispo=True, description="Voiture citadine économe"
        )
        self.assertEqual(v.id_vehicule, "AB-123-CD")
        self.assertEqual(v.nb_places, 5)

    #def test_vehicule_creation_invalide(self):
        #with self.assertRaises(ValueError):
            #Vehicule("A1-12A-CD", "Peugeot", "208", 45.0, 1200, 180, 110, 300, 5,
                     #"Essence", 1.45, "Citadine", "Manuelle", 200, True, "Voiture")


class TestUser(unittest.TestCase):
    def test_user_creation_valide(self):
        u = User("123456789", "Durand", "Paul", "paul@gmail.com", "0612345678", "C", "motdepasse")
        self.assertEqual(u.nom, "Durand")

    #def test_user_id_invalide(self):
        #with self.assertRaises(ValueError):
            #User("abc123", "Durand", "Paul", "paul@gmail.com", "0612345678", "C", "motdepasse")


class TestReservation(unittest.TestCase):
    def test_reservation_valide(self):
        r = Reservation("123456789", "987654321", "AB-123-CD", "05-01-2025", "05-03-2025", 2, 100.0, False)
        self.assertEqual(r.jours, 2)

    #def test_id_resa_invalide(self):
        #with self.assertRaises(ValueError):
            #Reservation("12345", "987654321", "AB-123-CD", "05-01-2025", "05-03-2025", 2, 100.0)

    #def test_date_invalide(self):
        #with self.assertRaises(ValueError):
            #Reservation("123456789", "987654321", "AB-123-CD", "2025-05-01", "05-03-2025", 2, 100.0)


class TestReservationDSL(unittest.TestCase):
    def test_parsing_valide(self):
        dsl = "RESERVATION 123456789 CLIENT 987654321 VEHICULE AB-123-CD DU 05-01-2025 AU 05-03-2025 JOURS 3 PRIX 120.0 SURCLASSEMENT True"
        resa_dsl = Reservation_DSL.from_dsl(dsl)
        self.assertIsInstance(resa_dsl, Reservation_DSL)
        self.assertEqual(resa_dsl.prix_total, 120.0)

    def test_parsing_invalide(self):
        bad_dsl = "RESERVATION 123 CLIENT 456 VEHICULE 123 DU 01-01-2025 AU 02-01-2025 JOURS 2 PRIX 50 SURCLASSEMENT False"
        with self.assertRaises(ValueError):
            Reservation_DSL.from_dsl(bad_dsl)


if __name__ == "__main__":
    unittest.main()
    