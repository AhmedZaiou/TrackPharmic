import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json


class Fournisseur:
    @staticmethod
    def create_table_fournisseur():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Fournisseur (
                id_fournisseur INTEGER PRIMARY KEY AUTO_INCREMENT,
                nom_fournisseur VARCHAR(100),
                telephone VARCHAR(15),
                email VARCHAR(100),
                adresse TEXT,
                ville VARCHAR(50),
                pays VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )
        conn.commit()
        conn.close()

    @staticmethod
    def ajouter_fournisseur(nom_fournisseur, telephone, email, adresse, ville, pays):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Fournisseur (nom_fournisseur, telephone, email, adresse, ville, pays)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (nom_fournisseur, telephone, email, adresse, ville, pays),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_fournisseur(id_fournisseur):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Fournisseur WHERE id_fournisseur = %s", (id_fournisseur,)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_fournisseur(
        id_fournisseur, nom_fournisseur, telephone, email, adresse, ville, pays
    ):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Fournisseur
            SET nom_fournisseur = %s, telephone = %s, email = %s, adresse = %s, ville = %s, pays = %s
            WHERE id_fournisseur = %s
        """,
            (nom_fournisseur, telephone, email, adresse, ville, pays, id_fournisseur),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_fournisseur(id_fournisseur):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Fournisseur WHERE id_fournisseur = %s", (id_fournisseur,)
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_fournisseur_nom(nom_fournisseur):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Fournisseur WHERE nom_fournisseur = %s", (nom_fournisseur,)
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_fournisseur_nom_like(nom_fournisseur_like):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Fournisseur WHERE nom_fournisseur LIKE %s",
            ("%" + nom_fournisseur_like + "%",),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_tous_fournisseurs():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Fournisseur")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
