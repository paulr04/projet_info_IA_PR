import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
import csv

VEHICULES_FILE = 'data/vehicules.csv'  # adapte le chemin si besoin

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Catalogue")
        self.setGeometry(200, 200, 700, 400)

        btn = QPushButton("Consulter catalogue", self)
        btn.clicked.connect(self.consulter_catalogue)
        self.setCentralWidget(btn)

    def consulter_catalogue(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Catalogue des véhicules")
        dialog.resize(700, 400)

        layout = QVBoxLayout(dialog)

        table = QTableWidget()
        layout.addWidget(table)

        try:
            with open(VEHICULES_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                
                if not rows:
                    table.setRowCount(0)
                    table.setColumnCount(0)
                    return
                
                headers = reader.fieldnames
                table.setColumnCount(len(headers))
                table.setHorizontalHeaderLabels(headers)
                table.setRowCount(len(rows))

                for row_idx, row in enumerate(rows):
                    for col_idx, header in enumerate(headers):
                        val = row[header]
                        # Transformer dispo en Oui/Non lisible
                        if header == 'dispo':
                            val = "Oui" if val.lower() in ['true', '1', 'oui'] else "Non"
                        item = QTableWidgetItem(val)
                        table.setItem(row_idx, col_idx, item)

                # Masquer les colonnes "entretien_annuel" et "dispo" si elles existent
                if 'entretien_annuel' in headers:
                    col_index = headers.index('entretien_annuel')
                    table.setColumnHidden(col_index, True)
                if 'dispo' in headers:
                    col_index = headers.index('dispo')
                    table.setColumnHidden(col_index, True)
                if 'description' in headers:
                    col_index = headers.index('description')
                    table.setColumnWidth(col_index, 450)
        except Exception as e:
            print(f"Erreur lors du chargement du catalogue : {e}")

        btn_close = QPushButton("Fermer")
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)

        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
