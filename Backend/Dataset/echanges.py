 
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
        return  dict(row)  if row else None

    @staticmethod
    def extraire_tous_echanges():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Echanges")
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 
    
    @staticmethod
    def get_total_echanges():
        # Connect to the database
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(total_facture) as totalEchanges FROM Echanges''')
        result = cursor.fetchone() 
        conn.close()
        return result[0]
    

    @staticmethod
    def get_total_echanges_salarie(salarie):
        # Connect to the database
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(total_facture) as totalEchanges FROM Echanges WHERE id_salarie = ?''', (salarie,))
        result = cursor.fetchone()
        conn.close()
        return result[0]
    


    @staticmethod
    def cloture_journee():
        # Connexion à la base de données
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()

        # Calcul du total des échanges de la journée
        cursor.execute("""
            SELECT SUM(total_facture) as total_journee
            FROM Echanges
            WHERE date_echange = ?
        """, (datetime.now().strftime('%Y-%m-%d'),))  # Filtrer pour la date d'aujourd'hui
        total_journee = cursor.fetchone()[0]

        # Nombre d'échanges réalisés aujourd'hui
        cursor.execute("""
            SELECT COUNT(id_echange) as nombre_echanges
            FROM Echanges
            WHERE date_echange = ?
        """, (datetime.now().strftime('%Y-%m-%d'),))
        nombre_echanges = cursor.fetchone()[0]

        # Total des échanges par salarié
        cursor.execute("""
            SELECT id_salarie, SUM(total_facture) as total_par_salarie
            FROM Echanges
            WHERE date_echange = ?
            GROUP BY id_salarie
        """, (datetime.now().strftime('%Y-%m-%d'),))
        echanges_par_salarie = cursor.fetchall()

        # Clôture des connexions
        conn.close()

        # Préparer les résultats sous forme de dictionnaire
        statistiques = {
                        "Calcul du total des échanges de la journée": total_journee if total_journee else 0,
                        "Nombre d'échanges réalisés aujourd'hui": nombre_echanges if nombre_echanges else 0,
                        "Total des échanges par salarié": [
                            {"id_salarie": e[0], "Calcul du total des échanges de la journée par salarié": e[1]} 
                            for e in echanges_par_salarie
                        ]
                    }

        return statistiques


