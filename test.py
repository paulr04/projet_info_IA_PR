import matplotlib.pyplot as plt

# Exemple de données (à remplacer par tes listes réelles)
ids_vehicules = ["V1", "V2", "V3"]
revenus = [3000, 1500, 4000]
entretiens = [1000, 1200, 2000]

# Calcul des indices de rentabilité
indices = []
for i in range(len(ids_vehicules)):
    revenu = revenus[i]
    cout = entretiens[i]
    indice = revenu / cout if cout != 0 else float('inf')
    indices.append(indice)
    print(f"Véhicule {ids_vehicules[i]} → Indice de rentabilité : {indice:.2f}")

# Position des barres
x = range(len(ids_vehicules))
width = 0.35

# Création du graphique
fig, ax = plt.subplots()
bar1 = ax.bar([i - width/2 for i in x], revenus, width, label="Revenus", color='green')
bar2 = ax.bar([i + width/2 for i in x], entretiens, width, label="Entretien", color='red')

# Ajout des indices au-dessus
for i in range(len(x)):
    ax.text(i, max(revenus[i], entretiens[i]) + 100, f"{indices[i]:.2f}", ha='center', fontsize=9, fontweight='bold')

# Personnalisation
ax.set_xlabel("ID Véhicule")
ax.set_ylabel("Euros")
ax.set_title("Revenus vs Entretien avec Indice de Rentabilité")
ax.set_xticks(x)
ax.set_xticklabels(ids_vehicules)
ax.legend()
plt.tight_layout()
plt.show()

print ("Graphique généré avec succès !")