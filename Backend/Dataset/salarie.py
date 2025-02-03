import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json

class Salaries:
    @staticmethod
    def create_table_salaries():
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Salaries (
                id_salarie INTEGER PRIMARY KEY AUTO_INCREMENT,
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

    @staticmethod
    def ajouter_salarie(nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            INSERT INTO Salaries (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_salarie(id_salarie):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("DELETE FROM Salaries WHERE id_salarie = %s", (id_salarie,))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_salarie(id_salarie, nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            UPDATE Salaries
            SET nom = %s, prenom = %s, cin = %s, telephone = %s, email = %s, adresse = %s, photo = %s, salaire = %s, 
                type_contrat = %s, date_embauche = %s, grade = %s, password_hash = %s
            WHERE id_salarie = %s
        """, (nom, prenom, cin, telephone, email, adresse, photo, salaire, type_contrat, date_embauche, grade, password_hash, id_salarie))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_salarie(id_salarie):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Salaries WHERE id_salarie = %s", (id_salarie,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_salarie_login(nom, password_hash):
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Salaries WHERE nom = %s AND password_hash = %s", (nom, password_hash))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_tous_salaries():
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Salaries")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_salaries():
        # Connect to the database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''SELECT id_salarie, nom, prenom FROM Salaries''')
        result = cursor.fetchall()
        conn.close()
        return [row['id_salarie'] for row in result], [row['nom'] for row in result], [row['prenom'] for row in result]
