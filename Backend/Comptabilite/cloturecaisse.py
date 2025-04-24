from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json

import smtplib
import matplotlib.pyplot as plt
import io
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


from Backend.Dataset.client import (
    Clients,
)  # Assurez-vous de l'existence des classes appropriées
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
receiver_email = "bichrjamai@icloud.com"


class Caisse:
    def __init__(self):
        self.dataset = dataset

    def cloture_journee(self):
        cloture_dict = {}
        cloture_dict["Client statistique"] = Clients.cloture_journee()
        cloture_dict["Commande statistique"] = Commandes.cloture_journee()
        cloture_dict["Credit statistique"] = Credit.cloture_journee()
        cloture_dict["Echange statistique"] = Echanges.cloture_journee()
        cloture_dict["Medicament statistique"] = Medicament.cloture_journee()
        cloture_dict["Paiment statistique"] = Payment.cloture_journee()
        cloture_dict["Retour statistique"] = Retour.cloture_journee()
        cloture_dict["Stock statistique"] = Stock.cloture_journee()
        cloture_dict["Vente statistique"] = Ventes.cloture_journee()
        cloture_dict = json.loads(json.dumps(cloture_dict, default=str))
        data = cloture_dict
        # Restructuration du dictionnaire
        result = {
            "Credit_situation_general": {
                "nombre_de_clients": data["Client statistique"][
                    "nombre_de_clients"
                ],
                "credit_max_autorise": data["Client statistique"][
                    "credit_max_autorise"
                ],
                "credit_actuel_pharmacie": data["Client statistique"][
                    "credit_actuel_pharmacie"
                ],
            },
            "Credit_situation_aujourdhui": {
                "total_restant_a_payer": data["Credit statistique"][
                    "Total restant à payer aujourd'hui"
                ],
                "total_paiements_effectues": data["Paiment statistique"][
                    "Total des paiements effectués aujourd'hui en Dhs"
                ],
                "nombre_paiements": data["Paiment statistique"][
                    "Nombre total de paiements effectués aujourd'hui"
                ],
            },
            "echange_situation_aujourdhui": {
                "echange_envoyer": data["Echange statistique"][
                    "Total des échanges de la journée envoyer"
                ],
                "echange_recus": data["Echange statistique"][
                    "Total des échanges de la journée recus"
                ],
            },
            "Stock_situation": {
                "total_medicaments": data["Medicament statistique"][
                    "Total des médicaments"
                ],
                "medicaments_stock_inferieur_min": data["Medicament statistique"][
                    "Total des médicaments avec stock inférieur au minimum"
                ],
                "medicaments_stock_positif": data["Medicament statistique"][
                    "Total des médicaments avec stock positif"
                ],
                "commandes_en_attente": data["Commande statistique"][
                    "statistique general"
                ]["commandes_en_attente"],
            },
            
            "commande_situation": {
                "commend_passer": data["Commande statistique"][
                    "statistique general"
                ][
                    "total_commandes"
                ],
                "commandes_recues": data["Commande statistique"][
                    "statistique general"
                ][
                    "commandes_recues"
                ],
                "commandes_en_attente": data["Commande statistique"][
                    "statistique general"
                ]["commandes_en_attente"],
            },
            "Vente_situation": {
                "nombre_ventes_effectuees": data["Vente statistique"][
                    "Nombre total de ventes effectuées aujourdhui"
                ],
                "montant_total_ventes": data["Vente statistique"][
                    "Montant total des ventes effectuées aujourdhui"
                ],
                "total_retours": data["Retour statistique"][
                    "Total des retours effectués aujourdhui"
                ],
            },
            "Performance_salarie": {
                "total_operations_par_salarie": [
                    {
                        "id_salarie": item["salarie"],
                        "total_commandes": item["statistique"]["total_commandes"],
                        "commandes_recues": item["statistique"]["commandes_recues"],
                        "commandes_en_attente": item["statistique"][
                            "commandes_en_attente"
                        ],
                        "total_paiements": next(
                            (
                                x["total_paiements_salarie"]
                                for x in data["Paiment statistique"][
                                    "Total des paiements effectués aujourd'hui par salarié"
                                ]
                                if x["id_salarie"] == item["salarie"]
                            ),
                            0,
                        ),
                        "total_retours": next(
                            (
                                x["total_retours_salarie"]
                                for x in data["Retour statistique"][
                                    "Total des retours effectués aujourdhui par salarié"
                                ]
                                if x["id_salarie"] == item["salarie"]
                            ),
                            0,
                        ),
                    }
                    for item in data["Commande statistique"]["statistique par salarie"]
                ]
            },
        }

        print(result)

        # Générer le HTML
        html_content = self.generate_htmla(result)
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
        msg["Subject"] = f"📊 Rapport Journalier des Ventes {datetime.now()}"
        msg["From"] = sender_email
        msg["To"] = receiver_email

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

    def generate_html(self, statistics_dict):
        html_content = """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Rapport Statistique</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 10px; text-align: left; border: 1px solid #ddd; }
                th { background-color: #4CAF50; color: white; }
                h1, h2 { color: #333; }
                .section { margin-bottom: 30px; }
                .subsection { margin-top: 20px; }
            </style>
        </head>
        <body>
        <h1>Rapport de Statistiques du Jour</h1>
        """

        # Client Statistique
        html_content += """
        <div class="section">
            <h2>Client Statistique</h2>
            <table>
                <tr><th>Nombre de clients</th><td>{}</td></tr>
                <tr><th>Crédit maximum autorisé</th><td>{}</td></tr>
                <tr><th>Crédit actuel en pharmacie</th><td>{}</td></tr>
            </table>
        </div>
        """.format(
            statistics_dict["Client statistique"]["nombre_de_clients"],
            statistics_dict["Client statistique"]["credit_max_autorise"],
            statistics_dict["Client statistique"]["credit_actuel_pharmacie"],
        )

        # Commande Statistique
        html_content += """
        <div class="section">
            <h2>Commande Statistique</h2>
            <div class="subsection">
                <h3>Statistiques Générales</h3>
                <table>
                    <tr><th>Date</th><td>{}</td></tr>
                    <tr><th>Total des commandes</th><td>{}</td></tr>
                    <tr><th>Commandes reçues</th><td>{}</td></tr>
                    <tr><th>Commandes en attente</th><td>{}</td></tr>
                </table>
            </div>
        """.format(
            statistics_dict["Commande statistique"]["statistique general"]["date"],
            statistics_dict["Commande statistique"]["statistique general"][
                "total_commandes"
            ],
            statistics_dict["Commande statistique"]["statistique general"][
                "commandes_recues"
            ],
            statistics_dict["Commande statistique"]["statistique general"][
                "commandes_en_attente"
            ],
        )

        # Statistiques par salarié
        html_content += """
            <div class="subsection">
                <h3>Statistiques par salarié</h3>
                <table>
                    <tr><th>Salarie</th><th>Total commandes</th><th>Commandes reçues</th><th>Commandes en attente</th></tr>
        """

        for salarie in statistics_dict["Commande statistique"][
            "statistique par salarie"
        ]:
            salarie_name = salarie["salarie"]
            salarie_stats = salarie["statistique"]
            html_content += """
                <tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                </tr>
            """.format(
                salarie_name,
                salarie_stats["total_commandes"],
                salarie_stats["commandes_recues"],
                salarie_stats["commandes_en_attente"],
            )

        html_content += """
                </table>
            </div>
        </div>
        """

        # Crédits Statistique
        html_content += """
        <div class="section">
            <h2>Crédit Statistique</h2>
            <table>
                <tr><th>Total restant à payer aujourd'hui</th><td>{}</td></tr>
            </table>
        </div>
        """.format(
            statistics_dict["Credit statistique"]["Total restant à payer aujourd'hui"]
        )

        # Paiement Statistique
        html_content += """
        <div class="section">
            <h2>Paiement Statistique</h2>
            <table>
                <tr><th>Total des paiements effectués aujourd'hui en Dhs</th><td>{}</td></tr>
                <tr><th>Nombre total de paiements effectués aujourd'hui</th><td>{}</td></tr>
            </table>
            <div class="subsection">
                <h3>Total des paiements effectués par salarié</h3>
                <table>
                    <tr><th>ID Salarié</th><th>Total des paiements</th></tr>
        """.format(
            statistics_dict["Paiment statistique"][
                "Total des paiements effectués aujourd'hui en Dhs"
            ],
            statistics_dict["Paiment statistique"][
                "Nombre total de paiements effectués aujourd'hui"
            ],
        )

        for payment in statistics_dict["Paiment statistique"][
            "Total des paiements effectués aujourd'hui par salarié"
        ]:
            html_content += """
                <tr>
                    <td>{}</td>
                    <td>{}</td>
                </tr>
            """.format(
                payment["id_salarie"], payment["total_paiements_salarie"]
            )

        html_content += """
                </table>
            </div>
        </div>
        """

        # Retour Statistique
        html_content += """
        <div class="section">
            <h2>Retour Statistique</h2>
            <table>
                <tr><th>Total des retours effectués aujourd'hui (prix total)</th><td>{}</td></tr>
                <tr><th>Nombre total de retours effectués aujourd'hui</th><td>{}</td></tr>
            </table>
            <div class="subsection">
                <h3>Total des retours effectués par salarié</h3>
                <table>
                    <tr><th>ID Salarié</th><th>Total des retours</th></tr>
        """.format(
            statistics_dict["Retour statistique"][
                "Total des retours effectués aujourdhui"
            ],
            statistics_dict["Retour statistique"][
                "Nombre total de retours effectués aujourdhui"
            ],
        )

        for retour in statistics_dict["Retour statistique"][
            "Total des retours effectués aujourdhui par salarié"
        ]:
            html_content += """
                <tr>
                    <td>{}</td>
                    <td>{}</td>
                </tr>
            """.format(
                retour["id_salarie"], retour["total_retours_salarie"]
            )

        html_content += """
                </table>
            </div>
        </div>
        """

        # Stock Statistique
        html_content += """
        <div class="section">
            <h2>Stock Statistique</h2>
            <table>
                <tr><th>Total des achats pour la journée</th><td>{}</td></tr>
                <tr><th>Total des ventes pour la journée</th><td>{}</td></tr>
                <tr><th>Quantités totales en stock aujourd'hui</th><td>{}</td></tr>
                <tr><th>Quantités minimales non respectées aujourd'hui</th><td>{}</td></tr>
                <tr><th>Nombre de médicaments proches de la date d'expiration aujourd'hui</th><td>{}</td></tr>
            </table>
        </div>
        """.format(
            statistics_dict["Stock statistique"]["Total des achats pour la journée"],
            statistics_dict["Stock statistique"]["Total des ventes pour la journée"],
            statistics_dict["Stock statistique"][
                "Quantités totales en stock aujourdhui"
            ],
            statistics_dict["Stock statistique"][
                "Quantités minimales non respectées aujourdhui"
            ],
            statistics_dict["Stock statistique"][
                "Nombre Médicaments proches de la date dexpiration aujourdhui"
            ],
        )

        # Vente Statistique
        html_content += """
        <div class="section">
            <h2>Vente Statistique</h2>
            <table>
                <tr><th>Nombre total de ventes effectuées aujourd'hui</th><td>{}</td></tr>
                <tr><th>Montant total des ventes effectuées aujourd'hui</th><td>{}</td></tr>
                <tr><th>Quantité totale vendue aujourd'hui</th><td>{}</td></tr>
                <tr><th>Total des achats effectués aujourd'hui</th><td>{}</td></tr>
                <tr><th>Total des profits réalisés aujourd'hui</th><td>{}</td></tr>
            </table>
        </div>
        """.format(
            statistics_dict["Vente statistique"][
                "Nombre total de ventes effectuées aujourdhui"
            ],
            statistics_dict["Vente statistique"][
                "Montant total des ventes effectuées aujourdhui"
            ],
            statistics_dict["Vente statistique"]["Quantité totale vendue aujourdhui"],
            statistics_dict["Vente statistique"][
                "Total des achats effectués aujourdhui"
            ],
            statistics_dict["Vente statistique"][
                "Total des profits réalisés aujourdhui"
            ],
        )

        html_content += """
        </body>
        </html>
        """

        return html_content

    def generate_htmla(self, data):
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Rapport de Situation - Pharmacie</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #e0f7fa; /* Fond bleu clair */
                }}
                .container {{
                    width: 80%;
                    margin: 20px auto;
                    padding: 20px;
                    border: 1px solid #00796b; /* Bordure verte foncée */
                    border-radius: 8px;
                    background-color: #ffffff; /* Fond blanc */
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #00796b; /* Vert foncé */
                    text-align: center;
                }}
                h2 {{
                    color: #004d40; /* Vert très foncé */
                    border-bottom: 2px solid #00796b; /* Ligne sous le titre */
                    padding-bottom: 5px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                table, th, td {{
                    border: 1px solid #00796b; /* Bordure verte foncée */
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                }}
                th {{
                    background-color: #00796b; /* Fond vert foncé */
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #e0f2f1; /* Fond bleu clair pour les lignes paires */
                }}
                .highlight {{
                    background-color: #b2dfdb; /* Fond vert clair pour les cellules importantes */
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Rapport de Situation - Pharmacie</h1>
                <!-- Section Cloture -->
                <h2>Situation Générale de caisse</h2>
                <table>
                    <tr>
                        <th>Total des ventes aujourd'hui</th>
                        <td>{data["Vente_situation"]["montant_total_ventes"]} Dh</td>
                    </tr>
                    <tr>
                        <th>Total des crédits accordés aujourd'hui</th>
                        <td>{data['Credit_situation_aujourdhui']['total_restant_a_payer']} Dh</td>
                    </tr>
                    <tr>
                        <th>Total des paiements de crédit aujourd'hui</th>
                        <td>{data['Credit_situation_aujourdhui']['total_paiements_effectues']} Dh</td>
                    </tr>
                    <tr>
                        <th>Total des retours aujourd'hui</th>
                        <td>{data['Vente_situation']['total_retours']} Dh</td>
                    </tr>
                    <tr>
                        <th>Total de la caisse provisoire aujourd'hui</th>
                        <td>{float(data["Vente_situation"]["montant_total_ventes"]) - float(data['Vente_situation']['total_retours']) - float(data['Credit_situation_aujourdhui']['total_restant_a_payer']) + float(data['Credit_situation_aujourdhui']['total_paiements_effectues']) } Dh</td>
                    </tr>
                </table>

                <!-- Section Crédit -->
                <h2>Situation Générale de Crédit</h2>
                <table>
                    <tr>
                        <th>Crédit Max Autorisé</th>
                        <td>{data['Credit_situation_general']['credit_max_autorise']} Dh</td>
                    </tr>
                    <tr>
                        <th>Crédit Actuel en Pharmacie</th>
                        <td>{data['Credit_situation_general']['credit_actuel_pharmacie']} Dh</td>
                    </tr>
                </table>

                <!-- Section Crédit -->
                <h2>Situation des échanges aujourd'hui</h2>
                <table>
                    <tr>
                        <th>Envoyer vers des pharmacies amies</th>
                        <td>{data['echange_situation_aujourdhui']['echange_envoyer']} Dh</td>
                    </tr>
                    <tr>
                        <th>Les reçus provenant de pharmacies amies</th>
                        <td>{data['echange_situation_aujourdhui']['echange_recus']} Dh</td>
                    </tr>
                </table>

                <!-- Section Stock -->
                <h2>Situation de Stock</h2>
                <table> 
                    <tr>
                        <th>Médicaments en stock Moins que le stock minimum</th>
                        <td>{data['Stock_situation']['medicaments_stock_inferieur_min']}</td>
                    </tr>
                    <tr>
                        <th>Médicaments en Stock Positif</th>
                        <td>{data['Stock_situation']['medicaments_stock_positif']}</td>
                    </tr> 
                    <tr>
                        <th>Nombre de médicaments proches de la date d'expiration</th>
                        <td>{data['Stock_situation']['medicaments_stock_positif']}</td>
                    </tr> 
                    
                </table>

                <!-- Section Crédit -->
                <h2>Situation des commandes aujourd'hui</h2>
                <table>
                    <tr>
                        <th>Nombre de commandes passées aujourd'hui</th>
                        <td>{data['commande_situation']['commend_passer']} </td>
                    </tr> 
                    <tr>
                        <th>Nombre de commandes reçus aujourd'hui</th>
                        <td>{data['commande_situation']['commandes_recues']} </td>
                    </tr> 
                    <tr>
                        <th>Commandes en Attente</th>
                        <td>{data['commande_situation']['commandes_en_attente']}</td>
                    </tr>
                </table>

                <!-- Section Performance des Salariés -->
                <h2>Performance des Salariés</h2>
                <table>
                    <tr>
                        <th>ID Salarié</th>
                        <th>Total des Commandes</th>
                        <th>Commandes Reçues</th>
                        <th>Commandes en Attente</th>
                        <th>Total des Paiements</th>
                        <th>Total des Retours</th>
                    </tr>
        """
        # Ajout des lignes pour chaque salarié
        for salarie in data["Performance_salarie"]["total_operations_par_salarie"]:
            html_content += f"""
                    <tr>
                        <td>{salarie['id_salarie']}</td>
                        <td>{salarie['total_commandes']}</td>
                        <td>{salarie['commandes_recues']}</td>
                        <td>{salarie['commandes_en_attente']}</td>
                        <td>{salarie['total_paiements']}</td>
                        <td>{salarie['total_retours']}</td>
                    </tr>
            """

        html_content += """
                </table>
            </div>
        </body>
        </html>
        """

        return html_content
    
