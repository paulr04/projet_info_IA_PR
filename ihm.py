import sys
from PyQt5.QtWidgets import (
    QInputDialog, QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QScrollArea, QDialog
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import fonctions as f
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class MenuClientIHM(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Client - Location de Véhicules")
        self.setGeometry(100, 100, 500, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("logo_cargo.png").scaledToWidth(200, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        title = QLabel("Bienvenue dans votre espace client")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)

        actions = [
            "Consulter le catalogue de véhicules",
            "Rechercher un véhicule et réserver",
            "Consulter mes réservations",
            "Réserver un véhicule",
            "Supprimer mon compte",
            "Annuler une réservation",
            "Changer mon mot de passe",
            "Modifier mes informations",
            "Quitter"
        ]

        for action in actions:
            btn = QPushButton(action)
            if action.startswith("Quitter"):
                btn.clicked.connect(self.close)
            else:
                btn.clicked.connect(lambda checked, a=action: self.show_message(a))
            layout.addWidget(btn)

        scroll = QScrollArea()
        content_widget = QWidget()
        content_widget.setLayout(layout)
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(scroll)
        self.setLayout(outer_layout)

    def show_message(self, action_name):
        QMessageBox.information(self, "Action", f"Action déclenchée : {action_name}")

class FenetreGraphiqueVentes(QDialog):
    def __init__(self, fonction_trace, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analyse des ventes")
        self.resize(700, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Appel de ta fonction matplotlib classique qui affiche un plot
        fonction_trace()

        # Récupération de la figure matplotlib active (celle créée par ta fonction)
        fig = plt.gcf()

        # Ferme la fenêtre matplotlib classique
        plt.close(fig)

        # Intègre cette figure dans le canvas Qt
        self.canvas = FigureCanvas(fig)
        layout.addWidget(self.canvas)

        btn_fermer = QPushButton("Fermer")
        btn_fermer.clicked.connect(self.close)
        layout.addWidget(btn_fermer)


class MenuAnalyseVentesDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Analyse des ventes")
        self.setGeometry(150, 150, 350, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("logo_cargo.png").scaledToWidth(200, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        title = QLabel("Analyse des Ventes")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)

        actions = [
            ("Consulter le nombre de réservations passées par mois", self.action1),
            ("Consulter le nombre de réservations passées par ans", self.action2),
            ("Calculer le bénéfice sur l'année", self.action3),
            ("Consulter le bénéfice par année", self.action4),
            ("Consulter le bénéfice total", self.action5),
            ("Consulter le nombre de réservation par véhicule par année", self.action6),
            ("Consulter le nombre de réservation par véhicule", self.action7),
            ("Consulter la rentabilité par véhicule", self.action8),
            ("Consulter Le type de réservation par véhicule (surclassement ou classique)", self.action9),
        ]

        for (label, func) in actions:
            btn = QPushButton(label)
            btn.clicked.connect(func)
            layout.addWidget(btn)

        btn_quitter = QPushButton("Retour")
        btn_quitter.clicked.connect(self.close)
        layout.addWidget(btn_quitter)

        self.setLayout(layout)

    def action1(self):
        dlg = FenetreGraphiqueVentes(f.plot_reservations_par_mois)
        dlg.exec_()

    def action2(self):
        dlg = FenetreGraphiqueVentes(f.plot_reservations_par_annee)
        dlg.exec_()
    def action3(self):
        annee, ok = QInputDialog.getInt(self, "Année", "Choisir l'année :")
        if ok:
            benefice = f.benefice_pour_annee(annee)
            QMessageBox.information(self, "Info", f"Benefice sur l'année {annee} : {round(benefice, 2)} € ")

    def action4(self):
        dlg = FenetreGraphiqueVentes(f.benefice_par_annee_histogramme)
        dlg.exec_()

    def action5(self):
        benef_tot = f.afficher_benefice_total()
        QMessageBox.information(self, "Info", f"Bénéfice total : {round(benef_tot, 2)} €")

    def action6(self):
        annee, ok = QInputDialog.getInt(self, "Année", "Choisir l'année :")
        if ok:
            dlg = FenetreGraphiqueVentes(lambda: f.reservations_par_vehicule_par_an(annee=annee))
            dlg.exec_()

    def action7(self):
        dlg = FenetreGraphiqueVentes(f.plot_reservations_par_vehicule)
        dlg.exec_()

    def action8(self):
        RESERVATIONS_FILE = 'data/reservations.csv'
        VEHICULES_FILE = 'data/vehicules.csv'
        dlg = FenetreGraphiqueVentes(f.plot_rentabilite_depuis_csv)
        dlg.exec_()
        

    def action9(self):
        RESERVATIONS_FILE = 'data/reservations.csv'
        dlg = FenetreGraphiqueVentes(f.plot_reservations_histogram)
        dlg.exec_()     

class MenuVendeurIHM(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Vendeur - Location de Véhicules")
        self.setGeometry(100, 100, 500, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("logo_cargo.png").scaledToWidth(200, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        title = QLabel("Bienvenue dans votre espace vendeur")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        actions = [
            "Consulter le catalogue de véhicules",
            "Consulter les utilisateurs",
            "Consulter les réservations",
            "Ajouter un véhicule",
            "Supprimer un véhicule",
            "Faire une réservation",
            "Annuler une réservation",
            "Créer un compte client",
            "Supprimer un compte client",
            "Changer de mot de passe",
            "Analyse des ventes",
            "Modifier une caractéristique sur un véhicule",
            "Modifier une caractéristique sur votre compte",
            "Consulter les réservations prochaines d'un véhicule",
            "Consulter un véhicule",
            "Quitter"
        ]

        for action in actions:
            btn = QPushButton(action)
            if action == "Quitter":
                btn.clicked.connect(self.close)
            elif action == "Analyse des ventes":
                btn.clicked.connect(self.ouvrir_menu_analyse_ventes)
            else:
                btn.clicked.connect(lambda checked, a=action: self.show_message(a))
            layout.addWidget(btn)  # Ajout de tous les boutons au layout

        scroll = QScrollArea()
        content_widget = QWidget()
        content_widget.setLayout(layout)
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(scroll)
        self.setLayout(outer_layout)

    def show_message(self, action_name):
        QMessageBox.information(self, "Action", f"Action déclenchée : {action_name}")
   
    def ouvrir_menu_analyse_ventes(self):
        dlg = MenuAnalyseVentesDialog()
        dlg.exec_()  # fenêtre modale

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Choisir quelle interface afficher pour test
    role = "V"  # ⇐ Change en "vendeur" pour tester le menu vendeur

    if role == "C":
        window = MenuClientIHM()
    else:
        window = MenuVendeurIHM()

    window.show()
    sys.exit(app.exec_())