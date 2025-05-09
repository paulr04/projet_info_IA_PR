def facture(reservation, user, vehicule):
    import os
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader

    # Récupération des infos
    id_resa = reservation.id_resa
    id_vehicule = reservation.id_vehicule
    date_debut = reservation.date_debut
    date_fin = reservation.date_fin
    jours_res = reservation.jours
    prix = reservation.prix_total
    id_user = reservation.id_user
    surclassement = reservation.surclassement

    nom = user.nom
    prenom = user.prenom
    email = user.email
    telephone = user.telephone

    modele = vehicule.modele
    marque_vehicule = vehicule.marque
    prix_jour = vehicule.prix_jour
    description = vehicule.description

    fichier_pdf = f"facture_{id_resa}.pdf"
    path_save = os.path.join(os.path.abspath("factures_pdf"), fichier_pdf)

    c = canvas.Canvas(path_save, pagesize=A4)
    width, height = A4
    logo_name = 'logo_cargo.png'
    logo_path = os.path.abspath(logo_name)

    # Ajout du logo
    if os.path.exists(logo_path):
        try:
            logo = ImageReader(logo_path)
            c.drawImage(logo, 50, height - 150, width=100, preserveAspectRatio=True, mask='auto')
            print("Logo ajouté avec succès !")
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'image : {e}")
    else:
        print("ERREUR : Le fichier logo n'existe pas !")

    # Titre
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 200, "Facture de Location")

    # Infos Client
    y = height - 250
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Informations du Client :")
    c.setFont("Helvetica", 12)
    c.drawString(50, y - 20, f"Nom : {prenom} {nom}")
    c.drawString(50, y - 40, f"Email : {email}")
    c.drawString(50, y - 60, f"Téléphone : {telephone}")
    c.drawString(50, y - 80, f"ID Utilisateur : {id_user}")

    # Infos Réservation
    y -= 120
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Informations de la Réservation :")
    c.setFont("Helvetica", 12)
    c.drawString(50, y - 20, f"ID Réservation : {id_resa}")
    c.drawString(50, y - 40, f"Surclassement : {'Oui' if surclassement else 'Non'}")  # <-- Ligne ajoutée
    c.drawString(50, y - 60, f"ID Véhicule : {id_vehicule}")
    c.drawString(50, y - 80, f"Date de Début : {date_debut}")
    c.drawString(50, y - 100, f"Date de Fin : {date_fin}")
    c.drawString(50, y - 120, f"Jours de Réservation : {jours_res}")

    # Infos Véhicule
    y -= 160
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Informations sur le Véhicule :")
    c.setFont("Helvetica", 12)
    c.drawString(50, y - 20, f"Marque : {marque_vehicule}")
    c.drawString(50, y - 40, f"Modèle : {modele}")
    c.drawString(50, y - 60, f"Prix par Jour : {prix_jour} €")
    c.drawString(50, y - 80, f"Description : {description}")

    # Prix total
    y -= 140
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Prix Total de la Location :")
    c.setFont("Helvetica", 12)
    c.drawString(50, y - 20, f"{prix} €")

    # Signature
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, "Merci pour votre confiance ! CarGo © 2025")

    c.save()
    print(f"Facture générée : {fichier_pdf}")
