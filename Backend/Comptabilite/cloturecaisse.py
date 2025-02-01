import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os


import smtplib
import matplotlib.pyplot as plt
import io
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage




from Backend.Dataset.achat import Achats  # Assurez-vous que l'import est correct
from Backend.Dataset.client import Clients  # Assurez-vous de l'existence des classes appropriées
from Backend.Dataset.commande import Commandes
from Backend.Dataset.credit import Credit
from Backend.Dataset.echanges import Echanges
from Backend.Dataset.fournisseur import Fournisseur
from Backend.Dataset.medicament import Medicament
from Backend.Dataset.salarie import Salaries
from Backend.Dataset.stock import Stock
from Backend.Dataset.payment import Payment
from Backend.Dataset.pharmacie import Pharmacies
from Backend.Dataset.ventes import Ventes
from Backend.Dataset.retour import Retour





# Informations de connexion Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "pharmacieapplication@gmail.com"  # Remplace par ton email
smtp_password = "adck kohd tuqu iomh"  # Utiliser un mot de passe d'application

# Définition de l'expéditeur et du destinataire
sender_email = smtp_user
receiver_email = "zaiou.ahm@gmail.com"

 
class Caisse:
    def __init__(self):
        self.dataset = dataset


    def cloture_journee(self): 
        cloture_dict = {}
        cloture_dict['Achat statistique'] = Achats.cloture_journee()
        cloture_dict['Client statistique'] = Clients.cloture_journee()
        cloture_dict['Commande statistique'] = Commandes.cloture_journee()
        cloture_dict['Credit statistique'] = Credit.cloture_journee()
        cloture_dict['Echange statistique'] = Echanges.cloture_journee()
        cloture_dict['Medicament statistique'] = Medicament.cloture_journee()
        cloture_dict['Paiment statistique'] = Payment.cloture_journee()
        cloture_dict['Retour statistique'] = Retour.cloture_journee()
        cloture_dict['Stock statistique'] = Stock.cloture_journee()
        cloture_dict['Vente statistique'] = Ventes.cloture_journee()
        print(cloture_dict)
        # Générer le HTML
        html_content = self.generate_html(cloture_dict)
        self.send_email(html_content)


    def fermeture_de_caisse(self):
        self.cloture_journee() 
    







    # Fonction pour créer un tableau HTML
    def create_table(self, data, title):
        html = f"<h2>{title}</h2>"
        html += "<table border='1' style='width: 100%; border-collapse: collapse; margin-bottom: 20px;'><tr><th>Indicateur</th><th>Valeur</th></tr>"
        for key, value in data.items():
            if isinstance(value, dict):
                # Cas où la valeur est un sous-ensemble de données
                html += self.create_table(value, key)
            elif isinstance(value, list) and value:
                # Cas où la valeur est une liste non vide
                for item in value:
                    if isinstance(item, dict): 
                        html += self.create_table(item, key) 
                    else:
                        html += f"<tr><td>{key}</td><td> {item}</td></tr>"
            else:
                html += f"<tr><td>{key}</td><td>{value if value is not None else 'N/A'}</td></tr>"
        html += "</table>"
        return html

    # Générer le code HTML pour tout le JSON
    def generate_html(self, data):
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h2 { color: #333366; }
                table { border: 1px solid #ccc; width: 100%; margin-bottom: 20px; }
                th, td { padding: 8px; text-align: left; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                tr:hover { background-color: #ddd; }
            </style>
        </head>
        <body>
        """
        
        # Parcourir les données pour générer les tables
        for section, content in data.items():
            html += f'<div class="section">{self.create_table(content, section)}</div>'

        html += """
        </body>
        </html>
        """
        return html






    def send_email(self, html_message):
        msg = MIMEMultipart()
        msg['Subject'] = f"📊 Rapport Journalier des Ventes {datetime.now()}"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        msg.attach(MIMEText(html_message, "html"))

        # Envoi du mail via Gmail SMTP
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(sender_email, [receiver_email], msg.as_string())
            print("✅ E-mail envoyé avec succès.")
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'e-mail : {e}")


 