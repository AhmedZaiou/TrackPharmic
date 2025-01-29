 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os


class Clients: 

    @staticmethod
    def create_table_clients( ):
        conn = sqlite3.connect(dataset)
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

    @staticmethod
    def ajouter_client(  nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Clients (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_client(  id_client):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clients WHERE id_client = ?", (id_client,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_client(  id_client, nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Clients
            SET nom = ?, prenom = ?, cin = ?, telephone = ?, email = ?, adresse = ?, max_credit = ?, credit_actuel = ?
            WHERE id_client = ?
        """, (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel, id_client))
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_credit_client(  id_client, montant_credit):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Clients
            SET credit_actuel = credit_actuel + ?
            WHERE id_client = ?
        """, (montant_credit, id_client))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_client(  id_client):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients WHERE id_client = ?", (id_client,))
        row = cursor.fetchone()
        conn.close()
        return  dict(row)  if row else None

    @staticmethod
    def extraire_client_id(  id_client):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients WHERE id_client = ?", (id_client,))
        row = cursor.fetchone()
        conn.close()
        return  dict(row)  if row else None

    @staticmethod
    def extraire_client_info(  nom, prenom, cin):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients WHERE nom = ? AND prenom = ? AND cin = ?", (nom, prenom, cin))
        row = cursor.fetchone()
        conn.close()
        return  dict(row)  if row else None

    @staticmethod
    def extraire_client_nom_like(  nom_part):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT nom, prenom, cin FROM Clients WHERE nom LIKE ?", ('%' + nom_part + '%',))
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 

    @staticmethod
    def extraire_tous_clients( ):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients")
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 

    @staticmethod
    def extraire_tous_client_with_credit( ):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients WHERE credit_actuel > 0")
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 
