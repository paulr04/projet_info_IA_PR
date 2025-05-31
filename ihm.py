import sys
import os
import csv
import re
import random
import string
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime

from PyQt5.QtWidgets import QDateEdit,QComboBox, QFormLayout, QHBoxLayout, QApplication, QTableWidgetItem, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QTextEdit, QTableWidget, QMessageBox, QDialog, QLineEdit, QInputDialog
from PyQt5.QtGui import QPixmap, QFont, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp, QDate

from facture import facture as fact
import fonctions as f
from objects import Client, Vendeur, Vehicule, Reservation_DSL, Admin

# Chemins des fichiers de données
USER_FILE = 'data/users.csv'
VEHICULES_FILE = 'data/vehicules.csv'
RESERVATIONS_FILE = 'data/reservations.csv'

CHAMPS_INTERDITS = ['id_user', 'id_resa', 'id_vehicule', 'role', 'mot_de_passe', 'type_moteur', 'type_vehicule', 'boite_vitesse']
NO_SURCLASSEMENT_TYPES = ["avion", "bateau", "militaire", "special"]
TYPES_VEHICULE = ["berline", "citadine", "avion", "bateau", "SUV", "special", "camion", "utilitaire", "militaire", "4x4", "supercar", "monospace", "pick-up"]
TYPES_MOTEUR = ["essence", "diesel", "electrique", "hybride", 'kerosene', 'hydrogene', 'fioul', 'nucleaire']
BOITES_VITESSE = ["manuelle", "automatique"]


class FenetreGraphiqueVentes(QDialog):
    """Fenêtre pour afficher les graphiques d'analyse des ventes."""
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
    """Fenêtre principale de l'application CarGo.
    
    Gère les menus, la connexion des utilisateurs et l'affichage des différentes fonctionnalités.

    Méthodes principales :
        - clear_layout: Vide le layout principal pour changer de "page".
        - creer_compte_client: Ouvre une boîte de dialogue pour créer un compte client.
        - verifier_identifiants: Vérifie les identifiants de l'utilisateur dans le fichier CSV.
        - retour_menu: Retourne au menu précédent selon le rôle de l'utilisateur connecté.
        - menu_initial: Affiche le menu initial de l'application.
        - se_connecter: Ouvre une boîte de dialogue pour la connexion.
        - verifier_connexion: Vérifie les identifiants et connecte l'utilisateur.
        - menu_vendeur: Affiche le menu pour les vendeurs.
        - menu_client: Affiche le menu pour les clients.
        - menu_analyse_ventes: Affiche les options d'analyse des ventes.
        - afficher_benefice_annee: Affiche le bénéfice pour une année donnée.
        - afficher_benefice_total: Affiche le bénéfice total.
        - afficher_reservations_par_vehicule_par_annee: Affiche les réservations par véhicule pour une année donnée.
        - afficher_resultat_texte: Affiche un texte dans une boîte de dialogue.
        - afficher_graphique_ventes: Affiche un graphique d'analyse des ventes.
        - consulter_catalogue: Affiche le catalogue des véhicules.
        - surclassement: Gère le surclassement d'un véhicule.
        - recherche_de_vehicule_pour_reservation: Ouvre une boîte de dialogue pour rechercher un véhicule à réserver.
        - demander_criteres_recherche: Ouvre une boîte de dialogue pour demander les critères de recherche.
        - reserver_vehicule: Gère la réservation d'un véhicule.
        - trouver_vehicule_disponible: Trouve les véhicules disponibles pour une période donnée.
        - annuler_reservation: Gère l'annulation d'une réservation.
        - supprimer_compte_client: Supprime le compte client de l'utilisateur connecté.
        - changer_de_mdp: Permet à l'utilisateur de changer son mot de passe.
        - changer_caracteristique_vehicule: Permet au vendeur de modifier les caractéristiques d'un véhicule.
        - changer_caracteristique_compte: Permet à l'utilisateur de modifier ses informations de compte.
        - consulter_reservations: Affiche les réservations de l'utilisateur connecté.
        - consulter_reservations_prochaines_vehicule: Affiche les réservations prochaines d'un véhicule.
        - consulter_vehicule: Affiche les détails d'un véhicule spécifique.
        - consulter_user: Affiche les informations des utilisateurs.
        - ajouter_vehicule: Permet au vendeur d'ajouter un nouveau véhicule.
        - supprimer_vehicule: Permet au vendeur de supprimer un véhicule.
    
    """
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
        """Supprime tous les widgets du layout principal pour changer de "page"."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def retour_menu(self):
        """Retourne au menu précédent selon le rôle de l'utilisateur connecté."""
        if self.utilisateur_connecte and self.utilisateur_connecte.role == "C":
            self.menu_client()
        elif self.utilisateur_connecte and self.utilisateur_connecte.role == "V":
            self.menu_vendeur()
        elif self.utilisateur_connecte and self.utilisateur_connecte.role == "A":
            self.menu_admin()
        else:
            self.menu_initial()
    
    def menu_initial(self):
        """Affiche le menu initial de l'application."""
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
        """Ouvre une boîte de dialogue pour la connexion de l'utilisateur."""
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
        """Vérifie les identifiants de l'utilisateur dans le fichier CSV."""
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
                        if role == "A":
                            return Admin(user_id, nom, prenom, email, telephone, role, mot_de_passe, app=self)  
            return None
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lecture fichier utilisateurs : {e}")
            return None

    def verifier_connexion(self, id_user, mdp, dialog):
        """Vérifie les identifiants et connecte l'utilisateur."""
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
            elif self.utilisateur_connecte.role == "A":
                self.menu_admin()
            else:
                QMessageBox.critical(self, "Erreur", "Rôle inconnu.")
        else:
            QMessageBox.critical(self, "Échec de connexion", "ID ou mot de passe incorrect.")

    def menu_admin(self):
        """Affiche le menu pour les admin."""
        self.clear_layout()
        self.layout = QVBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("logo_cargo.png").scaledToWidth(200, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo)

        title = QLabel(f"Bienvenue {self.utilisateur_connecte.prenom}, dans votre espace administrateur")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout.addWidget(title)

        # Liste des actions et méthodes associées
        actions = [
            ("Consulter le catalogue de véhicules", self.consulter_catalogue),
            ("Faire une recherche de véhicule et le réserver", self.recherche_de_vehicule_pour_reservation),
            ("Consulter les utilisateurs", self.consulter_user),
            ("Consulter les réservations", self.consulter_reservations),
            ("Ajouter un véhicule", self.ajouter_vehicule),
            ("Supprimer un véhicule", self.supprimer_vehicule),
            ("Faire une réservation", self.reserver_vehicule),
            ("Annuler une réservation", self.annuler_reservation),
            ("Créer un compte client", self.creer_compte_client),
            ("Créer un compte vendeur", self.creer_compte_vendeur),  
            ("Supprimer un compte", self.supprimer_compte_client),
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
    
    def menu_vendeur(self):
        """Affiche le menu pour les vendeurs."""
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
            ("Faire une recherche de véhicule et le réserver", self.recherche_de_vehicule_pour_reservation),
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
        """Affiche le menu pour les clients."""
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
        """Affiche les options d'analyse des ventes."""
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
        """Affiche le bénéfice pour une année donnée."""
        annee, ok = QInputDialog.getInt(self, "Bénéfice annuel", "Entrez l'année :",min=2000,max=2100)
        if ok:
            benefice = f.benefice_pour_annee(annee)
            self.afficher_resultat_texte(f"Bénéfice pour {annee} : {benefice} €")

    def afficher_benefice_total(self):
        """Affiche le bénéfice total."""
        benefice = f.afficher_benefice_total()
        self.afficher_resultat_texte(f"Bénéfice total : {round(benefice, 2)} €")

    def afficher_reservations_par_vehicule_par_annee(self):
        """Affiche les réservations par véhicule pour une année donnée."""
        annee, ok = QInputDialog.getInt(self, "Réservations par véhicule", "Entrez l'année :")
        if ok:
            self.afficher_graphique_ventes(lambda :f.reservations_par_vehicule_par_an(annee))

    def afficher_resultat_texte(self, texte):
        """Affiche un texte dans une boîte de dialogue."""
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
        """Affiche un graphique d'analyse des ventes."""
        fenetre = FenetreGraphiqueVentes(fonction_trace, self)
        fenetre.exec_()

    def consulter_catalogue(self):
        """Affiche le catalogue des véhicules."""
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
    
    def surclassement(self, Vehicule, vehicules_disponibles, date_debut, date_fin, id_user, jours, prix, type_vehicule, surclassement_choix):
        """Gère le surclassement d'un véhicule."""
        if Vehicule.type_vehicule in NO_SURCLASSEMENT_TYPES:
            QMessageBox.warning(self, "Fin", "Impossible de surclasser le type de véhicule sélectionné.")
            self.criteres_resa = None
            return
        if not self.criteres_resa:
            QMessageBox.information(self, "Info", "Le type de véhicule n'est pas pris en compte dans la recherche suivante.")
            self.criteres_resa = self.demander_criteres_recherche()

        if not surclassement_choix:
            QMessageBox.warning(self, "Fin", "Surclassement annulé.")
            self.criteres_resa = None
            return

        self.criteres_resa = [c for c in self.criteres_resa if c[0] != 'prix_jour' and c[0] != 'type_vehicule']
        self.criteres_resa.append(("type_vehicule", "=", type_vehicule))

        for v in vehicules_disponibles:
            if v.prix_jour >= Vehicule.prix_jour:
                v.prix_jour = Vehicule.prix_jour

        resultats = f.recherche(vehicules_disponibles, self.criteres_resa)

        if resultats:
            plaques = [f"{v.id_vehicule} - {v.marque} {v.modele}" for v in resultats]
            choix, ok = QInputDialog.getItem(self, "Surclassement", "Choisissez un véhicule :", plaques, 0, False)
            if ok:
                id_choisi = choix.split(" - ")[0]
                obj = f.info_vehicule(id_choisi)
                id_resa = f.generer_id_unique(RESERVATIONS_FILE, 'id_resa')
                surcl = obj.prix_jour >= Vehicule.prix_jour
                obj.prix_jour = Vehicule.prix_jour  # Assurer que le prix est celui du véhicule non disponible (le client est roi)
                prix = float(obj.prix_jour * jours)
                reduction = f.info_user(id_user).reduction_coef
                print(reduction)
                string = f"RESERVATION {id_resa} CLIENT {id_user} VEHICULE {obj.id_vehicule} DU {date_debut} AU {date_fin} JOURS {jours} PRIX {prix* reduction:.1f} SURCLASSEMENT {surcl}"
                resa = Reservation_DSL.from_dsl(string)
                Reservation_DSL.enregistrer(resa, RESERVATIONS_FILE)
                fact(resa, f.info_user(id_user), obj)
                QMessageBox.information(self, "Réservation réussie", f"Réservation {id_resa} enregistrée.")
                self.criteres_resa = None
            else:
                QMessageBox.information(self, "Annulé", "Surclassement annulé.")
                self.criteres_resa = None
        else:
            retry = QMessageBox.question(self, "Aucun résultat", "Voulez-vous un autre type de véhicule ?", QMessageBox.Yes | QMessageBox.No)
            if retry == QMessageBox.Yes:
                type_vehicule_failed, ok = QInputDialog.getItem(self, "Type", "Nouveau type de véhicule :", TYPES_VEHICULE, 0, False)
                if ok:
                    self.surclassement(Vehicule, vehicules_disponibles, date_debut, date_fin, id_user, jours, prix, type_vehicule_failed, True)
            else:
                QMessageBox.information(self, "Annulé", "Réservation annulée.")
                self.criteres_resa = None


    def recherche_de_vehicule_pour_reservation(self):
        """Ouvre une boîte de dialogue pour rechercher un véhicule à réserver."""
        # Chargement des véhicules
        vehicules_search = f.load_vehicules(VEHICULES_FILE)

        # Création de la boîte de dialogue
        dialog = QDialog(self)
        dialog.setWindowTitle("Recherche de véhicule")
        layout = QVBoxLayout()
        dialog.resize(800, 600)
        champs_recherche = [
            "marque", "modele", "prix_jour", "masse", "vitesse_max", "puissance",
            "volume_utile", "nb_places", "type_moteur", "hauteur", "boite_vitesse"
        ]

        OPERATEURS = ["=", "<", ">", "<=", ">="]

        form = QFormLayout()

        # Champ obligatoire : type_vehicule
        box_type_vehicule = QComboBox()
        box_type_vehicule.addItems(TYPES_VEHICULE)
        form.addRow("Type de véhicule (obligatoire)", box_type_vehicule)

        # Critères supplémentaires dynamiques
        criteres_widgets = []

        def add_critere():
            champ_cb = QComboBox()
            champ_cb.addItems(champs_recherche)
            op_cb = QComboBox()
            op_cb.addItems(OPERATEURS)
            val_le = QLineEdit()
            hl = QHBoxLayout()
            hl.addWidget(champ_cb)
            hl.addWidget(op_cb)
            hl.addWidget(val_le)
            layout.addLayout(hl)
            criteres_widgets.append((champ_cb, op_cb, val_le))

        btn_add_crit = QPushButton("Ajouter un critère")
        btn_add_crit.clicked.connect(add_critere)

        # Zone résultat
        zone_resultats = QTextEdit()
        zone_resultats.setReadOnly(True)

        # Bouton recherche
        btn_search = QPushButton("Lancer la recherche")

        # Réserver ?
        btn_reserver = QPushButton("Réserver un véhicule")
        btn_reserver.setEnabled(False)

        # Fermeture
        btn_close = QPushButton("Fermer")

        layout.addLayout(form)
        layout.addWidget(btn_add_crit)
        layout.addWidget(btn_search)
        layout.addWidget(zone_resultats)
        layout.addWidget(btn_reserver)
        layout.addWidget(btn_close)
        dialog.setLayout(layout)

        def lancer_recherche():
            """Lance la recherche de véhicules selon les critères spécifiés."""
            zone_resultats.clear()
            crit = []
            type_vehicule = box_type_vehicule.currentText().strip()
            crit.append(("type_vehicule", "=", type_vehicule))
            print("pas self", crit)
            for champ_cb, op_cb, val_le in criteres_widgets:
                champ = champ_cb.currentText()
                op = op_cb.currentText()
                val = val_le.text().strip().lower()

                if not val:
                    continue
                # Protection : éviter opérateurs invalides sur texte
                if op in [">", "<", ">=", "<="] and champ in ["marque", "modele", "type_moteur", "type_vehicule", "boite_vitesse"]:
                    QMessageBox.warning(dialog, "Erreur", f"Opérateur '{op}' invalide pour le champ texte '{champ}'.")
                    return
                crit.append((champ, op, val))

            resultats = f.recherche(vehicules_search, crit)
            self.criteres_resa = crit
            print("crit self", self.criteres_resa)
            if resultats:
                btn_reserver.setEnabled(True)
                texte = f"{len(resultats)} véhicule(s) trouvé(s) :\n\n"
                for v in resultats:
                    infos = [
                        f"ID : {v.id_vehicule}\n",
                        f"Prix/jour : {v.prix_jour} €\n",
                        f"Type : {v.type_vehicule}\n",
                        f"Marque : {v.marque}\n",
                        f"Modèle : {v.modele}\n",
                        f"{v.description}\n"   
                    ]
                    for champ, _, _ in crit:
                        if champ not in ['prix_jour', 'marque', 'modele', 'description', 'type_vehicule']:
                            infos.append(f"{champ}: {getattr(v, champ)}")
                    texte += "- ".join(infos) + "\n\n"
                zone_resultats.setText(texte)
            else:
                zone_resultats.setText("Aucun véhicule trouvé avec les critères spécifiés.")

        def reserver():
            """Gère la réservation d'un véhicule après une recherche."""
            reply = QMessageBox.question(dialog, "Réservation", "Souhaitez-vous réserver un véhicule ?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                dialog.close()
                self.reserver_vehicule()

        btn_search.clicked.connect(lancer_recherche)
        btn_reserver.clicked.connect(reserver)
        btn_close.clicked.connect(dialog.close)

        dialog.exec_()
    
    def demander_criteres_recherche(self):
        """"Ouvre une boîte de dialogue pour demander les critères de recherche."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Critères de recherche")
        dialog.resize(600, 400)
        layout = QVBoxLayout()

        champs_recherche = [
            "marque", "modele", "prix_jour", "masse", "vitesse_max", "puissance",
            "volume_utile", "nb_places", "type_moteur", "hauteur", "boite_vitesse"
        ]
        OPERATEURS = ["=", "<", ">", "<=", ">="]

        form = QFormLayout()
        box_type_vehicule = QComboBox()
        box_type_vehicule.addItems(TYPES_VEHICULE)
        form.addRow("Type de véhicule (obligatoire)", box_type_vehicule)

        criteres_widgets = []

        def add_critere():
            """Ajoute un critère de recherche dynamique."""
            champ_cb = QComboBox()
            champ_cb.addItems(champs_recherche)
            op_cb = QComboBox()
            op_cb.addItems(OPERATEURS)
            val_le = QLineEdit()
            hl = QHBoxLayout()
            hl.addWidget(champ_cb)
            hl.addWidget(op_cb)
            hl.addWidget(val_le)
            layout.addLayout(hl)
            criteres_widgets.append((champ_cb, op_cb, val_le))

        btn_add = QPushButton("Ajouter un critère")
        btn_add.clicked.connect(add_critere)

        btn_ok = QPushButton("Valider")
        btn_cancel = QPushButton("Annuler")

        btns = QHBoxLayout()
        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)

        layout.addLayout(form)
        layout.addWidget(btn_add)
        layout.addLayout(btns)

        dialog.setLayout(layout)

        result = []

        def valider():
            """Valide les critères de recherche et ferme la boîte de dialogue."""
            nonlocal result
            result = [("type_vehicule", "=", box_type_vehicule.currentText().strip())]
            for champ_cb, op_cb, val_le in criteres_widgets:
                champ = champ_cb.currentText()
                op = op_cb.currentText()
                val = val_le.text().strip().lower()
                if not val:
                    continue
                if op in [">", "<", ">=", "<="] and champ in ["marque", "modele", "type_moteur", "type_vehicule", "boite_vitesse"]:
                    QMessageBox.warning(dialog, "Erreur", f"Opérateur '{op}' invalide pour le champ '{champ}'.")
                    result = None
                    return
                result.append((champ, op, val))
            dialog.accept()

        btn_ok.clicked.connect(valider)
        btn_cancel.clicked.connect(dialog.reject)

        dialog.exec_()
        return result

    def reserver_vehicule(self):
        """ Ouvre une boîte de dialogue pour réserver un véhicule."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Formulaire de réservation")
        form_layout = QFormLayout()
        id_user = self.utilisateur_connecte.id_user
        user_combo = None
        if self.utilisateur_connecte.__class__.__name__ == "Vendeur" or self.utilisateur_connecte.__class__.__name__ == "Admin":
            users = f.load_users_POO(USER_FILE)
            user_combo = QComboBox()
            for user in users:
                user_combo.addItem(f"{user.nom} {user.prenom} ({user.id_user})", user.id_user)
            form_layout.addRow("Client :", user_combo)

        # Champs habituels
        plaque_input = QLineEdit()
        date_debut_input = QDateEdit()
        date_debut_input.setCalendarPopup(True)
        date_debut_input.setDate(QDate.currentDate())

        date_fin_input = QDateEdit()
        date_fin_input.setCalendarPopup(True)
        date_fin_input.setDate(QDate.currentDate().addDays(1))

        form_layout.addRow("Plaque du véhicule (AA-123-AA) :", plaque_input)
        form_layout.addRow("Date de début :", date_debut_input)
        form_layout.addRow("Date de fin :", date_fin_input)

        bouton_confirmer = QPushButton("Réserver")
        bouton_confirmer.clicked.connect(dialog.accept)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(bouton_confirmer)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            # Récupération de l'ID client selon le rôle
            if user_combo:
                id_user = user_combo.currentData()
            else:
                id_user = self.utilisateur_connecte.id_user

            id_vehicule = plaque_input.text().strip().upper()

            if not re.match(r"^[A-Z]{2}-\d{3}-[A-Z]{2}$", id_vehicule):
                QMessageBox.warning(self, "Erreur", "Format de plaque invalide. Format attendu : AA-123-AA.")
                return

            date_debut_qdate = date_debut_input.date()
            date_fin_qdate = date_fin_input.date()
            auj = QDate.currentDate()

            if date_debut_qdate < auj:
                QMessageBox.warning(self, "Erreur", "La date de début ne peut pas être dans le passé.")
                return
            if date_fin_qdate < date_debut_qdate:
                QMessageBox.warning(self, "Erreur", "La date de fin ne peut pas être antérieure à la date de début.")
                return

            date_debut = date_debut_qdate.toString("MM-dd-yyyy")
            date_fin = date_fin_qdate.toString("MM-dd-yyyy")

            # Recherche du véhicule
            vehicule = self.rechercher_vehicule_par_id(id_vehicule)
            if not vehicule:
                QMessageBox.warning(self, "Erreur", "Véhicule introuvable ou indisponible.")
                return

            try:
                f.verifier_dates(date_debut, date_fin)
                jours_res = f.calculer_jours_reservation(date_debut, date_fin)
            except Exception as e:
                QMessageBox.warning(self, "Erreur", str(e))
                return

            indispo = f.verifier_reservation(date_debut, date_fin, id_vehicule)

            if indispo:
                reply = QMessageBox.question(self, "Véhicule Indisponible", "Souhaitez-vous surclasser ?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    type_v = vehicule.type_vehicule
                    vehicules_dispos = self.trouver_vehicule_disponible(date_debut, date_fin)
                    self.criteres_resa = None
                    self.surclassement(
                        vehicule, vehicules_dispos, date_debut, date_fin,
                        id_user, jours_res, vehicule.prix_jour * jours_res,
                        type_v, True
                    )
            else:
                id_resa = f.generer_id_unique(RESERVATIONS_FILE, 'id_resa')
                reduction = f.info_user(id_user).reduction_coef
                print(reduction)
                string = f"RESERVATION {id_resa} CLIENT {id_user} VEHICULE {id_vehicule} DU {date_debut} AU {date_fin} JOURS {jours_res} PRIX {float(vehicule.prix_jour * jours_res) *  reduction:.2f} SURCLASSEMENT False"
                reservation = Reservation_DSL.from_dsl(string)
                Reservation_DSL.enregistrer(reservation, RESERVATIONS_FILE)
                fact(reservation, f.info_user(id_user), vehicule)
                QMessageBox.information(self, "Succès", f"Réservation confirmée pour {vehicule.marque} {vehicule.modele}.")


    def trouver_vehicule_disponible(self, date_debut, date_fin):
        """Trouve les véhicules disponibles pour les dates spécifiées."""
        vehicules_disponibles = []
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader: 
                if row['dispo'] == 'True' and not f.verifier_reservation(date_debut, date_fin, row['id_vehicule']):
                    vehicule = f.load_vehicule_POO(row)
                    vehicules_disponibles.append(vehicule)
        return vehicules_disponibles
        
    def annuler_reservation(self):
        """Ouvre une boîte de dialogue pour annuler une réservation."""
        user = self.utilisateur_connecte

        dialog = QDialog(self)
        dialog.setWindowTitle("Annuler une réservation")

        layout = QVBoxLayout()

        info_label = QLabel("Veuillez entrer votre mot de passe et l'ID de la réservation :")
        layout.addWidget(info_label)

        mdp_input = QLineEdit()
        mdp_input.setEchoMode(QLineEdit.Password)
        mdp_input.setPlaceholderText("Mot de passe")
        layout.addWidget(mdp_input)

        resa_input = QLineEdit()
        resa_input.setPlaceholderText("ID de réservation (9 chiffres)")
        layout.addWidget(resa_input)

        result_label = QLabel("")
        layout.addWidget(result_label)

        btn_annuler_resa = QPushButton("Annuler la réservation")
        btn_cancel = QPushButton("Fermer")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_annuler_resa)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        def on_annuler():
            """Gère l'annulation de la réservation."""
            mot_de_passe = mdp_input.text().strip()
            id_reservation = resa_input.text().strip()
            user_id = user.id_user

            if not id_reservation.isdigit() or len(id_reservation) != 9:
                result_label.setText("ID de réservation invalide (9 chiffres attendus).")
                return

            user_verifie = self.verifier_identifiants(user_id, mot_de_passe)
            if not user_verifie:
                result_label.setText("Mot de passe incorrect.")
                return

            date_debut_str = f.trouver_value(RESERVATIONS_FILE, id_reservation, 'id_resa', 'date_debut')
            if not date_debut_str:
                result_label.setText("Réservation introuvable.")
                return

            try:
                date_debut = f.convertir_date(date_debut_str).date()
            except:
                result_label.setText("Erreur de format de date.")
                return

            if date_debut < datetime.today().date():
                result_label.setText("Impossible d'annuler une réservation passée.")
                return

            if user.role == "C":
                id_user_resa = f.trouver_value(RESERVATIONS_FILE, id_reservation, 'id_resa', 'id_user')
                if id_user_resa != user_id:
                    result_label.setText("Vous ne pouvez annuler que vos propres réservations.")
                    return

            try:
                f.supprimer_ligne_par_id(RESERVATIONS_FILE, "id_resa", id_reservation)
                f.supprimer_facture(id_reservation)
                result_label.setText(f"Réservation {id_reservation} annulée avec succès.")
                dialog.accept()
            except Exception as e:
                result_label.setText(f"Erreur : {e}")

        btn_annuler_resa.clicked.connect(on_annuler)
        btn_cancel.clicked.connect(dialog.reject)

        dialog.setLayout(layout)
        dialog.exec_()


    def changer_de_mdp(self):
        """Ouvre une boîte de dialogue pour changer le mot de passe."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Changer de mot de passe")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Entrez votre mot de passe actuel :"))
        mdp_actuel_input = QLineEdit()
        mdp_actuel_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(mdp_actuel_input)

        layout.addWidget(QLabel("Nouveau mot de passe :"))
        nouv_mdp_input = QLineEdit()
        nouv_mdp_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(nouv_mdp_input)

        layout.addWidget(QLabel("Confirmation du mot de passe :"))
        conf_mdp_input = QLineEdit()
        conf_mdp_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(conf_mdp_input)

        result_label = QLabel("")
        layout.addWidget(result_label)

        btn_confirmer = QPushButton("Changer le mot de passe")
        btn_annuler = QPushButton("Annuler")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_confirmer)
        btn_layout.addWidget(btn_annuler)
        layout.addLayout(btn_layout)

        def filtrer_saisie(event, champ, numerique=False):
            """Filtre la saisie pour interdire certaines ponctuations et gérer les champs numériques."""
            ponctuation_interdite = [' ',',', ';', ':', '!', '?', "'", '"', '`', '´', '’', '“', '”']
            key = event.text()

            if event.key() in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Left, Qt.Key_Right, Qt.Key_Home, Qt.Key_End):
                QLineEdit.keyPressEvent(champ, event)
                return

            if key in ponctuation_interdite:
                return

            if numerique:
                if key and not (key.isdigit() or key == '.'):
                    return
                if key == '.' and '.' in champ.text():
                    return

            QLineEdit.keyPressEvent(champ, event)
        for champ in [mdp_actuel_input, nouv_mdp_input, conf_mdp_input]:
            champ.keyPressEvent = lambda event, c=champ: filtrer_saisie(event, c, numerique=False)

        def on_changer_mdp():
            """Gère le changement de mot de passe."""
            ancien_mdp = mdp_actuel_input.text().strip()
            nouv_mdp = nouv_mdp_input.text().strip()
            conf_mdp = conf_mdp_input.text().strip()

            user_id = self.utilisateur_connecte.id_user
            user = self.verifier_identifiants(user_id, ancien_mdp)

            if not user:
                result_label.setText("Mot de passe actuel incorrect.")
                return

            if nouv_mdp != conf_mdp:
                result_label.setText("Les nouveaux mots de passe ne correspondent pas.")
                return

            try:
                f.modifier_champ_csv_par_id(USER_FILE, user_id, "id_user", "mot_de_passe", nouv_mdp)
                result_label.setText("Mot de passe changé avec succès.")
                dialog.accept()
            except Exception as e:
                result_label.setText(f"Erreur : {e}")

        btn_confirmer.clicked.connect(on_changer_mdp)
        btn_annuler.clicked.connect(dialog.reject)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def changer_caracteristique_compte(self):
        """Ouvre une boîte de dialogue pour modifier les caractéristiques du compte utilisateur."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier une caractéristique du compte")

        layout = QVBoxLayout()

        label_info = QLabel("Veuillez entrer votre mot de passe pour confirmer :")
        layout.addWidget(label_info)

        mdp_input = QLineEdit()
        mdp_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(mdp_input)

        label_error = QLabel("")
        layout.addWidget(label_error)

        champs_modifiables = ['nom', 'prenom', 'email', 'telephone']  # Exemple
        inputs = {}

        for champ in champs_modifiables:
            lbl = QLabel(f"{champ.capitalize()} :")
            inp = QLineEdit()
            layout.addWidget(lbl)
            layout.addWidget(inp)
            inputs[champ] = inp

        btn_valider = QPushButton("Valider")
        btn_annuler = QPushButton("Annuler")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_valider)
        btn_layout.addWidget(btn_annuler)
        layout.addLayout(btn_layout)

        # Fonction interne pour filtrer la saisie (bloque ponctuation)
        def filtrer_saisie(event, champ, numerique=False):
            ponctuation_interdite = [' ', ',', ';', ':', '!', '?', "'", '"', '`', '´', '’', '“', '”']
            key = event.text()

            if event.key() in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Left, Qt.Key_Right, Qt.Key_Home, Qt.Key_End):
                QLineEdit.keyPressEvent(champ, event)
                return

            if key in ponctuation_interdite:
                return

            if numerique:
                if key and not (key.isdigit() or key == '.'):
                    return
                if key == '.' and '.' in champ.text():
                    return

            QLineEdit.keyPressEvent(champ, event)

        # On applique le filtre sur tous les champs sauf email (qui peut contenir @ etc)
        for champ_nom, champ_widget in inputs.items():
            if champ_nom == 'telephone':
                # Pour téléphone, on filtre uniquement chiffres et pas plus de 10 caractères
                def keypress_tel(event, c=champ_widget):
                    # On autorise uniquement chiffres, backspace, suppr, flèches
                    if event.key() in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Left, Qt.Key_Right, Qt.Key_Home, Qt.Key_End):
                        QLineEdit.keyPressEvent(c, event)
                        return
                    key_text = event.text()
                    if not key_text.isdigit():
                        return
                    if len(c.text()) >= 10:
                        return
                    QLineEdit.keyPressEvent(c, event)

                champ_widget.keyPressEvent = keypress_tel
            else:
                # Pour les autres champs, on bloque ponctuation
                champ_widget.keyPressEvent = lambda event, c=champ_widget: filtrer_saisie(event, c, numerique=False)

        def valider():
            """Valide les modifications et enregistre les changements."""
            mot_de_passe = mdp_input.text().strip()
            user_id = self.utilisateur_connecte.id_user
            user = self.verifier_identifiants(user_id, mot_de_passe)
            if not user:
                label_error.setText("Mot de passe incorrect.")
                return

            # Validation spécifique téléphone
            tel = inputs['telephone'].text().strip()
            if tel and (not tel.isdigit() or len(tel) != 10):
                label_error.setText("Le numéro de téléphone doit contenir exactement 10 chiffres.")
                return

            for champ, widget in inputs.items():
                nouvelle_valeur = widget.text().strip()
                if nouvelle_valeur:
                    f.modifier_champ_csv_par_id(USER_FILE, user_id, "id_user", champ, nouvelle_valeur)

            label_error.setText("Caractéristiques modifiées avec succès.")
            dialog.accept()

        btn_valider.clicked.connect(valider)
        btn_annuler.clicked.connect(dialog.reject)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def changer_caracteristique_vehicule(self):
        """Ouvre une boîte de dialogue pour modifier les caractéristiques d'un véhicule."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier une caractéristique d'un véhicule")
        layout = QVBoxLayout()

        def filtrer_saisie(event, champ, numerique=False):
            ponctuation_interdite = [',', ';', ':', '!', '?', "'", '"', '`', '´', '’', '“', '”']
            key = event.text()

            if event.key() in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Left, Qt.Key_Right, Qt.Key_Home, Qt.Key_End):
                QLineEdit.keyPressEvent(champ, event)
                return

            if key in ponctuation_interdite:
                return

            if numerique:
                if key and not (key.isdigit() or key == '.'):
                    return
                if key == '.' and '.' in champ.text():
                    return

            QLineEdit.keyPressEvent(champ, event)

        label_mdp = QLabel("Entrez votre mot de passe :")
        mdp_input = QLineEdit()
        mdp_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_mdp)
        layout.addWidget(mdp_input)

        label_plaque = QLabel("Plaque du véhicule (format AA-000-AA) :")
        plaque_input = QLineEdit()
        layout.addWidget(label_plaque)
        layout.addWidget(plaque_input)
        plaque_input.keyPressEvent = lambda event: filtrer_saisie(event, plaque_input)

        champs_modifiables = [
            "marque", "modele", "prix_jour", "masse", "vitesse_max", "puissance",
            "volume_utile", "nb_places", "type_moteur", "hauteur", "type_vehicule",
            "boite_vitesse", "entretien_annuel", "dispo", "description"
        ]
        label_champ = QLabel("Choisissez la caractéristique à modifier :")
        champ_combo = QComboBox()
        champ_combo.addItems(champs_modifiables)
        layout.addWidget(label_champ)
        layout.addWidget(champ_combo)

        label_nouvelle_valeur = QLabel("Nouvelle valeur :")
        nouvelle_valeur_input = QLineEdit()
        layout.addWidget(label_nouvelle_valeur)
        layout.addWidget(nouvelle_valeur_input)

        def maj_filtre_saisie():
            """filtre les valeurs numériques ou non selon le champ sélectionné."""
            champ = champ_combo.currentText()
            numerique = champ in ["prix_jour", "masse", "vitesse_max", "puissance", "volume_utile", "hauteur", "entretien_annuel"]
            nouvelle_valeur_input.keyPressEvent = lambda event: filtrer_saisie(event, nouvelle_valeur_input, numerique=numerique)
        champ_combo.currentTextChanged.connect(maj_filtre_saisie)
        maj_filtre_saisie()

        btn_valider = QPushButton("Valider la modification")
        btn_annuler = QPushButton("Annuler")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_valider)
        btn_layout.addWidget(btn_annuler)
        layout.addLayout(btn_layout)

        label_message = QLabel("")
        layout.addWidget(label_message)

        def valider():
            """Valide les entrées et modifie la caractéristique du véhicule."""
            user_id = self.utilisateur_connecte.id_user
            mdp = mdp_input.text().strip()
            if not self.verifier_identifiants(user_id, mdp):
                label_message.setText("Mot de passe incorrect.")
                return

            plaque = plaque_input.text().strip().upper()
            import re
            if not re.match(r"^[A-Z]{2}-\d{3}-[A-Z]{2}$", plaque):
                label_message.setText("Plaque invalide (format attendu AA-000-AA).")
                return

            champ = champ_combo.currentText()
            nouvelle_valeur = nouvelle_valeur_input.text().strip()

            if champ in ["marque", "modele", "description"]:
                nouvelle_valeur = nouvelle_valeur.lower().replace("'", "").replace(",", "").replace("’", "").replace("‘", "").replace("`", "")

            if champ in ["prix_jour", "masse", "vitesse_max", "puissance", "volume_utile", "nb_places", "hauteur", "entretien_annuel"]:
                try:
                    nouvelle_valeur = int(nouvelle_valeur) if champ == "nb_places" else float(nouvelle_valeur)
                except ValueError:
                    label_message.setText(f"Le champ {champ} doit être un nombre valide.")
                    return

            elif champ == "dispo":
                if nouvelle_valeur.lower() in ("true", "1", "oui"):
                    nouvelle_valeur = True
                elif nouvelle_valeur.lower() in ("false", "0", "non"):
                    nouvelle_valeur = False
                else:
                    label_message.setText("Le champ 'dispo' doit être True/False.")
                    return

            elif champ == "type_moteur":
                if nouvelle_valeur.lower() not in [m.lower() for m in TYPES_MOTEUR]:
                    label_message.setText(f"Type de moteur invalide.\nChoix possibles : {', '.join(TYPES_MOTEUR)}")
                    return
                nouvelle_valeur = nouvelle_valeur.lower()

            elif champ == "type_vehicule":
                if nouvelle_valeur.lower() not in [v.lower() for v in TYPES_VEHICULE]:
                    label_message.setText(f"Type de véhicule invalide.\nChoix possibles : {', '.join(TYPES_VEHICULE)}")
                    return
                nouvelle_valeur = nouvelle_valeur.lower()

            elif champ == "boite_vitesse":
                if nouvelle_valeur.lower() not in [b.lower() for b in BOITES_VITESSE]:
                    label_message.setText(f"Boîte de vitesse invalide.\nChoix possibles : {', '.join(BOITES_VITESSE)}")
                    return
                nouvelle_valeur = nouvelle_valeur.lower()

            try:
                f.modifier_champ_csv_par_id(VEHICULES_FILE, plaque, "id_vehicule", champ, nouvelle_valeur)
                label_message.setText("Modification réussie !")
            except Exception as e:
                label_message.setText(f"Erreur lors de la modification : {e}")

        btn_valider.clicked.connect(valider)
        btn_annuler.clicked.connect(dialog.reject)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def consulter_reservations_prochaines_vehicule(self):
        """Ouvre une boîte de dialogue pour consulter les réservations à venir d'un véhicule."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Réservations à venir pour un véhicule")

        layout = QVBoxLayout()

        # Label d'instruction
        label_instruction = QLabel("Plaque d'immatriculation (format AA-000-AA) :")
        layout.addWidget(label_instruction)

        # Champ de saisie pour la plaque
        champ_plaque = QLineEdit()
        layout.addWidget(champ_plaque)

        # Zone d'affichage des résultats
        zone_resultats = QTextEdit()
        zone_resultats.setReadOnly(True)
        layout.addWidget(zone_resultats)

        # Boutons
        bouton_valider = QPushButton("Rechercher")
        bouton_fermer = QPushButton("Fermer")
        layout.addWidget(bouton_valider)
        layout.addWidget(bouton_fermer)

        dialog.setLayout(layout)

        def rechercher():
            zone_resultats.clear()
            plaque = champ_plaque.text().strip().upper()

            # Validation format
            if not re.match(r"^[A-Z]{2}-\d{3}-[A-Z]{2}$", plaque):
                zone_resultats.setText("Plaque invalide. Format attendu : AA-000-AA")
                return

            trouve = False
            try:
                with open(RESERVATIONS_FILE, mode='r', newline='') as fichier:
                    lecteur = csv.DictReader(fichier)
                    for ligne in lecteur:
                        if ligne['id_vehicule'] == plaque and f.convertir_date(ligne['date_fin']).date() >= datetime.today().date():
                            info = (
                                f"Réservation : {ligne['id_resa']}\n"
                                f"Client : {ligne['id_user']}\n"
                                f"Début : {ligne['date_debut']}\n"
                                f"Fin : {ligne['date_fin']}\n"
                                f"Prix : {ligne['prix_total']} €\n"
                                "----------------------------\n"
                            )
                            zone_resultats.append(info)
                            trouve = True

                if not trouve:
                    zone_resultats.setText("Aucune réservation à venir pour ce véhicule ou véhicule introuvable.")
            except Exception as e:
                zone_resultats.setText(f"Erreur : {e}")

        bouton_valider.clicked.connect(rechercher)
        bouton_fermer.clicked.connect(dialog.close)

        dialog.exec_()
    
    def ajouter_vehicule(self):
        """Ouvre une boîte de dialogue pour ajouter un nouveau véhicule."""
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
        description_input = QLineEdit()

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

        def filtrer_saisie(event, champ, numerique=False):
            """Filtre la saisie pour interdire certaines ponctuations et gérer les champs numériques."""
            ponctuation_interdite = [',', ';', ':', '!', '?', "'", '"', '`', '´', '’', '“', '”']
            key = event.text()

            if event.key() in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Left, Qt.Key_Right, Qt.Key_Home, Qt.Key_End):
                QLineEdit.keyPressEvent(champ, event)
                return

            if key in ponctuation_interdite:
    
                return

            if numerique:
   
                if key and not (key.isdigit() or key == '.'):
                    return
                if key == '.' and '.' in champ.text():
                    return

            QLineEdit.keyPressEvent(champ, event)

        numeriques = [prix_input, masse_input, vitesse_input, puissance_input,
                    volume_input, places_input, hauteur_input, entretien_input]

        for champ in numeriques:
            champ.keyPressEvent = lambda event, c=champ: filtrer_saisie(event, c, numerique=True)

        # Bloquer ponctuation dans les autres QLineEdit
        autres = [plaque_input, marque_input, modele_input, description_input]
        for champ in autres:
            champ.keyPressEvent = lambda event, c=champ: filtrer_saisie(event, c, numerique=False)

        # Note: description_input est un QTextEdit, on ne bloque pas la ponctuation dedans (libre)

        def on_valider():
            """Valide les entrées et ajoute le véhicule."""
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
                description = description_input.text().strip()

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

                # Clear inputs
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
                confirmation.setText("Erreur : Plaque invalide ou champ invalide")
            except Exception as e:
                confirmation.setText(f"Erreur : {e}")

        def on_fermer():
            """Ferme la boîte de dialogue."""
            dialog.accept()

        btn_valider.clicked.connect(on_valider)
        btn_fermer.clicked.connect(on_fermer)

        dialog.setLayout(layout)
        dialog.show()
    
    def generer_plaque_aleatoire(self):
        """Génère une plaque d'immatriculation aléatoire au format AA-123-AA."""
        lettres = string.ascii_uppercase
        chiffres = string.digits
        # Format AA-123-AA
        return (
            random.choice(lettres) + random.choice(lettres) + "-" +
            ''.join(random.choices(chiffres, k=3)) + "-" +
            random.choice(lettres) + random.choice(lettres)
        )

    def demander_plaque_ajout(self, plaque, fichier):
        """Demande une plaque d'immatriculation et vérifie son unicité."""
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
        """Ouvre une boîte de dialogue pour supprimer un véhicule."""
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
            """Gère la suppression du véhicule."""
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
            """Annule la suppression et ferme la boîte de dialogue."""
            dialog.reject()

        btn_supprimer.clicked.connect(on_supprimer)
        btn_annuler.clicked.connect(on_annuler)

        dialog.setLayout(layout)
        dialog.exec_()

    def creer_compte_client(self):
        """Ouvre une boîte de dialogue pour créer un compte client."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Créer un compte client")

        layout = QVBoxLayout()

        nom_input = QLineEdit()
        prenom_input = QLineEdit()
        email_input = QLineEdit()
        tel_input = QLineEdit()
        mdp_input = QLineEdit()
        mdp_input.setEchoMode(QLineEdit.Password)

        def bloquer_virgules(event, input_field):
            """Bloque la saisie de virgules dans les champs d'entrée."""
            if event.text() == ',':
                return 
            QLineEdit.keyPressEvent(input_field, event)

        for champ in [nom_input, prenom_input, email_input, tel_input, mdp_input]:
            champ.keyPressEvent = lambda event, champ=champ: bloquer_virgules(event, champ)

        phone_regex = QRegExp(r"^\d{10}$")
        phone_validator = QRegExpValidator(phone_regex)
        tel_input.setValidator(phone_validator)

        form_layout = QFormLayout()
        form_layout.addRow("Nom :", nom_input)
        form_layout.addRow("Prénom :", prenom_input)
        form_layout.addRow("Email :", email_input)
        form_layout.addRow("Téléphone (ex: 0102030405) :", tel_input)
        form_layout.addRow("Mot de passe :", mdp_input)
        layout.addLayout(form_layout)

        btn_valider = QPushButton("Créer le compte")
        layout.addWidget(btn_valider)

        confirmation = QLabel("")
        layout.addWidget(confirmation)

        btn_fermer = QPushButton("Fermer")
        btn_fermer.hide()
        layout.addWidget(btn_fermer)
        
        def filtrer_saisie(event, champ, numerique=False):
            """Filtre la saisie pour interdire certaines ponctuations et gérer les champs numériques."""
            ponctuation_interdite = [' ',',', ';', ':', '!', '?', "'", '"', '`', '´', '’', '“', '”']
            key = event.text()

            if event.key() in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Left, Qt.Key_Right, Qt.Key_Home, Qt.Key_End):
                QLineEdit.keyPressEvent(champ, event)
                return

            if key in ponctuation_interdite:
    
                return

            if numerique:
   
                if key and not (key.isdigit() or key == '.'):
                    return
                if key == '.' and '.' in champ.text():
                    return

            QLineEdit.keyPressEvent(champ, event)
        autres = [nom_input, prenom_input, email_input, tel_input, mdp_input]
        for champ in autres:
            champ.keyPressEvent = lambda event, c=champ: filtrer_saisie(event, c, numerique=False)

        def on_valider():
            """Valide les entrées et crée le compte client."""
            nom = nom_input.text().strip()
            prenom = prenom_input.text().strip()
            email = email_input.text().strip()
            telephone = tel_input.text().strip()
            mot_de_passe = mdp_input.text()

            if not all([nom, prenom, email, telephone, mot_de_passe]):
                confirmation.setText("Veuillez remplir tous les champs.")
                return

            if not phone_regex.exactMatch(telephone):
                confirmation.setText("Téléphone invalide. Format attendu : 0102030405")
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
            """Ferme la boîte de dialogue."""
            dialog.accept()

        btn_valider.clicked.connect(on_valider)
        btn_fermer.clicked.connect(on_fermer)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def creer_compte_vendeur(self):
        """Ouvre une boîte de dialogue pour créer un compte vendeur."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Créer un compte vendeur")

        layout = QVBoxLayout()

        nom_input = QLineEdit()
        prenom_input = QLineEdit()
        email_input = QLineEdit()
        tel_input = QLineEdit()
        mdp_input = QLineEdit()
        mdp_input.setEchoMode(QLineEdit.Password)

        def bloquer_virgules(event, input_field):
            """Bloque la saisie de virgules dans les champs d'entrée."""
            if event.text() == ',':
                return 
            QLineEdit.keyPressEvent(input_field, event)

        for champ in [nom_input, prenom_input, email_input, tel_input, mdp_input]:
            champ.keyPressEvent = lambda event, champ=champ: bloquer_virgules(event, champ)

        phone_regex = QRegExp(r"^\d{10}$")
        phone_validator = QRegExpValidator(phone_regex)
        tel_input.setValidator(phone_validator)

        form_layout = QFormLayout()
        form_layout.addRow("Nom :", nom_input)
        form_layout.addRow("Prénom :", prenom_input)
        form_layout.addRow("Email :", email_input)
        form_layout.addRow("Téléphone (ex: 0102030405) :", tel_input)
        form_layout.addRow("Mot de passe :", mdp_input)
        layout.addLayout(form_layout)

        btn_valider = QPushButton("Créer le compte")
        layout.addWidget(btn_valider)

        confirmation = QLabel("")
        layout.addWidget(confirmation)

        btn_fermer = QPushButton("Fermer")
        btn_fermer.hide()
        layout.addWidget(btn_fermer)
        
        def filtrer_saisie(event, champ, numerique=False):
            """Filtre la saisie pour interdire certaines ponctuations et gérer les champs numériques."""
            ponctuation_interdite = [' ',',', ';', ':', '!', '?', "'", '"', '`', '´', '’', '“', '”']
            key = event.text()

            if event.key() in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Left, Qt.Key_Right, Qt.Key_Home, Qt.Key_End):
                QLineEdit.keyPressEvent(champ, event)
                return

            if key in ponctuation_interdite:
    
                return

            if numerique:
   
                if key and not (key.isdigit() or key == '.'):
                    return
                if key == '.' and '.' in champ.text():
                    return

            QLineEdit.keyPressEvent(champ, event)
        autres = [nom_input, prenom_input, email_input, tel_input, mdp_input]
        for champ in autres:
            champ.keyPressEvent = lambda event, c=champ: filtrer_saisie(event, c, numerique=False)

        def on_valider():
            """Valide les entrées et crée le compte vendeur."""
            nom = nom_input.text().strip()
            prenom = prenom_input.text().strip()
            email = email_input.text().strip()
            telephone = tel_input.text().strip()
            mot_de_passe = mdp_input.text()

            if not all([nom, prenom, email, telephone, mot_de_passe]):
                confirmation.setText("Veuillez remplir tous les champs.")
                return

            if not phone_regex.exactMatch(telephone):
                confirmation.setText("Téléphone invalide. Format attendu : 0102030405")
                return

            client_id = f.generer_id_unique(USER_FILE, 'id_user')
            role = 'V'
            user = Vendeur(client_id, nom, prenom, email, telephone, role, mot_de_passe, app=self)

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
            """Ferme la boîte de dialogue."""
            dialog.accept()

        btn_valider.clicked.connect(on_valider)
        btn_fermer.clicked.connect(on_fermer)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def supprimer_compte_client(self):
        """Ouvre une boîte de dialogue pour supprimer un compte client (ou vendeur)."""
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
            """Gère la suppression du compte client."""
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

                elif user.role == "V" or user.role == "A":
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
                        """Supprime le client avec l'ID entré."""
                        id_supp = id_input.text().strip()
                        if not id_supp:
                            id_confirmation.setText("Veuillez entrer un ID.")
                            return
                        
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
                        elif user_trouve.get('role') != 'C' and self.utilisateur_connecte.role != 'A':
                            id_confirmation.setText("Vous ne pouvez supprimer que des clients.")
                            return
                        elif user_trouve.get('role') == 'A':
                            id_confirmation.setText("Vous ne pouvez pas supprimer un administrateur.")
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
            """Annule la suppression et ferme la boîte de dialogue."""
            dialog.reject()

        btn_supprimer.clicked.connect(on_supprimer)
        btn_annuler.clicked.connect(on_annuler)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def trouver_vehicule_disponible(self, date_debut, date_fin):
        """Recherche les véhicules disponibles entre deux dates."""
        vehicules_disponibles = []
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['dispo'] == 'True' and not f.verifier_reservation(date_debut, date_fin, row['id_vehicule']):
                    vehicule = f.load_vehicule_POO(row)
                    vehicules_disponibles.append(vehicule)
        return vehicules_disponibles

    def consulter_vehicule(self):
        """Ouvre une boîte de dialogue pour consulter les informations d'un véhicule."""
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
            """Valide la plaque et affiche les informations du véhicule."""
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
        """Ouvre une boîte de dialogue pour consulter la liste des utilisateurs."""
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
        """Recherche un véhicule par son ID dans le fichier des véhicules."""
        # Recherche du véhicule par ID dans le fichier des véhicules
        with open(VEHICULES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id_vehicule'] == vehicule_id and row['dispo'] == 'True':
                    return f.load_vehicule_POO(row)
        return None

    def consulter_reservations(self):
        """
        Ouvre une boîte de dialogue pour consulter les réservations à venir.
        Affiche les réservations à venir dans une table.
        """
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
                        if self.utilisateur_connecte.role == "V" or self.utilisateur_connecte.role == 'A' or row["id_user"] == self.utilisateur_connecte.id_user:
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
