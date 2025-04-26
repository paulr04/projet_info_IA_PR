from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader 
import os 

def facture(reservation,user):
    print("Je suis dans la fonction facture")
    id_resa = reservation.id_resa
    id_vehicule = reservation.id_vehicule
    date_debut = reservation.date_debut
    date_fin = reservation.date_fin
    jours_res = reservation.jours
    prix = reservation.prix_total
    id_user = reservation.id_user
    nom = user.nom
    prenom = user.prenom
    email = user.email
    telephone = user.telephone

    fichier_pdf = f"facture_{id_resa}.pdf"
    c = canvas.Canvas(fichier_pdf, pagesize=A4)
    width, height = A4

    # Ajout d'une image
    logo_path = r"C:\Users\Utilisateur\projet_voiture\projet_info_IA_PR\onlydrive_logo.png"
    print(f"Je cherche le logo ici : {logo_path}")

    if not os.path.exists(logo_path):
        print("ERREUR : Le fichier logo n'existe pas !")
    else:
        try:
            logo = ImageReader(logo_path)
            c.drawImage(logo, 50, height - 150, width=100, preserveAspectRatio=True, mask='auto')
            print("Logo ajouté avec succès !")
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'image : {e}")

    # Titre (un peu plus bas pour laisser l'image tranquille)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 200, "Facture de Location")

    # Informations du client
    y = height - 250  # Décaler tout le texte en fonction
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Informations du Client :")
    c.setFont("Helvetica", 12)
    c.drawString(50, y - 20, f"Nom : {prenom} {nom}")
    c.drawString(50, y - 40, f"Email : {email}")
    c.drawString(50, y - 60, f"Téléphone : {telephone}")
    c.drawString(50, y - 80, f"ID Utilisateur : {id_user}")

    # Informations de réservation
    y -= 120
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Informations de la Réservation :")
    c.setFont("Helvetica", 12)
    c.drawString(50, y - 20, f"ID Réservation : {id_resa}")
    c.drawString(50, y - 40, f"ID Véhicule : {id_vehicule}")
    c.drawString(50, y - 60, f"Date de Début : {date_debut}")
    c.drawString(50, y - 80, f"Date de Fin : {date_fin}")
    c.drawString(50, y - 100, f"Jours de Réservation : {jours_res}")

    # Prix
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 140, "Prix Total :")
    c.setFont("Helvetica", 12)
    c.drawString(50, y - 160, f"{prix} €")

    # Signature
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, "Merci pour votre confiance ! OnlyDrive © 2025")
    c.save()
    print(f"Facture générée : {fichier_pdf}")
