import mysql.connector
from Frontend.utils.utils import *
from datetime import datetime

class Echanges:
    @staticmethod
    def create_table_echanges():
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Echanges (
                id_echange INTEGER PRIMARY KEY AUTO_INCREMENT,
                id_pharmacie INTEGER,
                id_facture INTEGER,
                date_echange DATE NOT NULL,
                total_facture REAL,
                sens VARCHAR(10),
                id_salarie INTEGER
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_echange(id_pharmacie, id_facture, date_echange, total_facture, sens, id_salarie):
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO Echanges (id_pharmacie, id_facture, date_echange, total_facture, sens, id_salarie)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_pharmacie, id_facture, date_echange, total_facture, sens, id_salarie))
        conn.commit()
        conn.close()

    @staticmethod
    def get_total_echanges():
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT SUM(total_facture) as totalEchanges FROM Echanges")
        result = cursor.fetchone()
        conn.close()
        return result.get("totalEchanges", 0)

    @staticmethod
    def cloture_journee():
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(dictionary=True)
        date_aujourdhui = datetime.now().strftime('%Y-%m-%d')

        # Calcul du total des échanges de la journée
        cursor.execute("""
            SELECT SUM(total_facture) as total_journee
            FROM Echanges
            WHERE DATE(date_echange) = %s
        """, (date_aujourdhui,))
        total_journee = cursor.fetchone().get("total_journee", 0)

        # Nombre d'échanges réalisés aujourd'hui
        cursor.execute("""
            SELECT COUNT(id_echange) as nombre_echanges
            FROM Echanges
            WHERE DATE(date_echange) = %s
        """, (date_aujourdhui,))
        nombre_echanges = cursor.fetchone().get("nombre_echanges", 0)

        # Total des échanges par salarié
        cursor.execute("""
            SELECT id_salarie, SUM(total_facture) as total_par_salarie
            FROM Echanges
            WHERE DATE(date_echange) = %s
            GROUP BY id_salarie
        """, (date_aujourdhui,))
        echanges_par_salarie = cursor.fetchall()

        conn.close()

        return {
            "Total des échanges de la journée": total_journee,
            "Nombre d'échanges réalisés aujourd'hui": nombre_echanges,
            "Total des échanges par salarié": [
                {"id_salarie": e["id_salarie"], "Total des échanges du salarié": e["total_par_salarie"]}
                for e in echanges_par_salarie
            ]
        }
