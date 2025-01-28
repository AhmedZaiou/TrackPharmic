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

class Salaries:
    def __init__(self):
        self.dataset = dataset

    def create_table_salaries(self):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Salaries (
                id_salarie INTEGER PRIMARY KEY AUTOINCREMENT,
                nom VARCHAR(100),
                prenom VARCHAR(100),
                cin VARCHAR(20) UNIQUE,
                telephone VARCHAR(15),
                email VARCHAR(100),
                adresse TEXT,
                photo TEXT,
                salaire REAL,
                type_contrat VARCHAR(50),
                date_embauche DATE,
                grade VARCHAR(50),
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    def ajouter_salarie(self, nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Salaries (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash))
        conn.commit()
        conn.close()

    def supprimer_salarie(self, id_salarie):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Salaries WHERE id_salarie = ?", (id_salarie,))
        conn.commit()
        conn.close()

    def modifier_salarie(self, id_salarie, nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Salaries
            SET nom = ?, prenom = ?, cin = ?, telephone = ?, email = ?, adresse = ?, photo = ?, salaire = ?, type_contrat = ?, date_embauche = ?, grade = ?, password_hash = ?
            WHERE id_salarie = ?
        """, (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash, id_salarie))
        conn.commit()
        conn.close()

    def extraire_salarie(self, id_salarie):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Salaries WHERE id_salarie = ?", (id_salarie,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_salarie_login(self, nom, password_hash):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Salaries WHERE nom = ? AND password_hash = ?", (nom, password_hash))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_tous_salaries(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Salaries")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)



import unittest
import json

class TestSalariesMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_salaries.db'
        cls.salaries_db = Salaries()
        cls.salaries_db.create_table_salaries()

    def test_all_functions(self):
        # 1. Ajouter un salarié
        self.salaries_db.ajouter_salarie('John', 'Doe', '123456', '0123456789', 'johndoe@example.com', '123 Main St', 'photo.jpg', 3000.0, 'CDI', '2025-01-28', 'Junior', 'passwordhash')
        salarie_info = json.loads(self.salaries_db.extraire_salarie(1))
        self.assertEqual(salarie_info['nom'], 'John')
        self.assertEqual(salarie_info['prenom'], 'Doe')

        # 2. Modifier un salarié
        self.salaries_db.modifier_salarie(1, 'John', 'Doe', '123456', '0987654321', 'johndoe@newmail.com', '456 Another St', 'newphoto.jpg', 3500.0, 'CDI', '2025-02-01', 'Senior', 'newpasswordhash')
        salarie_info = json.loads(self.salaries_db.extraire_salarie(1))
        self.assertEqual(salarie_info['telephone'], '0987654321')
        self.assertEqual(salarie_info['email'], 'johndoe@newmail.com')

        # 3. Extraire un salarié par login
        salarie_info = json.loads(self.salaries_db.extraire_salarie_login('John', 'newpasswordhash'))
        self.assertEqual(salarie_info['nom'], 'John')
        self.assertEqual(salarie_info['prenom'], 'Doe')

        # 4. Supprimer un salarié
        self.salaries_db.supprimer_salarie(1)
        salarie_info = self.salaries_db.extraire_salarie(1)
        self.assertIsNone(salarie_info)

        # 5. Ajouter deux salariés pour le test d'extraction de tous les salariés
        self.salaries_db.ajouter_salarie('Jane', 'Smith', '654321', '0123456789', 'janesmith@example.com', '789 Another St', 'photo2.jpg', 3200.0, 'CDD', '2025-02-28', 'Junior', 'passwordhash2')
        self.salaries_db.ajouter_salarie('Jack', 'White', '789012', '0123456789', 'jackwhite@example.com', '456 Main St', 'photo3.jpg', 3300.0, 'CDI', '2025-03-01', 'Senior', 'passwordhash3')

        all_salaries = json.loads(self.salaries_db.extraire_tous_salaries())
        self.assertEqual(len(all_salaries), 2)

if __name__ == '__main__':
    unittest.main()

