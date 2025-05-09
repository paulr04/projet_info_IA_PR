import re

# La chaîne générée par ton code
string = "RESERVATION 578878064 CLIENT 123456789 VEHICULE FR-416-FR DU 08-08-2025 AU 08-09-2025 JOURS 2 PRIX 30000.0 SURCLASSEMENT False"

# Variables dynamiques
id_resa = 578878064
id_user = 123456789
id_vehicule = "FR-416-FR"
date_debut = "08-08-2025"
date_fin = "08-09-2025"
jours_res = 2
prix = 30000.0
surclassement = False

# Générer la chaîne avec une f-string
string = f"RESERVATION {id_resa} CLIENT {id_user} VEHICULE {id_vehicule} DU {date_debut} AU {date_fin} JOURS {jours_res} PRIX {prix} SURCLASSEMENT {surclassement}"

# Afficher la chaîne générée
print(string)

# Pattern regex amélioré pour correspondre au format exact
pattern = r"RESERVATION (\d{9}) CLIENT (\d{9}) VEHICULE ([A-Z]{2}-\d{3}-[A-Z]{2}) DU (\d{2}-\d{2}-\d{4}) AU (\d{2}-\d{2}-\d{4}) JOURS (\d+) PRIX ([\d\.]+) SURCLASSEMENT (True|False)"

# Recherche avec le pattern
match = re.match(pattern, string)

# Vérification et affichage des groupes capturés
if match:
    print("Match trouvé !")
    print(f"ID Réservation: {match.group(1)}")
    print(f"ID Client: {match.group(2)}")
    print(f"Véhicule: {match.group(3)}")
    print(f"Date de début: {match.group(4)}")
    print(f"Date de fin: {match.group(5)}")
    print(f"Jours: {match.group(6)}")
    print(f"Prix: {match.group(7)}")
    print(f"Surclassement: {match.group(8)}")
else:
    print("Aucun match trouvé.")
