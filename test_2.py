import csv
import matplotlib.pyplot as plt
from collections import defaultdict

def plot_rentabilite_depuis_csv(fichier_resa, fichier_vehicules):
    revenus = defaultdict(float)
    entretiens = {}

    # Lecture des revenus depuis le fichier des réservations 
    with open(fichier_resa, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_vehicule = row["id_vehicule"]
            prix = float(row["prix_total"])
            revenus[id_vehicule] += prix

    #Lecture des coûts d'entretien depuis le fichier des véhicules
    with open(fichier_vehicules, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_vehicule = row["id_vehicule"]
            entretien = float(row["entretien_annuel"])
            entretiens[id_vehicule] = entretien

    #Fusion des véhicules présents dans les deux fichiers
    ids_vehicules = sorted(list(set(revenus.keys()) & set(entretiens.keys())))
    liste_revenus = [revenus[v] for v in ids_vehicules]
    liste_entretiens = [entretiens[v] for v in ids_vehicules]

    #Calcul des indices de rentabilité
    indices = []
    for i in range(len(ids_vehicules)):
        revenu = liste_revenus[i]
        cout = liste_entretiens[i]
        indice = revenu / cout if cout != 0 else float('inf')
        indices.append(indice)
        print(f"Véhicule {ids_vehicules[i]}  Indice de rentabilité : {indice:.2f}")

    #Affichage du graphique
    x = range(len(ids_vehicules))
    width = 0.35
    fig, ax = plt.subplots(figsize=(14, 8))
    #Diviser les valeurs par 1000 pour affichage en k€
    bar1 = ax.bar([i - width/2 for i in x], [r / 1000 for r in liste_revenus], width, label="Revenus (k€)", color='green')
    bar2 = ax.bar([i + width/2 for i in x], [e / 1000 for e in liste_entretiens], width, label="Entretien (k€)", color='red')

    #Ajout des indices de rentabilité au-dessus des barres
    for i in range(len(x)):
        pos = max(liste_revenus[i], liste_entretiens[i]) / 1000 + 0.05
        ax.text(i, pos, f"{indices[i]:.2f}", ha='center', fontsize=11, fontweight='bold')

    ax.set_xlabel("ID Véhicule")
    ax.set_ylabel("Montant (k€)")
    ax.set_title("Revenus vs Entretien (en k€) avec Indice de Rentabilité")
    ax.set_xticks(x)
    ax.set_xticklabels(ids_vehicules)
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    print("Graphique généré avec succès !")

# Exemple d'appel :
# plot_rentabilite_depuis_csv("reservations.csv", "vehicules.csv")

if __name__ == "__main__":
    # Exemple d'utilisation
    plot_rentabilite_depuis_csv("data/reservations.csv", "data/vehicules.csv")
