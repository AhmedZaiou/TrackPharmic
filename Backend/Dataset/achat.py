 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json

class Achats: 

    @staticmethod
    def create_table_achats ():
        conn = sqlite3.connect( dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Achats (
                id_achat INTEGER PRIMARY KEY AUTOINCREMENT,
                id_medicament INTEGER NOT NULL,
                id_fournisseur INTEGER,
                quantite_achetee INTEGER DEFAULT 0,
                prix_achat_unitaire REAL,
                prix_vente_unitaire REAL,
                date_achat DATE NOT NULL,
                date_expiration DATE,
                id_salarie INTEGER,
                FOREIGN KEY (id_medicament) REFERENCES Medicament (id_medicament),
                FOREIGN KEY (id_fournisseur) REFERENCES Fournisseur (id_fournisseur),
                FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_achat( id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, date_achat, date_expiration, id_salarie):
        conn = sqlite3.connect( dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Achats (id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, date_achat, date_expiration, id_salarie)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, date_achat, date_expiration, id_salarie))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_achat( id_achat):
        conn = sqlite3.connect( dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Achats WHERE id_achat = ?", (id_achat,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_achat( id_achat, id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, date_achat, date_expiration, id_salarie):
        conn = sqlite3.connect( dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Achats
            SET id_medicament = ?, id_fournisseur = ?, quantite_achetee = ?, prix_achat_unitaire = ?, prix_vente_unitaire = ?, date_achat = ?, date_expiration = ?, id_salarie = ?
            WHERE id_achat = ?
        """, (id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, date_achat, date_expiration, id_salarie, id_achat))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_achat( id_achat):
        conn = sqlite3.connect( dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Achats WHERE id_achat = ?", (id_achat,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    @staticmethod
    def extraire_tous_achats ():
        conn = sqlite3.connect( dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Achats")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)
    



    @staticmethod
    def cloture_journee():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get total number of purchases made today, total quantity of items purchased today,
        # total amount spent on purchases today, and total amount earned from sales today
        cursor.execute("""
            SELECT 
            COUNT(*) AS total_purchases,
            SUM(quantite_achetee) AS total_quantity,
            SUM(prix_achat_unitaire * quantite_achetee) AS total_amount_spent,
            SUM(prix_vente_unitaire * quantite_achetee) AS total_amount_earned
            FROM Achats
            WHERE date_achat = ?
        """, (datetime.now().date(),))
        result = cursor.fetchone()
        total_purchases = result[0]
        total_quantity = result[1]
        total_amount_spent = result[2]
        total_amount_earned = result[3]
        
        conn.close()
        
        return {
            "Nombre de transactions achat": total_purchases,
            "Quantité des produits vendus": total_quantity,
            "Montant total dépensé": total_amount_spent,
            "Montant total gagné": total_amount_earned
        }
    


    

