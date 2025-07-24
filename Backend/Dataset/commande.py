import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json

from Backend.Dataset.salarie import Salaries


class Commandes:
    @staticmethod
    def __init__():
        dataset = dataset

    @staticmethod
    def create_table_commandes(conn):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Commandes (
                id_commande INT PRIMARY KEY AUTO_INCREMENT,
                id_fournisseur INT,
                date_commande DATE NOT NULL,
                date_reception_prev DATE,
                statut_reception VARCHAR(50),
                receptionniste VARCHAR(100),
                produits_recus TEXT,
                date_reception DATE,
                id_salarie INT,
                status_incl VARCHAR(50),
                Liste_Produits TEXT
            );
        """
        )
        conn.commit()

    @staticmethod
    def ajouter_commande(
        conn,
        Liste_Produits,
        id_fournisseur,
        date_commande,
        date_reception_prev,
        statut_reception,
        receptionniste,
        produits_recus,
        date_reception,
        id_salarie,
        status_incl,
    ):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            INSERT INTO Commandes (id_fournisseur, date_commande, date_reception_prev, statut_reception, receptionniste, produits_recus, date_reception, id_salarie, status_incl, Liste_Produits)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                id_fournisseur,
                date_commande,
                date_reception_prev,
                statut_reception,
                receptionniste,
                produits_recus,
                date_reception,
                id_salarie,
                status_incl,
                Liste_Produits,
            ),
        )
        conn.commit()

    @staticmethod
    def supprimer_commande(conn, id_commande):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("DELETE FROM Commandes WHERE id_commande = %s", (id_commande,))
        conn.commit()

    @staticmethod
    def modifier_commande(
        conn,
        Liste_Produits,
        id_commande,
        id_fournisseur,
        date_commande,
        date_reception_prev,
        statut_reception,
        receptionniste,
        produits_recus,
        date_reception,
        id_salarie,
        status_incl,
    ):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            UPDATE Commandes
            SET id_fournisseur = %s, date_commande = %s, date_reception_prev = %s, statut_reception = %s, receptionniste = %s, produits_recus = %s, date_reception = %s, id_salarie = %s, status_incl = %s, Liste_Produits = %s
            WHERE id_commande = %s
        """,
            (
                id_fournisseur,
                date_commande,
                date_reception_prev,
                statut_reception,
                receptionniste,
                produits_recus,
                date_reception,
                id_salarie,
                status_incl,
                Liste_Produits,
                id_commande,
            ),
        )
        conn.commit()

    @staticmethod
    def complet_commande(conn, id_commande):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            UPDATE Commandes
            SET statut_reception = 'Complète', date_reception = %s
            WHERE id_commande = %s
        """,
            (datetime.now(), id_commande),
        )
        conn.commit()

    @staticmethod
    def extraire_commande(conn, id_commande):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Commandes WHERE id_commande = %s", (id_commande,))
        row = cursor.fetchone()

        return dict(row) if row else None

    @staticmethod
    def extraire_tous_commandes(conn):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Commandes")
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    @staticmethod
    def extraire_tous_commandes_table(conn):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Commandes WHERE Statut_Reception != 'Complète'")
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    @staticmethod
    def get_commandes_jour(conn):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """SELECT ID_Commande FROM Commandes WHERE DATE(Date_Commande) = %s""",
            (datetime.now().date(),),
        )
        result = cursor.fetchall()

        return [dict(row) for row in result]

    @staticmethod
    def get_commandes_recues_jour(conn):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """SELECT ID_Commande FROM Commandes WHERE DATE(Date_Reception) = %s""",
            (datetime.now().date(),),
        )
        result = cursor.fetchall()

        return [dict(row) for row in result]

    @staticmethod
    def get_commandes_jour_salarie(conn, salarie):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """SELECT ID_Commande FROM Commandes WHERE DATE(Date_Commande) = %s AND ID_Salarie = %s""",
            (datetime.now().date(), salarie),
        )
        result = cursor.fetchall()

        return [dict(row) for row in result]

    @staticmethod
    def get_commandes_recues_jour_salarie(conn, salarie):
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """SELECT ID_Commande FROM Commandes WHERE DATE(Date_Reception) = %s AND ID_Salarie = %s""",
            (datetime.now().date(), salarie),
        )
        result = cursor.fetchall()

        return [dict(row) for row in result]

    @staticmethod
    def statistic_commande_salarie(conn, salarie):
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_jour = datetime.now().date()

        cursor.execute(
            """SELECT COUNT(*) as total FROM Commandes 
                        WHERE DATE(Date_Commande) = %s 
                        AND ID_Salarie = %s""",
            (date_jour, salarie),
        )
        total_commandes = cursor.fetchone()["total"]

        cursor.execute(
            """SELECT COUNT(*) as recues FROM Commandes 
                        WHERE DATE(Date_Reception) = %s 
                        AND ID_Salarie = %s""",
            (date_jour, salarie),
        )
        commandes_recues = cursor.fetchone()["recues"]

        commandes_en_attente = total_commandes - commandes_recues

        return {
            "salarie": salarie,
            "date": date_jour,
            "total_commandes": total_commandes,
            "commandes_recues": commandes_recues,
            "commandes_en_attente": commandes_en_attente,
        }

    @staticmethod
    def statistic_commande_generale(conn):
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        date_jour = datetime.now().date()

        cursor.execute(
            """SELECT COUNT(*) as total FROM Commandes 
                        WHERE DATE(Date_Commande) = %s""",
            (date_jour,),
        )
        total_commandes = cursor.fetchone()["total"]

        cursor.execute(
            """SELECT COUNT(*) as recues FROM Commandes 
                        WHERE DATE(Date_Reception) = %s""",
            (date_jour,),
        )
        commandes_recues = cursor.fetchone()["recues"]

        commandes_en_attente = total_commandes - commandes_recues

        return {
            "date": date_jour,
            "total_commandes": total_commandes or 0,
            "commandes_recues": commandes_recues or 0,
            "commandes_en_attente": commandes_en_attente or 0,
        }

    @staticmethod
    def cloture_journee(conn):
        commande_cloture = {}
        commande_cloture["statistique general"] = Commandes.statistic_commande_generale(
            conn
        )
        commande_cloture["statistique par salarie"] = []
        salaries, noms, prenoms = Salaries.get_salaries(conn)
        for salarie, nom, prenom in zip(salaries, noms, prenoms):
            performance = {"salarie": str(nom) + " " + str(prenom)}
            performance["statistique"] = Commandes.statistic_commande_salarie(
                conn, salarie
            )
            commande_cloture["statistique par salarie"].append(performance)

        return commande_cloture
