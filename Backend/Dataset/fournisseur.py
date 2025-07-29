import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json


class Fournisseur:
    @staticmethod
    def create_table_fournisseur(conn):
        try:
            conn = reconnexion_database(conn)
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
        except Exception as e:
            print(f"Erreur lors de la création de la table Fournisseur : {e}")
            

    @staticmethod
    def ajouter_fournisseur(
        conn, nom_fournisseur, telephone, email, adresse, ville, pays
    ):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Fournisseur (nom_fournisseur, telephone, email, adresse, ville, pays)
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
                (nom_fournisseur, telephone, email, adresse, ville, pays),
            )
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout du fournisseur : {e}")
            
    @staticmethod
    def supprimer_fournisseur(conn, id_fournisseur):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM Fournisseur WHERE id_fournisseur = %s", (id_fournisseur,)
            )
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de la suppression du fournisseur : {e}")

    @staticmethod
    def modifier_fournisseur(
        conn, id_fournisseur, nom_fournisseur, telephone, email, adresse, ville, pays
    ):
        try:
            conn = reconnexion_database(conn)
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
        except Exception as e:
            print(f"Erreur lors de la modification du fournisseur : {e}")

    @staticmethod
    def extraire_fournisseur(conn, id_fournisseur):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM Fournisseur WHERE id_fournisseur = %s", (id_fournisseur,)
            )
            row = cursor.fetchone()

            return dict(row) if row else None
        except Exception as e:
            print(f"Erreur lors de l'extraction du fournisseur : {e}")
            return None

    @staticmethod
    def extraire_fournisseur_nom(conn, nom_fournisseur):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM Fournisseur WHERE nom_fournisseur = %s", (nom_fournisseur,)
            )
            row = cursor.fetchone()

            return dict(row) if row else None
        except Exception as e:
            print(f"Erreur lors de l'extraction du fournisseur par nom : {e}")
            return None

    @staticmethod
    def extraire_fournisseur_nom_like(conn, nom_fournisseur_like):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM Fournisseur WHERE nom_fournisseur LIKE %s",
                ("%" + nom_fournisseur_like + "%",),
            )
            rows = cursor.fetchall()

            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Erreur lors de l'extraction des fournisseurs par nom : {e}")
            return []

    @staticmethod
    def extraire_tous_fournisseurs(conn):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM Fournisseur")
            rows = cursor.fetchall()

            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Erreur lors de l'extraction de tous les fournisseurs : {e}")
            return []
