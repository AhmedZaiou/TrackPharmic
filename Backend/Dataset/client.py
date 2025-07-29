import pymysql
from Frontend.utils.utils import *
from datetime import datetime


class Clients:
    @staticmethod
    def create_table_clients(conn):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
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
            """
            )
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de la création de la table Clients: {e}")
            

    @staticmethod
    def ajouter_client(
        conn, nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel
    ):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Clients (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel),
            )
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de la création de la table Clients: {e}")
            

    @staticmethod
    def supprimer_client(conn, id_client):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Clients WHERE id_client = %s", (id_client,))
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de la suppression du client: {e}")
            

    @staticmethod
    def modifier_client(
        conn,
        id_client,
        nom,
        prenom,
        cin,
        telephone,
        email,
        adresse,
        max_credit,
        credit_actuel,
    ):
        try : 
            conn = reconnexion_database(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Clients
                SET nom = %s, prenom = %s, cin = %s, telephone = %s, email = %s, adresse = %s,
                    max_credit = %s, credit_actuel = %s
                WHERE id_client = %s
            """,
                (
                    nom,
                    prenom,
                    cin,
                    telephone,
                    email,
                    adresse,
                    max_credit,
                    credit_actuel,
                    id_client,
                ),
            )
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de la modification du client: {e}")

    @staticmethod
    def modifier_info_client(
        conn,
        id_client,
        nom,
        prenom,
        cin,
        telephone,
        email,
        adresse,
        max_credit,
    ):
        try : 
            conn = reconnexion_database(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Clients
                SET nom = %s, prenom = %s, cin = %s, telephone = %s, email = %s, adresse = %s,
                    max_credit = %s
                WHERE id_client = %s
            """,
                (
                    nom,
                    prenom,
                    cin,
                    telephone,
                    email,
                    adresse,
                    max_credit,
                    id_client,
                ),
            )
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de la modification des informations du client: {e}")

    @staticmethod
    def ajouter_credit_client(conn, id_client, montant_credit):
        try: 
            conn = reconnexion_database(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Clients
                SET credit_actuel = credit_actuel + %s
                WHERE id_client = %s
            """,
                (montant_credit, id_client),
            )
            conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout de crédit au client: {e}")

    @staticmethod
    def extraire_client(conn, id_client):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM Clients WHERE id_client = %s", (id_client,))
            row = cursor.fetchone()

            return dict(row) if row else None
        except Exception as e:
            print(f"Erreur lors de l'extraction du client: {e}")
            return None

    @staticmethod
    def extraire_client_info(conn, nom, prenom, cin):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM Clients WHERE nom = %s AND prenom = %s AND cin = %s",
                (nom, prenom, cin),
            )
            row = cursor.fetchone()

            return dict(row) if row else None
        except Exception as e:
            print(f"Erreur lors de l'extraction des informations du client: {e}")
            return None

    @staticmethod
    def extraire_client_nom_like(conn, nom_part):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT nom, prenom, cin FROM Clients WHERE nom LIKE %s",
                ("%" + nom_part + "%",),
            )
            rows = cursor.fetchall()

            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Erreur lors de l'extraction des clients par nom: {e}")
            return []

    @staticmethod
    def extraire_tous_clients(conn):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM Clients order by nom;")
            rows = cursor.fetchall()

            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Erreur lors de l'extraction de tous les clients: {e}")
            return []

    @staticmethod
    def extraire_tous_clients_with_credit(conn):
        try:
            conn = reconnexion_database(conn)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM Clients WHERE credit_actuel > 0 ORDER BY nom; ")
            rows = cursor.fetchall()

            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Erreur lors de l'extraction des clients avec crédit: {e}")
            return []

    @staticmethod
    def cloture_journee(conn, date_jour=None):
        try:
            conn = reconnexion_database(conn)
            if date_jour is None:
                date_jour = datetime.now().strftime("%Y-%m-%d")

            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                """
                SELECT 
                    COUNT(*) AS total_clients,
                    SUM(max_credit) AS total_max_credit,
                    SUM(credit_actuel) AS total_credit_actuel
                FROM Clients
            """
            )
            result_clients = cursor.fetchone()

            return {
                "nombre_de_clients": result_clients["total_clients"] or 0,
                "credit_max_autorise": result_clients["total_max_credit"] or 0,
                "credit_actuel_pharmacie": result_clients["total_credit_actuel"] or 0,
            }
        except Exception as e:
            print(f"Erreur lors de la clôture de la journée: {e}")
            return {
                "nombre_de_clients": 0,
                "credit_max_autorise": 0,
                "credit_actuel_pharmacie": 0,
            }
