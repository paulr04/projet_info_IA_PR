import sys
import os

import re
import random
import string 

from PyQt5.QtWidgets import (
    QComboBox, QFormLayout, QHBoxLayout, QApplication, QTableWidgetItem, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QTextEdit, QTableWidget, QMessageBox, QDialog, QLineEdit, QInputDialog
)
from PyQt5.QtGui import QPixmap, QFont, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import csv
from facture import facture as fact
import fonctions as f
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
from objects import Client, Vendeur, Vehicule, Reservation_DSL

# Constantes pour le test
TYPES_MOTEUR = ["essence", "diesel", "électrique", "turbine"]
TYPES_VEHICULE = ["voiture", "camion", "char", "moto"]
BOITES_VITESSE = ["manuelle", "automatique"]

VEHICULES_FILE = "vehicules_test.csv"

# Classe Vehicule de test simplifiée
class Vehicule:
    def __init__(self, id_vehicule, marque, modele, prix_jour, masse, vitesse_max,
                 puissance, volume_utile, nb_places, type_moteur, hauteur,
                 type_vehicule, boite_vitesse, entretien_annuel, dispo, description):
        self.id_vehicule = id_vehicule
        self.marque = marque
        self.modele = modele
        self.prix_jour = prix_jour
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
        self.dispo = dispo
        self.description = description

    def to_dict(self):
        return {
            "id_vehicule": self.id_vehicule,
            "marque": self.marque,
            "modele": self.modele,
            "prix_jour": self.prix_jour,
            "masse": self.masse,
            "vitesse_max": self.vitesse_max,
            "puissance": self.puissance,
            "volume_utile": self.volume_utile,
            "nb_places": self.nb_places,
            "type_moteur": self.type_moteur,
            "hauteur": self.hauteur,
            "type_vehicule": self.type_vehicule,
            "boite_vitesse": self.boite_vitesse,
            "entretien_annuel": self.entretien_annuel,
            "dispo": self.dispo,
            "description": self.description
        }

# Fonction simulée pour générer/valider plaque
def demander_plaque_ajout(plaque, fichier):
    # Ici on retourne simplement la plaque entrée, sans vérification
    if len(plaque) == 0:
        raise ValueError("La plaque ne peut pas être vide")
    return plaque

class FenetreTest(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test ajout véhicule")
        self.ajouter_vehicule()

    def ajouter_vehicule(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un véhicule")

        layout = QVBoxLayout()

        plaque_input = QLineEdit()
        marque_input = QLineEdit()
        modele_input = QLineEdit()
        prix_input = QLineEdit()
        masse_input = QLineEdit()
        vitesse_input = QLineEdit()
        puissance_input = QLineEdit()
        volume_input = QLineEdit()
        places_input = QLineEdit()
        moteur_input = QComboBox()
        moteur_input.addItems(TYPES_MOTEUR)
        hauteur_input = QLineEdit()
        type_vehicule_input = QComboBox()
        type_vehicule_input.addItems(TYPES_VEHICULE)
        boite_input = QComboBox()
        boite_input.addItems(BOITES_VITESSE)
        entretien_input = QLineEdit()
        dispo_input = QComboBox()
        dispo_input.addItems(["True", "False"])
        description_input = QTextEdit()

        form = QFormLayout()
        form.addRow("Plaque (AA-000-AA) :", plaque_input)
        form.addRow("Marque :", marque_input)
        form.addRow("Modèle :", modele_input)
        form.addRow("Prix par jour (€) :", prix_input)
        form.addRow("Masse (kg) :", masse_input)
        form.addRow("Vitesse max (km/h) :", vitesse_input)
        form.addRow("Puissance (ch) :", puissance_input)
        form.addRow("Volume utile (m³) :", volume_input)
        form.addRow("Nombre de places :", places_input)
        form.addRow("Type de moteur :", moteur_input)
        form.addRow("Hauteur (m) :", hauteur_input)
        form.addRow("Type de véhicule :", type_vehicule_input)
        form.addRow("Boîte de vitesse :", boite_input)
        form.addRow("Entretien annuel (€) :", entretien_input)
        form.addRow("Disponible :", dispo_input)
        form.addRow("Description :", description_input)
        layout.addLayout(form)

        btn_valider = QPushButton("Ajouter le véhicule")
        layout.addWidget(btn_valider)

        confirmation = QLabel("")
        layout.addWidget(confirmation)

        btn_fermer = QPushButton("Fermer")
        btn_fermer.hide()
        layout.addWidget(btn_fermer)

        def on_valider():
            try:
                id_vehicule = self.demander_plaque_ajout(plaque_input.text().strip(), VEHICULES_FILE)
                marque = marque_input.text().strip()
                modele = modele_input.text().strip()
                prix_jour = float(prix_input.text())
                masse = float(masse_input.text())
                vitesse_max = float(vitesse_input.text())
                puissance = float(puissance_input.text())
                volume_utile = float(volume_input.text())
                nb_places = int(places_input.text())
                type_moteur = moteur_input.currentText()
                hauteur = float(hauteur_input.text())
                type_vehicule = type_vehicule_input.currentText()
                boite_vitesse = boite_input.currentText()
                entretien_annuel = float(entretien_input.text())
                dispo = dispo_input.currentText() == "True"
                description = description_input.toPlainText().strip()

                vehicule = Vehicule(
                    id_vehicule, marque, modele, prix_jour, masse, vitesse_max,
                    puissance, volume_utile, nb_places, type_moteur, hauteur,
                    type_vehicule, boite_vitesse, entretien_annuel, dispo, description
                )

                file_exists = os.path.exists(VEHICULES_FILE)
                with open(VEHICULES_FILE, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=vehicule.to_dict().keys())
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(vehicule.to_dict())

                confirmation.setText("Véhicule ajouté avec succès !")
                # Clear inputs optionally:
                plaque_input.clear()
                marque_input.clear()
                modele_input.clear()
                prix_input.clear()
                masse_input.clear()
                vitesse_input.clear()
                puissance_input.clear()
                volume_input.clear()
                places_input.clear()
                hauteur_input.clear()
                entretien_input.clear()
                description_input.clear()
                dispo_input.setCurrentIndex(0)
                moteur_input.setCurrentIndex(0)
                type_vehicule_input.setCurrentIndex(0)
                boite_input.setCurrentIndex(0)

                btn_fermer.show()

            except ValueError:
                confirmation.setText("Erreur : un champ numérique est invalide.")
            except Exception as e:
                confirmation.setText(f"Erreur : {e}")

        def on_fermer():
            dialog.accept()

        btn_valider.clicked.connect(on_valider)
        btn_fermer.clicked.connect(on_fermer)

        dialog.setLayout(layout)
        dialog.show()
        
    def generer_plaque_aleatoire(self):
        lettres = string.ascii_uppercase
        chiffres = string.digits
        # Format AA-123-AA
        return (
            random.choice(lettres) + random.choice(lettres) + "-" +
            ''.join(random.choices(chiffres, k=3)) + "-" +
            random.choice(lettres) + random.choice(lettres)
        )

    def demander_plaque_ajout(self, plaque, fichier):
        pattern = r"^[A-Z]{2}-\d{3}-[A-Z]{2}$"
        plaque = plaque.upper()
        if not re.match(pattern, plaque):
            raise ValueError("Format de plaque invalide. Exemple valide : AB-123-CD")

        plaques_existantes = set()
        if os.path.exists(fichier):
            with open(fichier, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    plaques_existantes.add(row.get("id_vehicule", "").upper())

        if plaque in plaques_existantes:
            # Génère une plaque unique aléatoire
            tentative = 0
            while True:
                nouvelle_plaque = self.generer_plaque_aleatoire()
                if nouvelle_plaque not in plaques_existantes:
                    plaque = nouvelle_plaque
                    break
                tentative += 1
                if tentative > 1000:
                    raise RuntimeError("Impossible de générer une plaque unique après 1000 tentatives.")

        return plaque

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fen = FenetreTest()
    fen.show()
    sys.exit(app.exec_())
