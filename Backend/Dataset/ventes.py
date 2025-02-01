 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta, date
import os
import json
import pandas as pd
import matplotlib.pyplot as plt


class Ventes:
    @staticmethod
    def __init__():
        dataset = dataset

    @staticmethod
    def create_table_ventes():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ventes (
                id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
                id_medicament INTEGER NOT NULL,
                id_commande_entre INTEGER,
                prix_achat REAL,
                prix_vente REAL,
                date_vente DATE NOT NULL,
                quantite_vendue INTEGER DEFAULT 0,
                total_facture REAL,
                id_client INTEGER,
                numero_facture VARCHAR(50),
                id_salarie INTEGER,
                id_stock_item INTEGER,
                FOREIGN KEY (id_medicament) REFERENCES Medicament (id_medicament),
                FOREIGN KEY (id_commande_entre) REFERENCES Commandes (id_commande),
                FOREIGN KEY (id_client) REFERENCES Clients (id_client),
                FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie),
                FOREIGN KEY (id_stock_item) REFERENCES Stock (id_stock)
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_vente(id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture, id_client, numero_facture, id_salarie, id_stock_item):
        Ventes.create_table_ventes()
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Ventes (id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture, id_client, numero_facture, id_salarie, id_stock_item)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture, id_client, numero_facture, id_salarie, id_stock_item))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_vente(  id_vente):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ventes WHERE id_vente = ?", (id_vente,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_vente(  id_vente, id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture, id_client, numero_facture, id_salarie, id_stock_item):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Ventes
            SET id_medicament = ?, id_commande_entre = ?, prix_achat = ?, prix_vente = ?, date_vente = ?, quantite_vendue = ?, total_facture = ?, id_client = ?, numero_facture = ?, id_salarie = ?, id_stock_item = ?
            WHERE id_vente = ?
        """, (id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture, id_client, numero_facture, id_salarie, id_stock_item, id_vente))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_vente(  id_vente):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ventes WHERE id_vente = ?", (id_vente,))
        row = cursor.fetchone()
        conn.close()
        return   dict(row)   if row else None

    @staticmethod
    def extraire_tous_ventes():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ventes")
        rows = cursor.fetchall()
        conn.close()
        return   [dict(row) for row in rows]  
    


    @staticmethod
    def get_transactions_jour(salarie):
        # Connect to the database
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT id_vente FROM Ventes WHERE date_vente = ? AND id_salarie = ?''', (datetime.now().date(), salarie))
        result = cursor.fetchall()
        conn.close()
        return [dict(row) for row in result]
    
    @staticmethod
    def get_total_vendu_salarie(salarie):
        # Connect to the database
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(total_facture) as totalVendu FROM Ventes WHERE id_salarie = ?''', (salarie,))
        result = cursor.fetchone()
        conn.close()
        return result['totalVendu']
    

    @staticmethod
    def get_statistique():
        # Connect to the database
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Ventes''')
        result = cursor.fetchall()
        conn.close()
        return [dict(row) for row in result]


    @staticmethod
    def cloture_journee(date_jour=None):
        if date_jour is None:
            date_jour = datetime.now().strftime("%Y-%m-%d")  # Par défaut, utilise la date du jour

        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()

        # Nombre total de ventes effectuées aujourd'hui
        cursor.execute("SELECT COUNT(*) FROM Ventes WHERE date_vente = ?", (date_jour,))
        total_ventes_jour = cursor.fetchone()[0]

        # Montant total des ventes effectuées aujourd'hui
        cursor.execute("SELECT SUM(total_facture) FROM Ventes WHERE date_vente = ?", (date_jour,))
        total_vente_jour = cursor.fetchone()[0] or 0

        # Quantité totale vendue aujourd'hui
        cursor.execute("SELECT SUM(quantite_vendue) FROM Ventes WHERE date_vente = ?", (date_jour,))
        quantite_vendue_jour = cursor.fetchone()[0] or 0

        # Total des achats effectués aujourd'hui
        cursor.execute("SELECT SUM(prix_achat * quantite_vendue) FROM Ventes WHERE date_vente = ?", (date_jour,))
        total_achat_jour = cursor.fetchone()[0] or 0

        # Total des profits réalisés aujourd'hui
        cursor.execute("SELECT SUM((prix_vente - prix_achat) * quantite_vendue) FROM Ventes WHERE date_vente = ?", (date_jour,))
        total_profit_jour = cursor.fetchone()[0] or 0

        # Résumé des statistiques pour la journée
        statistiques_ventes_jour = {
            "Nombre total de ventes effectuées aujourd'hui": total_ventes_jour,
            "Montant total des ventes effectuées aujourd'hui": total_vente_jour,
            "Quantité totale vendue aujourd'hui": quantite_vendue_jour,
            "Total des achats effectués aujourd'hui": total_achat_jour,
            "Total des profits réalisés aujourd'hui": total_profit_jour
        }

        conn.close()
        return statistiques_ventes_jour
    



    def get_evolution():
        d_now=datetime.now().date()
        res = []

        # Obtenir la date du début de l'année
        satrt_year = date(d_now.year, 1, 1)

        # Parcourir les dates de début de l'année jusqu'à aujourd'hui
        date_actuelle = satrt_year
        while date_actuelle <= d_now:
            dy=Ventes.cloture_journee(date_actuelle)
            dy['date'] = date_actuelle
            res.append(dy)
            date_actuelle += timedelta(days=1)
        df = pd.DataFrame(res)

        # Définition des variables à tracer
        variables = ["Nombre total de ventes effectuées aujourd'hui", "Montant total des ventes effectuées aujourd'hui", 
                    "Quantité totale vendue aujourd'hui", "Total des achats effectués aujourd'hui", 
                    "Total des profits réalisés aujourd'hui"]

        # Création du plot 
        fig, ax = plt.subplots()
        # Plot de chaque variable
        for var in variables:
            ax.plot(df['date'], df[var], label=var)

        # Personnalisation du graphique
        ax.set_xlabel('Date')
        ax.set_ylabel('Valeur')
        ax.set_title('Évolution des variables en fonction des dates') 
        ax.legend()
        return fig