import pymysql
from Frontend.utils.utils import *
from datetime import datetime


class Credit:
    @staticmethod
    def create_table_credit():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Credit (
                id_credit INTEGER PRIMARY KEY AUTO_INCREMENT,
                id_client INTEGER,
                numero_facture VARCHAR(50),
                montant_paye DECIMAL(10,2),
                reste_a_payer DECIMAL(10,2),
                date_dernier_paiement DATETIME,
                statut VARCHAR(50),
                id_salarie INTEGER
            );
        """
        )
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_credit(
        id_client,
        numero_facture,
        montant_paye,
        reste_a_payer,
        date_dernier_paiement,
        statut,
        id_salarie,
    ):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            INSERT INTO Credit (id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            (
                id_client,
                numero_facture,
                montant_paye,
                reste_a_payer,
                date_dernier_paiement,
                statut,
                id_salarie,
            ),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_credit(id_credit):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("DELETE FROM Credit WHERE id_credit = %s", (id_credit,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_credit(
        id_credit,
        id_client,
        numero_facture,
        montant_paye,
        reste_a_payer,
        date_dernier_paiement,
        statut,
        id_salarie,
    ):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            UPDATE Credit
            SET id_client = %s, numero_facture = %s, montant_paye = %s, reste_a_payer = %s, date_dernier_paiement = %s, statut = %s, id_salarie = %s
            WHERE id_credit = %s
        """,
            (
                id_client,
                numero_facture,
                montant_paye,
                reste_a_payer,
                date_dernier_paiement,
                statut,
                id_salarie,
                id_credit,
            ),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_credit(id_credit):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Credit WHERE id_credit = %s", (id_credit,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_tous_credits():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Credit")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_credit_with_id_client(id_client):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Credit WHERE id_client = %s", (id_client,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_total_credits():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT SUM(reste_a_payer) as totalCredits FROM Credit")
        result = cursor.fetchone()
        conn.close()
        return result["totalCredits"] if result["totalCredits"] else 0

    @staticmethod
    def get_total_credits_salarie(salarie):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT SUM(reste_a_payer) as totalCredits FROM Credit WHERE id_salarie = %s",
            (salarie,),
        )
        result = cursor.fetchone()
        conn.close()
        return result["totalCredits"] if result["totalCredits"] else 0

    @staticmethod
    def cloture_journee():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_aujourdhui = datetime.now().strftime("%Y-%m-%d")

        cursor.execute(
            """
            SELECT SUM(reste_a_payer) as total_restant 
            FROM Credit
            WHERE DATE(date_dernier_paiement) = %s
        """,
            (date_aujourdhui,),
        )

        total_restant = cursor.fetchone()
        total_restant = (
            total_restant["total_restant"] if total_restant["total_restant"] else 0
        )

        conn.close()
        return {"Total restant à payer aujourd'hui": total_restant}
    

    @staticmethod
    def evolution_par_jour_moiis_courant():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_debut_annee = f"{datetime.now().year}-{datetime.now().month}-01"

        cursor.execute(
            """
            SELECT DATE(date_dernier_paiement) as date_paiement, SUM(reste_a_payer) as total_restant
            FROM Credit
            WHERE DATE(date_dernier_paiement) >= %s
            GROUP BY DATE(date_dernier_paiement)
            ORDER BY DATE(date_dernier_paiement) ASC
            """,
            (date_debut_annee,),
        )

        evolution_credit = cursor.fetchall()
        conn.close()

        return {row["date_paiement"].strftime("%Y-%m-%d"): row["total_restant"] for row in evolution_credit}

    @staticmethod
    def evolution_par_mois():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_debut_annee = f"{datetime.now().year}-01-01"
        query = """
                SELECT 
                    DATE_FORMAT(date_dernier_paiement, '%%Y-%%m') AS mois_paiement, 
                    SUM(reste_a_payer) AS total_restant
                FROM 
                    Credit
                WHERE 
                    date_dernier_paiement >= %s
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
        conn.close()

        return {row["mois_paiement"]: row["total_restant"] for row in evolution_credit}
    




    




    
