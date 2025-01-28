 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Pharmacies:
    def __init__(self):
        self.dataset = dataset

    def create_table_pharmacies(self):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pharmacies (
                id_pharmacie INTEGER PRIMARY KEY AUTOINCREMENT,
                nom VARCHAR(100),
                adresse TEXT,
                telephone VARCHAR(15),
                email VARCHAR(100),
                outvalue TEXT,
                invalue TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    def ajouter_pharmacie(self, nom, adresse, telephone, email, outvalue, invalue):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Pharmacies (nom, adresse, telephone, email, outvalue, invalue)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, adresse, telephone, email, outvalue, invalue))
        conn.commit()
        conn.close()

    def modifier_pharmacie(self, id_pharmacie, nom, adresse, telephone, email, outvalue, invalue):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Pharmacies
            SET nom = ?, adresse = ?, telephone = ?, email = ?, outvalue = ?, invalue = ?
            WHERE id_pharmacie = ?
        """, (nom, adresse, telephone, email, outvalue, invalue, id_pharmacie))
        conn.commit()
        conn.close()

    def extraire_tous_pharma(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pharmacies")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

    def extraire_pharma_nom_like(self, nom_part):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pharmacies WHERE nom LIKE ?", ('%' + nom_part + '%',))
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

