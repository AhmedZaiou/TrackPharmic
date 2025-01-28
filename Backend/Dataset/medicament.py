import sqlite3
from pathlib import Path  
from datetime import datetime, timedelta
import os
import json
current_directory = Path(__file__).parent
Front_end = current_directory.parent 

Tracpharmic = Path.home()/"Tracpharmic"

images = Tracpharmic/"images"

dataset = Tracpharmic/"dataset"/"pharmadataset.db" 


name_application = "TracPharmic"  
 

class Medicament:
    def __init__(self):
        self.dataset = dataset

    def supprimer_toute_base_donnees(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA writable_schema = 1;")
        cursor.execute("DELETE FROM sqlite_master WHERE type IN ('table', 'index', 'trigger');")
        cursor.execute("PRAGMA writable_schema = 0;")
        conn.commit()
        conn.close()

    def create_table_medicament(self):
        conn = sqlite3.connect(self.dataset)
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

    def ajouter_medicament(self, nom, caracteristique, code_ean_13, generique, prix_officine, prix_public, prix_remboursement, prix_hospitalier, substance_active, classe_therapeutique, min_stock, stock_actuel):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Medicament (Nom, Caracteristique, Code_EAN_13, Medicament_Generique, Prix_Officine, Prix_Public_De_Vente, Prix_Base_Remboursement, Prix_Hospitalier, Substance_Active_DCI, Classe_Therapeutique, Min_Stock, Stock_Actuel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (nom, caracteristique, code_ean_13, generique, prix_officine, prix_public, prix_remboursement, prix_hospitalier, substance_active, classe_therapeutique, min_stock, stock_actuel))
        conn.commit()
        conn.close()

    def supprimer_medicament(self, id_medicament):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Medicament WHERE ID_Medicament = ?;", (id_medicament,))
        conn.commit()
        conn.close()

    def modifier_medicament(self, id_medicament, **kwargs):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        columns = [f"{key} = ?" for key in kwargs.keys()]
        values = list(kwargs.values()) + [id_medicament]
        query = f"UPDATE Medicament SET {', '.join(columns)} WHERE ID_Medicament = ?;"
        cursor.execute(query, values)
        conn.commit()
        conn.close()

    def extraire_medicament(self, id_medicament):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE ID_Medicament = ?;", (id_medicament,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row) if row else None, default=str)

    def extraire_medicament_code_barre(self, code_barre):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE Code_EAN_13 = ?;", (code_barre,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row) if row else None, default=str)

    def extraire_medicament_code_barre_like(self, pattern):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE Code_EAN_13 LIKE ?;", (f"%{pattern}%",))
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

    def extraire_medicament_nom_like(self, pattern):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE Nom LIKE ?;", (f"%{pattern}%",))
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

    def extraire_tous_medicament(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament;")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

    def extraire_medicament_quantite_minimale_sup_0(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE Min_Stock > 0;")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

