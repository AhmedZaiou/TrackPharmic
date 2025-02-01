 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json

class Salaries:  
    @staticmethod
    @staticmethod
    def create_table_salaries():
        conn = sqlite3.connect(dataset)
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

    @staticmethod
    @staticmethod
    def ajouter_salarie( nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Salaries (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash))
        conn.commit()
        conn.close()

    @staticmethod
    @staticmethod
    def supprimer_salarie( id_salarie):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Salaries WHERE id_salarie = ?", (id_salarie,))
        conn.commit()
        conn.close()

    @staticmethod
    @staticmethod
    def modifier_salarie( id_salarie, nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Salaries
            SET nom = ?, prenom = ?, cin = ?, telephone = ?, email = ?, adresse = ?, photo = ?, salaire = ?, type_contrat = ?, date_embauche = ?, grade = ?, password_hash = ?
            WHERE id_salarie = ?
        """, (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash, id_salarie))
        conn.commit()
        conn.close()

    @staticmethod
    @staticmethod
    def extraire_salarie( id_salarie):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Salaries WHERE id_salarie = ?", (id_salarie,))
        row = cursor.fetchone()
        conn.close()
        return  dict(row)  if row else None

    @staticmethod
    @staticmethod
    def extraire_salarie_login( nom, password_hash):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Salaries WHERE nom = ? AND password_hash = ?", (nom, password_hash))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    @staticmethod
    def extraire_tous_salaries():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Salaries")
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 
    

    def get_salaries():
        # Connect to the database
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT id_salarie, nom, prenom FROM Salaries''')
        result = cursor.fetchall()
        conn.close()
        return [row['id_salarie'] for row in result], [row['nom'] for row in result], [row['prenom'] for row in result]
