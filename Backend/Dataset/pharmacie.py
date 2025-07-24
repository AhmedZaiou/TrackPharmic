import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os


class Pharmacies:
    @staticmethod
    def create_table_pharmacies(conn):
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

    @staticmethod
    def ajouter_pharmacie(conn, nom, adresse, telephone, email, outvalue, invalue):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            INSERT INTO Pharmacies (nom, adresse, telephone, email, outvalue, invalue)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (nom, adresse, telephone, email, outvalue, invalue),
        )
        conn.commit()

    @staticmethod
    def modifier_pharmacie(
        conn, id_pharmacie, nom, adresse, telephone, email, outvalue, invalue
    ):
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

    @staticmethod
    def modifier_pharmacie_echange(conn, id_pharmacie, value, out_in):
        value = float(value)

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

    @staticmethod
    def extraire_tous_pharma(conn):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Pharmacies")
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    @staticmethod
    def extraire_pharma_nom_like(conn, nom_part):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT nom FROM Pharmacies WHERE nom LIKE %s", ("%" + nom_part + "%",)
        )
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    @staticmethod
    def extraire_pharma_nom(conn, nom):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Pharmacies WHERE nom = %s", (nom,))
        rows = cursor.fetchone()

        return dict(rows) if rows else None
