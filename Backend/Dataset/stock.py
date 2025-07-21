import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
from Backend.Dataset.medicament import Medicament


class Stock:
    @staticmethod
    def create_table_stock(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
        CREATE TABLE IF NOT EXISTS Stock (
            id_stock INT AUTO_INCREMENT PRIMARY KEY,
            id_medicament INT NOT NULL,
            id_commande INT,
            id_salarie INT,
            prix_achat DECIMAL(10, 2),
            prix_vente DECIMAL(10, 2),
            prix_conseille DECIMAL(10, 2),
            date_achat DATE,
            date_expiration DATE,
            stock_initial INT DEFAULT 0,
            quantite_actuelle INT DEFAULT 0,
            quantite_minimale INT DEFAULT 0,
            quantite_maximale INT,
            date_reception DATE,
            date_derniere_sortie DATE
        );
        """
        cursor.execute(query)
        conn.commit()
        

    @staticmethod
    def ajouter_stock(conn,
        id_medicament,
        id_commande,
        id_salarie,
        prix_achat,
        prix_vente,
        prix_conseille,
        date_achat,
        date_expiration,
        stock_initial,
        quantite_actuelle,
        quantite_minimale,
        quantite_maximale,
        date_reception,
        date_derniere_sortie,
    ):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
        INSERT INTO Stock (id_medicament, id_commande, id_salarie, prix_achat, prix_vente, prix_conseille,
                           date_achat, date_expiration, stock_initial, quantite_actuelle, quantite_minimale,
                           quantite_maximale, date_reception, date_derniere_sortie)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(
            query,
            (
                id_medicament,
                id_commande,
                id_salarie,
                prix_achat,
                prix_vente,
                prix_conseille,
                date_achat,
                date_expiration,
                stock_initial,
                quantite_actuelle,
                quantite_minimale,
                quantite_maximale,
                date_reception,
                date_derniere_sortie,
            ),
        )
        conn.commit()
        
        Medicament.effectuer_stock_medicament(id_medicament, quantite_actuelle)

    @staticmethod
    def supprimer_stock(conn,id_stock):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "DELETE FROM Stock WHERE id_stock = %s;"
        cursor.execute(query, (id_stock,))
        conn.commit()
        

    @staticmethod
    def modifier_stock(conn,
        id_stock,
        id_medicament,
        id_commande,
        id_salarie,
        prix_achat,
        prix_vente,
        prix_conseille,
        date_achat,
        date_expiration,
        stock_initial,
        quantite_actuelle,
        quantite_minimale,
        quantite_maximale,
        date_reception,
        date_derniere_sortie,
    ):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
        UPDATE Stock SET
            id_medicament = %s, id_commande = %s, id_salarie = %s, prix_achat = %s, prix_vente = %s, prix_conseille = %s,
            date_achat = %s, date_expiration = %s, stock_initial = %s, quantite_actuelle = %s, quantite_minimale = %s,
            quantite_maximale = %s, date_reception = %s, date_derniere_sortie = %s
        WHERE id_stock = %s;
        """
        cursor.execute(
            query,
            (
                id_medicament,
                id_commande,
                id_salarie,
                prix_achat,
                prix_vente,
                prix_conseille,
                date_achat,
                date_expiration,
                stock_initial,
                quantite_actuelle,
                quantite_minimale,
                quantite_maximale,
                date_reception,
                date_derniere_sortie,
                id_stock,
            ),
        )
        conn.commit()
        

    @staticmethod
    def effectuer_vente_stock(conn,id_stock, quantite_vendu):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
        UPDATE Stock SET quantite_actuelle = quantite_actuelle - %s
        WHERE id_stock = %s;
        """
        cursor.execute(query, (quantite_vendu, id_stock))
        cursor.execute("DELETE FROM Stock WHERE quantite_actuelle = 0;")
        conn.commit()
        

    @staticmethod
    def extraire_medicament_id_stock(conn,id_medicament):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM Stock WHERE id_medicament = %s ORDER BY date_expiration;"
        cursor.execute(query, (id_medicament,))
        row = cursor.fetchall()
        
        if row is None or len(row) == 0:
            return None
        else:
            dic = {}
            dic["id_medicament"] = row[0]["id_medicament"]
            dic["prix_vente"] = [item["prix_vente"] for item in row]
            dic["date_expiration"] = [item["date_expiration"] for item in row]
            dic["quantite_actuelle"] = sum(
                [int(item["quantite_actuelle"]) for item in row]
            )
            dic["list_quantity"] = [int(item["quantite_actuelle"]) for item in row]
            dic["id_commande"] = [item["id_commande"] for item in row]
            dic["id_stock"] = [item["id_stock"] for item in row]
            dic["prix_achat"] = [item["prix_achat"] for item in row]
            return dic

    @staticmethod
    def extraire_stock(conn,id_stock):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM Stock WHERE id_stock = %s;"
        cursor.execute(query, (id_stock,))
        row = cursor.fetchone()
        
        return dict(row) if row else None

    @staticmethod
    def extraire_tous_stock(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM Stock;"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def extraire_tous_medicament_with_expiration_date_minim(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """SELECT m.*,s.* 
            FROM Stock s 
            JOIN 
            Medicament m 
            ON 
            s.id_medicament = m.id_medicament
            WHERE Date(s.date_expiration) <= DATE_ADD(CURDATE(), INTERVAL 60 DAY) """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    

    @staticmethod
    def extraire_stock_medicament(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """SELECT 
                        m.Nom,
                        m.Code_EAN_13,
                        s.date_expiration,
                        s.quantite_actuelle
                    FROM 
                        Stock s
                    JOIN 
                        Medicament m 
                    ON 
                        s.id_medicament = m.id_medicament
                    ORDER BY m.Nom;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    

 
    @staticmethod
    def extraire_medicament_quantite_minimale_sup_0(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM Stock WHERE quantite_minimale > 0;"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

    @staticmethod
    def get_situation_stock(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id_medicament, quantite_actuelle FROM Stock")
        result = cursor.fetchall()
        
        return {row["id_medicament"]: row["quantite_actuelle"] for row in result}
    

    @staticmethod
    def get_medicament_commande(conn,id_commande):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT m.Code_EAN_13, m.Nom,s.quantite_actuelle FROM Stock s JOIN  Medicament m  ON s.id_medicament = m.id_medicament where id_commande = %s",(id_commande,))
        result = cursor.fetchall()
        
        return [dict(row) for row in result]
    



    @staticmethod
    def calculer_total_achat_vente(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT SUM(prix_achat) AS total_achat, SUM(prix_vente) AS total_vente FROM Stock"
        )
        result = cursor.fetchone()
        
        return result["total_achat"], result["total_vente"]

    @staticmethod
    def cloture_journee(conn):
        today = datetime.now().strftime("%Y-%m-%d")
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Total des achats et ventes pour la journée
        cursor.execute(
            """
            SELECT SUM(prix_achat) AS total_achat, SUM(prix_vente) AS total_vente 
            FROM Stock 
            WHERE DATE(date_reception) = %s OR DATE(date_derniere_sortie) = %s
        """,
            (today, today),
        )
        result = cursor.fetchone()
        total_achat = result["total_achat"]
        total_vente = result["total_vente"]

        # Quantités totales en stock aujourd'hui
        cursor.execute(
            """
            SELECT SUM(quantite_actuelle) AS total_quantite 
            FROM Stock 
            WHERE DATE(date_reception) = %s OR DATE(date_derniere_sortie) = %s
        """,
            (today, today),
        )
        result = cursor.fetchone()
        total_quantite = result["total_quantite"]

        # Quantités minimales non respectées aujourd'hui
        cursor.execute(
            """
            SELECT COUNT(*) AS count 
            FROM Stock 
            WHERE quantite_actuelle < quantite_minimale 
            AND (date_reception = %s OR date_derniere_sortie = %s)
        """,
            (today, today),
        )
        result = cursor.fetchone()
        quantites_minimales_non_respectees = result["count"]

        # Médicaments proches de la date d'expiration aujourd'hui
        cursor.execute(
            """
            SELECT COUNT(*) AS count 
            FROM Stock 
            WHERE Date(date_expiration) <= DATE_ADD(CURDATE(), INTERVAL 60 DAY)  
        """
        )
        result = cursor.fetchone()
        medicaments_proches_expiration = result["count"]
        

        return {
            "Total des achats pour la journée": total_achat or 0,
            "Total des ventes pour la journée": total_vente or 0,
            "Quantités totales en stock aujourdhui": total_quantite or 0,
            "Quantités minimales non respectées aujourdhui": quantites_minimales_non_respectees or 0,
            "Nombre Médicaments proches de la date dexpiration aujourdhui": medicaments_proches_expiration or 0,
        }
