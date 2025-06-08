# projet_info_IA_PR
# Application de Location de Véhicules

# Organisation du dossier :

data/ 
# Contient les fichiers CSV pour les utilisateurs, véhicules, réservations
factures_pdf/ 
# Dossier où sont enregistrées les factures PDF générées
app_ihm.py 
# Point d’entrée principal avec interface graphique (PyQt5)
application.py
 # Ancienne version console du programme (obsolète)
objects.py 
# Définit les classes principales : Vehicule, User, Client, etc.
fonctions.py 
# Fonctions utilitaires : chargement de données, statistiques, etc.
facture.py 
# Génération des factures PDF

## Lancer le projet

1. Assurez-vous que tous les fichiers `.py` et les dossiers `data/` et `factures_pdf/` sont dans le même répertoire.
2. Installez les dépendances nécessaires si besoin (voir ci-dessous).
3. Exécutez le fichier principal avec la commande :

python app_ihm.py

4. Utilisez les identifiants suivants pour une démonstration (vendeur) :

ID : 954644716

Mot de passe : mdp_obi-wan

## Modules à importer

Voici la liste complète des modules nécessaires au bon fonctionnement de l’application :

```python
import sys
import os
import csv
import re
import random
import string
import pandas as pd
import numpy as np
from collections import defaultdict
from collections import Counter
import unittest
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime

# Modules PyQt5
from PyQt5.QtWidgets import (
    QDateEdit, QComboBox, QFormLayout, QHBoxLayout, QApplication, QTableWidgetItem,
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QTextEdit,
    QTableWidget, QMessageBox, QDialog, QLineEdit, QInputDialog
)
from PyQt5.QtGui import QPixmap, QFont, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp, QDate

# Modules internes
from facture import facture as fact
import fonctions as f
from objects import Client, Vendeur, Vehicule, Reservation_DSL, Admin