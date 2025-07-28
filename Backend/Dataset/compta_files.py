import pymysql
from Frontend.utils.utils import *
from datetime import datetime, timedelta, date
import os
import json
import pandas as pd
import matplotlib.pyplot as plt


class ComptaFilesGeneration:
    @staticmethod
    def __init__(self):
        pass

    @staticmethod
    def extraire_vente(conn):
        conn = reconnexion_database(conn)
        request = """SELECT
                        V.id_vente,
                        V.date_vente,
                        V.numero_facture,
                        V.quantite_vendue,
                        V.prix_vente,
                        V.total_facture,
                        V.prix_achat,

                        M.Nom AS nom_medicament,
                        M.Code_EAN_13,

                        C.date_commande,
                        C.date_reception,
                        C.id_fournisseur,

                        P.montant_paye,
                        P.date_paiement,

                        R.quantite_retour,
                        R.date_retour,
                        R.prix AS prix_retour,

                        CL.nom AS nom_client,
                        S.nom AS nom_salarie

                    FROM Ventes V
                    LEFT JOIN Medicament M ON V.id_medicament = M.id_medicament
                    LEFT JOIN Commandes C ON V.id_commande_entre = C.id_commande
                    LEFT JOIN Payment P ON V.numero_facture = P.numero_facture
                    LEFT JOIN Retours R ON V.numero_facture = R.numero_facture AND V.id_medicament = R.id_medicament
                    LEFT JOIN Clients CL ON V.id_client = CL.id_client
                    LEFT JOIN Salaries S ON V.id_salarie = S.id_salarie
                    ORDER BY V.date_vente DESC;
                    """

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(request)
        rows = cursor.fetchall()

        fichier_excel = "rapport.xlsx"
        if rows:
            df = pd.DataFrame(rows)
            df.to_excel(fichier_excel, index=False)
            print(f"✅ Données exportées dans {fichier_excel}")
            return fichier_excel
        else:
            print("❌ Aucune donnée à exporter.")
            return None
