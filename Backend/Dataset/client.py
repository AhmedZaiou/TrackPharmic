 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os


class Clients:
    def __init__(self):
        self.dataset = dataset

    def create_table_clients(self):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clients (
                id_client INTEGER PRIMARY KEY AUTOINCREMENT,
                nom VARCHAR(100),
                prenom VARCHAR(100),
                cin VARCHAR(20) UNIQUE,
                telephone VARCHAR(15),
                email VARCHAR(100),
                adresse TEXT,
                max_credit REAL,
                credit_actuel REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    def ajouter_client(self, nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Clients (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel))
        conn.commit()
        conn.close()

    def supprimer_client(self, id_client):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clients WHERE id_client = ?", (id_client,))
        conn.commit()
        conn.close()

    def modifier_client(self, id_client, nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Clients
            SET nom = ?, prenom = ?, cin = ?, telephone = ?, email = ?, adresse = ?, max_credit = ?, credit_actuel = ?
            WHERE id_client = ?
        """, (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel, id_client))
        conn.commit()
        conn.close()

    def ajouter_credit_client(self, id_client, montant_credit):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Clients
            SET credit_actuel = credit_actuel + ?
            WHERE id_client = ?
        """, (montant_credit, id_client))
        conn.commit()
        conn.close()

    def extraire_client(self, id_client):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients WHERE id_client = ?", (id_client,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_client_id(self, id_client):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients WHERE id_client = ?", (id_client,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_client_info(self, nom, prenom, cin):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients WHERE nom = ? AND prenom = ? AND cin = ?", (nom, prenom, cin))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_client_nom_like(self, nom_part):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients WHERE nom LIKE ?", ('%' + nom_part + '%',))
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

    def extraire_tous_clients(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

    def extraire_tous_client_with_credit(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients WHERE credit_actuel > 0")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)
