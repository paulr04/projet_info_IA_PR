print("on enmerde l'info")
print("SCIENCE BITCH")
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader 


def facture ():
    id_resa = 165750512
    id_vehicule = 'AA-123-AA'
    date_debut = '10-05-2025'
    date_fin = '12-05-2025'
    jours_res = 60
    prix = 2170.0
    id_user = 123456789
    nom = 'Doe'
    prenom = 'John'
    email = 'john.doe@example.com'
    telephone = '0123456789'
    role = 'C'
    mot_de_passe = 'mdp_client'
    #creation du fichier PDF
    fichier_pdf = f"facture_{id_resa}.pdf"
    c = canvas.Canvas(fichier_pdf, pagesize=A4)
    width, height = A4
    #ajout d'une image
    logo_path = "onlydrive_logo.png"
    try:
        logo = ImageReader(logo_path)
        c.drawImage(logo,50,height -120,width=150,preserveAspectRatio=True,mask='auto')
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'image : {e}")
    #ajout du texte
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 150, "Facture de Location")

    #informations du client 
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 200, "Informations du Client :")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 220, f"Nom : {prenom} {nom}")
    c.drawString(50, height - 240, f"Email : {email}")
    c.drawString(50, height - 260, f"Téléphone : {telephone}")
    c.drawString(50, height - 280, f"ID Utilisateur : {id_user}")
    #informations de la réservation
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 300, "Informations de la Réservation :")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 320, f"ID Réservation : {id_resa}")
    c.drawString(50, height - 340, f"ID Véhicule : {id_vehicule}")
    c.drawString(50, height - 360, f"Date de Début : {date_debut}")
    c.drawString(50, height - 380, f"Date de Fin : {date_fin}")
    c.drawString(50, height - 400, f"Jours de Réservation : {jours_res}")
    #Prix
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 440, "Prix Total :")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 460, f"{prix} €")
    #Signature
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, "Merci pour votre confiance ! OnlyDrive © 2025")
    c.save()
    print(f"Facture générée : {fichier_pdf}")

facture()