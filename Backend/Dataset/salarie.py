 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Salaries:
    def __init__(self):
        self.dataset = dataset

    def create_table_salaries(self):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Salaries (
                id_salarie INTEGER PRIMARY KEY AUTOINCREMENT,
                nom VARCHAR(100),
                prenom VARCHAR(100),
                cin VARCHAR(20) UNIQUE,
                telephone VARCHAR(15),
                email VARCHAR(100),
                adresse TEXT,
                photo TEXT,
                salaire REAL,
                type_contrat VARCHAR(50),
                date_embauche DATE,
                grade VARCHAR(50),
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    def ajouter_salarie(self, nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Salaries (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash))
        conn.commit()
        conn.close()

    def supprimer_salarie(self, id_salarie):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Salaries WHERE id_salarie = ?", (id_salarie,))
        conn.commit()
        conn.close()

    def modifier_salarie(self, id_salarie, nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Salaries
            SET nom = ?, prenom = ?, cin = ?, telephone = ?, email = ?, adresse = ?, photo = ?, salaire = ?, type_contrat = ?, date_embauche = ?, grade = ?, password_hash = ?
            WHERE id_salarie = ?
        """, (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash, id_salarie))
        conn.commit()
        conn.close()

    def extraire_salarie(self, id_salarie):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Salaries WHERE id_salarie = ?", (id_salarie,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_salarie_login(self, nom, password_hash):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Salaries WHERE nom = ? AND password_hash = ?", (nom, password_hash))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_tous_salaries(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Salaries")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

