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
    logo_path = 