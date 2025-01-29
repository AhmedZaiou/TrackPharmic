 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Pharmacies: 
    @staticmethod
    def create_table_pharmacies():
        conn = sqlite3.connect(dataset)
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

    @staticmethod
    def ajouter_pharmacie(  nom, adresse, telephone, email, outvalue, invalue):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Pharmacies (nom, adresse, telephone, email, outvalue, invalue)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, adresse, telephone, email, outvalue, invalue))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_pharmacie(  id_pharmacie, nom, adresse, telephone, email, outvalue, invalue):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Pharmacies
            SET nom = ?, adresse = ?, telephone = ?, email = ?, outvalue = ?, invalue = ?
            WHERE id_pharmacie = ?
        """, (nom, adresse, telephone, email, outvalue, invalue, id_pharmacie))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_tous_pharma():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pharmacies")
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 

    @staticmethod
    def extraire_pharma_nom_like(  nom_part):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT nom FROM Pharmacies WHERE nom LIKE ?", ('%' + nom_part + '%',))
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 
    
    def extraire_pharma_nom(nom):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pharmacies WHERE Nom = ?", (nom,))
        rows = cursor.fetchone()
        conn.close()
        return   dict(rows) if rows else None
    
     

