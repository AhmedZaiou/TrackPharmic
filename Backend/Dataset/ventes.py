 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

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

