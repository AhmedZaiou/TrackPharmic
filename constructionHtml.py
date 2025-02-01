import json
import matplotlib.pyplot as plt
import io
import base64

# Exemple de données JSON
data_json = {
    "Achat statistique": {
        "total_achats": 0,
        "quantite_totale": None,
        "montant_total_depense": None,
        "montant_total_gagne": None
    },
    "Client statistique": {
        "total_ventes": 0,
        "total_vente_jour": 0,
        "quantite_vendue_jour": 0,
        "total_achat_jour": 0,
        "total_profit_jour": 0,
        "total_clients": 1,
        "total_max_credit": 500.0,
        "total_credit_actuel": 100.0
    },
    "Commande statistique": {
        "statistique general": {
            "date": "29/01/2025",
            "total_commandes": 1,
            "commandes_recues": 1,
            "commandes_en_attente": 0
        },
        "statistique par salarie": [
            {"salarie": "user prenom", "statistique": {"salarie": 1, "date": "29/01/2025", "total_commandes": 1, "commandes_recues": 1, "commandes_en_attente": 0}},
            {"salarie": "Zaiou Ahmed", "statistique": {"salarie": 2, "date": "29/01/2025", "total_commandes": 0, "commandes_recues": 0, "commandes_en_attente": 0}}
        ]
    },
    "Credit statistique": {
        "total_paye": 0,
        "total_restant": 340.0,
        "nb_credits_clotures": 0,
        "montant_moyen": 0,
        "paiements_du_jour": []
    },
    "Echange statistique": {
        "total_journee": 0,
        "nombre_echanges": 0,
        "echanges_par_salarie": []
    },
    "Medicament statistique": {
        "total_medicaments": 2,
        "medicaments_en_rupture": 2,
        "medicaments_avec_stock": 0,
        "total_stock": 0
    },
    "Paiment statistique": {
        "total_paiements": 0.0,
        "total_paiements_count": 0,
        "paiements_salaries": [],
        "paiements_clients": []
    },
    "Retour statistique": {
        "total_retours": 0.0,
        "total_retours_count": 0,
        "retours_salaries": [],
        "retours_medicaments": []
    },
    "Stock statistique": {
        "total_achat": None,
        "total_vente": None,
        "total_quantite": None,
        "quantites_minimales_non_respectees": 0,
        "quantites_maximales_depassees": 0,
        "medicaments_proches_expiration": 0,
        "stocks": []
    },
    "Vente statistique": {
        "total_ventes_jour": 0,
        "total_vente_jour": 0,
        "quantite_vendue_jour": 0,
        "total_achat_jour": 0,
        "total_profit_jour": 0
    }
}

# Fonction pour générer le HTML
def generate_html(data):
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
        <p>Voici un résumé des performances :</p>
    """

    # Ajout des statistiques
    for category, stats in data.items():
        html_content += f"<h3>📌 {category} :</h3>"
        html_content += "<table>"
        for key, value in stats.items():
            html_content += f"<tr><th>{key}</th><td>{value if value is not None else 'Non spécifié'}</td></tr>"
        html_content += "</table>"

    # Création d'un graphique pour les ventes
    categories = ["Total Vendu", "Total Paiement", "Total Crédits", "Total Échanges"]
    valeurs = [1700, 240, 340, 500]  # Utilisation des données fixes pour l'exemple

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

    # Ajout du graphique au HTML
    html_content += f"<h3>📈 Graphique des ventes :</h3>"
    html_content += f"<img src='data:image/png;base64,{img_base64}' alt='Graphique des ventes' style='width:100%; max-width:600px;'>"

    html_content += """
        <p>Cordialement,<br>Votre équipe</p>
    </body>
    </html>
    """
    return html_content

# Générer le contenu HTML à partir du JSON
html_output = generate_html(data_json)

# Sauvegarder le HTML dans un fichier
with open("rapport_journalier.html", "w") as file:
    file.write(html_output)

print("✅ Le rapport HTML a été généré avec succès.")
