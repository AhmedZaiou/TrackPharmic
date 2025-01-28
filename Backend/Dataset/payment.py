 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Payment:
    def __init__(self, dataset):
        self.dataset = dataset

    def create_table_payment(self):
        conn = sqlite3.connect(self.dataset)
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

    def ajouter_payment(self, id_client, numero_facture, montant_paye, date_paiement, id_salarie):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Payment (id_client, numero_facture, montant_paye, date_paiement, id_salarie)
            VALUES (?, ?, ?, ?, ?)
        """, (id_client, numero_facture, montant_paye, date_paiement, id_salarie))
        conn.commit()
        conn.close()

    def extraire_payment_with_id_client(self, id_client):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Payment WHERE id_client = ?", (id_client,))
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)



