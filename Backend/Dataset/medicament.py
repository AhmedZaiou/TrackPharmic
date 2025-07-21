import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os
import json


class Medicament:
    @staticmethod
    def supprimer_toute_base_donnees(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table['Tables_in_' + database]};")
        conn.commit()
        

    @staticmethod
    def create_table_new_medicament(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
        CREATE TABLE Medicament (
            id_medicament INT PRIMARY KEY AUTO_INCREMENT,
            Code_EAN_13 VARCHAR(20),
            Nom VARCHAR(255),
            Image_URL TEXT,
            Présentation TEXT,
            Dosage VARCHAR(100),
            Distributeur_ou_fabriquant VARCHAR(255),
            Composition TEXT,
            Classe_thérapeutique VARCHAR(255),
            Statut VARCHAR(100),
            Code_ATC VARCHAR(20),
            PPV DECIMAL(10, 2),
            Prix_hospitalier DECIMAL(10, 2),
            Tableau VARCHAR(50),
            Indications TEXT,
            Min_Stock INT,
            Stock_Actuel INT,
            url_medicament TEXT
        );
        """
        )
        conn.commit()
        
    
    @staticmethod
    def ajouter_medicament_code_barre(conn,code_barre):
        """
        Ajoute un médicament à la base de données à partir du code-barres.
        Le code-barres est utilisé pour extraire les informations du médicament.
        """
        from Backend.Datascraping.extraire_medicament import Scraper_medicament

        values = Scraper_medicament.get_medicament_codeBarre(code_barre)
         
        
        #if values[0]['Nom'] == 'Page non trouvée.':
        #    print('medicament not found')
        #    #return None 
        
         
        #if Medicament.test_existance_url(values.get('url')):
        #        return None
        Code_EAN_13 = values.get('Code_EAN_13')
        Nom = values.get('Nom')
        Image_URL = values.get('Image URL')
        Présentation = values.get('Présentation')
        Dosage = values.get('Dosage')
        Distributeur_ou_fabriquant = values.get('Distributeur ou fabriquant')
        Composition = values.get('Composition')
        Classe_thérapeutique = values.get('Classe thérapeutique')
        Statut = values.get('Statut')
        Code_ATC = values.get('Code ATC')
        PPV = values.get('PPV')
        Prix_hospitalier =  values.get('Prix hospitalier')
        Tableau =   values.get('Tableau')
        Indications =   values.get('Indication(s)') 
        Min_Stock   = 0
        Stock_Actuel =  0
        url_medicament = values.get('url') 
        Medicament.ajouter_medicament(conn,Code_EAN_13,
            Nom,
            Image_URL,
            Présentation,
            Dosage,
            Distributeur_ou_fabriquant,
            Composition,
            Classe_thérapeutique,
            Statut,
            Code_ATC,
            PPV,
            Prix_hospitalier,
            Tableau,
            Indications,
            Min_Stock,
            Stock_Actuel,
            url_medicament) 
        return values

    @staticmethod
    def ajouter_medicament_data_frame(conn,dataframe):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.executemany(
            """
        INSERT INTO Medicament (
                            Code_EAN_13,
                            Nom,
                            Image_URL,
                            Présentation,
                            Dosage,
                            Distributeur_ou_fabriquant,
                            Composition,
                            Classe_thérapeutique,
                            Statut,
                            Code_ATC,
                            PPV,
                            Prix_hospitalier,
                            Tableau,
                            Indications,
                            Min_Stock,
                            Stock_Actuel, 
                            url_medicament
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        );""",  
            (
                 list(dataframe.itertuples(index=False, name=None))
            ),
        )
        conn.commit()
        

            

    @staticmethod
    def ajouter_medicament(conn,
        Code_EAN_13,
        Nom,
        Image_URL,
        Présentation,
        Dosage,
        Distributeur_ou_fabriquant,
        Composition,
        Classe_thérapeutique,
        Statut,
        Code_ATC,
        PPV,
        Prix_hospitalier,
        Tableau,
        Indications,
        Min_Stock,
        Stock_Actuel,
        url_medicament,
    ):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
        INSERT INTO Medicament (
                            Code_EAN_13,
                            Nom,
                            Image_URL,
                            Présentation,
                            Dosage,
                            Distributeur_ou_fabriquant,
                            Composition,
                            Classe_thérapeutique,
                            Statut,
                            Code_ATC,
                            PPV,
                            Prix_hospitalier,
                            Tableau,
                            Indications,
                            Min_Stock,
                            Stock_Actuel, 
                            url_medicament
                        ) VALUES (
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        );""",  
            (
                Code_EAN_13,
                Nom,
                Image_URL,
                Présentation,
                Dosage,
                Distributeur_ou_fabriquant,
                Composition,
                Classe_thérapeutique,
                Statut,
                Code_ATC,
                PPV,
                Prix_hospitalier,
                Tableau,
                Indications,
                Min_Stock,
                Stock_Actuel,
                url_medicament,
            ),
        )
        conn.commit()
        

    @staticmethod
    def supprimer_medicament(conn,id_medicament):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "DELETE FROM Medicament WHERE id_medicament = %s;", (id_medicament,)
        )
        conn.commit()
        

    @staticmethod
    def modifier_medicament(conn,id_medicament, 
                Code_EAN_13,
                Nom,
                Image_URL,
                Présentation,
                Dosage,
                Distributeur_ou_fabriquant,
                Composition,
                Classe_thérapeutique,
                Statut,
                Code_ATC,
                PPV,
                Prix_hospitalier,
                Tableau,
                Indications,
                Min_Stock,
                Stock_Actuel,
                url_medicament,
            ):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)  
        query = f"UPDATE Medicament SET Code_EAN_13 = %s, \
                    Nom = %s, \
                    Image_URL = %s, \
                    Présentation = %s, \
                    Dosage = %s, \
                    Distributeur_ou_fabriquant = %s, \
                    Composition = %s, \
                    Classe_thérapeutique = %s, \
                    Statut = %s, \
                    Code_ATC = %s, \
                    PPV = %s, \
                    Prix_hospitalier = %s, \
                    Tableau = %s, \
                    Indications = %s, \
                    Min_Stock = %s, \
                    Stock_Actuel = %s, \
                    url_medicament = %s WHERE id_medicament = %s;"
        cursor.execute(query, (
                Code_EAN_13,
                Nom,
                Image_URL,
                Présentation,
                Dosage,
                Distributeur_ou_fabriquant,
                Composition,
                Classe_thérapeutique,
                Statut,
                Code_ATC,
                PPV,
                Prix_hospitalier,
                Tableau,
                Indications,
                Min_Stock,
                Stock_Actuel,
                url_medicament,
                id_medicament,
            ))
        conn.commit()
        

    @staticmethod
    def extraire_medicament(conn,id_medicament):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Medicament WHERE id_medicament = %s;", (id_medicament,)
        )
        row = cursor.fetchone()
        
        return dict(row) if row else None
    @staticmethod
    def effectuer_vente_medicament(conn,id_medicament, quantite_vendu):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
        UPDATE Medicament SET Stock_Actuel = Stock_Actuel - %s
        WHERE id_medicament = %s;
        """
        cursor.execute(query, (quantite_vendu, id_medicament))
        conn.commit()
        

    @staticmethod
    def test_existance_url(conn,url):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
        SELECT 1 FROM Medicament WHERE url_medicament = %s LIMIT 1;
        """
        cursor.execute(query, (url,))
        result = cursor.fetchone()  # récupère une ligne si elle existe
        
        return result is not None

    def effectuer_stock_medicament(conn,id_medicament, quantite_vendu):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
        UPDATE Medicament SET Stock_Actuel = Stock_Actuel + %s
        WHERE id_medicament = %s;
        """
        cursor.execute(query, (quantite_vendu, id_medicament))
        conn.commit()
        
    
    @staticmethod
    def get_medicament_by_code_barre(conn,code_barre):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Medicament WHERE Code_EAN_13 = %s;", (code_barre,)
        )
        row = cursor.fetchone()
        
        return dict(row) if row else None

    @staticmethod
    def extraire_medicament_code_barre(conn,code_barre):
        row = Medicament.get_medicament_by_code_barre(conn,code_barre)
        if not row:
            Medicament.ajouter_medicament_code_barre(conn,code_barre)
        return Medicament.get_medicament_by_code_barre(conn,code_barre)

    @staticmethod
    def extraire_medicament_code_barre_like(conn,pattern):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Medicament WHERE Code_EAN_13 LIKE %s;", (f"%{pattern}%",)
        )
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_medicament_nom_like(conn,pattern):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Medicament WHERE Nom LIKE %s;", (f"%{pattern}%",))
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    def extraire_medicament_nom_like_name(conn,pattern):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT Nom FROM Medicament WHERE Nom LIKE %s;", (f"%{pattern}%",))
        rows = cursor.fetchall()
        
        return [dict(row)['Nom'] for row in rows]

    @staticmethod
    def extraire_tous_medicament(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Medicament WHERE Code_EAN_13 IS NOT NULL ORDER BY Nom;")
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    @staticmethod
    def extraire_tous_new_medicament(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Medicament WHERE Code_EAN_13 IS NULL ORDER BY Nom;")
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

    @staticmethod
    def extraire_medicament_quantite_minimale_sup_0(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Medicament WHERE Min_Stock > 0;")
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def extraire_medicament_quantite_minimale_repture(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Medicament WHERE Min_Stock > 0 and Stock_Actuel<Min_Stock; ")
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

    @staticmethod
    def cloture_journee(conn):
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Total des médicaments
        cursor.execute(
            """
            SELECT COUNT(id_medicament) as total_medicaments
            FROM Medicament
        """
        )
        total_medicaments = cursor.fetchone()
        total_medicaments = total_medicaments["total_medicaments"]

        # Total des médicaments avec stock inférieur au minimum
        cursor.execute(
            """
            SELECT COUNT(id_medicament) as medicaments_en_rupture
            FROM Medicament
            WHERE Stock_Actuel < Min_Stock
        """
        )
        medicaments_en_rupture = cursor.fetchone()
        medicaments_en_rupture = medicaments_en_rupture["medicaments_en_rupture"]

        # Total des médicaments avec stock positif
        cursor.execute(
            """
            SELECT COUNT(id_medicament) as medicaments_avec_stock
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
