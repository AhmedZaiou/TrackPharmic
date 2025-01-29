 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Payment:
    @staticmethod
    def __init__(  dataset):
        dataset = dataset

    @staticmethod
    def create_table_payment():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Payment (
                id_payment INTEGER PRIMARY KEY AUTOINCREMENT,
                id_client INTEGER,
                numero_facture VARCHAR(50),
                montant_paye REAL,
                date_paiement DATE NOT NULL,
                id_salarie INTEGER,
                FOREIGN KEY (id_client) REFERENCES Clients (id_client),
                FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_payment(  id_client, numero_facture, montant_paye, date_paiement, id_salarie):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Payment (id_client, numero_facture, montant_paye, date_paiement, id_salarie)
            VALUES (?, ?, ?, ?, ?)
        """, (id_client, numero_facture, montant_paye, date_paiement, id_salarie))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_payment_with_id_client(  id_client):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Payment WHERE id_client = ?", (id_client,))
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 



