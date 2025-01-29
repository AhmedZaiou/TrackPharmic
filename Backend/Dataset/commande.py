 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os 
import json

class Commandes:
    @staticmethod
    def __init__():
        dataset = dataset

    @staticmethod
    def create_table_commandes():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Commandes (
                id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
                id_fournisseur INTEGER,
                date_commande DATE NOT NULL,
                date_reception_prev DATE,
                statut_reception TEXT,
                receptionniste VARCHAR(100),
                produits_recus TEXT,
                date_reception DATE,
                id_salarie INTEGER,
                status_incl TEXT,
                Liste_Produits TEXT,
                FOREIGN KEY (id_fournisseur) REFERENCES Fournisseur (id_fournisseur),
                FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_commande(  Liste_Produits,id_fournisseur, date_commande, date_reception_prev, statut_reception, receptionniste, produits_recus, date_reception, id_salarie, status_incl):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Commandes (id_fournisseur, date_commande, date_reception_prev, statut_reception, receptionniste, produits_recus, date_reception, id_salarie, status_incl, Liste_Produits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_fournisseur, date_commande, date_reception_prev, statut_reception, receptionniste, produits_recus, date_reception, id_salarie, status_incl, Liste_Produits))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_commande(  id_commande):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Commandes WHERE id_commande = ?", (id_commande,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_commande( Liste_Produits, id_commande, id_fournisseur, date_commande, date_reception_prev, statut_reception, receptionniste, produits_recus, date_reception, id_salarie, status_incl):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Commandes
            SET id_fournisseur = ?, date_commande = ?, date_reception_prev = ?, statut_reception = ?, receptionniste = ?, produits_recus = ?, date_reception = ?, id_salarie = ?, status_incl = ?, Liste_Produits = ?
            WHERE id_commande = ?
        """, (id_fournisseur, date_commande, date_reception_prev, statut_reception, receptionniste, produits_recus, date_reception, id_salarie, status_incl,Liste_Produits, id_commande))
        conn.commit()
        conn.close()

    @staticmethod
    def complet_commande(  id_commande):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Commandes
            SET statut_reception = 'Complète', date_reception = ?
            WHERE id_commande = ?
        """, (datetime.now(), id_commande))  # You can set the reception date dynamically
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_commande(  id_commande):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Commandes WHERE id_commande = ?", (id_commande,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_tous_commandes():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Commandes")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def extraire_tous_commandes_table():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM  Commandes where Statut_Reception != 'Complet'")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    
        

