import sqlite3
import json 
import sqlite3
from pathlib import Path  
from datetime import datetime, timedelta
import os
import json
current_directory = Path(__file__).parent
Front_end = current_directory.parent 

Tracpharmic = Path.home()/"Tracpharmic"

images = Tracpharmic/"images"

dataset = Tracpharmic/"dataset"/"pharmadataset.db" 


name_application = "TracPharmic"  

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



import unittest
import json

class TestPaymentMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_payment.db'
        cls.payment_db = Payment(cls.db_name)
        cls.payment_db.create_table_payment()

    def test_all_functions(self):
        # 1. Ajouter un paiement
        self.payment_db.ajouter_payment(1, 'FACT123', 150.0, '2025-01-28', 2)
        payment_info = json.loads(self.payment_db.extraire_payment_with_id_client(1))
        self.assertEqual(payment_info[0]['numero_facture'], 'FACT123')
        self.assertEqual(payment_info[0]['montant_paye'], 150.0)

        # 2. Extraire les paiements en fonction de l'ID du client
        payments_by_client = json.loads(self.payment_db.extraire_payment_with_id_client(1))
        self.assertEqual(len(payments_by_client), 1)
        self.assertEqual(payments_by_client[0]['id_client'], 1)

if __name__ == '__main__':
    unittest.main()

