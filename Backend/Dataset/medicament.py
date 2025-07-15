import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json


class Medicament:
    @staticmethod
    def supprimer_toute_base_donnees():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table['Tables_in_' + database]};")
        conn.commit()
        conn.close()

    @staticmethod
    def create_table_medicament():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Medicament (
            ID_Medicament INT AUTO_INCREMENT PRIMARY KEY,
            Nom VARCHAR(255) NOT NULL,
            Caracteristique TEXT,
            Code_EAN_13 VARCHAR(13),
            Medicament_Generique VARCHAR(255),
            Prix_Officine DECIMAL(10, 2),
            Prix_Public_De_Vente DECIMAL(10, 2),
            Prix_Base_Remboursement DECIMAL(10, 2),
            Prix_Hospitalier DECIMAL(10, 2),
            Substance_Active_DCI VARCHAR(255),
            Classe_Therapeutique VARCHAR(255),
            Min_Stock INT,
            Stock_Actuel INT
        );
        """
        )
        conn.commit()
        conn.close()

    @staticmethod
    def create_table_new_medicament():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS New_medicament (
            ID_Medicament INT AUTO_INCREMENT PRIMARY KEY,
            Nom VARCHAR(255) NOT NULL,
            Caracteristique TEXT,
            Code_EAN_13 VARCHAR(13),
            Medicament_Generique VARCHAR(255),
            Prix_Officine DECIMAL(10, 2),
            Prix_Public_De_Vente DECIMAL(10, 2),
            Prix_Base_Remboursement DECIMAL(10, 2),
            Prix_Hospitalier DECIMAL(10, 2),
            Substance_Active_DCI VARCHAR(255),
            Classe_Therapeutique VARCHAR(255),
            Min_Stock INT,
            Stock_Actuel INT
        );
        """
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def ajouter_medicament_code_barre(code_barre):
        """
        Ajoute un médicament à la base de données à partir du code-barres.
        Le code-barres est utilisé pour extraire les informations du médicament.
        """
        from Backend.Datascraping.extraire_medicament import scrap_page_url

        values = scrap_page_url(code_barre)
        if values[0] is 'Page not found':
            return None

        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""INSERT INTO Medicament (
            Nom,
            Caracteristique,
            Code_EAN_13,
            Medicament_Generique,
            Prix_Officine,
            Prix_Public_De_Vente,
            Prix_Base_Remboursement,
            Prix_Hospitalier,
            Substance_Active_DCI,
            Classe_Therapeutique,
            Min_Stock,
            Stock_Actuel
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", values)
        conn.commit()
        conn.close()
        return True

            

    @staticmethod
    def ajouter_medicament(
        nom,
        caracteristique,
        code_ean_13,
        generique,
        prix_officine,
        prix_public,
        prix_remboursement,
        prix_hospitalier,
        substance_active,
        classe_therapeutique,
        min_stock,
        stock_actuel,
    ):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
        INSERT INTO Medicament (Nom, Caracteristique, Code_EAN_13, Medicament_Generique, Prix_Officine, Prix_Public_De_Vente, Prix_Base_Remboursement, Prix_Hospitalier, Substance_Active_DCI, Classe_Therapeutique, Min_Stock, Stock_Actuel)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
            (
                nom,
                caracteristique,
                code_ean_13,
                generique,
                prix_officine,
                prix_public,
                prix_remboursement,
                prix_hospitalier,
                substance_active,
                classe_therapeutique,
                min_stock,
                stock_actuel,
            ),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer_medicament(id_medicament):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "DELETE FROM Medicament WHERE ID_Medicament = %s;", (id_medicament,)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def modifier_medicament(id_medicament, **kwargs):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        columns = [f"{key} = %s" for key in kwargs.keys()]
        values = list(kwargs.values()) + [id_medicament]
        query = f"UPDATE Medicament SET {', '.join(columns)} WHERE ID_Medicament = %s;"
        cursor.execute(query, values)
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_medicament(id_medicament):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Medicament WHERE ID_Medicament = %s;", (id_medicament,)
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def effectuer_vente_medicament(id_medicament, quantite_vendu):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
        UPDATE Medicament SET Stock_Actuel = Stock_Actuel - %s
        WHERE ID_Medicament = %s;
        """
        cursor.execute(query, (quantite_vendu, id_medicament))
        conn.commit()
        conn.close()

    def effectuer_stock_medicament(id_medicament, quantite_vendu):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
        UPDATE Medicament SET Stock_Actuel = Stock_Actuel + %s
        WHERE ID_Medicament = %s;
        """
        cursor.execute(query, (quantite_vendu, id_medicament))
        conn.commit()
        conn.close()

    @staticmethod
    def extraire_medicament_code_barre(code_barre):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Medicament WHERE Code_EAN_13 = %s;", (code_barre,)
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def extraire_medicament_code_barre_like(pattern):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Medicament WHERE Code_EAN_13 LIKE %s;", (f"%{pattern}%",)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_medicament_nom_like(pattern):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Medicament WHERE Nom LIKE %s;", (f"%{pattern}%",))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    def extraire_medicament_nom_like_name(pattern):
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT Nom FROM Medicament WHERE Nom LIKE %s;", (f"%{pattern}%",))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row)['Nom'] for row in rows]

    @staticmethod
    def extraire_tous_medicament():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Medicament ORDER BY Nom;")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_medicament_quantite_minimale_sup_0():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Medicament WHERE Min_Stock > 0;")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def extraire_medicament_quantite_minimale_repture():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Medicament WHERE Min_Stock > 0 and Stock_Actuel<Min_Stock; ")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def cloture_journee():
        conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Total des médicaments
        cursor.execute(
            """
            SELECT COUNT(ID_Medicament) as total_medicaments
            FROM Medicament
        """
        )
        total_medicaments = cursor.fetchone()
        total_medicaments = total_medicaments["total_medicaments"]

        # Total des médicaments avec stock inférieur au minimum
        cursor.execute(
            """
            SELECT COUNT(ID_Medicament) as medicaments_en_rupture
            FROM Medicament
            WHERE Stock_Actuel < Min_Stock
        """
        )
        medicaments_en_rupture = cursor.fetchone()
        medicaments_en_rupture = medicaments_en_rupture["medicaments_en_rupture"]

        # Total des médicaments avec stock positif
        cursor.execute(
            """
            SELECT COUNT(ID_Medicament) as medicaments_avec_stock
            FROM Medicament
            WHERE Stock_Actuel > 0
        """
        )
        medicaments_avec_stock = cursor.fetchone()
        medicaments_avec_stock = medicaments_avec_stock["medicaments_avec_stock"]

        # Calcul du stock total disponible
        cursor.execute(
            """
            SELECT SUM(Stock_Actuel) as total_stock
            FROM Medicament
        """
        )
        total_stock = cursor.fetchone()
        total_stock = total_stock["total_stock"]

        conn.close()

        # Préparer les résultats sous forme de dictionnaire
        statistiques = {
            "Total des médicaments": total_medicaments if total_medicaments else 0,
            "Total des médicaments avec stock inférieur au minimum": medicaments_en_rupture
            if medicaments_en_rupture
            else 0,
            "Total des médicaments avec stock positif": medicaments_avec_stock
            if medicaments_avec_stock
            else 0,
            "Calcul du stock total disponible de tous les medicaments": total_stock
            if total_stock
            else 0,
        }

        return statistiques
