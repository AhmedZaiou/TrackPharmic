from pathlib import Path
from qtpy.QtGui import QIntValidator, QDoubleValidator
from Frontend.utils.validators import *
from qtpy.QtGui import QRegularExpressionValidator
from qtpy.QtCore import QRegularExpression
from dotenv import load_dotenv
import os


load_dotenv("config.env")


current_directory = Path(__file__).parent
Front_end = current_directory.parent
Tracpharmic = Path.home() / "Tracpharmic"
images = Tracpharmic / "images"
dataset = Tracpharmic / "dataset" / "pharmadataset.db"
name_application = "TracPharmic"

matricul_pharma = "10"


def set_styles():
    try:
        with open(Front_end / "style" / "style.qss", "r") as file:
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
commande_client_logo = f"{Front_end}/images/commande_client.png"
credit_logo = f"{Front_end}/images/creditlogoa.png"
vente_logo = f"{Front_end}/images/ventelogo.png"
client_logo = f"{Front_end}/images/clientlogo.png"
echange_logo = f"{Front_end}/images/echangelogo.png"
stock_logo = f"{Front_end}/images/stocklogo.png"
stock_gestion_logo = f"{Front_end}/images/gestionstock_logo.png"
medicament_logo = f"{Front_end}/images/medicamentlogo.png"
ferme_logo = f"{Front_end}/images/ferme.png"
retour_logo = f"{Front_end}/images/retour.png"
font_path = f"{Front_end}/Monopoly.ttf"

# sumatra_path =r"C:\Users\dikster\AppData\Local\SumatraPDF\SumatraPDF.exe"

sumatra_path = os.getenv(
    "sumatra_path"
)  # r"C:\Users\Admin\AppData\Local\SumatraPDF\SumatraPDF.exe"


# Informations de connexion Gmail
smtp_server = os.getenv("smtp_server")
smtp_port = os.getenv("smtp_port")
smtp_user = os.getenv("smtp_user")
smtp_password = os.getenv("smtp_password")
# Définition de l'expéditeur et du destinataire
sender_email = smtp_user


# Informations de connexion à la base de données et facture Pharmacie Rachad Taza
"""
host = "srv1905.hstgr.io"
user = "u791384722_pharma"
password = "@sCM^n4L"
database = "u791384722_pharma"
"""

"""Name_pharma = "RACHAD TAZA"
Email_pharma = "bichrjamai@icloud.com"
receiver_email =  "zaiou.ahm@gmail.com" #"bichrjamai@icloud.com" #
Adresse_pharma = "Hay Rachad,Bloc2,n:75,Taza"
Tel_pharma = "0535285298, 0680061368"""


# data base original


host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
database = os.getenv("database")

Name_pharma = os.getenv("Name_pharma")
Email_pharma = os.getenv("Email_pharma")
receiver_email = os.getenv("receiver_email")  # "bichrjamai@icloud.com" #
Adresse_pharma = os.getenv("Adresse_pharma")
Tel_pharma = os.getenv("Tel_pharma")


from PyQt5.QtWidgets import QMessageBox


def confirm_sale(interface, titre, message):
    msg_box = QMessageBox(interface)
    msg_box.setFixedWidth(1500)
    msg_box.setWindowTitle(titre)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
    return msg_box.exec_()


def calculate_check_digit(ean12):
    total = 0
    for i, digit in enumerate(ean12):
        digit = int(digit)
        if i % 2 == 0:
            total += digit  # Chiffres impairs (index pair)
        else:
            total += digit * 3  # Chiffres pairs (index impair)
    remainder = total % 10
    check_digit = (10 - remainder) % 10
    return check_digit
