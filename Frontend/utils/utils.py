from pathlib import Path 
from qtpy.QtGui import QIntValidator, QDoubleValidator


current_directory = Path(__file__).parent
Front_end = current_directory.parent 

Tracpharmic = Path.home()/"Tracpharmic"

images = Tracpharmic/"images"

dataset = Tracpharmic/"dataset"/"pharmadataset.db" 


name_application = "TracPharmic"  


def set_styles():
    try:
        with open(Front_end/"style"/"style.qss", "r") as file:
            style = file.read()
            """background_path_str =  str(background_path).replace("\\", "/") 
            arrowdrop_str =  str(arrowdrop).replace("\\", "/") 
            style = style.replace("background_image",background_path_str)
            style = style.replace("arrowdrop", arrowdrop_str)""" 
            return style
    except FileNotFoundError:
        print("Style file not found. Using default styles.")


int_validator = QIntValidator()
float_validator = QDoubleValidator() 

profile_salarie = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/profilsalarie.png"

app_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/pharmacie_bloc.png"

deconexion_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/deconexion.png"

salare_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/salarielogo.png"
fournisseur_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/fournisseurlogo.png"

kpi_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/kpi.png"
acceuil_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/logoacceuil.png"
commande_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/commandelogo.png"
credit_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/creditlogoa.png"
vente_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/ventelogo.svg"
client_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/clientlogo.png"
echange_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/echangelogo.png"
stock_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/stocklogo.png"
medicament_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/medicamentlogo.png"
ferme_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/ferme.png"
retour_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/retour.png"





# Informations de connexion Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "pharmacieapplication@gmail.com"  # Remplace par ton email
smtp_password = "adck kohd tuqu iomh"  # Utiliser un mot de passe d'application

# Définition de l'expéditeur et du destinataire
sender_email = smtp_user
receiver_email = "zaiou.ahm@gmail.com"
