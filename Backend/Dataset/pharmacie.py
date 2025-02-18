import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os


class Pharmacies:
    @staticmethod
    def create_table_pharmacies():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Pharmacies (
                id_pharmacie INTEGER PRIMARY KEY AUTO_INCREMENT,
                nom VARCHAR(100),
                adresse TEXT,
                telephone VARCHAR(15),
                email VARCHAR(100),
                outvalue TEXT,
                invalue TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_pharmacie(nom, adresse, telephone, email, outvalue, invalue):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            INSERT INTO Pharmacies (nom, adresse, telephone, email, outvalue, invalue)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (nom, adresse, telephone, email, outvalue, invalue),
        )
        conn.commit()
        conn.close()
    

    @staticmethod
    def modifier_pharmacie(
        id_pharmacie, nom, adresse, telephone, email, outvalue, invalue
    ):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            UPDATE Pharmacies
            SET nom = %s, adresse = %s, telephone = %s, email = %s, outvalue = %s, invalue = %s
            WHERE id_pharmacie = %s
        """,
            (nom, adresse, telephone, email, outvalue, invalue, id_pharmacie),
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def modifier_pharmacie_echange(
        id_pharmacie, value, out_in
    ):
        value = float(value)
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if out_in == 1:
            cursor.execute(
            """
            UPDATE Pharmacies
            SET  outvalue = outvalue + %s
            WHERE id_pharmacie = %s
            """,
                (value, id_pharmacie),
            )

        else:
            cursor.execute(
            """
            UPDATE Pharmacies
            SET  invalue = invalue + %s
            WHERE id_pharmacie = %s
            """,
                (value, id_pharmacie),
            )
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_tous_pharma():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Pharmacies")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_pharma_nom_like(nom_part):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT nom FROM Pharmacies WHERE nom LIKE %s", ("%" + nom_part + "%",)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_pharma_nom(nom):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Pharmacies WHERE nom = %s", (nom,))
        rows = cursor.fetchone()
        conn.close()
        return dict(rows) if rows else None
