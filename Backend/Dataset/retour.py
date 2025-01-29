 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json


class Retour:
    @staticmethod
    def __init__():
        dataset = dataset

    @staticmethod
    def create_table_retours():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Retours (
                id_retour INTEGER PRIMARY KEY AUTOINCREMENT,
                id_medicament INTEGER NOT NULL, 
                prix REAL, 
                date_retour DATE NOT NULL,
                quantite_retour INTEGER DEFAULT 0,  
                numero_facture VARCHAR(50),
                id_salarie INTEGER 
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_retour(id_medicament, prix, date_retour, quantite_retour, numero_facture, id_salarie):
        Retour.create_table_retours()
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Retours (id_medicament, prix, date_retour, quantite_retour, numero_facture, id_salarie)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_medicament, prix, date_retour, quantite_retour, numero_facture, id_salarie))  # Corrected column names
        conn.commit()
        conn.close()
        

    @staticmethod
    def extraire_tous_retours():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Retours")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

