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

class Pharmacies:
    def __init__(self):
        self.dataset = dataset

    def create_table_pharmacies(self):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pharmacies (
                id_pharmacie INTEGER PRIMARY KEY AUTOINCREMENT,
                nom VARCHAR(100),
                adresse TEXT,
                telephone VARCHAR(15),
                email VARCHAR(100),
                outvalue TEXT,
                invalue TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    def ajouter_pharmacie(self, nom, adresse, telephone, email, outvalue, invalue):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Pharmacies (nom, adresse, telephone, email, outvalue, invalue)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, adresse, telephone, email, outvalue, invalue))
        conn.commit()
        conn.close()

    def modifier_pharmacie(self, id_pharmacie, nom, adresse, telephone, email, outvalue, invalue):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Pharmacies
            SET nom = ?, adresse = ?, telephone = ?, email = ?, outvalue = ?, invalue = ?
            WHERE id_pharmacie = ?
        """, (nom, adresse, telephone, email, outvalue, invalue, id_pharmacie))
        conn.commit()
        conn.close()

    def extraire_tous_pharma(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pharmacies")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

    def extraire_pharma_nom_like(self, nom_part):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pharmacies WHERE nom LIKE ?", ('%' + nom_part + '%',))
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)


import unittest
import json

class TestPharmaciesMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_pharmacies.db'
        cls.pharmacies_db = Pharmacies()
        cls.pharmacies_db.create_table_pharmacies()

    def test_all_functions(self):
        # 1. Ajouter une pharmacie
        self.pharmacies_db.ajouter_pharmacie('Pharmacie ABC', '123 Rue Principale', '0123456789', 'abcpharma@example.com', '1000', '500')
        pharmacie_info = json.loads(self.pharmacies_db.extraire_pharma_nom_like('ABC'))[0]
        self.assertEqual(pharmacie_info['nom'], 'Pharmacie ABC')

        # 2. Modifier une pharmacie
        self.pharmacies_db.modifier_pharmacie(1, 'Pharmacie XYZ', '456 Rue Secondaire', '0987654321', 'xyzpharma@example.com', '2000', '800')
        pharmacie_info = json.loads(self.pharmacies_db.extraire_pharma_nom_like('XYZ'))[0]
        self.assertEqual(pharmacie_info['nom'], 'Pharmacie XYZ')
        self.assertEqual(pharmacie_info['adresse'], '456 Rue Secondaire')

        # 3. Extraire toutes les pharmacies
        all_pharmacies = json.loads(self.pharmacies_db.extraire_tous_pharma())
        self.assertEqual(len(all_pharmacies), 1)

        # 4. Extraire des pharmacies par nom partiel
        pharmacies_info = json.loads(self.pharmacies_db.extraire_pharma_nom_like('XYZ'))
        self.assertEqual(len(pharmacies_info), 1)
        self.assertEqual(pharmacies_info[0]['nom'], 'Pharmacie XYZ')

        # 5. Supprimer une pharmacie (juste pour démonstration, bien que la méthode de suppression ne soit pas incluse)
        # self.pharmacies_db.supprimer_pharmacie(1)  # Si vous ajoutez une méthode de suppression
        # pharmacie_info = self.pharmacies_db.extraire_pharma_nom_like('XYZ')
        # self.assertEqual(len(pharmacie_info), 0)

if __name__ == '__main__':
    unittest.main()

