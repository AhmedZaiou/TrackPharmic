import sqlite3
from pathlib import Path  
from datetime import datetime, timedelta
import os

current_directory = Path(__file__).parent
Front_end = current_directory.parent 
Tracpharmic = Path.home()/"Tracpharmic"
images = Tracpharmic/"images"
dataset = Tracpharmic/"dataset"/"pharmadataset.db" 
name_application = "TracPharmic"  





def get_commandes_jour():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT ID_Commande FROM Commandes WHERE strftime('%d/%m/%Y', Date_Commande) = ?''', (datetime.now().date().strftime('%d/%m/%Y'),))
    result = cursor.fetchall()
    conn.close()
    return result

def get_commandes_recues_jour():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT ID_Commande FROM Commandes WHERE strftime('%d/%m/%Y', Date_Reception) = ?''', (datetime.now().date().strftime('%d/%m/%Y'),))
    result = cursor.fetchall()
    conn.close()
    return result

def get_total_paiement():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(Montant_Paye) as totalPaiement FROM Payment''')
    result = cursor.fetchone()
    conn.close()
    return result['totalPaiement']

def get_total_credits():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(Reste_A_Payer) as totalCredits FROM Credit''')
    result = cursor.fetchone()
    conn.close()
    return result['totalCredits']

def get_total_echanges():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(Total_Facture) as totalEchanges FROM Echanges''')
    result = cursor.fetchone()
    conn.close()
    return result['totalEchanges']

def get_situation_stock():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT ID_Medicament, Quantite_Actuelle FROM Stock''')
    result = cursor.fetchall()
    conn.close()
    return {row['ID_Medicament']: row['Quantite_Actuelle'] for row in result}

def get_salaries():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT ID_Salarie FROM Salaries''')
    result = cursor.fetchall()
    conn.close()
    return [row['ID_Salarie'] for row in result]

def get_transactions_jour(salarie):
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT ID_Vente FROM Ventes WHERE strftime('%d/%m/%Y', Date_Vente) = ? AND ID_Salarie = ?''', (datetime.now().date().strftime('%d/%m/%Y'), salarie))
    result = cursor.fetchall()
    conn.close()
    return result

def get_commandes_jour_salarie(salarie):
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT ID_Commande FROM Commandes WHERE strftime('%d/%m/%Y', Date_Commande) = ? AND ID_Salarie = ?''', (datetime.now().date().strftime('%d/%m/%Y'), salarie))
    result = cursor.fetchall()
    conn.close()
    return result

def get_commandes_recues_jour_salarie(salarie):
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT ID_Commande FROM Commandes WHERE strftime('%d/%m/%Y', Date_Reception) = ? AND ID_Salarie = ?''', (datetime.now().date().strftime('%d/%m/%Y'), salarie))
    result = cursor.fetchall()
    conn.close()
    return result

def get_total_vendu_salarie(salarie):
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(Total_Facture) as totalVendu FROM Ventes WHERE ID_Salarie = ?''', (salarie,))
    result = cursor.fetchone()
    conn.close()
    return result['totalVendu']

def get_total_paiement_salarie(salarie):
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(Montant_Paye) as totalPaiement FROM Payment WHERE ID_Salarie = ?''', (salarie,))
    result = cursor.fetchone()
    conn.close()
    return result['totalPaiement']

def get_total_credits_salarie(salarie):
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(Reste_A_Payer) as totalCredits FROM Credit WHERE ID_Salarie = ?''', (salarie,))
    result = cursor.fetchone()
    conn.close()
    return result['totalCredits']

def get_total_echanges_salarie(salarie):
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(Total_Facture) as totalEchanges FROM Echanges WHERE ID_Salarie = ?''', (salarie,))
    result = cursor.fetchone()
    conn.close()
    return result['totalEchanges']

def get_statistique():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Ventes''')
    result = cursor.fetchall()
    conn.close()
    return result


def fermeture_de_caisse():
    # Nombre de ventes de jour
    ventes_jour = get_statistique()

    nombre_ventes_jour = len(ventes_jour)
    print("Nombre de ventes de jour:", nombre_ventes_jour)
    
    # Nombre de commande passer dans la journée
    commandes_jour = get_commandes_jour()
    nombre_commandes_jour = len(commandes_jour)
    print("Nombre de commandes passées dans la journée:", nombre_commandes_jour)
    
    # Nombre de Commande reçu dans la journée
    commandes_recues_jour = get_commandes_recues_jour()
    nombre_commandes_recues_jour = len(commandes_recues_jour)
    print("Nombre de commandes reçues dans la journée:", nombre_commandes_recues_jour)
    print(ventes_jour)
    # Totale de vendu en DHs
    total_vendu = sum([vente['totalDh'] for vente in ventes_jour])
    print("Total vendu en DHs:", total_vendu)
    
    # Totale de paiement en DHs
    total_paiement = get_total_paiement()
    print("Total paiement en DHs:", total_paiement)
    
    # Totale de credits en DHs
    total_credits = get_total_credits()
    print("Total crédits en DHs:", total_credits)
    
    # Totale d'échange en DHs
    total_echanges = get_total_echanges()
    print("Total échanges en DHs:", total_echanges)
    
    # Situation de stock
    situation_stock = get_situation_stock()
    print("Situation de stock:")
    for medicament, quantite in situation_stock.items():
        print(f"{medicament}: {quantite}")
    
    # Pour chaque salarié:
    salaries = get_salaries()
    for salarie in salaries:
        # Nombre de transactions de jour
        transactions_jour = get_transactions_jour(salarie)
        nombre_transactions_jour = len(transactions_jour)
        print(f"Nombre de transactions de jour pour le salarié {salarie}: {nombre_transactions_jour}")
        
        # Nombre de commandes passées dans la journée
        commandes_jour_salarie = get_commandes_jour_salarie(salarie)
        nombre_commandes_jour_salarie = len(commandes_jour_salarie)
        print(f"Nombre de commandes passées dans la journée pour le salarié {salarie}: {nombre_commandes_jour_salarie}")
        
        # Nombre de commandes reçues dans la journée
        commandes_recues_jour_salarie = get_commandes_recues_jour_salarie(salarie)
        nombre_commandes_recues_jour_salarie = len(commandes_recues_jour_salarie)
        print(f"Nombre de commandes reçues dans la journée pour le salarié {salarie}: {nombre_commandes_recues_jour_salarie}")
        
        # Totale de vendu en DHs
        total_vendu_salarie = get_total_vendu_salarie(salarie)
        print(f"Total vendu en DHs pour le salarié {salarie}: {total_vendu_salarie}")
        
        # Totale de paiement en DHs
        total_paiement_salarie = get_total_paiement_salarie(salarie)
        print(f"Total paiement en DHs pour le salarié {salarie}: {total_paiement_salarie}")
        
        # Totale de crédits en DHs
        total_credits_salarie = get_total_credits_salarie(salarie)
        print(f"Total crédits en DHs pour le salarié {salarie}: {total_credits_salarie}")
        
        # Totale d'échange en DHs
        total_echanges_salarie = get_total_echanges_salarie(salarie)
        print(f"Total échanges en DHs pour le salarié {salarie}: {total_echanges_salarie}")


fermeture_de_caisse()