import pymysql
from Frontend.utils.utils import *
from datetime import datetime
from Backend.Dataset.pharmacie import Pharmacies


class Echanges:
    @staticmethod
    def create_table_echanges():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Echanges (
                id_echange INTEGER PRIMARY KEY AUTO_INCREMENT,
                id_pharmacie INTEGER,
                id_facture INTEGER,
                date_echange DATE NOT NULL,
                total_facture REAL,
                sens VARCHAR(10),
                id_salarie INTEGER
            );
        """
        )
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_echange(
        id_pharmacie, id_facture, date_echange, total_facture, sens, id_salarie
    ):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            INSERT INTO Echanges (id_pharmacie, id_facture, date_echange, total_facture, sens, id_salarie)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (id_pharmacie, id_facture, date_echange, total_facture, sens, id_salarie),
        )
        conn.commit()
        conn.close()
        Pharmacies.modifier_pharmacie_echange(
        id_pharmacie, total_facture, sens
    )



    @staticmethod
    def extraire_tous_echanges_pharma(id_pharma):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Echanges  WHERE id_pharmacie = %s;",
            (id_pharma,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    

    @staticmethod
    def get_total_echanges():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT SUM(total_facture) as totalEchanges FROM Echanges")
        result = cursor.fetchone()
        conn.close()
        return result.get("totalEchanges", 0)

    @staticmethod
    def cloture_journee():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        date_aujourdhui = datetime.now().strftime("%Y-%m-%d")

        # Calcul du total des échanges de la journée
        cursor.execute(
            """
            SELECT SUM(total_facture) as total_journee
            FROM Echanges
            WHERE DATE(date_echange) = %s and sens = 1
        """,
            (date_aujourdhui,),
        )
        total_journee_envoyer = cursor.fetchone().get("total_journee", 0)

        cursor.execute(
            """
            SELECT SUM(total_facture) as total_journee
            FROM Echanges
            WHERE DATE(date_echange) = %s and sens = 0
        """,
            (date_aujourdhui,),
        )
        total_journee_recus = cursor.fetchone().get("total_journee", 0)

        # Nombre d'échanges réalisés aujourd'hui
        cursor.execute(
            """
            SELECT COUNT(id_echange) as nombre_echanges
            FROM Echanges
            WHERE DATE(date_echange) = %s
        """,
            (date_aujourdhui,),
        )
        nombre_echanges = cursor.fetchone().get("nombre_echanges", 0)

        # Total des échanges par salarié
        cursor.execute(
            """
            SELECT id_salarie, SUM(total_facture) as total_par_salarie
            FROM Echanges
            WHERE DATE(date_echange) = %s
            GROUP BY id_salarie
        """,
            (date_aujourdhui,),
        )
        echanges_par_salarie = cursor.fetchall()

        conn.close()

        return {
            "Total des échanges de la journée envoyer": total_journee_envoyer ,
            "Total des échanges de la journée recus": total_journee_recus ,
            "Nombre d'échanges réalisés aujourd'hui": nombre_echanges,
            "Total des échanges par salarié": [
                {
                    "id_salarie": e["id_salarie"],
                    "Total des échanges du salarié": e["total_par_salarie"],
                }
                for e in echanges_par_salarie
            ],
        }
    
    @staticmethod
    def evolution_par_jour_moiis_courant():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_debut_annee = f"{datetime.now().year}-{datetime.now().month}-01"

        cursor.execute(
            """
            SELECT DATE(date_echange) as date_echange, SUM(total_facture) as total_facture
            FROM Echanges
            WHERE DATE(date_echange) >= %s and sens = 1
            GROUP BY DATE(date_echange)
            ORDER BY DATE(date_echange) ASC
            """,
            (date_debut_annee,),
        )

        evolution_credit = cursor.fetchall() 

        sens1 = {row["date_echange"].strftime("%Y-%m-%d"): row["total_facture"] for row in evolution_credit}
        cursor.execute(
            """
            SELECT DATE(date_echange) as date_echange, SUM(total_facture) as total_facture
            FROM Echanges
            WHERE DATE(date_echange) >= %s and sens = 0
            GROUP BY DATE(date_echange)
            ORDER BY DATE(date_echange) ASC
            """,
            (date_debut_annee,),
        )

        evolution_credit = cursor.fetchall()
        conn.close()

        sens0 = {row["date_echange"].strftime("%Y-%m-%d"): row["total_facture"] for row in evolution_credit}
        return { "Echange_envoyer": sens1, "Echange_recu": sens0}

    @staticmethod
    def evolution_par_mois():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_debut_annee = f"{datetime.now().year}-01-01"
        query = """
                SELECT 
                    DATE_FORMAT(date_echange, '%%Y-%%m') AS mois_paiement, 
                    SUM(total_facture) AS total_restant
                FROM 
                    Echanges
                WHERE 
                    date_echange >= %s and sens = 1
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

        sens1 =  {row["mois_paiement"]: row["total_restant"] for row in evolution_credit}
        query = """
                SELECT 
                    DATE_FORMAT(date_echange, '%%Y-%%m') AS mois_paiement, 
                    SUM(total_facture) AS total_restant
                FROM 
                    Echanges
                WHERE 
                    date_echange >= %s and sens = 0
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

        sens0 =  {row["mois_paiement"]: row["total_restant"] for row in evolution_credit}
        return { "Echange_envoyer": sens1, "Echange_recu": sens0}
    




    




    

