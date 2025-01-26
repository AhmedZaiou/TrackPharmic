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






def create_ventes_table():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    cursor = conn.cursor()

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
    conn = sqlite3.connect(dataset)
    cursor = conn.cursor()

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
    conn = sqlite3.connect(dataset)

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''SELECT COUNT(ID_Vente) as numberVentes, SUM(Quantite_Vendue) as NumberProducts, SUM(Total_Facture) as totalDh, SUM(Prix_Achat) as totalAchat FROM Ventes WHERE strftime('%d/%m/%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ?''', (datetime.now().date().strftime('%d/%m/%Y'),))
    result = cursor.fetchone()
    conn.close()
    return dict(result)

 
# get statistics par salarié pour la  journé 
def get_stat_salarie():
        # Connect to the database
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT ID_Salarie, COUNT(ID_Vente) as numberVentes, SUM(Quantite_Vendue) as NumberProducts, SUM(Total_Facture) as totalDh FROM Ventes WHERE strftime('%d/%m/%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? GROUP BY ID_Salarie''', (datetime.now().date().strftime('%d/%m/%Y'),))
        result = cursor.fetchall()
        conn.close()
        return result


# extraire les medicaments vendus pour la journée
def get_medicament_vendu():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT ID_Medicament, SUM(Quantite_Vendue) as NumberProducts, SUM(Total_Facture) as TotalMoney, SUM(Prix_Achat) as TotalCost FROM Ventes WHERE strftime('%d/%m/%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? GROUP BY ID_Medicament''', (datetime.now().date().strftime('%d/%m/%Y'),))
    result = cursor.fetchall()
    conn.close()
    return result


"""# get statistics générales
print(get_statistique())

# get statistics par salarié
data = get_stat_salarie()
for i in data:
    print(dict(i)) 

# extraire les medicaments vendus pour la journée
data = get_medicament_vendu()
for i in data:
    print(dict(i)) 
 """



# get statistics générales pour le mois

def get_statistique_mois():
    # Connect to the database
    conn = sqlite3.connect(dataset)

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''SELECT COUNT(ID_Vente) as numberVentes, SUM(Quantite_Vendue) as NumberProducts, SUM(Total_Facture) as totalDh, SUM(Prix_Achat) as totalAchat FROM Ventes WHERE strftime('%m', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? AND strftime('%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ?''', (datetime.now().date().strftime('%m'), datetime.now().date().strftime('%Y')))
    result = cursor.fetchone()
    conn.close()
    return dict(result)

# get statistics par salarié pour le mois

def get_stat_salarie_mois():
        # Connect to the database
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT ID_Salarie, COUNT(ID_Vente) as numberVentes, SUM(Quantite_Vendue) as NumberProducts, SUM(Total_Facture) as totalDh FROM Ventes WHERE strftime('%m', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? AND strftime('%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? GROUP BY ID_Salarie''', (datetime.now().date().strftime('%m'), datetime.now().date().strftime('%Y')))
        result = cursor.fetchall()
        conn.close()
        return result

# extraire les medicaments vendus pour le mois

def get_medicament_vendu_mois():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT ID_Medicament, SUM(Quantite_Vendue) as NumberProducts, SUM(Total_Facture) as TotalMoney, SUM(Prix_Achat) as TotalCost FROM Ventes WHERE strftime('%m/%Y', substr(Date_Vente, 7, 4) || '-' || substr(Date_Vente, 4, 2) || '-' || substr(Date_Vente, 1, 2))  = ? GROUP BY ID_Medicament''', (datetime.now().date().strftime('%m/%Y'),))

    result = cursor.fetchall()
    conn.close()
    return result



"""
print("1.  ",get_statistique_mois())
# get statistics par salarié
data = get_stat_salarie_mois()
for i in data:
    print("2.    ",dict(i)) 
# extraire les medicaments vendus pour la journée
data = get_medicament_vendu_mois() 
for i in data:
    print(dict(i)) """



def create_stock_table():
        # Connect to the database
        conn = sqlite3.connect(dataset)
        cursor = conn.cursor()
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
        conn = sqlite3.connect(dataset)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(ID_Stock) as numberStock, SUM(Quantite_Actuelle) as NumberProducts, SUM(Prix_Achat) as totalAchat, SUM(Prix_Vente) as totalVente FROM Stock''')
        result = cursor.fetchone()
        conn.close()
        return dict(result)

# get les medicament avec leur quentité qui expirand dans les deux mois prochaines 
def get_medicament_expirant():
    # Connect to the database
    conn = sqlite3.connect(dataset)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
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




print("1.  ",get_statistique_stock())

print("2.  ",[ dict(i) for i in get_medicament_expirant()])






