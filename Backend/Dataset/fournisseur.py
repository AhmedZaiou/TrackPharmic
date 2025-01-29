 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json

class Fournisseur:
    @staticmethod
    def __init__(  dataset):
        dataset = dataset

    @staticmethod
    def create_table_fournisseur():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Fournisseur (
                id_fournisseur INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_fournisseur VARCHAR(100),
                telephone VARCHAR(15),
                email VARCHAR(100),
                adresse TEXT,
                ville VARCHAR(50),
                pays VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_fournisseur(  nom_fournisseur, telephone, email, adresse, ville, pays):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Fournisseur (nom_fournisseur, telephone, email, adresse, ville, pays)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom_fournisseur, telephone, email, adresse, ville, pays))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_fournisseur(  id_fournisseur):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Fournisseur WHERE id_fournisseur = ?", (id_fournisseur,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_fournisseur(  id_fournisseur, nom_fournisseur, telephone, email, adresse, ville, pays):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Fournisseur
            SET nom_fournisseur = ?, telephone = ?, email = ?, adresse = ?, ville = ?, pays = ?
            WHERE id_fournisseur = ?
        """, (nom_fournisseur, telephone, email, adresse, ville, pays, id_fournisseur))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_fournisseur(  id_fournisseur):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseur WHERE id_fournisseur = ?", (id_fournisseur,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_fournisseur_nom(  nom_fournisseur):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseur WHERE nom_fournisseur = ?", (nom_fournisseur,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_fournisseur_nom_like(  nom_fournisseur_like):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseur WHERE nom_fournisseur LIKE ?", ('%' + nom_fournisseur_like + '%',))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_tous_fournisseurs():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseur")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def extraire_fournisseur_nom(nom):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseur WHERE Nom_Fournisseur = ?", (nom,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None 

