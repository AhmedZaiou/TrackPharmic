import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json

from Backend.Dataset.salarie import Salaries


class CommandeClient:
    @staticmethod
    def __init__():
        dataset = dataset
    
    @staticmethod
    def create_table_commandes_client(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Commandes_client (
                id_commande_client INT PRIMARY KEY AUTO_INCREMENT,
                numero_facture VARCHAR(50),
                code_ean_13 VARCHAR(50),
                id_medicament INT,
                prix_vente FLOAT,
                date_vente DATE,
                quantite_vendue INT,
                id_client INT,
                id_salarie INT,
                nom_medicament VARCHAR(255),
                to_pay_now FLOAT,
                total_facture_calculer FLOAT,
                now_str VARCHAR(100),
                statut_de_commande VARCHAR(50)
            );
            """
        )
        conn.commit()
        

    @staticmethod
    def ajouter_commande_client(conn,
        numero_facture, code_ean_13, id_medicament, prix_vente, date_vente,
        quantite_vendue, id_client, id_salarie, nom_medicament,
        to_pay_now, total_facture_calculer, now_str, statut_de_commande
    ):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            INSERT INTO Commandes_client (
                numero_facture, code_ean_13, id_medicament, prix_vente, date_vente,
                quantite_vendue, id_client, id_salarie, nom_medicament,
                to_pay_now, total_facture_calculer, now_str, statut_de_commande
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                numero_facture, code_ean_13, id_medicament, prix_vente, date_vente,
                quantite_vendue, id_client, id_salarie, nom_medicament,
                to_pay_now, total_facture_calculer, now_str, statut_de_commande
            )
        )
        conn.commit()
        

    @staticmethod
    def modifier_statut_commande_client(conn,numero_facture, nouveau_statut):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            UPDATE Commandes_client
            SET statut_de_commande = %s
            WHERE numero_facture = %s
            """,
            (nouveau_statut, numero_facture)
        )
        conn.commit()
        

    @staticmethod
    def get_commande(conn, numero_facture):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            Select * from  Commandes_client 
            WHERE numero_facture = %s
            """,
            (numero_facture)
        )
        conn.commit()
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def get_all_commandes_client(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT *
                FROM Commandes_client
                WHERE statut_de_commande = 'in progresse'
                AND id_commande_client IN (
                    SELECT MIN(id_commande_client)
                    FROM Commandes_client
                    GROUP BY numero_facture
                );
            """
        )
        rows = cursor.fetchall()
        conn.commit()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def cloture_journee(conn,date_jour=None):
        if date_jour is None:
            date_jour = datetime.now().strftime("%Y-%m-%d")

        
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute( 
            """SELECT COUNT(*) as count, SUM(to_pay_now) as total
                    FROM Commandes_client
                    WHERE DATE(date_vente) = %s
                    AND id_commande_client IN (
                        SELECT MIN(id_commande_client)
                        FROM Commandes_client
                        GROUP BY numero_facture
                    );""",
            (date_jour,),
        )
        resultats = cursor.fetchone()
        total_ventes_jour = resultats["count"]
        total_vente_jour = resultats["total"] 

        statistiques_ventes_jour = {
            "Nombre total de commandes clients effectuées aujourdhui": total_ventes_jour or 0,
            "Montant total des commandes clients effectuées aujourdhui": total_vente_jour or 0
        }
        
        return statistiques_ventes_jour