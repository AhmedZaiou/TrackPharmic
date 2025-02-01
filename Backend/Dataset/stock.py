 
import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

class Stock: 
    @staticmethod
    def create_table_stock():
        conn = sqlite3.connect(dataset)
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

    @staticmethod
    def ajouter_stock(  id_medicament, id_commande, id_salarie, prix_achat, prix_vente,
                      prix_conseille, date_achat, date_expiration, stock_initial, quantite_actuelle,
                      quantite_minimale, quantite_maximale, date_reception, date_derniere_sortie):
        conn =  sqlite3.connect(dataset)
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

    @staticmethod
    def supprimer_stock(  id_stock):
        conn =  sqlite3.connect(dataset)
        cursor = conn.cursor()
        query = "DELETE FROM Stock WHERE id_stock = ?;"
        cursor.execute(query, (id_stock,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_stock(  id_stock, id_medicament, id_commande, id_salarie, prix_achat, prix_vente,
                       prix_conseille, date_achat, date_expiration, stock_initial, quantite_actuelle,
                       quantite_minimale, quantite_maximale, date_reception, date_derniere_sortie):
        conn =  sqlite3.connect(dataset)
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
    
    @staticmethod
    def effectuer_vente_stock(  id_stock, quantite_vendu):
        conn =  sqlite3.connect(dataset)
        cursor = conn.cursor()
        query = '''
        UPDATE Stock SET  quantite_actuelle = quantite_actuelle - ?
        WHERE id_stock = ?;
        '''
        cursor.execute(query, ( quantite_vendu, id_stock))
        cursor.execute("DELETE FROM Stock WHERE quantite_actuelle = 0;")
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_medicament_id_stock( id_medicament):
        conn =  sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM Stock WHERE id_medicament = ?;"
        cursor.execute(query, (id_medicament,))
        row = cursor.fetchall()
        conn.close()
        if row is None or len(row) == 0:
            return None 
        else:
            dic = {}
            dic['id_medicament'] = row[0]['id_medicament']
            dic['prix_vente'] = [item['prix_vente'] for item in row]
            dic['date_expiration'] = [item['date_expiration'] for item in row]
            dic['quantite_actuelle'] = sum([int(item['quantite_actuelle']) for item in row])
            dic['list_quantity'] = [int(item['quantite_actuelle']) for item in row]
            dic['id_commande'] = [item['id_commande'] for item in row]
            dic['id_stock'] = [item['ID_Stock'] for item in row]
            dic['prix_achat'] = [item['prix_achat'] for item in row]
            return dic 

    @staticmethod
    def extraire_stock(  id_stock):
        conn =  sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM Stock WHERE id_stock = ?;"
        cursor.execute(query, (id_stock,))
        row = cursor.fetchone()
        conn.close()
        return  dict(row)  if row else None

    @staticmethod
    def extraire_tous_stock():
        conn =  sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM Stock;"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 

    @staticmethod
    def extraire_medicament_quantite_minimale_sup_0():
        conn =  sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM Stock WHERE quantite_minimale > 0;"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return  [dict(row) for row in rows] 




    @staticmethod
    def get_situation_stock():
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id_medicament, quantite_actuelle FROM Stock")
        result = cursor.fetchall()
        conn.close()
        return {row['id_medicament']: row['quantite_actuelle'] for row in result}
    
    @staticmethod
    def calculer_total_achat_vente():
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(prix_achat) AS total_achat, SUM(prix_vente) AS total_vente FROM Stock")
        result = cursor.fetchone()
        conn.close()

        return result['total_achat'], result['total_vente']
    

    def cloture_journee():
        today = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()

        # Total des achats et ventes pour la journée
        cursor.execute("""
            SELECT SUM(prix_achat) AS total_achat, SUM(prix_vente) AS total_vente 
            FROM Stock 
            WHERE date_reception = ? OR date_derniere_sortie = ?
        """, (today, today))
        result = cursor.fetchone() 
        total_achat = result[0]
        total_vente = result[0]

        # Quantités totales en stock aujourd'hui
        cursor.execute("""
            SELECT SUM(quantite_actuelle) AS total_quantite 
            FROM Stock 
            WHERE date_reception = ? OR date_derniere_sortie = ?
        """, (today, today))
        result = cursor.fetchone() 
        total_quantite = result[0]

        # Quantités minimales non respectées aujourd'hui
        cursor.execute("""
            SELECT COUNT(*) AS count 
            FROM Stock 
            WHERE quantite_actuelle < quantite_minimale 
            AND (date_reception = ? OR date_derniere_sortie = ?)
        """, (today, today))
        result = cursor.fetchone() 
        quantites_minimales_non_respectees = result[0]

        

        # Médicaments proches de la date d'expiration aujourd'hui
        cursor.execute("""
            SELECT COUNT(*) AS count 
            FROM Stock 
            WHERE date_expiration <= DATE('now', '+30 days') 
            AND (date_reception = ? OR date_derniere_sortie = ?)
        """, (today, today))
        result = cursor.fetchone() 
        medicaments_proches_expiration = result[0]

        

        conn.close()

        return {
            "Total des achats pour la journée": total_achat,
            "Total des ventes pour la journée": total_vente,
            "Quantités totales en stock aujourd'hui": total_quantite,
            "Quantités minimales non respectées aujourd'hui": quantites_minimales_non_respectees, 
            "Nombre Médicaments proches de la date d'expiration aujourd'hui": medicaments_proches_expiration
        }
