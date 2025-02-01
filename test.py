
import smtplib
import matplotlib.pyplot as plt
import io
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

 

# Informations de connexion Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "pharmacieapplication@gmail.com"  # Remplace par ton email
smtp_password = "adck kohd tuqu iomh"  # Utiliser un mot de passe d'application

# Définition de l'expéditeur et du destinataire
sender_email = smtp_user
receiver_email = "zaiou.ahm@gmail.com"

# Données pour le graphique
categories = ["Total Vendu", "Total Paiement", "Total Crédits", "Total Échanges"]
valeurs = [1700, 240, 340, 500]

# Création du graphique
fig, ax = plt.subplots(figsize=(5, 3))
ax.bar(categories, valeurs, color=["blue", "green", "red", "orange"])
ax.set_title("Statistiques des ventes (DHs)")
ax.set_ylabel("Montant (DHs)")

# Sauvegarde du graphique en mémoire (format base64)
img_buf = io.BytesIO()
plt.savefig(img_buf, format="png")
img_buf.seek(0)
img_base64 = base64.b64encode(img_buf.getvalue()).decode("utf-8")
plt.close()

# Contenu HTML avec tableau et graphique
html_content = f"""
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        h2 {{
            color: #2c3e50;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
        }}
        th {{
            background-color: #2c3e50;
            color: white;
        }}
    </style>
</head>
<body>
    <h2>📊 Rapport de la journée</h2>
    <p>Bonjour Ahmed, voici un résumé des performances :</p>

    <h3>📌 Statistiques des Achats :</h3>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Total achats</td><td>0</td></tr>
        <tr><td>Quantité totale</td><td>None</td></tr>
        <tr><td>Montant total dépensé</td><td>None</td></tr>
        <tr><td>Montant total gagné</td><td>None</td></tr>
    </table>

    <h3>📌 Statistiques des Clients :</h3>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Total ventes</td><td>0</td></tr>
        <tr><td>Total vente du jour</td><td>0</td></tr>
        <tr><td>Quantité vendue du jour</td><td>0</td></tr>
        <tr><td>Total achat du jour</td><td>0</td></tr>
        <tr><td>Total profit du jour</td><td>0</td></tr>
        <tr><td>Total clients</td><td>1</td></tr>
        <tr><td>Total crédit maximum</td><td>500.0</td></tr>
        <tr><td>Total crédit actuel</td><td>100.0</td></tr>
    </table>

    <h3>📌 Statistiques des Commandes :</h3>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Date</td><td>29/01/2025</td></tr>
        <tr><td>Total commandes</td><td>1</td></tr>
        <tr><td>Commandes reçues</td><td>1</td></tr>
        <tr><td>Commandes en attente</td><td>0</td></tr>
    </table>

    <h4>📌 Statistiques par salarié :</h4>
    <h5>Salarie : user prenom</h5>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Total commandes</td><td>1</td></tr>
        <tr><td>Commandes reçues</td><td>1</td></tr>
        <tr><td>Commandes en attente</td><td>0</td></tr>
    </table>

    <h5>Salarie : Zaiou Ahmed</h5>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Total commandes</td><td>0</td></tr>
        <tr><td>Commandes reçues</td><td>0</td></tr>
        <tr><td>Commandes en attente</td><td>0</td></tr>
    </table>

    <h3>📌 Statistiques des Crédits :</h3>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Total payé</td><td>0</td></tr>
        <tr><td>Total restant</td><td>340.0</td></tr>
        <tr><td>Nombre de crédits clôturés</td><td>0</td></tr>
        <tr><td>Montant moyen</td><td>0</td></tr>
    </table>

    <h3>📌 Statistiques des Échanges :</h3>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Total échangés du jour</td><td>0</td></tr>
        <tr><td>Nombre d'échanges</td><td>0</td></tr>
    </table>

    <h3>📌 Statistiques des Médicaments :</h3>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Total médicaments</td><td>2</td></tr>
        <tr><td>Médicaments en rupture</td><td>2</td></tr>
        <tr><td>Médicaments avec stock</td><td>0</td></tr>
        <tr><td>Total stock</td><td>0</td></tr>
    </table>

    <h3>📌 Statistiques des Paiements :</h3>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Total paiements</td><td>0.0</td></tr>
        <tr><td>Nombre de paiements</td><td>0</td></tr>
    </table>

    <h3>📌 Statistiques des Retours :</h3>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Total retours</td><td>0.0</td></tr>
        <tr><td>Nombre de retours</td><td>0</td></tr>
    </table>

    <h3>📌 Statistiques du Stock :</h3>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Total achat</td><td>None</td></tr>
        <tr><td>Total vente</td><td>None</td></tr>
        <tr><td>Total quantité</td><td>None</td></tr>
    </table>

    <h3>📌 Statistiques des Ventes :</h3>
    <table>
        <tr><th>Indicateur</th><th>Valeur</th></tr>
        <tr><td>Total ventes du jour</td><td>0</td></tr>
        <tr><td>Total vente du jour</td><td>0</td></tr>
        <tr><td>Quantité vendue du jour</td><td>0</td></tr>
        <tr><td>Total achat du jour</td><td>0</td></tr>
        <tr><td>Total profit du jour</td><td>0</td></tr>
    </table>

    <h3>📈 Graphique des ventes :</h3>
    <img src="data:image/png;base64,{img_base64}" alt="Graphique des ventes" style="width:100%; max-width:600px;">
    
    <p>Cordialement,<br>Ton équipe</p>
</body>
</html>
"""

# Création du message email en HTML
msg = MIMEMultipart()
msg['Subject'] = "📊 Rapport Journalier des Ventes"
msg['From'] = sender_email
msg['To'] = receiver_email

msg.attach(MIMEText(html_content, "html"))

# Envoi du mail via Gmail SMTP
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, [receiver_email], msg.as_string())
    print("✅ E-mail envoyé avec succès.")
except Exception as e:
    print(f"❌ Erreur lors de l'envoi de l'e-mail : {e}")