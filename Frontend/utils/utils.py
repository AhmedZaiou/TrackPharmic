from pathlib import Path 
from qtpy.QtGui import QIntValidator, QDoubleValidator
from Frontend.utils.validators import *
from qtpy.QtGui import QRegularExpressionValidator
from qtpy.QtCore import QRegularExpression

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


int_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{1,15}$"))
float_validator = QDoubleValidator() 
email_validator = EmailValidator()
phone_validator = PhoneValidator()

profile_salarie = f"{Front_end}/images/profilsalarie.png"
app_logo = f"{Front_end}/images/pharmacie_bloc.png"
deconexion_logo = f"{Front_end}/images/deconexion.png"
salare_logo = f"{Front_end}/images/salarielogo.png"
fournisseur_logo = f"{Front_end}/images/fournisseurlogo.png"
kpi_logo = f"{Front_end}/images/kpi.png"
acceuil_logo = f"{Front_end}/images/logoacceuil.png"
commande_logo = f"{Front_end}/images/commandelogo.png"
credit_logo = f"{Front_end}/images/creditlogoa.png"
vente_logo = f"{Front_end}/images/ventelogo.svg"
client_logo = f"{Front_end}/images/clientlogo.png"
echange_logo = f"{Front_end}/images/echangelogo.png"
stock_logo = f"{Front_end}/images/stocklogo.png"
medicament_logo = f"{Front_end}/images/medicamentlogo.png"
ferme_logo = f"{Front_end}/images/ferme.png"
retour_logo = f"{Front_end}/images/retour.png"





# Informations de connexion Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "pharmacieapplication@gmail.com"  # Remplace par ton email
smtp_password = "adck kohd tuqu iomh"  # Utiliser un mot de passe d'application

# Définition de l'expéditeur et du destinataire
sender_email = smtp_user
receiver_email = "zaiou.ahm@gmail.com"











# data base

host = "srv1653.hstgr.io"
user = "u454999796_root"
password = "Ah@2019@"
database = "u454999796_pharma"





