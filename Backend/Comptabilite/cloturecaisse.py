import sqlite3
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os

from Backend.Comptabilite.mailSender import MailSender

class Caisse:
    def __init__(self):
        self.dataset = dataset


        """Détail des entrées et sorties de caisse

            Espèces encaissées
            Paiements par carte ou autres moyens
            Remboursements ou retraits
            Solde initial et final de la caisse

            Montant en début de journée
            Montant théorique en fin de journée (en fonction des transactions)
            Montant réel compté en caisse
            Écart de caisse

            Différence entre le montant théorique et le montant réellement présent
            Justification des écarts éventuels
            Suivi des transactions par mode de paiement

            Espèces, carte bancaire, virement, etc.
            Validation des crédits et des échanges

            Vérification des dettes clients non réglées
            Confirmation des échanges réalisés
            Détails des ventes

            Articles vendus, quantités, remises appliquées
            Signature ou validation du responsable

            Pour confirmer la clôture et éviter toute contestation
            """

    def get_commandes_jour(self):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT ID_Commande FROM Commandes WHERE strftime('%d/%m/%Y', Date_Commande) = ?''', (datetime.now().date().strftime('%d/%m/%Y'),))
        result = cursor.fetchall()
        conn.close()
        return [dict(row) for row in result]
 
    def get_commandes_recues_jour(self):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT ID_Commande FROM Commandes WHERE strftime('%d/%m/%Y', Date_Reception) = ?''', (datetime.now().date().strftime('%d/%m/%Y'),))
        result = cursor.fetchall()
        conn.close()
        return [dict(row) for row in result]

    def get_total_paiement(self):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(Montant_Paye) as totalPaiement FROM Payment''')
        result = cursor.fetchone()
        conn.close()
        return result['totalPaiement']

    def get_total_credits(self):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(Reste_A_Payer) as totalCredits FROM Credit''')
        result = cursor.fetchone()
        conn.close()
        return result['totalCredits']

    def get_total_echanges(self):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(Total_Facture) as totalEchanges FROM Echanges''')
        result = cursor.fetchone()
        conn.close()
        return result['totalEchanges']

    def get_situation_stock(self):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT ID_Medicament, Quantite_Actuelle FROM Stock''')
        result = cursor.fetchall()
        conn.close()
        return {row['ID_Medicament']: row['Quantite_Actuelle'] for row in result}

    def get_salaries(self):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT ID_Salarie FROM Salaries''')
        result = cursor.fetchall()
        conn.close()
        return [row['ID_Salarie'] for row in result]

    def get_transactions_jour(self, salarie):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT ID_Vente FROM Ventes WHERE strftime('%d/%m/%Y', Date_Vente) = ? AND ID_Salarie = ?''', (datetime.now().date().strftime('%d/%m/%Y'), salarie))
        result = cursor.fetchall()
        conn.close()
        return [dict(row) for row in result]

    def get_commandes_jour_salarie(self, salarie):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT ID_Commande FROM Commandes WHERE strftime('%d/%m/%Y', Date_Commande) = ? AND ID_Salarie = ?''', (datetime.now().date().strftime('%d/%m/%Y'), salarie))
        result = cursor.fetchall()
        conn.close()
        return [dict(row) for row in result]

    def get_commandes_recues_jour_salarie(self, salarie):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT ID_Commande FROM Commandes WHERE strftime('%d/%m/%Y', Date_Reception) = ? AND ID_Salarie = ?''', (datetime.now().date().strftime('%d/%m/%Y'), salarie))
        result = cursor.fetchall()
        conn.close()
        return [dict(row) for row in result]

    def get_total_vendu_salarie(self, salarie):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(Total_Facture) as totalVendu FROM Ventes WHERE ID_Salarie = ?''', (salarie,))
        result = cursor.fetchone()
        conn.close()
        return result['totalVendu']

    def get_total_paiement_salarie(self, salarie):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(Montant_Paye) as totalPaiement FROM Payment WHERE ID_Salarie = ?''', (salarie,))
        result = cursor.fetchone()
        conn.close()
        return result['totalPaiement']

    def get_total_credits_salarie(self, salarie):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(Reste_A_Payer) as totalCredits FROM Credit WHERE ID_Salarie = ?''', (salarie,))
        result = cursor.fetchone()
        conn.close()
        return result['totalCredits']

    def get_total_echanges_salarie(self, salarie):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(Total_Facture) as totalEchanges FROM Echanges WHERE ID_Salarie = ?''', (salarie,))
        result = cursor.fetchone()
        conn.close()
        return result['totalEchanges']

    def get_statistique(self):
        # Connect to the database
        conn = sqlite3.connect(self.dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Ventes''')
        result = cursor.fetchall()
        conn.close()
        return [dict(row) for row in result]

    def fermeture_de_caisse(self):
        message_text = ""
        # Nombre de ventes de jour
        ventes_jour = self.get_statistique()

        nombre_ventes_jour = len(ventes_jour)
        print("Nombre de ventes de jour:", nombre_ventes_jour)
        message_text+= "Nombre de ventes de jour: " + str(nombre_ventes_jour)

        # Nombre de commande passer dans la journée
        commandes_jour = self.get_commandes_jour()
        nombre_commandes_jour = len(commandes_jour)
        print("Nombre de commandes passées dans la journée:", nombre_commandes_jour)
        message_text += "Nombre de commandes passées dans la journée:"+ str(nombre_commandes_jour)

        # Nombre de Commande reçu dans la journée
        commandes_recues_jour = self.get_commandes_recues_jour()
        nombre_commandes_recues_jour = len(commandes_recues_jour)
        print("Nombre de commandes reçues dans la journée:", nombre_commandes_recues_jour)
        message_text += "Nombre de commandes reçues dans la journée: "+ str(nombre_commandes_recues_jour)
        MailSender.send_email('Stat', message_text)
        print(ventes_jour)
        # Totale de vendu en DHs
        total_vendu = sum([vente['total_facture'] for vente in ventes_jour])
        print("Total vendu en DHs:", total_vendu)
        message_text += "Total vendu en DHs: "+ str(total_vendu)


        # Totale de paiement en DHs
        total_paiement = self.get_total_paiement()
        print("Total paiement en DHs:", total_paiement)

        # Totale de credits en DHs
        total_credits = self.get_total_credits()
        print("Total crédits en DHs:", total_credits)

        # Totale d'échange en DHs
        total_echanges = self.get_total_echanges()
        print("Total échanges en DHs:", total_echanges)

        # Situation de stock
        situation_stock = self.get_situation_stock()
        print("Situation de stock:")
        for medicament, quantite in situation_stock.items():
            print(f"{medicament}: {quantite}")

        # Pour chaque salarié:
        salaries = self.get_salaries()
        for salarie in salaries:
            # Nombre de transactions de jour
            transactions_jour = self.get_transactions_jour(salarie)
            nombre_transactions_jour = len(transactions_jour)
            print(f"Nombre de transactions de jour pour le salarié {salarie}: {nombre_transactions_jour}")

            # Nombre de commandes passées dans la journée
            commandes_jour_salarie = self.get_commandes_jour_salarie(salarie)
            nombre_commandes_jour_salarie = len(commandes_jour_salarie)
            print(f"Nombre de commandes passées dans la journée pour le salarié {salarie}: {nombre_commandes_jour_salarie}")

            # Nombre de commandes reçues dans la journée
            commandes_recues_jour_salarie = self.get_commandes_recues_jour_salarie(salarie)
            nombre_commandes_recues_jour_salarie = len(commandes_recues_jour_salarie)
            print(f"Nombre de commandes reçues dans la journée pour le salarié {salarie}: {nombre_commandes_recues_jour_salarie}")

            # Totale de vendu en DHs
            total_vendu_salarie = self.get_total_vendu_salarie(salarie)
            print(f"Total vendu en DHs pour le salarié {salarie}: {total_vendu_salarie}")

            # Totale de paiement en DHs
            total_paiement_salarie = self.get_total_paiement_salarie(salarie)
            print(f"Total paiement en DHs pour le salarié {salarie}: {total_paiement_salarie}")

            # Totale de crédits en DHs
            total_credits_salarie = self.get_total_credits_salarie(salarie)
            print(f"Total crédits en DHs pour le salarié {salarie}: {total_credits_salarie}")

            # Totale d'échange en DHs
            total_echanges_salarie = self.get_total_echanges_salarie(salarie)
            print(f"Total échanges en DHs pour le salarié {salarie}: {total_echanges_salarie}")



