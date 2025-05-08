import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

def generer_compte_rendu_ventes(fichier='data/reservations.csv'):
    ca_par_mois = defaultdict(float)
    ca_par_annee = defaultdict(float)
    reservations_par_jour = defaultdict(int)

    with open(fichier, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for ligne in reader:
            date_str = ligne['date_debut']
            prix = float(ligne['prix_total'])

            try:
                date = datetime.strptime(date_str, "%m-%d-%Y")
                mois = date.strftime('%Y-%m')  # ex: '2025-04'
                annee = date.year             # ex: 2025
                jour = date.strftime('%Y-%m-%d')  # ex: '2025-04-27'

                ca_par_mois[mois] += prix
                ca_par_annee[annee] += prix
                reservations_par_jour[jour] += 1

            except ValueError:
                print(f"Date invalide ignorée : {date_str}")

    # === Histogramme 1 : Chiffre d'affaires par mois ===
    plt.figure(figsize=(12, 6))
    mois_tries = sorted(ca_par_mois.keys())
    valeurs_mois = [ca_par_mois[mois] for mois in mois_tries]
    plt.bar(mois_tries, valeurs_mois, color='skyblue')
    plt.xticks(rotation=45)
    plt.title("Chiffre d'affaires par mois")
    plt.xlabel("Mois")
    plt.ylabel("CA (€)")
    plt.tight_layout()
    plt.show()

    # === Histogramme 2 : Chiffre d'affaires par année ===
    plt.figure(figsize=(8, 5))
    annees_tries = sorted(ca_par_annee.keys())
    valeurs_annee = [ca_par_annee[a] for a in annees_tries]
    plt.bar([str(a) for a in annees_tries], valeurs_annee, color='orange')
    plt.title("Chiffre d'affaires par année")
    plt.xlabel("Année")
    plt.ylabel("CA (€)")
    plt.tight_layout()
    plt.show()

    # === Histogramme 3 : Nombre de réservations par jour ===
    plt.figure(figsize=(14, 6))
    jours_tries = sorted(reservations_par_jour.keys())
    nb_reservations = [reservations_par_jour[jour] for jour in jours_tries]
    plt.bar(jours_tries, nb_reservations, color='green')
    plt.xticks(rotation=45, fontsize=8)
    plt.title("Nombre de réservations par jour")
    plt.xlabel("Jour")
    plt.ylabel("Nombre de réservations")
    plt.tight_layout()
    plt.show()

generer_compte_rendu_ventes('C:\\Users\\Utilisateur\\projet_voiture\\projet_info_IA_PR\\data\\reservations.csv')
