 
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
    def create_table_payment():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Payment (
                id_payment INTEGER PRIMARY KEY AUTOINCREMENT,
                id_credit INTEGER,
                montant REAL,
                date_payment DATE NOT NULL,
                FOREIGN KEY (id_credit) REFERENCES Credit (id_credit)
            );
        """)
        conn.commit()
        conn.close()

