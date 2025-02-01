 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json

class Medicament: 


    @staticmethod
    def supprimer_toute_base_donnees():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA writable_schema = 1;")
        cursor.execute("DELETE FROM sqlite_master WHERE type IN ('table', 'index', 'trigger');")
        cursor.execute("PRAGMA writable_schema = 0;")
        conn.commit()
        conn.close()

    @staticmethod
    def create_table_medicament():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Medicament (
            ID_Medicament INTEGER PRIMARY KEY AUTOINCREMENT,
            Nom TEXT NOT NULL,
            Caracteristique TEXT,
            Code_EAN_13 TEXT,
            Medicament_Generique TEXT,
            Prix_Officine REAL,
            Prix_Public_De_Vente REAL,
            Prix_Base_Remboursement REAL,
            Prix_Hospitalier REAL,
            Substance_Active_DCI TEXT,
            Classe_Therapeutique TEXT,
            Min_Stock INTEGER,
            Stock_Actuel INTEGER
        );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_medicament(  nom, caracteristique, code_ean_13, generique, prix_officine, prix_public, prix_remboursement, prix_hospitalier, substance_active, classe_therapeutique, min_stock, stock_actuel):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Medicament (Nom, Caracteristique, Code_EAN_13, Medicament_Generique, Prix_Officine, Prix_Public_De_Vente, Prix_Base_Remboursement, Prix_Hospitalier, Substance_Active_DCI, Classe_Therapeutique, Min_Stock, Stock_Actuel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (nom, caracteristique, code_ean_13, generique, prix_officine, prix_public, prix_remboursement, prix_hospitalier, substance_active, classe_therapeutique, min_stock, stock_actuel))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_medicament(  id_medicament):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Medicament WHERE ID_Medicament = ?;", (id_medicament,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_medicament(  id_medicament, **kwargs):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        columns = [f"{key} = ?" for key in kwargs.keys()]
        values = list(kwargs.values()) + [id_medicament]
        query = f"UPDATE Medicament SET {', '.join(columns)} WHERE ID_Medicament = ?;"
        cursor.execute(query, values)
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_medicament(  id_medicament):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE ID_Medicament = ?;", (id_medicament,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_medicament_code_barre(  code_barre):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE Code_EAN_13 = ?;", (code_barre,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_medicament_code_barre_like(  pattern):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE Code_EAN_13 LIKE ?;", (f"%{pattern}%",))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_medicament_nom_like(  pattern):
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE Nom LIKE ?;", (f"%{pattern}%",))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_tous_medicament():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament;")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_medicament_quantite_minimale_sup_0():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE Min_Stock > 0;")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    

 

    @staticmethod
    def cloture_journee():
        # Connexion à la base de données
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()

        # Total des médicaments
        cursor.execute("""
            SELECT COUNT(ID_Medicament) as total_medicaments
            FROM Medicament
        """)
        total_medicaments = cursor.fetchone()[0]

        # Total des médicaments avec stock inférieur au minimum
        cursor.execute("""
            SELECT COUNT(ID_Medicament) as medicaments_en_rupture
            FROM Medicament
            WHERE Stock_Actuel < Min_Stock
        """)
        medicaments_en_rupture = cursor.fetchone()[0]

        # Total des médicaments avec stock positif
        cursor.execute("""
            SELECT COUNT(ID_Medicament) as medicaments_avec_stock
            FROM Medicament
            WHERE Stock_Actuel > 0
        """)
        medicaments_avec_stock = cursor.fetchone()[0]

        # Calcul du stock total disponible
        cursor.execute("""
            SELECT SUM(Stock_Actuel) as total_stock
            FROM Medicament
        """)
        total_stock = cursor.fetchone()[0]

        

        # Clôture de la connexion
        conn.close()

        # Préparer les résultats sous forme de dictionnaire
        statistiques = {
            "Total des médicaments": total_medicaments if total_medicaments else 0,
            "Total des médicaments avec stock inférieur au minimum": medicaments_en_rupture if medicaments_en_rupture else 0,
            "Total des médicaments avec stock positif": medicaments_avec_stock if medicaments_avec_stock else 0,
            "Calcul du stock total disponible de tous les medicaments": total_stock if total_stock else 0
        }

        return statistiques


