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

class Credit:
    def __init__(self):
        self.dataset = dataset

    def create_table_credit(self):
        conn = sqlite3.connect(self.dataset)
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

    def ajouter_credit(self, id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Credit (id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie))
        conn.commit()
        conn.close()

    def supprimer_credit(self, id_credit):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Credit WHERE id_credit = ?", (id_credit,))
        conn.commit()
        conn.close()

    def modifier_credit(self, id_credit, id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Credit
            SET id_client = ?, numero_facture = ?, montant_paye = ?, reste_a_payer = ?, date_dernier_paiement = ?, statut = ?, id_salarie = ?
            WHERE id_credit = ?
        """, (id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie, id_credit))
        conn.commit()
        conn.close()

    def extraire_credit(self, id_credit):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Credit WHERE id_credit = ?", (id_credit,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_tous_credits(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Credit")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

    def extraire_credit_with_id_client(self, id_client):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Credit WHERE id_client = ?", (id_client,))
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

    def create_table_payment(self):
        conn = sqlite3.connect(self.dataset)
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

