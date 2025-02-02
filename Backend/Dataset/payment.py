import mysql.connector
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Payment:
    @staticmethod
    def __init__(dataset):
        dataset = dataset

    @staticmethod
    def create_table_payment():
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Payment (
                id_payment INTEGER PRIMARY KEY AUTO_INCREMENT,
                id_client INTEGER,
                numero_facture VARCHAR(50),
                montant_paye REAL,
                date_paiement DATETIME NOT NULL,
                id_salarie INTEGER
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_payment(id_client, numero_facture, montant_paye, date_paiement, id_salarie):
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO Payment (id_client, numero_facture, montant_paye, date_paiement, id_salarie)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_client, numero_facture, montant_paye, date_paiement, id_salarie))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_payment_with_id_client(id_client):
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Payment WHERE id_client = %s", (id_client,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_total_paiement():
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''SELECT SUM(montant_paye) as totalPaiement FROM Payment''')
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    @staticmethod
    def get_total_paiement_salarie(salarie):
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''SELECT SUM(montant_paye) as totalPaiement FROM Payment WHERE id_salarie = %s''', (salarie,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    @staticmethod
    def cloture_journee():
        # Connexion à la base de données
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(dictionary=True)

        # Obtenir la date actuelle au format YYYY-MM-DD
        today = datetime.today().strftime('%Y-%m-%d')
        print(today)

        # Total des paiements effectués aujourd'hui
        cursor.execute("""
            SELECT SUM(montant_paye) as total_paiements
            FROM Payment
            WHERE DATE(date_paiement) = %s
        """, (today,))
        total_paiements = cursor.fetchone()
        total_paiements = total_paiements['total_paiements']

        # Total des paiements effectués aujourd'hui par salarié
        cursor.execute("""
            SELECT id_salarie, SUM(montant_paye) as total_paiements_salarie
            FROM Payment
            WHERE DATE(date_paiement) = %s
            GROUP BY id_salarie
        """, (today,))
        paiements_salaries = cursor.fetchall()
        

        # Nombre total de paiements effectués aujourd'hui
        cursor.execute("""
            SELECT COUNT(id_payment) as total_paiements_count
            FROM Payment
            WHERE DATE(date_paiement) = %s
        """, (today,))
        total_paiements_count = cursor.fetchone()
        total_paiements_count = total_paiements_count['total_paiements_count']

        # Total des paiements effectués aujourd'hui par client
        cursor.execute("""
            SELECT id_client, SUM(montant_paye) as total_paiements_client
            FROM Payment
            WHERE DATE(date_paiement) = %s
            GROUP BY id_client
        """, (today,))
        paiements_clients = cursor.fetchall()

        # Clôture de la connexion
        conn.close()

        # Préparer les résultats sous forme de dictionnaire
        statistiques = {
            "Total des paiements effectués aujourd'hui en Dhs": total_paiements if total_paiements else 0.0,
            "Nombre total de paiements effectués aujourd'hui": total_paiements_count if total_paiements_count else 0,
            "Total des paiements effectués aujourd'hui par salarié":  paiements_salaries,
            "Total des paiements effectués aujourd'hui par client":  paiements_clients
        }

        return statistiques
