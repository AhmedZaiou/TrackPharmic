 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os 

class Commandes:
    def __init__(self):
        self.dataset = dataset

    def create_table_commandes(self):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Commandes (
                id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
                id_fournisseur INTEGER,
                date_commande DATE NOT NULL,
                date_reception_prev DATE,
                statut_reception TEXT,
                receptionniste VARCHAR(100),
                produits_recus TEXT,
                date_reception DATE,
                id_salarie INTEGER,
                status_incl TEXT,
                FOREIGN KEY (id_fournisseur) REFERENCES Fournisseur (id_fournisseur),
                FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
            );
        """)
        conn.commit()
        conn.close()

    def ajouter_commande(self, id_fournisseur, date_commande, date_reception_prev, statut_reception, receptionniste, produits_recus, date_reception, id_salarie, status_incl):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Commandes (id_fournisseur, date_commande, date_reception_prev, statut_reception, receptionniste, produits_recus, date_reception, id_salarie, status_incl)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_fournisseur, date_commande, date_reception_prev, statut_reception, receptionniste, produits_recus, date_reception, id_salarie, status_incl))
        conn.commit()
        conn.close()

    def supprimer_commande(self, id_commande):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Commandes WHERE id_commande = ?", (id_commande,))
        conn.commit()
        conn.close()

    def modifier_commande(self, id_commande, id_fournisseur, date_commande, date_reception_prev, statut_reception, receptionniste, produits_recus, date_reception, id_salarie, status_incl):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Commandes
            SET id_fournisseur = ?, date_commande = ?, date_reception_prev = ?, statut_reception = ?, receptionniste = ?, produits_recus = ?, date_reception = ?, id_salarie = ?, status_incl = ?
            WHERE id_commande = ?
        """, (id_fournisseur, date_commande, date_reception_prev, statut_reception, receptionniste, produits_recus, date_reception, id_salarie, status_incl, id_commande))
        conn.commit()
        conn.close()

    def complet_commande(self, id_commande):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Commandes
            SET statut_reception = 'Complète', date_reception = ?
            WHERE id_commande = ?
        """, ('2025-01-28', id_commande))  # You can set the reception date dynamically
        conn.commit()
        conn.close()

    def extraire_commande(self, id_commande):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Commandes WHERE id_commande = ?", (id_commande,))
        row = cursor.fetchone()
        conn.close()
        return json.dumps(dict(row), default=str) if row else None

    def extraire_tous_commandes(self):
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Commandes")
        rows = cursor.fetchall()
        conn.close()
        return json.dumps([dict(row) for row in rows], default=str)

