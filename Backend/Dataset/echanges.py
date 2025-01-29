 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Echanges:
    @staticmethod
    def __init__():
        dataset = dataset

    @staticmethod
    def create_table_echanges():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Echanges (
                id_echange INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pharmacie INTEGER,
                id_facture INTEGER,
                date_echange DATE NOT NULL,
                total_facture REAL,
                sens VARCHAR(10),
                id_salarie INTEGER,
                FOREIGN KEY (id_pharmacie) REFERENCES Pharmacies (id_pharmacie),
                FOREIGN KEY (id_facture) REFERENCES Ventes (id_vente),
                FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_echange(  id_pharmacie, id_facture, date_echange, total_facture, sens, id_salarie):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Echanges (id_pharmacie, id_facture, date_echange, total_facture, sens, id_salarie)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_pharmacie, id_facture, date_echange, total_facture, sens, id_salarie))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_echange(  id_echange):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Echanges WHERE id_echange = ?", (id_echange,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_echange(  id_echange, id_pharmacie, id_facture, date_echange, total_facture, sens, id_salarie):
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Echanges
            SET id_pharmacie = ?, id_facture = ?, date_echange = ?, total_facture = ?, sens = ?, id_salarie = ?
            WHERE id_echange = ?
        """, (id_pharmacie, id_facture, date_echange, total_facture, sens, id_salarie, id_echange))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_echange(  id_echange):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Echanges WHERE id_echange = ?", (id_echange,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    @staticmethod
    def extraire_tous_echanges():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Echanges")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)


