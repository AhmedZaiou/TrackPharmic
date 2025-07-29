import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os


class Pharmacies:
    @staticmethod
    def create_table_pharmacies(conn):
        try:
            conn = reconnexion_database(conn)
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
        except Exception as e:
            print(f"Erreur lors de la création de la table Pharmacies: {e}")
        

    @staticmethod
    def ajouter_pharmacie(conn, nom, adresse, telephone, email, outvalue, invalue):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                """
                INSERT INTO Pharmacies (nom, adresse, telephone, email, outvalue, invalue)
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
                (nom, adresse, telephone, email, outvalue, invalue),
            )
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout de la pharmacie: {e}")

    @staticmethod
    def modifier_pharmacie(
        conn, id_pharmacie, nom, adresse, telephone, email, outvalue, invalue
    ):
        try:
            conn = reconnexion_database(conn)
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
        except Exception as e:
            print(f"Erreur lors de la modification de la pharmacie: {e}")

    @staticmethod
    def modifier_pharmacie_echange(conn, id_pharmacie, value, out_in):
        try:
            conn = reconnexion_database(conn)
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
        except Exception as e:
            print(f"Erreur lors de la modification de l'échange de la pharmacie: {e}")

    @staticmethod
    def extraire_tous_pharma(conn):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM Pharmacies")
            rows = cursor.fetchall()

            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Erreur lors de l'extraction des pharmacies: {e}")
            return []

    @staticmethod
    def extraire_pharma_nom_like(conn, nom_part):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT nom FROM Pharmacies WHERE nom LIKE %s", ("%" + nom_part + "%",)
            )
            rows = cursor.fetchall()

            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Erreur lors de l'extraction des pharmacies par nom: {e}")
            return []

    @staticmethod
    def extraire_pharma_nom(conn, nom):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM Pharmacies WHERE nom = %s", (nom,))
            rows = cursor.fetchone()

            return dict(rows) if rows else None
        except Exception as e:
            print(f"Erreur lors de l'extraction de la pharmacie par nom: {e}")
            return None
