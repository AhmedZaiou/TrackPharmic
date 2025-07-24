import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os


class Payment:
    @staticmethod
    def __init__(dataset):
        dataset = dataset

    @staticmethod
    def create_table_payment(conn):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Payment (
                id_payment INTEGER PRIMARY KEY AUTO_INCREMENT,
                id_client INTEGER,
                numero_facture VARCHAR(50),
                montant_paye REAL,
                date_paiement DATETIME NOT NULL,
                id_salarie INTEGER
            );
        """
        )
        conn.commit()

    @staticmethod
    def ajouter_payment(
        conn, id_client, numero_facture, montant_paye, date_paiement, id_salarie
    ):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            INSERT INTO Payment (id_client, numero_facture, montant_paye, date_paiement, id_salarie)
            VALUES (%s, %s, %s, %s, %s)
        """,
            (id_client, numero_facture, montant_paye, date_paiement, id_salarie),
        )
        conn.commit()

    @staticmethod
    def extraire_payment_with_id_client(conn, id_client):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Payment WHERE id_client = %s", (id_client,))
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    @staticmethod
    def extraire_paiements_par_numero_facture(conn, numero_facture):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Payment WHERE numero_facture = %s", (numero_facture,)
        )
        rows = cursor.fetchall()

        return [dict(row) for row in rows] if rows else []

    @staticmethod
    def get_total_paiement(conn):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""SELECT SUM(montant_paye) as totalPaiement FROM Payment""")
        result = cursor.fetchone()

        return result[0] if result else 0

    @staticmethod
    def get_total_paiement_salarie(conn, salarie):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """SELECT SUM(montant_paye) as totalPaiement FROM Payment WHERE id_salarie = %s""",
            (salarie,),
        )
        result = cursor.fetchone()

        return result[0] if result else 0

    @staticmethod
    def cloture_journee(conn):
        # Connexion à la base de données

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Obtenir la date actuelle au format YYYY-MM-DD
        today = datetime.today().strftime("%Y-%m-%d")
        print(today)

        # Total des paiements effectués aujourd'hui
        cursor.execute(
            """
            SELECT SUM(montant_paye) as total_paiements
            FROM Payment
            WHERE DATE(date_paiement) = %s
        """,
            (today,),
        )
        total_paiements = cursor.fetchone()
        total_paiements = total_paiements["total_paiements"]

        # Total des paiements effectués aujourd'hui par salarié
        cursor.execute(
            """
            SELECT id_salarie, SUM(montant_paye) as total_paiements_salarie
            FROM Payment
            WHERE DATE(date_paiement) = %s
            GROUP BY id_salarie
        """,
            (today,),
        )
        paiements_salaries = cursor.fetchall()

        # Nombre total de paiements effectués aujourd'hui
        cursor.execute(
            """
            SELECT COUNT(id_payment) as total_paiements_count
            FROM Payment
            WHERE DATE(date_paiement) = %s
        """,
            (today,),
        )
        total_paiements_count = cursor.fetchone()
        total_paiements_count = total_paiements_count["total_paiements_count"]

        # Total des paiements effectués aujourd'hui par client
        cursor.execute(
            """
            SELECT id_client, SUM(montant_paye) as total_paiements_client
            FROM Payment
            WHERE DATE(date_paiement) = %s
            GROUP BY id_client
        """,
            (today,),
        )
        paiements_clients = cursor.fetchall()

        # Clôture de la connexion

        # Préparer les résultats sous forme de dictionnaire
        statistiques = {
            "Total des paiements effectués aujourd'hui en Dhs": total_paiements
            if total_paiements
            else 0.0,
            "Nombre total de paiements effectués aujourd'hui": total_paiements_count
            if total_paiements_count
            else 0,
            "Total des paiements effectués aujourd'hui par salarié": paiements_salaries,
            "Total des paiements effectués aujourd'hui par client": paiements_clients,
        }

        return statistiques

    @staticmethod
    def evolution_par_jour_moiis_courant(conn):
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_debut_annee = f"{datetime.now().year}-{datetime.now().month}-01"

        cursor.execute(
            """
            SELECT DATE(date_paiement) as date_paiements, SUM(montant_paye) as total_restant
            FROM Payment
            WHERE DATE(date_paiement) >= %s
            GROUP BY DATE(date_paiement)
            ORDER BY DATE(date_paiement) ASC
            """,
            (date_debut_annee,),
        )

        evolution_credit = cursor.fetchall()

        return {
            row["date_paiements"].strftime("%Y-%m-%d"): row["total_restant"]
            for row in evolution_credit
        }

    @staticmethod
    def evolution_par_mois(conn):
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_debut_annee = f"{datetime.now().year}-01-01"
        query = """
                SELECT 
                    DATE_FORMAT(date_paiement, '%%Y-%%m') AS mois_paiement, 
                    SUM(montant_paye) AS total_restant
                FROM 
                    Payment
                WHERE 
                    date_paiement >= %s
                GROUP BY 
                    mois_paiement
                ORDER BY 
                    mois_paiement ASC;
                """

        cursor.execute(
            query,
            (date_debut_annee,),
        )

        evolution_credit = cursor.fetchall()

        return {row["mois_paiement"]: row["total_restant"] for row in evolution_credit}
