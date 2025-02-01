 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Credit:
    @staticmethod
    def __init__():
        dataset = dataset

    @staticmethod
    def create_table_credit():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Credit (
                id_credit INTEGER PRIMARY KEY AUTOINCREMENT,
                id_client INTEGER,
                numero_facture VARCHAR(50),
                montant_paye REAL,
                reste_a_payer REAL,
                date_dernier_paiement DATE,
                statut TEXT,
                id_salarie INTEGER,
                FOREIGN KEY (id_client) REFERENCES Clients (id_client),
                FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_credit(  id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Credit (id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_credit(  id_credit):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Credit WHERE id_credit = ?", (id_credit,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_credit(  id_credit, id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Credit
            SET id_client = ?, numero_facture = ?, montant_paye = ?, reste_a_payer = ?, date_dernier_paiement = ?, statut = ?, id_salarie = ?
            WHERE id_credit = ?
        """, (id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie, id_credit))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_credit(  id_credit):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Credit WHERE id_credit = ?", (id_credit,))
        row = cursor.fetchone()
        conn.close()
        return  dict(row)  if row else None

    @staticmethod
    def extraire_tous_credits():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Credit")
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 

    @staticmethod
    def extraire_credit_with_id_client(  id_client):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Credit WHERE id_client = ?", (id_client,))
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 

    
    
    @staticmethod
    def get_total_credits():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(reste_a_payer) as totalCredits FROM Credit")
        result = cursor.fetchone()
        conn.close()
        return result[0]
    

    @staticmethod
    def get_total_credits_salarie(salarie):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(reste_a_payer) as totalCredits FROM Credit WHERE id_salarie = ?", (salarie,))
        result = cursor.fetchone()
        conn.close()
        return result[0]
    

    @staticmethod
    def cloture_journee():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        date_aujourdhui = datetime.now().date().strftime('%d/%m/%Y')
        cursor.execute("""
            SELECT  strftime('%d-%m-%Y', date_dernier_paiement) as date
            FROM Credit 
        """)
        total_restant = cursor.fetchall() 
        print([dict(a) for a in total_restant] )

        cursor.execute("""
            SELECT SUM(reste_a_payer) as total_restant 
            FROM Credit
            WHERE  strftime('%d/%m/%Y', date_dernier_paiement) = ?
        """, (date_aujourdhui,))
        total_restant = cursor.fetchone()["total_restant"] or 0 
        print(total_restant)  
         
        # Total restant à payer
        

        cursor.execute("""
            SELECT   date_dernier_paiement
            FROM Credit 
        """ )
        total_restants = cursor.fetchone()
        print(dict(total_restants), date_aujourdhui)  

         
        conn.close()

        return { 
            "Total restant à payer aujourd'hui ": total_restant
        }



     