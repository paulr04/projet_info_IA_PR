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

# from facture import facture as fact
USER_FILE = 'data/users.csv'
VEHICULES_FILE = 'data/vehicules.csv'
RESERVATIONS_FILE = 'data/reservations.csv'
CHAMPS_INTERDITS = ['id_user', 'id_resa', 'id_vehicule', 'role', 'mot_de_passe', 'type_moteur', 'type_vehicule', 'boite_vitesse']
NO_SURCLASSEMENT_TYPES = ["avion", "bateau", "militaire", "special"]
TYPES_VEHICULE = ["berline", "citadine", "avion", "bateau", "SUV", "special", "camion", "utilitaire", "militaire", "4x4", "supercar", "monospace", "pick-up"]
TYPES_MOTEUR = ["essence", "diesel", "electrique", "hybride", 'kerosene', 'hydrogene', 'fioul', 'nucleaire']
BOITES_VITESSE = ["manuelle", "automatique"]

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class FenetreGraphiqueVentes(QDialog):
    def __init__(self, fonction_trace, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analyse des ventes")
        self.resize(700, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        fonction_trace()

        fig = plt.gcf()
        plt.close(fig)

        self.canvas = FigureCanvas(fig)
        layout.addWidget(self.canvas)

        btn_fermer = QPushButton("Fermer")
        btn_fermer.clicked.connect(self.close)
        layout.addWidget(btn_fermer)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Location de Véhicules - CarGo")
        self.setGeometry(100, 100, 600, 700)
        self.utilisateur_connecte = None
        self.criteres_resa = None
        # Widget principal (container)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.menu_initial()

    def clear_layout(self):
        # Supprime tous les widgets du layout principal pour changer de "page"
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def retour_menu(self):
        if self.utilisateur_connecte and self.utilisateur_connecte.role == "C":
            self.menu_client()
        elif self.utilisateur_connecte and self.utilisateur_connecte.role == "V":
            self.menu_vendeur()
        else:
            self.menu_initial()
    
    def menu_initial(self):
        self.clear_layout()
        logo = QLabel()
        pixmap = QPixmap("logo_cargo.png").scaledToWidth(200, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo)

        title = QLabel("Bienvenue dans l'application CarGo !")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        self.layout.addWidget(title)

        btn_connexion = QPushButton("Se connecter")
        btn_connexion.clicked.connect(self.se_connecter)
        self.layout.addWidget(btn_connexion)

        btn_creer = QPushButton("Créer un compte Client")
        btn_creer.clicked.connect(self.creer_compte_client)
        self.layout.addWidget(btn_creer)

        btn_quitter = QPushButton("Quitter")
        btn_quitter.clicked.connect(self.close)
        self.layout.addWidget(btn_quitter)

    def se_connecter(self):
        self.clear_layout()
        dialog = QDialog(self)
        dialog.setWindowTitle("Connexion")
        dialog.setFixedSize(300, 200)

        self.layout = QVBoxLayout(dialog)

        label_id = QLabel("ID (9 chiffres) :")
        input_id = QLineEdit()
        input_id.setPlaceholderText("Ex : 123456789")
        input_id.setMaxLength(9)
        input_id.setValidator(QRegExpValidator(QRegExp(r"\d{9}")))

        label_mdp = QLabel("Mot de passe :")
        input_mdp = QLineEdit()
        input_mdp.setPlaceholderText("Votre mot de passe")
        input_mdp.setEchoMode(QLineEdit.Password)

        btn_connexion = QPushButton("Se connecter")
        btn_connexion.clicked.connect(lambda: self.verifier_connexion(input_id.text(), input_mdp.text(), dialog))

        self.layout.addWidget(label_id)
        self.layout.addWidget(input_id)
        self.layout.addWidget(label_mdp)
        self.layout.addWidget(input_mdp)
        self.layout.addWidget(btn_connexion)

        dialog.exec_()

    def verifier_identifiants(self, user_id, mot_de_passe):
        try:
            with open(USER_FILE, mode='r', newline='', encoding='utf-8') as file:
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
                        if role == "V":
                            return Vendeur(user_id, nom, prenom, email, telephone, role, mot_de_passe, app=self)  
                        if role == "C":
                            return Client(user_id, nom, prenom, email, telephone, role, mot_de_passe, app=self)  
            return None
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lecture fichier utilisateurs : {e}")
            return None

    def verifier_connexion(self, id_user, mdp, dialog):
        if not id_user or not mdp:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        user = self.verifier_identifiants(id_user, mdp)

        if user:
            self.utilisateur_connecte = user
            QMessageBox.information(self, "Connexion réussie", f"Bonjour, {user.prenom} !")
            dialog.accept()
            print(f"Utilisateur connecté : {self.utilisateur_connecte}")
            # Afficher menu adapté selon rôle
            if self.utilisateur_connecte.role == "C":
                self.menu_client()
            elif self.utilisateur_connecte.role == "V":
                self.menu_vendeur()
            else:
                QMessageBox.critical(self, "Erreur", "Rôle inconnu.")
        else:
            QMessageBox.critical(self, "Échec de connexion", "ID ou mot de passe incorrect.")

    def menu_vendeur(self):
        self.clear_layout()
        self.layout = QVBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("logo_cargo.png").scaledToWidth(200, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo)

        title = QLabel(f"Bienvenue {self.utilisateur_connecte.prenom}, dans votre espace vendeur")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout.addWidget(title)

        # Liste des actions et méthodes associées
        actions = [
            ("Consulter le catalogue de véhicules", self.consulter_catalogue),
            ("Consulter les utilisateurs", self.consulter_user),
            ("Consulter les réservations", self.consulter_reservations),
            ("Ajouter un véhicule", self.ajouter_vehicule),
            ("Supprimer un véhicule", self.supprimer_vehicule),
            ("Faire une réservation", self.reserver_vehicule),
            ("Annuler une réservation", self.annuler_reservation),
            ("Créer un compte client", self.creer_compte_client),
            ("Supprimer un compte client", self.supprimer_compte_client),
            ("Changer de mot de passe", self.changer_de_mdp),
            ("Analyse des ventes", self.menu_analyse_ventes),
            ("Modifier une caractéristique sur un véhicule", self.changer_caracteristique_vehicule),
            ("Modifier une caractéristique sur votre compte", self.changer_caracteristique_compte),
            ("Consulter les réservations prochaines d'un véhicule", self.consulter_reservations_prochaines_vehicule),
            ("Consulter un véhicule", self.consulter_vehicule),
            ("Quitter", self.menu_initial)
        ]

        for label, method in actions:
            btn = QPushButton(label)
            btn.clicked.connect(method)
            self.layout.addWidget(btn)

        content_widget = QWidget()
        content_widget.setLayout(self.layout)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)

        self.setCentralWidget(scroll)
    
    
    def menu_client(self):
        self.clear_layout()
        self.layout = QVBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("logo_cargo.png").scaledToWidth(200, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo)

        title = QLabel(f"Bienvenue {self.utilisateur_connecte.prenom}, dans votre espace client")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout.addWidget(title)

        actions = [
            ("Consulter le catalogue de véhicules", lambda: self.consulter_catalogue()),
            ("Faire une recherche de véhicule et le réserver", self.recherche_de_vehicule_pour_reservation),
            ("Consulter vos réservations", self.consulter_reservations),
            ("Faire une réservation", self.reserver_vehicule),
            ("Supprimer le compte", self.supprimer_compte_client),
            ("Annuler une réservation", self.annuler_reservation),
            ("Changer de mot de passe", self.changer_de_mdp),
            ("Modifier une caractéristique sur votre compte", self.changer_caracteristique_compte),
            ("Quitter", self.menu_initial)
        ]

        for label, method in actions:
            btn = QPushButton(label)
            btn.clicked.connect(method)
            self.layout.addWidget(btn)

        content_widget = QWidget()
        content_widget.setLayout(self.layout)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)

        self.setCentralWidget(scroll)

    def menu_analyse_ventes(self):
        self.clear_layout()
        self.layout = QVBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("logo_cargo.png").scaledToWidth(200, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo)

        title = QLabel(f"Analyse des ventes")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout.addWidget(title)


        actions = [
            ("Réservations par mois", lambda: self.afficher_graphique_ventes(f.plot_reservations_par_mois)),
            ("Réservations par an", lambda: self.afficher_graphique_ventes(f.plot_reservations_par_annee)),
            ("Bénéfice pour une année", self.afficher_benefice_annee),
            ("Bénéfice par année", lambda: self.afficher_graphique_ventes(f.benefice_par_annee_histogramme)),
            ("Bénéfice total", self.afficher_benefice_total),
            ("Réservations par véhicule par an", self.afficher_reservations_par_vehicule_par_annee),
            ("Réservations par véhicule", lambda: self.afficher_graphique_ventes(f.plot_reservations_par_vehicule)),
            ("Rentabilité par véhicule", lambda: self.afficher_graphique_ventes(lambda: f.plot_rentabilite_depuis_csv("data/reservations.csv", "data/vehicules.csv"))),
            ("Types de réservation par véhicule", lambda: self.afficher_graphique_ventes(lambda: f.plot_reservations_histogram("data/reservations.csv"))),
            ("Retour", self.retour_menu)
        ]

        for label, action in actions:
            btn = QPushButton(label)
            btn.clicked.connect(action)
            self.layout.addWidget(btn)

        widget = QWidget()
        widget.setLayout(self.layout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

    def afficher_benefice_annee(self):
        annee, ok = QInputDialog.getInt(self, "Bénéfice annuel", "Entrez l'année :",min=2000,max=2100)
        if ok:
            benefice = f.benefice_pour_annee(annee)
            self.afficher_resultat_texte(f"Bénéfice pour {annee} : {benefice} €")

    def afficher_benefice_total(self):
        benefice = f.afficher_benefice_total()
        self.afficher_resultat_texte(f"Bénéfice total : {round(benefice, 2)} €")

    def afficher_reservations_par_vehicule_par_annee(self):
        annee, ok = QInputDialog.getInt(self, "Réservations par véhicule", "Entrez l'année :")
        if ok:
            self.afficher_graphique_ventes(lambda :f.reservations_par_vehicule_par_an(annee))

    def afficher_resultat_texte(self, texte):
        dialog = QDialog(self)
        dialog.setWindowTitle("Résultat")

        layout = QVBoxLayout()
        label = QLabel(texte)
        label.setWordWrap(True)
        layout.addWidget(label)

        btn_ok = QPushButton("Fermer")
        btn_ok.clicked.connect(dialog.accept)
        layout.addWidget(btn_ok)

        dialog.setLayout(layout)
        dialog.exec_()

    def afficher_graphique_ventes(self, fonction_trace):
        fenetre = FenetreGraphiqueVentes(fonction_trace, self)
        fenetre.exec_()

    def consulter_catalogue(self):
        self.clear_layout()  
        self.layout = QVBoxLayout()
        title = QLabel("Catalogue des véhicules")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout.addWidget(title)
        table = QTableWidget()
        self.layout.addWidget(table)
        try:
            with open(VEHICULES_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                if not rows:
                    self.layout.addWidget(QLabel("Aucun véhicule disponible"))
                else:
                    headers = reader.fieldnames

                    # Colonnes à masquer
                    cols_to_hide = ['entretien_annuel', 'dispo']

                    # Filtrer les colonnes à afficher
                    headers_filtered = [h for h in headers if h not in cols_to_hide]

                    table.setColumnCount(len(headers_filtered))
                    table.setRowCount(len(rows))
                    table.setHorizontalHeaderLabels(headers_filtered)

                    for row_idx, row in enumerate(rows):
                        for col_idx, header in enumerate(headers_filtered):
                            val = row[header]
                            if header == 'description':
                                item = QTableWidgetItem(val)
                            else:
                                item = QTableWidgetItem(str(val))
                            table.setItem(row_idx, col_idx, item)
                    if 'description' in headers_filtered:
                        col_index = headers_filtered.index('description')
                        table.setColumnWidth(col_index, 450)
        except Exception as e:
            self.layout.addWidget(QLabel(f"Erreur lors du chargement : {e}"))

        btn_retour = QPushButton("Retour")
        btn_retour.clicked.connect(self.retour_menu)
        self.layout.addWidget(btn_retour)


        content_widget = QWidget()
        content_widget.setLayout(self.layout)
        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)
    
    def surclassement(self): pass
    def criteres(self): pass
    def recherche(self): pass
    def recherche_de_vehicule_pour_reservation(self):pass
    def reserver_vehicule(self):pass
    
    def annuler_reservation(self):pass
    def changer_de_mdp(self):pass
    def changer_caracteristique_compte(self):pass
    def changer_caracteristique_vehicule(self): pass
    def consulter_reservations_prochaines_vehicule(self): pass
    
    
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
    def supprimer_vehicule(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Supprimer un véhicule")

        layout = QVBoxLayout()

        info_label = QLabel("Veuillez entrer votre mot de passe pour confirmer la suppression du véhicule :")
        layout.addWidget(info_label)

        mdp_input = QLineEdit()
        mdp_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(mdp_input)

        id_label = QLabel("Entrez l'ID du véhicule à supprimer (format AA-123-AA) :")
        layout.addWidget(id_label)

        id_input = QLineEdit()
        id_input.setPlaceholderText("ID du véhicule")
        layout.addWidget(id_input)

        confirmation_label = QLabel("")
        layout.addWidget(confirmation_label)

        btn_supprimer = QPushButton("Confirmer la suppression")
        btn_annuler = QPushButton("Annuler")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_supprimer)
        btn_layout.addWidget(btn_annuler)
        layout.addLayout(btn_layout)

        def on_supprimer():
            mot_de_passe = mdp_input.text().strip()
            user_id = self.utilisateur_connecte.id_user  # Id de l'utilisateur connecté

            # Vérifier mot de passe
            user = self.verifier_identifiants(user_id, mot_de_passe)
            if not user:
                confirmation_label.setText("Mot de passe incorrect.")
                return

            id_vehicule = id_input.text().strip().upper()
            pattern = r"^[A-Z]{2}-\d{3}-[A-Z]{2}$"
            if not re.match(pattern, id_vehicule):
                confirmation_label.setText("Format d'ID invalide. Exemple : AB-123-CD")
                return

            # Vérifier si le véhicule existe
            vehicule_trouve = False
            with open(VEHICULES_FILE, newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get("id_vehicule", "").upper() == id_vehicule:
                        vehicule_trouve = True
                        break

            if not vehicule_trouve:
                confirmation_label.setText("ID véhicule introuvable.")
                return

            try:
                f.supprimer_ligne_par_id(VEHICULES_FILE, "id_vehicule", id_vehicule)
                confirmation_label.setText(f"Véhicule {id_vehicule} supprimé avec succès.")
                dialog.accept()
                self.retour_menu()  # ou autre méthode de rafraîchissement/retour

            except Exception as e:
                confirmation_label.setText(f"Erreur lors de la suppression : {e}")

        def on_annuler():
            dialog.reject()

        btn_supprimer.clicked.connect(on_supprimer)
        btn_annuler.clicked.connect(on_annuler)

        dialog.setLayout(layout)
        dialog.exec_()

    def creer_compte_client(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Créer un compte client")

        layout = QVBoxLayout()

        nom_input = QLineEdit()
        prenom_input = QLineEdit()
        email_input = QLineEdit()
        tel_input = QLineEdit()
        mdp_input = QLineEdit()
        mdp_input.setEchoMode(QLineEdit.Password)

        form_layout = QFormLayout()
        form_layout.addRow("Nom :", nom_input)
        form_layout.addRow("Prénom :", prenom_input)
        form_layout.addRow("Email :", email_input)
        form_layout.addRow("Téléphone :", tel_input)
        form_layout.addRow("Mot de passe :", mdp_input)
        layout.addLayout(form_layout)

        btn_valider = QPushButton("Créer le compte")
        layout.addWidget(btn_valider)

        confirmation = QLabel("")
        layout.addWidget(confirmation)

        btn_fermer = QPushButton("Fermer")
        btn_fermer.hide()
        layout.addWidget(btn_fermer)

        def on_valider():
            nom = nom_input.text().strip()
            prenom = prenom_input.text().strip()
            email = email_input.text().strip()
            telephone = tel_input.text().strip()
            mot_de_passe = mdp_input.text()

            if not all([nom, prenom, email, telephone, mot_de_passe]):
                confirmation.setText("Veuillez remplir tous les champs.")
                return

            client_id = f.generer_id_unique(USER_FILE, 'id_user')
            role = 'C'
            user = Client(client_id, nom, prenom, email, telephone, role, mot_de_passe, app=self)

            try:
                user_dict = {k: v for k, v in user.__dict__.items() if k != 'app'}

                file_exists = os.path.exists(USER_FILE)
                with open(USER_FILE, mode='a', newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=user_dict.keys())
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(user_dict)

                confirmation.setText(f"Compte créé ! ID : {client_id}")
                nom_input.clear()
                prenom_input.clear()
                email_input.clear()
                tel_input.clear()
                mdp_input.clear()
                btn_fermer.show()

            except Exception as e:
                confirmation.setText(f"Erreur : {e}")

        def on_fermer():
            dialog.accept()

        btn_valider.clicked.connect(on_valider)
        btn_fermer.clicked.connect(on_fermer)

        dialog.setLayout(layout)
        dialog.exec_()

    def supprimer_compte_client(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Supprimer un compte client")

        layout = QVBoxLayout()

        info_label = QLabel("Veuillez entrer votre mot de passe pour confirmer :")
        layout.addWidget(info_label)

        mdp_input = QLineEdit()
        mdp_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(mdp_input)

        confirmation_label = QLabel("")
        layout.addWidget(confirmation_label)

        btn_supprimer = QPushButton("Confirmer la suppression")
        btn_annuler = QPushButton("Annuler")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_supprimer)
        btn_layout.addWidget(btn_annuler)
        layout.addLayout(btn_layout)

        def on_supprimer():
            mot_de_passe = mdp_input.text().strip()
            user_id = self.utilisateur_connecte.id_user
            user = self.verifier_identifiants(user_id, mot_de_passe)

            if user:
                if user.role == "C":
                    id_supp = user_id
                    f.supprimer_ligne_par_id(USER_FILE, "id_user", id_supp)
                    confirmation_label.setText("Votre compte a été supprimé.")
                    dialog.accept()
                    self.menu_initial()

                elif user.role == "V":
                    # Boîte pour entrer un ID
                    id_dialog = QDialog(dialog)
                    id_dialog.setWindowTitle("ID du client à supprimer")

                    id_layout = QVBoxLayout()
                    id_input = QLineEdit()
                    id_input.setPlaceholderText("ID du client à supprimer")
                    id_confirmation = QLabel("")
                    btn_confirmer_id = QPushButton("Supprimer")
                    btn_annuler_id = QPushButton("Annuler")

                    btn_id_layout = QHBoxLayout()
                    btn_id_layout.addWidget(btn_confirmer_id)
                    btn_id_layout.addWidget(btn_annuler_id)

                    id_layout.addWidget(QLabel("Entrer l'ID du client à supprimer :"))
                    id_layout.addWidget(id_input)
                    id_layout.addWidget(id_confirmation)
                    id_layout.addLayout(btn_id_layout)

                    id_dialog.setLayout(id_layout)

                    def supprimer_client():
                        id_supp = id_input.text().strip()
                        if not id_supp:
                            id_confirmation.setText("Veuillez entrer un ID.")
                            return

                        # Vérification : l'utilisateur à supprimer existe et est bien un client
                        user_trouve = None
                        with open(USER_FILE, newline='', encoding="utf-8") as file:
                            reader = csv.DictReader(file)
                            for row in reader:
                                if row['id_user'] == id_supp:
                                    user_trouve = row
                                    break

                        if user_trouve is None:
                            id_confirmation.setText("ID introuvable.")
                            return
                        elif user_trouve.get('role') != 'C':
                            id_confirmation.setText("Vous ne pouvez supprimer que des clients.")
                            return

                        try:
                            f.supprimer_ligne_par_id(USER_FILE, "id_user", id_supp)
                            id_confirmation.setText(f"Client {id_supp} supprimé.")
                            id_dialog.accept()
                            dialog.accept()
                            self.retour_menu()
                        except Exception as e:
                            id_confirmation.setText(f"Erreur : {e}")

                    btn_confirmer_id.clicked.connect(supprimer_client)
                    btn_annuler_id.clicked.connect(id_dialog.reject)

                    id_dialog.exec_()

                else:
                    confirmation_label.setText("Rôle inconnu.")
            else:
                confirmation_label.setText("Mot de passe incorrect.")

        def on_annuler():
            dialog.reject()

        btn_supprimer.clicked.connect(on_supprimer)
        btn_annuler.clicked.connect(on_annuler)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def trouver_vehicule_disponible(self, date_debut, date_fin):
        # Recherche des véhicules disponibles dans le fichier des véhicules
        vehicules_disponibles = []
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['dispo'] == 'True' and not f.verifier_reservation(date_debut, date_fin, row['id_vehicule']):
                    # Vérification de la disponibilité du véhicule
                    vehicule = f.load_vehicule_POO(row)
                    vehicules_disponibles.append(vehicule)
        return vehicules_disponibles

    def consulter_vehicule(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Consulter un véhicule")

        layout = QVBoxLayout()

        label = QLabel("Entrer la plaque du véhicule (AA-000-AA) :")
        layout.addWidget(label)

        input_line = QLineEdit()
        regex = QRegExp("[A-Z]{2}-[0-9]{3}-[A-Z]{2}")
        validator = QRegExpValidator(regex)
        input_line.setValidator(validator)
        layout.addWidget(input_line)

        # Zone d'erreur
        error_label = QLabel("")
        error_label.setStyleSheet("color: red;")
        layout.addWidget(error_label)

        # Boutons
        btn_layout = QHBoxLayout()
        btn_valider = QPushButton("Valider")
        btn_annuler = QPushButton("Annuler")
        btn_layout.addWidget(btn_valider)
        btn_layout.addWidget(btn_annuler)
        layout.addLayout(btn_layout)

        dialog.setLayout(layout)

        def on_valider():
            id_vehicule = input_line.text()
            if not regex.exactMatch(id_vehicule):
                error_label.setText("Format invalide. Utilise AA-000-AA.")
                return

            vehicule = self.rechercher_vehicule_par_id(id_vehicule)
            if vehicule:
                vehicule_obj = f.info_vehicule(id_vehicule)
                vdict = vehicule_obj.to_dict()

                info_dialog = QDialog(self)
                info_dialog.setWindowTitle(f"Véhicule {id_vehicule}")
                info_layout = QVBoxLayout()

                for cle, val in vdict.items():
                    info_layout.addWidget(QLabel(f"{cle} : {val}"))

                btn_fermer = QPushButton("Fermer")
                btn_fermer.clicked.connect(info_dialog.accept)
                info_layout.addWidget(btn_fermer)

                info_dialog.setLayout(info_layout)
                info_dialog.exec_()
                dialog.accept()
            else:
                self.afficher_resultat_texte("Véhicule non trouvé.")
                dialog.accept()

        btn_valider.clicked.connect(on_valider)
        btn_annuler.clicked.connect(dialog.reject)

        dialog.exec_()

    def consulter_user(self): 
        self.clear_layout()
        self.layout = QVBoxLayout()

        title = QLabel("Liste des utilisateurs")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout.addWidget(title)

        table = QTableWidget()
        self.layout.addWidget(table)

        try:
            with open(USER_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

                if not rows:
                    self.layout.addWidget(QLabel("Aucun utilisateur trouvé"))
                else:
                    headers = reader.fieldnames

                    # Colonnes à ne pas afficher
                    cols_to_hide = ['mot_de_passe']
                    headers_filtered = [h for h in headers if h not in cols_to_hide]

                    table.setColumnCount(len(headers_filtered))
                    table.setRowCount(len(rows))
                    table.setHorizontalHeaderLabels(headers_filtered)

                    for row_idx, row in enumerate(rows):
                        for col_idx, header in enumerate(headers_filtered):
                            val = row[header]
                            item = QTableWidgetItem(str(val))
                            table.setItem(row_idx, col_idx, item)

        except Exception as e:
            self.layout.addWidget(QLabel(f"Erreur lors du chargement des utilisateurs : {e}"))

        btn_retour = QPushButton("Retour")
        btn_retour.clicked.connect(self.retour_menu)  # Ou menu_vendeur si c'est réservé aux vendeurs
        self.layout.addWidget(btn_retour)

        content_widget = QWidget()
        content_widget.setLayout(self.layout)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)

        self.setCentralWidget(scroll)

    def rechercher_vehicule_par_id(self, vehicule_id):
        # Recherche du véhicule par ID dans le fichier des véhicules
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id_vehicule'] == vehicule_id and row['dispo'] == 'True':
                    return f.load_vehicule_POO(row)
        return None

    def consulter_reservations(self):

        self.clear_layout()
        self.layout = QVBoxLayout()

        title = QLabel("Réservations à venir")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout.addWidget(title)

        table = QTableWidget()
        self.layout.addWidget(table)

        try:
            with open(RESERVATIONS_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = []

                for row in reader:
                    date_fin = f.convertir_date(row['date_fin']).date()
                    if date_fin >= datetime.today().date():
                        if self.utilisateur_connecte.role == "V" or row["id_user"] == self.utilisateur_connecte.id_user:
                            rows.append(row)

                if not rows:
                    self.layout.addWidget(QLabel("Aucune réservation à venir trouvée"))
                else:
                    headers = ['id_resa', 'id_user', 'id_vehicule', 'date_debut', 'date_fin', 'prix_total']
                    table.setColumnCount(len(headers))
                    table.setRowCount(len(rows))
                    table.setHorizontalHeaderLabels(headers)

                    for row_idx, row in enumerate(rows):
                        for col_idx, header in enumerate(headers):
                            val = row[header]
                            item = QTableWidgetItem(str(val))
                            table.setItem(row_idx, col_idx, item)

        except Exception as e:
            self.layout.addWidget(QLabel(f"Erreur lors du chargement des réservations : {e}"))

        btn_retour = QPushButton("Retour")
        btn_retour.clicked.connect(self.retour_menu)
        self.layout.addWidget(btn_retour)

        content_widget = QWidget()
        content_widget.setLayout(self.layout)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)

        self.setCentralWidget(scroll)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fen = MainWindow()
    fen.show()
    sys.exit(app.exec_())
