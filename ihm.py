import sys
from PyQt5.QtWidgets import (
    QApplication, QTableWidgetItem, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QTextEdit, QTableWidget, QMessageBox, QDialog, QLineEdit, QInputDialog
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

        btn_creer = QPushButton("Créer un compte (non implémenté)")
        btn_creer.clicked.connect(lambda: QMessageBox.information(self, "Info", "Fonction création compte non encore implémentée"))
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

        # Mise en place du layout dans un widget et affichage avec scroll
        content_widget = QWidget()
        content_widget.setLayout(self.layout)
        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

    def recherche_de_vehicule_pour_reservation(self):
        pass

    def reserver_vehicule(self):
        pass

    def supprimer_compte_client(self):
        pass

    def annuler_reservation(self):
        pass

    def changer_de_mdp(self):
        pass

    def changer_caracteristique_compte(self):
        pass
    
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
    def ajouter_vehicule(self): pass
    def supprimer_vehicule(self): pass
    def reserver_vehicule(self): pass
    def annuler_reservation(self): pass
    def creer_compte_client(self): pass
    def supprimer_compte_client(self): pass
    def changer_de_mdp(self): pass
    
    def changer_caracteristique_vehicule(self): pass
    def changer_caracteristique_compte(self): pass
    def consulter_reservations_prochaines_vehicule(self): pass
    def consulter_vehicule(self): pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fen = MainWindow()
    fen.show()
    sys.exit(app.exec_())
