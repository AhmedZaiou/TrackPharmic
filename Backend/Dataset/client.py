import pymysql
from Frontend.utils.utils import *
from datetime import datetime

class Clients:
    @staticmethod
    def create_table_clients():
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clients (
                id_client INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(100),
                prenom VARCHAR(100),
                cin VARCHAR(20) UNIQUE,
                telephone VARCHAR(15),
                email VARCHAR(100),
                adresse TEXT,
                max_credit DECIMAL(10,2),
                credit_actuel DECIMAL(10,2) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_client(nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Clients (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_client(id_client):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clients WHERE id_client = %s", (id_client,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_client(id_client, nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Clients
            SET nom = %s, prenom = %s, cin = %s, telephone = %s, email = %s, adresse = %s,
                max_credit = %s, credit_actuel = %s
            WHERE id_client = %s
        """, (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel, id_client))
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_credit_client(id_client, montant_credit):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Clients
            SET credit_actuel = credit_actuel + %s
            WHERE id_client = %s
        """, (montant_credit, id_client))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_client(id_client):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Clients WHERE id_client = %s", (id_client,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_client_info(nom, prenom, cin):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Clients WHERE nom = %s AND prenom = %s AND cin = %s", (nom, prenom, cin))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_client_nom_like(nom_part):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT nom, prenom, cin FROM Clients WHERE nom LIKE %s", ('%' + nom_part + '%',))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_tous_clients():
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Clients")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_tous_clients_with_credit():
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Clients WHERE credit_actuel > 0")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def cloture_journee(date_jour=None):
        if date_jour is None:
            date_jour = datetime.now().strftime("%Y-%m-%d")
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT 
                COUNT(*) AS total_clients,
                SUM(max_credit) AS total_max_credit,
                SUM(credit_actuel) AS total_credit_actuel
            FROM Clients
            WHERE credit_actuel > 0 
        """)
        result_clients = cursor.fetchone()
        conn.close()
        return {
            "nombre_de_clients": result_clients['total_clients'],
            "credit_max_autorise": result_clients['total_max_credit'] or 0,
            "credit_actuel_pharmacie": result_clients['total_credit_actuel'] or 0
        }
