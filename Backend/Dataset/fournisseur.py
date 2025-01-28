 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Fournisseur:
    def __init__(self, dataset):
        self.dataset = dataset

    def create_table_fournisseur(self):
        conn = sqlite3.connect(self.dataset)
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

    def ajouter_fournisseur(self, nom_fournisseur, telephone, email, adresse, ville, pays):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Fournisseur (nom_fournisseur, telephone, email, adresse, ville, pays)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom_fournisseur, telephone, email, adresse, ville, pays))
        conn.commit()
        conn.close()

    def supprimer_fournisseur(self, id_fournisseur):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Fournisseur WHERE id_fournisseur = ?", (id_fournisseur,))
        conn.commit()
        conn.close()

    def modifier_fournisseur(self, id_fournisseur, nom_fournisseur, telephone, email, adresse, ville, pays):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Fournisseur
            SET nom_fournisseur = ?, telephone = ?, email = ?, adresse = ?, ville = ?, pays = ?
            WHERE id_fournisseur = ?
        """, (nom_fournisseur, telephone, email, adresse, ville, pays, id_fournisseur))
        conn.commit()
        conn.close()

    def extraire_fournisseur(self, id_fournisseur):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseur WHERE id_fournisseur = ?", (id_fournisseur,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_fournisseur_nom(self, nom_fournisseur):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseur WHERE nom_fournisseur = ?", (nom_fournisseur,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_fournisseur_nom_like(self, nom_fournisseur_like):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseur WHERE nom_fournisseur LIKE ?", ('%' + nom_fournisseur_like + '%',))
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

    def extraire_tous_fournisseurs(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseur")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

