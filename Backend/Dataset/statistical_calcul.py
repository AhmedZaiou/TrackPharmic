 
import mysql.connector
from Frontend.utils.utils import *
from datetime import datetime, timedelta
import os




def create_ventes_table():
    # Connect to the database
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)

    # Execute the query to create the Ventes table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Ventes (
                    ID_Vente INTEGER PRIMARY KEY AUTOINCREMENT,
                    ID_Medicament INTEGER NOT NULL,
                    ID_Commande_Entre INTEGER NOT NULL,
                    Prix_Achat REAL,
                    Prix_Vente REAL,
                    Date_Vente TEXT,
                    Quantite_Vendue INTEGER,
                    Total_Facture REAL,
                    ID_Client INTEGER,
                    Numero_Facture TEXT,
                    ID_Salarie INTEGER,
                    FOREIGN KEY(ID_Medicament) REFERENCES Medicament(ID_Medicament),
                    FOREIGN KEY(ID_Commande_Entre) REFERENCES Commande_Entre(ID_Commande_Entre)
                    )''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def test():
    # Connect to the database
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)

    # Execute the query to get the statistics 
    cursor.execute('''SELECT strftime('%d/%m/%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2)) 
AS Date_Formattee
FROM Ventes; ''')
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Return the statistics
    return result

# statistique pour la journée

# get statistics générales pour la journée
def get_statistique():
    # Connect to the database
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)

     
    cursor =  conn.cursor(dictionary=True)

    cursor.execute('''SELECT COUNT(ID_Vente) as numberVentes, SUM(Quantite_Vendue) as NumberProducts, SUM(Total_Facture) as totalDh, SUM(Prix_Achat) as totalAchat FROM Ventes WHERE strftime('%d/%m/%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ?''', (datetime.now().date().strftime('%d/%m/%Y'),))
    result = cursor.fetchone()
    conn.close()
    return dict(result)

 
# get statistics par salarié pour la  journé 
def get_stat_salarie():
        # Connect to the database
        conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
         
        cursor =  conn.cursor(dictionary=True)
        cursor.execute('''SELECT ID_Salarie, COUNT(ID_Vente) as numberVentes, SUM(Quantite_Vendue) as NumberProducts, SUM(Total_Facture) as totalDh FROM Ventes WHERE strftime('%d/%m/%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? GROUP BY ID_Salarie''', (datetime.now().date().strftime('%d/%m/%Y'),))
        result = cursor.fetchall()
        conn.close()
        return result


# extraire les medicaments vendus pour la journée
def get_medicament_vendu():
    # Connect to the database
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
     
    cursor =  conn.cursor(dictionary=True)
    cursor.execute('''SELECT ID_Medicament, SUM(Quantite_Vendue) as NumberProducts, SUM(Total_Facture) as TotalMoney, SUM(Prix_Achat) as TotalCost FROM Ventes WHERE strftime('%d/%m/%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? GROUP BY ID_Medicament''', (datetime.now().date().strftime('%d/%m/%Y'),))
    result = cursor.fetchall()
    conn.close()
    return result





# get statistics générales pour le mois

def get_statistique_mois():
    # Connect to the database
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)

     
    cursor =  conn.cursor(dictionary=True)

    cursor.execute('''SELECT COUNT(ID_Vente) as numberVentes, SUM(Quantite_Vendue) as NumberProducts, SUM(Total_Facture) as totalDh, SUM(Prix_Achat) as totalAchat FROM Ventes WHERE strftime('%m', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? AND strftime('%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ?''', (datetime.now().date().strftime('%m'), datetime.now().date().strftime('%Y')))
    result = cursor.fetchone()
    conn.close()
    return dict(result)

# get statistics par salarié pour le mois

def get_stat_salarie_mois():
        # Connect to the database
        conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
         
        cursor =  conn.cursor(dictionary=True)
        cursor.execute('''SELECT ID_Salarie, COUNT(ID_Vente) as numberVentes, SUM(Quantite_Vendue) as NumberProducts, SUM(Total_Facture) as totalDh FROM Ventes WHERE strftime('%m', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? AND strftime('%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? GROUP BY ID_Salarie''', (datetime.now().date().strftime('%m'), datetime.now().date().strftime('%Y')))
        result = cursor.fetchall()
        conn.close()
        return result

# extraire les medicaments vendus pour le mois

def get_medicament_vendu_mois():
    # Connect to the database
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
     
    cursor =  conn.cursor(dictionary=True)
    cursor.execute('''SELECT ID_Medicament, SUM(Quantite_Vendue) as NumberProducts, 
                   SUM(Total_Facture) as TotalMoney, SUM(Prix_Achat) as TotalCost 
                   FROM Ventes 
                   WHERE strftime('%m/%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? GROUP BY ID_Medicament''', (datetime.now().date().strftime('%m/%Y'),))

    result = cursor.fetchall()
    conn.close()
    return result







def create_stock_table():
        # Connect to the database
        conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
        cursor =  conn.cursor(dictionary=True)
        # Execute the query to create the Stock table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS Stock (
                        ID_Stock INTEGER PRIMARY KEY AUTOINCREMENT,
                        ID_Medicament INTEGER NOT NULL,  
                        ID_Commande INTEGER,  
                        ID_Salarie INTEGER,            
                        Prix_Achat REAL NOT NULL,       
                        Prix_Vente REAL NOT NULL,        
                        Prix_Conseille REAL,            
                        Date_Achat TEXT NOT NULL,       
                        Date_Expiration TEXT,           
                        Date_Reception TEXT,            
                        Date_Derniere_Sortie TEXT,      
                        Stock_Initial INTEGER NOT NULL, 
                        Quantite_Actuelle INTEGER NOT NULL, 
                        Quantite_Minimale INTEGER NOT NULL, 
                        Quantite_Maximale INTEGER,    
                        FOREIGN KEY (ID_Salarie) REFERENCES Salaries(ID_Salarie),
                        FOREIGN KEY (ID_Medicament) REFERENCES Medicament(ID_Medicament),
                        FOREIGN KEY (ID_Commande) REFERENCES Commande(ID_Commande)
                        )''')
        # Commit the changes and close the connection
        conn.commit()
        conn.close()


# get statistics générales pour le stock

def get_statistique_stock():
        # Connect to the database
        conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
         
        cursor =  conn.cursor(dictionary=True)
        cursor.execute('''SELECT COUNT(ID_Stock) as numberStock, SUM(Quantite_Actuelle) as NumberProducts, 
                       SUM(Prix_Achat) as totalAchat, SUM(Prix_Vente) as totalVente FROM Stock''')
        result = cursor.fetchone()
        conn.close()
        return dict(result)

# get les medicament avec leur quentité qui expirand dans les deux mois prochaines 
def get_medicament_expirant():
    # Connect to the database
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
     
    cursor =  conn.cursor(dictionary=True)
    # Calculate the date two months from now
    two_months_from_now = datetime.now() + timedelta(days=60) 
    # Execute the query to get the medications expiring in the next two months
    cursor.execute('''SELECT ID_Medicament, SUM(Quantite_Actuelle) as NumberProducts, Date_Expiration  
                    FROM Stock 
                    WHERE strftime( '%d/%m/%Y',Date_Expiration) <= ? 
                    GROUP BY ID_Medicament''', (two_months_from_now.date().strftime('%d/%m/%Y'),))
    result = cursor.fetchall()
    conn.close()
    return result 


# get medicament qui il s'ont une quantité inférieur à la quantité minimale
def get_medicament_faible_medicament():
    # Connect to the database
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
     
    cursor =  conn.cursor(dictionary=True)
    cursor.execute('''SELECT ID_Medicament, stock_actuel , min_stock  
                    FROM Medicament 
                    WHERE stock_actuel < min_stock ''')
    result = cursor.fetchall()
    conn.close()
    return result

# get all possibl statistic for credit 
"""CREATE TABLE IF NOT EXISTS Credit (
                ID_Credit INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Client INTEGER NOT NULL,
                Numero_Facture TEXT NOT NULL,
                Montant_Paye REAL NOT NULL,
                Reste_A_Payer REAL NOT NULL,
                Date_Dernier_Paiement TEXT,
                Statut TEXT NOT NULL,
                ID_Salarie INTEGER NOT NULL,
                FOREIGN KEY (ID_Client) REFERENCES Clients(ID_Client)
            )
            
            
            CREATE TABLE IF NOT EXISTS Payment (
                ID_Payment INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Client INTEGER NOT NULL,
                Numero_Facture TEXT NOT NULL,
                Montant_Paye REAL NOT NULL, 
                Date_Paiement TEXT, 
                ID_Salarie INTEGER NOT NULL
            )
            
            
             CREATE TABLE IF NOT EXISTS Echanges (
                ID_Echange INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Pharmacie INTEGER NOT NULL,
                ID_facture TEXT NOT NULL,
                Date_Echange TEXT NOT NULL,
                Total_Facture REAL NOT NULL,
                sens TEXT NOT NULL,
                ID_Salarie INTEGER NOT NULL
            )
            
            
            CREATE TABLE IF NOT EXISTS Commandes (
                ID_Commande INTEGER PRIMARY KEY AUTOINCREMENT,
                Liste_Produits TEXT,
                ID_Fournisseur INTEGER NOT NULL,
                Date_Commande TEXT,
                Date_Reception_Prevue TEXT,
                Statut_Reception TEXT,
                Receptionniste TEXT,
                Produits_Reçus TEXT,
                Date_Reception TEXT,
                ID_Salarie INTEGER,
                Status_Incl BOOLEAN,
                FOREIGN KEY(ID_Fournisseur) REFERENCES Fournisseur(ID_Fournisseur)
            )"""
def get_statistique_credit():
    # Connect to the database
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
     
    cursor =  conn.cursor(dictionary=True)
    cursor.execute('''SELECT COUNT(ID_Credit) as numberCredit, SUM(Montant_Paye) as totalPaye, SUM(Reste_A_Payer) as totalReste FROM Credit''')
    result = cursor.fetchone()
    conn.close()
    return dict(result)

# get statistics par salarié pour le credit
     











# Situation caisse aujourdhui

def get_situation_caisse(): 
    # get statistics générales
    statistics = get_statistique()
    print("Statistics générales pour la journée:")
    print(statistics)
    print()

    # get statistics par salarié
    salaries = get_stat_salarie()
    print("Statistics par salarié pour la journée:")
    for salary in salaries:
        print(dict(salary))
    print()

    # extraire les medicaments vendus pour la journée
    medicaments = get_medicament_vendu()
    print("Medicaments vendus pour la journée:")
    for medicament in medicaments:
        print(dict(medicament))
    print()

    # get statistics générales pour le mois
    statistics_mois = get_statistique_mois()
    print("Statistics générales pour le mois:")
    print(statistics_mois)
    print()

    # get statistics par salarié pour le mois
    salaries_mois = get_stat_salarie_mois()
    print("Statistics par salarié pour le mois:")
    for salary_mois in salaries_mois:
        print(dict(salary_mois))
    print()

    # extraire les medicaments vendus pour le mois
    medicaments_mois = get_medicament_vendu_mois()
    print("Medicaments vendus pour le mois:")
    for medicament_mois in medicaments_mois:
        print(dict(medicament_mois))
    print()

    # get statistics générales pour le stock
    statistics_stock = get_statistique_stock()
    print("Statistics générales pour le stock:")
    print(statistics_stock)
    print()

    # get les medicament avec leur quentité qui expirand dans les deux mois prochaines
    medicaments_expirant = get_medicament_expirant()
    print("Medicaments expirant dans les deux mois prochaines:")
    for medicament_expirant in medicaments_expirant:
        print(dict(medicament_expirant))
    print()

    # get medicament qui il s'ont une quantité inférieur à la quantité minimale
    medicaments_faible = get_medicament_faible_medicament()
    print("Medicaments avec une quantité inférieure à la quantité minimale:")
    for medicament_faible in medicaments_faible:
        print(dict(medicament_faible))
    print()



get_situation_caisse()






def fermeture_de_caisse():
     pass
    
