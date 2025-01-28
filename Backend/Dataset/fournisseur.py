import sqlite3
import json 
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


import unittest
import json

class TestFournisseurMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_fournisseur.db'
        cls.fournisseur_db = Fournisseur(cls.db_name)
        cls.fournisseur_db.create_table_fournisseur()

    def test_all_functions(self):
        # 1. Ajouter un fournisseur
        self.fournisseur_db.ajouter_fournisseur('Fournisseur A', '0123456789', 'fournisseurA@example.com', 'Adresse A', 'Ville A', 'Pays A')
        fournisseur_info = json.loads(self.fournisseur_db.extraire_fournisseur(1))
        self.assertEqual(fournisseur_info['nom_fournisseur'], 'Fournisseur A')
        self.assertEqual(fournisseur_info['telephone'], '0123456789')

        # 2. Modifier un fournisseur
        self.fournisseur_db.modifier_fournisseur(1, 'Fournisseur B', '0987654321', 'fournisseurB@example.com', 'Adresse B', 'Ville B', 'Pays B')
        fournisseur_info = json.loads(self.fournisseur_db.extraire_fournisseur(1))
        self.assertEqual(fournisseur_info['nom_fournisseur'], 'Fournisseur B')
        self.assertEqual(fournisseur_info['telephone'], '0987654321')

        # 3. Extraire un fournisseur par son nom
        fournisseur_info_by_nom = json.loads(self.fournisseur_db.extraire_fournisseur_nom('Fournisseur B'))
        self.assertEqual(fournisseur_info_by_nom['telephone'], '0987654321')

        # 4. Extraire des fournisseurs par nom contenant une chaîne
        fournisseurs_by_nom_like = json.loads(self.fournisseur_db.extraire_fournisseur_nom_like('Fournisseur'))
        self.assertEqual(len(fournisseurs_by_nom_like), 1)

        # 5. Extraire tous les fournisseurs
        all_fournisseurs = json.loads(self.fournisseur_db.extraire_tous_fournisseurs())
        self.assertEqual(len(all_fournisseurs), 1)

        # 6. Supprimer un fournisseur
        self.fournisseur_db.supprimer_fournisseur(1)
        fournisseur_info = self.fournisseur_db.extraire_fournisseur(1)
        self.assertIsNone(fournisseur_info)

if __name__ == '__main__':
    unittest.main()
