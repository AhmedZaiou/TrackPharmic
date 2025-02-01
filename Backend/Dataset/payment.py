 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Payment:
    @staticmethod
    def __init__(  dataset):
        dataset = dataset
        

    @staticmethod
    def create_table_payment():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Payment (
                id_payment INTEGER PRIMARY KEY AUTOINCREMENT,
                id_client INTEGER,
                numero_facture VARCHAR(50),
                montant_paye REAL,
                date_paiement DATE NOT NULL,
                id_salarie INTEGER,
                FOREIGN KEY (id_client) REFERENCES Clients (id_client),
                FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_payment(  id_client, numero_facture, montant_paye, date_paiement, id_salarie):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Payment (id_client, numero_facture, montant_paye, date_paiement, id_salarie)
            VALUES (?, ?, ?, ?, ?)
        """, (id_client, numero_facture, montant_paye, date_paiement, id_salarie))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_payment_with_id_client(  id_client):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Payment WHERE id_client = ?", (id_client,))
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 
    
    @staticmethod
    def get_total_paiement():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(montant_paye) as totalPaiement FROM Payment''')
        result = cursor.fetchone()
         
        conn.close()
        return result[0] if result else 0
    

    @staticmethod
    def get_total_paiement_salarie(salarie):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(montant_paye) as totalPaiement FROM Payment WHERE id_salarie = ?''', (salarie,))
        result = cursor.fetchone() 
        conn.close()
        return result[0] if result else 0
    
    @staticmethod
    def cloture_journee():
        # Connexion à la base de données
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()

        # Obtenir la date actuelle au format YYYY-MM-DD
        today = datetime.today().strftime('%Y-%m-%d')

        # Total des paiements effectués aujourd'hui
        cursor.execute("""
            SELECT SUM(montant_paye) as total_paiements
            FROM Payment
            WHERE date_paiement = ?
        """, (today,))
        total_paiements = cursor.fetchone()[0]

        # Total des paiements effectués aujourd'hui par salarié
        cursor.execute("""
            SELECT id_salarie, SUM(montant_paye) as total_paiements_salarie
            FROM Payment
            WHERE date_paiement = ?
            GROUP BY id_salarie
        """, (today,))
        paiements_salaries = cursor.fetchall()

        # Nombre total de paiements effectués aujourd'hui
        cursor.execute("""
            SELECT COUNT(id_payment) as total_paiements_count
            FROM Payment
            WHERE date_paiement = ?
        """, (today,))
        total_paiements_count = cursor.fetchone()[0]

        # Total des paiements effectués aujourd'hui par client
        cursor.execute("""
            SELECT id_client, SUM(montant_paye) as total_paiements_client
            FROM Payment
            WHERE date_paiement = ?
            GROUP BY id_client
        """, (today,))
        paiements_clients = cursor.fetchall()

        # Clôture de la connexion
        conn.close()

        # Préparer les résultats sous forme de dictionnaire
        statistiques = {
            "Total des paiements effectués aujourd'hui en Dhs": total_paiements if total_paiements else 0.0,
            "Nombre total de paiements effectués aujourd'hui": total_paiements_count if total_paiements_count else 0,
            "Total des paiements effectués aujourd'hui par salarié": [{"id_salarie": row[0], "total_paiements_salarie": row[1]} for row in paiements_salaries],
            "Total des paiements effectués aujourd'hui par client": [{"id_client": row[0], "total_paiements_client": row[1]} for row in paiements_clients]
        }

        return statistiques