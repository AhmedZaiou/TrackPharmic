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

class Ventes:
    def __init__(self):
        self.dataset = dataset

    def create_table_ventes(self):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ventes (
                id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
                id_medicament INTEGER NOT NULL,
                id_commande_entre INTEGER,
                prix_achat REAL,
                prix_vente REAL,
                date_vente DATE NOT NULL,
                quantite_vendue INTEGER DEFAULT 0,
                total_facture REAL,
                id_client INTEGER,
                numero_facture VARCHAR(50),
                id_salarie INTEGER,
                id_stock_item INTEGER,
                FOREIGN KEY (id_medicament) REFERENCES Medicament (id_medicament),
                FOREIGN KEY (id_commande_entre) REFERENCES Commandes (id_commande),
                FOREIGN KEY (id_client) REFERENCES Clients (id_client),
                FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie),
                FOREIGN KEY (id_stock_item) REFERENCES Stock (id_stock)
            );
        """)
        conn.commit()
        conn.close()

    def ajouter_vente(self, id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture, id_client, numero_facture, id_salarie, id_stock_item):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Ventes (id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture, id_client, numero_facture, id_salarie, id_stock_item)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture, id_client, numero_facture, id_salarie, id_stock_item))
        conn.commit()
        conn.close()

    def supprimer_vente(self, id_vente):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ventes WHERE id_vente = ?", (id_vente,))
        conn.commit()
        conn.close()

    def modifier_vente(self, id_vente, id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture, id_client, numero_facture, id_salarie, id_stock_item):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Ventes
            SET id_medicament = ?, id_commande_entre = ?, prix_achat = ?, prix_vente = ?, date_vente = ?, quantite_vendue = ?, total_facture = ?, id_client = ?, numero_facture = ?, id_salarie = ?, id_stock_item = ?
            WHERE id_vente = ?
        """, (id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture, id_client, numero_facture, id_salarie, id_stock_item, id_vente))
        conn.commit()
        conn.close()

    def extraire_vente(self, id_vente):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ventes WHERE id_vente = ?", (id_vente,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_tous_ventes(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ventes")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)



import unittest
import json

class TestVentesMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls): 
        cls.ventes_db = Ventes()
        cls.ventes_db.create_table_ventes()

    def test_all_functions(self):
        # 1. Ajouter une vente
        self.ventes_db.ajouter_vente(1, 1, 100.0, 120.0, '2025-01-28', 5, 600.0, 1, 'F001', 1, 1)
        vente_info = json.loads(self.ventes_db.extraire_vente(1))
        self.assertEqual(vente_info['id_medicament'], 1)
        self.assertEqual(vente_info['prix_achat'], 100.0)
        self.assertEqual(vente_info['quantite_vendue'], 5)

        # 2. Modifier la vente
        self.ventes_db.modifier_vente(1, 1, 1, 110.0, 130.0, '2025-02-01', 6, 780.0, 2, 'F002', 1, 1)
        vente_info = json.loads(self.ventes_db.extraire_vente(1))
        self.assertEqual(vente_info['prix_achat'], 110.0)
        self.assertEqual(vente_info['quantite_vendue'], 6)
        self.assertEqual(vente_info['total_facture'], 780.0)

        # 3. Supprimer la vente
        self.ventes_db.supprimer_vente(1)
        vente_info = self.ventes_db.extraire_vente(1)
        self.assertIsNone(vente_info)

        # 4. Ajouter deux ventes pour le test d'extraction de toutes les ventes
        self.ventes_db.ajouter_vente(1, 1, 100.0, 120.0, '2025-01-28', 5, 600.0, 1, 'F001', 1, 1)
        self.ventes_db.ajouter_vente(2, 2, 150.0, 180.0, '2025-02-01', 3, 540.0, 2, 'F002', 2, 2)

        all_ventes = json.loads(self.ventes_db.extraire_tous_ventes())
        self.assertEqual(len(all_ventes), 2)

if __name__ == '__main__':
    unittest.main()
