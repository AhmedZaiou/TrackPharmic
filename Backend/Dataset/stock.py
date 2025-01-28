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

class Stock:
    def __init__(self):
        self.db_name = dataset

    def create_table_stock(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = '''
        CREATE TABLE IF NOT EXISTS Stock (
            id_stock INTEGER PRIMARY KEY AUTOINCREMENT,
            id_medicament INTEGER NOT NULL,
            id_commande INTEGER,
            id_salarie INTEGER,
            prix_achat REAL,
            prix_vente REAL,
            prix_conseille REAL,
            date_achat DATE,
            date_expiration DATE,
            stock_initial INTEGER DEFAULT 0,
            quantite_actuelle INTEGER DEFAULT 0,
            quantite_minimale INTEGER DEFAULT 0,
            quantite_maximale INTEGER,
            date_reception DATE,
            date_derniere_sortie DATE,
            FOREIGN KEY (id_medicament) REFERENCES Medicament (id_medicament) ON DELETE CASCADE,
            FOREIGN KEY (id_commande) REFERENCES Commandes (id_commande),
            FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
        );
        '''
        cursor.execute(query)
        conn.commit()
        conn.close()

    def ajouter_stock(self, id_medicament, id_commande, id_salarie, prix_achat, prix_vente,
                      prix_conseille, date_achat, date_expiration, stock_initial, quantite_actuelle,
                      quantite_minimale, quantite_maximale, date_reception, date_derniere_sortie):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = '''
        INSERT INTO Stock (id_medicament, id_commande, id_salarie, prix_achat, prix_vente, prix_conseille,
                           date_achat, date_expiration, stock_initial, quantite_actuelle, quantite_minimale,
                           quantite_maximale, date_reception, date_derniere_sortie)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        cursor.execute(query, (id_medicament, id_commande, id_salarie, prix_achat, prix_vente, prix_conseille,
                               date_achat, date_expiration, stock_initial, quantite_actuelle, quantite_minimale,
                               quantite_maximale, date_reception, date_derniere_sortie))
        conn.commit()
        conn.close()

    def supprimer_stock(self, id_stock):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = "DELETE FROM Stock WHERE id_stock = ?;"
        cursor.execute(query, (id_stock,))
        conn.commit()
        conn.close()

    def modifier_stock(self, id_stock, id_medicament, id_commande, id_salarie, prix_achat, prix_vente,
                       prix_conseille, date_achat, date_expiration, stock_initial, quantite_actuelle,
                       quantite_minimale, quantite_maximale, date_reception, date_derniere_sortie):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = '''
        UPDATE Stock SET
            id_medicament = ?, id_commande = ?, id_salarie = ?, prix_achat = ?, prix_vente = ?, prix_conseille = ?,
            date_achat = ?, date_expiration = ?, stock_initial = ?, quantite_actuelle = ?, quantite_minimale = ?,
            quantite_maximale = ?, date_reception = ?, date_derniere_sortie = ?
        WHERE id_stock = ?;
        '''
        cursor.execute(query, (id_medicament, id_commande, id_salarie, prix_achat, prix_vente, prix_conseille,
                               date_achat, date_expiration, stock_initial, quantite_actuelle, quantite_minimale,
                               quantite_maximale, date_reception, date_derniere_sortie, id_stock))
        conn.commit()
        conn.close()

    def extraire_medicament_id_stock(self, id_stock):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM Stock WHERE id_stock = ?;"
        cursor.execute(query, (id_stock,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_stock(self, id_stock):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM Stock WHERE id_stock = ?;"
        cursor.execute(query, (id_stock,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_tous_stock(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM Stock;"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

    def extraire_medicament_quantite_minimale_sup_0(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM Stock WHERE quantite_minimale > 0;"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)




import unittest
import json

class TestStockMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_stock.db'
        cls.stock_db = Stock()
        cls.stock_db.create_table_stock()

    def test_all_functions(self):
        # 1. Ajouter un stock
        self.stock_db.ajouter_stock(1, 1, 1, 100.0, 120.0, 110.0, '2025-01-28', '2025-12-31', 100, 50, 10, 200, '2025-01-29', '2025-01-27')
        stock_info = json.loads(self.stock_db.extraire_stock(1)) 
        self.assertEqual(stock_info['id_medicament'], 1)
        self.assertEqual(stock_info['prix_achat'], 100.0)
        self.assertEqual(stock_info['quantite_actuelle'], 50)

        # 2. Modifier le stock
        self.stock_db.modifier_stock(1, 1, 1, 1, 110.0, 130.0, 120.0, '2025-02-01', '2026-01-01', 150, 70, 20, 250, '2025-02-01', '2025-02-01')
        stock_info = json.loads(self.stock_db.extraire_stock(1))
        self.assertEqual(stock_info['prix_achat'], 110.0)
        self.assertEqual(stock_info['quantite_actuelle'], 70)
        self.assertEqual(stock_info['quantite_minimale'], 20)

        # 3. Supprimer le stock
        self.stock_db.supprimer_stock(1)
        stock_info = self.stock_db.extraire_stock(1)
        self.assertIsNone(stock_info)

        # 4. Ajouter deux stocks pour le test d'extraction avec quantite_minimale > 0
        self.stock_db.ajouter_stock(1, 1, 1, 100.0, 120.0, 110.0, '2025-01-28', '2025-12-31', 100, 50, 10, 200, '2025-01-29', '2025-01-27')
        self.stock_db.ajouter_stock(2, 2, 2, 200.0, 220.0, 210.0, '2025-02-01', '2026-12-31', 200, 80, 0, 250, '2025-02-02', '2025-02-01')

        stocks_minimale = json.loads(self.stock_db.extraire_medicament_quantite_minimale_sup_0())
        self.assertEqual(len(stocks_minimale), 1)
        self.assertEqual(stocks_minimale[0]['id_medicament'], 1)

        # 5. Extraire tous les stocks
        all_stocks = json.loads(self.stock_db.extraire_tous_stock())
        self.assertEqual(len(all_stocks), 2)

if __name__ == '__main__':
    unittest.main()
