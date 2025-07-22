import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta, date
import os
import json
import pandas as pd
import matplotlib.pyplot as plt


class Ventes:
    @staticmethod
    def __init__(self):
        dataset = dataset

    @staticmethod
    def create_table_ventes(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Ventes (
                id_vente INT PRIMARY KEY AUTO_INCREMENT,
                id_medicament INT NOT NULL,
                id_commande_entre INT,
                prix_achat REAL,
                prix_vente REAL,
                date_vente DATETIME NOT NULL,
                quantite_vendue INT DEFAULT 0,
                total_facture REAL,
                id_client INT,
                numero_facture VARCHAR(50),
                id_salarie INT,
                id_stock_item INT
            );
        """
        )
        conn.commit()
        

    @staticmethod
    def ajouter_vente(conn,
        id_medicament,
        id_commande_entre,
        prix_achat,
        prix_vente,
        date_vente,
        quantite_vendue,
        total_facture,
        id_client,
        numero_facture,
        id_salarie,
        id_stock_item,
    ):
        Ventes.create_table_ventes(conn)
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            INSERT INTO Ventes (id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture, id_client, numero_facture, id_salarie, id_stock_item)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                id_medicament,
                id_commande_entre,
                prix_achat,
                prix_vente,
                date_vente,
                quantite_vendue,
                total_facture,
                id_client,
                numero_facture,
                id_salarie,
                id_stock_item,
            ),
        )
        conn.commit()
        

    @staticmethod
    def supprimer_vente(conn,id_vente):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("DELETE FROM Ventes WHERE id_vente = %s", (id_vente,))
        conn.commit()
        

    @staticmethod
    def modifier_vente(conn,
        id_vente,
        id_medicament,
        id_commande_entre,
        prix_achat,
        prix_vente,
        date_vente,
        quantite_vendue,
        total_facture,
        id_client,
        numero_facture,
        id_salarie,
        id_stock_item,
    ):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            UPDATE Ventes
            SET id_medicament = %s, id_commande_entre = %s, prix_achat = %s, prix_vente = %s, date_vente = %s, quantite_vendue = %s, total_facture = %s, id_client = %s, numero_facture = %s, id_salarie = %s, id_stock_item = %s
            WHERE id_vente = %s
        """,
            (
                id_medicament,
                id_commande_entre,
                prix_achat,
                prix_vente,
                date_vente,
                quantite_vendue,
                total_facture,
                id_client,
                numero_facture,
                id_salarie,
                id_stock_item,
                id_vente,
            ),
        )
        conn.commit()
        

    @staticmethod
    def extraire_vente(conn,id_vente):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Ventes WHERE id_vente = %s", (id_vente,))
        row = cursor.fetchone()
        
        return dict(row) if row else None

    @staticmethod
    def extraire_tous_ventes(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Ventes")
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

    @staticmethod
    def get_transactions_jour(conn,salarie):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """SELECT id_vente FROM Ventes WHERE date_vente = %s AND id_salarie = %s""",
            (datetime.now().date(), salarie),
        )
        result = cursor.fetchall()
        
        return [dict(row) for row in result]

    @staticmethod
    def get_total_vendu_salarie(conn,salarie):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """SELECT SUM(total_facture) as totalVendu FROM Ventes WHERE id_salarie = %s""",
            (salarie,),
        )
        result = cursor.fetchone()
        
        return result["totalVendu"]

    @staticmethod
    def get_statistique(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""SELECT * FROM Ventes""")
        result = cursor.fetchall()
        
        return [dict(row) for row in result]

    @staticmethod
    def cloture_journee(conn,date_jour=None):
        if date_jour is None:
            date_jour = datetime.now().strftime("%Y-%m-%d")

        
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            """SELECT COUNT(*) as count, SUM(total_facture) as total, SUM(quantite_vendue) as quanti,
                       SUM(prix_achat * quantite_vendue) as total_achat,
                       SUM((prix_vente - prix_achat) * quantite_vendue) as profit
                    FROM Ventes WHERE Date(date_vente) = %s""",
            (date_jour,),
        )
        resultats = cursor.fetchone()
        total_ventes_jour = resultats["count"]
        total_vente_jour = resultats["total"]
        quantite_vendue_jour = resultats["quanti"]
        total_achat_jour = resultats["total_achat"]
        total_profit_jour = resultats["profit"]

        statistiques_ventes_jour = {
            "Nombre total de ventes effectuées aujourdhui": total_ventes_jour or 0,
            "Montant total des ventes effectuées aujourdhui": total_vente_jour or 0,
            "Quantité totale vendue aujourdhui": quantite_vendue_jour or 0,
            "Total des achats effectués aujourdhui": total_achat_jour or 0,
            "Total des profits réalisés aujourdhui": total_profit_jour or 0,
        }

        
        return statistiques_ventes_jour

    @staticmethod
    def get_evolution(conn):
        d_now = datetime.now().date()
        res = []
        start_year = date(d_now.year, 1, 1)
        date_actuelle = start_year
        while date_actuelle <= d_now:
            dy = Ventes.cloture_journee(conn,date_actuelle)
            dy["date"] = date_actuelle
            res.append(dy)
            date_actuelle += timedelta(days=1)
        df = pd.DataFrame(res)

        variables = [
            "Nombre total de ventes effectuées aujourd'hui",
            "Montant total des ventes effectuées aujourd'hui",
            "Quantité totale vendue aujourd'hui",
            "Total des achats effectués aujourd'hui",
            "Total des profits réalisés aujourd'hui",
        ]

        fig, ax = plt.subplots()
        for var in variables:
            ax.plot(df["date"], df[var], label=var)

        ax.set_xlabel("Date")
        ax.set_ylabel("Valeur")
        ax.set_title("Évolution des variables en fonction des dates")
        ax.legend()
        return fig
    
    @staticmethod
    def extraire_ventes_par_numero_facture(conn,numero_facture):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Ventes WHERE numero_facture = %s", (numero_facture,))
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows] if rows else []
 

    @staticmethod
    def evolution_par_jour_moiis_courant(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_debut_annee = f"{datetime.now().year}-{datetime.now().month}-01"

        cursor.execute(
            """
            SELECT DATE(date_vente) as date_paiements, SUM(total_facture) as total_restant
            FROM Ventes
            WHERE DATE(date_vente) >= %s
            GROUP BY DATE(date_vente)
            ORDER BY DATE(date_vente) ASC
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
                    DATE_FORMAT(date_vente, '%%Y-%%m') AS mois_paiement, 
                    SUM(total_facture) AS total_restant
                FROM 
                    Ventes
                WHERE 
                    date_vente >= %s
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
    




    




    


