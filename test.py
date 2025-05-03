import csv

def modifier_champ_csv(fichier_csv, champ_id, id_val, champs_interdits):
    # Lecture du fichier
    with open(fichier_csv, mode='r', newline='', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)
        lignes = list(lecteur)
        champs = lecteur.fieldnames

    if champ_id not in champs:
        print(f"Erreur : le champ ID '{champ_id}' n'existe pas.")
        return

    ligne_modifiee = False
    for ligne in lignes:
        if ligne[champ_id] == id_val:
            champs_modifiables = [c for c in champs if c not in champs_interdits]
            print("Champs modifiables :", champs_modifiables)

            champ_a_modifier = input("Quel champ voulez-vous modifier ? ")
            if champ_a_modifier not in champs_modifiables:
                print("Erreur : champ interdit ou inexistant.")
                return

            nouvelle_valeur = input(f"Nouvelle valeur pour '{champ_a_modifier}' : ")
            ligne[champ_a_modifier] = nouvelle_valeur
            ligne_modifiee = True
            break

    if not ligne_modifiee:
        print(f"Aucune ligne trouvée avec {champ_id} = {id_val}.")
        return

    with open(fichier_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(lignes)

    print("Modification effectuée avec succès.")

CHAMPS_INTERDITS = ['id_user', 'id_resa', 'id_vehicule', 'role', 'mot_de_passe', 'dimensions', 'type_moteur', 'type_vehicule', 'boite_vitesse']
id_val = "FR-416-FR"
modifier_champ_csv("data/vehicules.csv", "id_vehicule", id_val, CHAMPS_INTERDITS)
