 
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
        return   [dict(row) for row in rows]  
    

    @staticmethod
    def cloture_journee():
        # Connexion à la base de données
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()

        # Obtenir la date actuelle au format YYYY-MM-DD
        today = datetime.today().strftime('%Y-%m-%d')

        # Total des retours effectués aujourd'hui (prix total des retours)
        cursor.execute("""
            SELECT SUM(prix * quantite_retour) as total_retours
            FROM Retours
            WHERE date_retour = ?
        """, (today,))
        total_retours = cursor.fetchone()[0]

        # Total des retours effectués aujourd'hui par salarié
        cursor.execute("""
            SELECT id_salarie, SUM(prix * quantite_retour) as total_retours_salarie
            FROM Retours
            WHERE date_retour = ?
            GROUP BY id_salarie
        """, (today,))
        retours_salaries = cursor.fetchall()

        # Nombre total de retours effectués aujourd'hui
        cursor.execute("""
            SELECT COUNT(id_retour) as total_retours_count
            FROM Retours
            WHERE date_retour = ?
        """, (today,))
        total_retours_count = cursor.fetchone()[0]

        # Total des retours effectués aujourd'hui par médicament
        cursor.execute("""
            SELECT id_medicament, SUM(prix * quantite_retour) as total_retours_medicament
            FROM Retours
            WHERE date_retour = ?
            GROUP BY id_medicament
        """, (today,))
        retours_medicaments = cursor.fetchall()

        # Clôture de la connexion
        conn.close()

        # Préparer les résultats sous forme de dictionnaire
        statistiques = {
            "Total des retours effectués aujourd'hui (prix total des retours)": total_retours if total_retours else 0.0,
            "Nombre total de retours effectués aujourd'hui": total_retours_count if total_retours_count else 0,
            "Total des retours effectués aujourd'hui par salarié en Dhs": [{"id_salarie": row[0], "total_retours_salarie": row[1]} for row in retours_salaries],
            "Total des retours effectués aujourd'hui par médicament en Dhs": [{"id_medicament": row[0], "total_retours_medicament": row[1]} for row in retours_medicaments]
        }

        return statistiques
