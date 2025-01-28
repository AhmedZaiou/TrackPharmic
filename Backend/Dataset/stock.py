 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

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



