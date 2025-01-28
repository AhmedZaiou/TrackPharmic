 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Achats:
    def __init__(self):
        self.dataset = dataset

    def create_table_achats(self):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Achats (
                id_achat INTEGER PRIMARY KEY AUTOINCREMENT,
                id_medicament INTEGER NOT NULL,
                id_fournisseur INTEGER,
                quantite_achetee INTEGER DEFAULT 0,
                prix_achat_unitaire REAL,
                prix_vente_unitaire REAL,
                date_achat DATE NOT NULL,
                date_expiration DATE,
                id_salarie INTEGER,
                FOREIGN KEY (id_medicament) REFERENCES Medicament (id_medicament),
                FOREIGN KEY (id_fournisseur) REFERENCES Fournisseur (id_fournisseur),
                FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
            );
        """)
        conn.commit()
        conn.close()

    def ajouter_achat(self, id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, date_achat, date_expiration, id_salarie):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Achats (id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, date_achat, date_expiration, id_salarie)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, date_achat, date_expiration, id_salarie))
        conn.commit()
        conn.close()

    def supprimer_achat(self, id_achat):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Achats WHERE id_achat = ?", (id_achat,))
        conn.commit()
        conn.close()

    def modifier_achat(self, id_achat, id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, date_achat, date_expiration, id_salarie):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Achats
            SET id_medicament = ?, id_fournisseur = ?, quantite_achetee = ?, prix_achat_unitaire = ?, prix_vente_unitaire = ?, date_achat = ?, date_expiration = ?, id_salarie = ?
            WHERE id_achat = ?
        """, (id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, date_achat, date_expiration, id_salarie, id_achat))
        conn.commit()
        conn.close()

    def extraire_achat(self, id_achat):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Achats WHERE id_achat = ?", (id_achat,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_tous_achats(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Achats")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

