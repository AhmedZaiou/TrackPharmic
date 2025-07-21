import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json


class Retour:
    @staticmethod
    def __init__():
        dataset = dataset

    @staticmethod
    def create_table_retours(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Retours (
                id_retour INTEGER PRIMARY KEY AUTO_INCREMENT,
                id_medicament INTEGER NOT NULL, 
                prix REAL, 
                date_retour DATETIME NOT NULL,
                quantite_retour INTEGER DEFAULT 0,  
                numero_facture VARCHAR(50),
                id_salarie INTEGER 
            );
        """
        )
        conn.commit()
        

    @staticmethod
    def ajouter_retour(conn,
        id_medicament, prix, date_retour, quantite_retour, numero_facture, id_salarie
    ):
        Retour.create_table_retours(conn)
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            INSERT INTO Retours (id_medicament, prix, date_retour, quantite_retour, numero_facture, id_salarie)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (
                id_medicament,
                prix,
                date_retour,
                quantite_retour,
                numero_facture,
                id_salarie,
            ),
        )
        conn.commit()
        

    @staticmethod
    def extraire_tous_retours(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Retours")
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def extraire_tous_table_retours(conn):
       
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""SELECT 
                            r.id_retour, 
                            r.id_medicament, 
                            m.Nom AS nom_medicament,
                            r.prix, 
                            r.date_retour, 
                            r.quantite_retour, 
                            r.numero_facture, 
                            r.id_salarie
                        FROM 
                            Retours r
                        JOIN 
                            Medicament m ON r.id_medicament = m.ID_Medicament
                        WHERE 
                            1
                        LIMIT 30;""")
        rows = cursor.fetchall()
        
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def extraire_retours_par_numero_facture(conn,numero_facture):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Retours WHERE numero_facture = %s", (numero_facture,))
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows] if rows else []
    
    @staticmethod
    def cloture_journee(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Get today's date in YYYY-MM-DD format
        today = datetime.today().strftime("%Y-%m-%d")

        # Total returns made today (total price of returns)
        cursor.execute(
            """
            SELECT SUM(prix * quantite_retour) AS total_retours
            FROM Retours
            WHERE Date(date_retour) = %s
        """,
            (today,),
        )
        total_retours = cursor.fetchone()
        total_retours = total_retours["total_retours"]

        # Total returns made today by employee
        cursor.execute(
            """
            SELECT id_salarie, SUM(prix * quantite_retour) AS total_retours_salarie
            FROM Retours
            WHERE Date(date_retour) = %s
            GROUP BY id_salarie
        """,
            (today,),
        )
        retours_salaries = cursor.fetchall()

        # Total number of returns made today
        cursor.execute(
            """
            SELECT COUNT(id_retour) AS total_retours_count
            FROM Retours
            WHERE Date(date_retour) = %s
        """,
            (today,),
        )
        total_retours_count = cursor.fetchone()
        total_retours_count = total_retours_count["total_retours_count"]

        # Total returns made today by medication
        cursor.execute(
            """
            SELECT id_medicament, SUM(prix * quantite_retour) AS total_retours_medicament
            FROM Retours
            WHERE Date(date_retour) = %s
            GROUP BY id_medicament
        """,
            (today,),
        )
        retours_medicaments = cursor.fetchall()

        # Close the connection
        

        # Prepare results as a dictionary
        statistiques = {
            "Total des retours effectués aujourdhui": total_retours
            if total_retours
            else 0.0,
            "Nombre total de retours effectués aujourdhui": total_retours_count
            if total_retours_count
            else 0,
            "Total des retours effectués aujourdhui par salarié": retours_salaries ,
            "Total des retours effectués aujourdhui par médicament en Dhs": retours_medicaments or 0,
        }

        return statistiques
    
 


    @staticmethod
    def evolution_par_jour_moiis_courant(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_debut_annee = f"{datetime.now().year}-{datetime.now().month}-01"

        cursor.execute(
            """
            SELECT DATE(date_retour) as date_paiements, SUM(quantite_retour * prix) as total_restant
            FROM Retours
            WHERE DATE(date_retour) >= %s
            GROUP BY DATE(date_retour)
            ORDER BY DATE(date_retour) ASC
            """,
            (date_debut_annee,),
        )

        evolution_credit = cursor.fetchall()
        

        return {row["date_paiements"].strftime("%Y-%m-%d"): row["total_restant"] for row in evolution_credit}

    @staticmethod
    def evolution_par_mois(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_debut_annee = f"{datetime.now().year}-01-01"
        query = """
                SELECT 
                    DATE_FORMAT(date_retour, '%%Y-%%m') AS mois_paiement, 
                    SUM(quantite_retour * prix) AS total_restant
                FROM 
                    Retours
                WHERE 
                    date_retour >= %s
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
    





