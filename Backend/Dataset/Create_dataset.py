import mysql.connector
from Frontend.utils.utils import *




def create_medicament_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Medicament (
        ID_Medicament INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom TEXT NOT NULL,
        Caracteristique TEXT,
        Code_EAN_13 TEXT,
        Medicament_Generique TEXT,
        Prix_Officine REAL,
        Prix_Public_De_Vente REAL,
        Prix_Base_Remboursement REAL,
        Prix_Hospitalier REAL,
        Substance_Active_DCI TEXT,
        Classe_Therapeutique TEXT,
        Min_Stock INTEGER,
        Stock_Actuel INTEGER
    );
    """)
    conn.commit()
    conn.close()

def create_stock_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Stock (
        ID_Stock INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Medicament INTEGER,
        ID_Commande INTEGER,
        ID_Salarie INTEGER,
        Prix_Achat REAL,
        Prix_Vente REAL,
        Prix_Conseille REAL,
        Date_Achat TEXT,
        Date_Expiration TEXT,
        Stock_Initial INTEGER,
        Quantite_Actuelle INTEGER,
        Quantite_Minimale INTEGER,
        Quantite_Maximale INTEGER,
        Date_Reception TEXT,
        Date_Derniere_Sortie TEXT,
        FOREIGN KEY (ID_Medicament) REFERENCES Medicament (ID_Medicament),
        FOREIGN KEY (ID_Commande) REFERENCES Commandes (ID_Commande),
        FOREIGN KEY (ID_Salarie) REFERENCES Salaries (ID_Salarie)
    );
    """)
    conn.commit()
    conn.close()

def create_ventes_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ventes (
        ID_Vente INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Medicament INTEGER,
        ID_Commande_Entre INTEGER,
        Prix_Achat REAL,
        Prix_Vente REAL,
        Date_Vente TEXT,
        Quantite_Vendue INTEGER,
        Total_Facture REAL,
        ID_Client INTEGER,
        Numero_Facture TEXT,
        ID_Salarie INTEGER,
        ID_Stock_Item INTEGER,
        FOREIGN KEY (ID_Medicament) REFERENCES Medicament (ID_Medicament),
        FOREIGN KEY (ID_Commande_Entre) REFERENCES Commandes (ID_Commande),
        FOREIGN KEY (ID_Client) REFERENCES Clients (ID_Client),
        FOREIGN KEY (ID_Salarie) REFERENCES Salaries (ID_Salarie),
        FOREIGN KEY (ID_Stock_Item) REFERENCES Stock (ID_Stock)
    );
    """)
    conn.commit()
    conn.close()

def create_achats_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Achats (
        ID_Achat INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Medicament INTEGER,
        ID_Fournisseur INTEGER,
        Quantite_Achetee INTEGER,
        Prix_Achat_Unitaire REAL,
        Prix_Vente_Unitaire REAL,
        Date_Achat TEXT,
        Date_Expiration TEXT,
        ID_Salarie INTEGER,
        FOREIGN KEY (ID_Medicament) REFERENCES Medicament (ID_Medicament),
        FOREIGN KEY (ID_Fournisseur) REFERENCES Fournisseur (ID_Fournisseur),
        FOREIGN KEY (ID_Salarie) REFERENCES Salaries (ID_Salarie)
    );
    """)
    conn.commit()
    conn.close()

def create_commandes_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Commandes (
        ID_Commande INTEGER PRIMARY KEY AUTOINCREMENT,
        Liste_Produits TEXT,
        ID_Fournisseur INTEGER,
        Date_Commande TEXT,
        Date_Reception_Prev TEXT,
        Statut_Reception TEXT,
        Receptionniste TEXT,
        Produits_Reçus TEXT,
        Date_Reception TEXT,
        ID_Salarie INTEGER,
        Status_Incl TEXT,
        FOREIGN KEY (ID_Fournisseur) REFERENCES Fournisseur (ID_Fournisseur),
        FOREIGN KEY (ID_Salarie) REFERENCES Salaries (ID_Salarie)
    );
    """)
    conn.commit()
    conn.close()

def create_salaries_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Salaries (
        ID_Salarie INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom TEXT,
        Prenom TEXT,
        CIN TEXT,
        Telephone TEXT,
        Email TEXT,
        Adresse TEXT,
        Photo TEXT,
        Salaire REAL,
        Type_Contrat TEXT,
        Date_Embauche TEXT,
        Grade TEXT,
        Password TEXT
    );
    """)
    conn.commit()
    conn.close()

def create_clients_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Clients (
        ID_Client INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom TEXT,
        Prenom TEXT,
        CIN TEXT,
        Telephone TEXT,
        Email TEXT,
        Adresse TEXT,
        Max_Credit REAL,
        Credit_Actuel REAL
    );
    """)
    conn.commit()
    conn.close()

def create_pharmacies_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pharmacies (
        ID_Pharmacie INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom TEXT,
        Adresse TEXT,
        Telephone TEXT,
        Email TEXT,
        Outvalue TEXT,
        Invalue TEXT
    );
    """)
    conn.commit()
    conn.close()

def create_echanges_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Echanges (
        ID_Echange INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Pharmacie INTEGER,
        ID_Facture INTEGER,
        Date_Echange TEXT,
        Total_Facture REAL,
        Sens TEXT,
        ID_Salarie INTEGER,
        FOREIGN KEY (ID_Pharmacie) REFERENCES Pharmacies (ID_Pharmacie),
        FOREIGN KEY (ID_Facture) REFERENCES Ventes (ID_Vente),
        FOREIGN KEY (ID_Salarie) REFERENCES Salaries (ID_Salarie)
    );
    """)
    conn.commit()
    conn.close()

def create_credit_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Credit (
        ID_Credit INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Client INTEGER,
        Numero_Facture TEXT,
        Montant_Paye REAL,
        Reste_A_Payer REAL,
        Date_Dernier_Paiement TEXT,
        Statut TEXT,
        ID_Salarie INTEGER,
        FOREIGN KEY (ID_Client) REFERENCES Clients (ID_Client),
        FOREIGN KEY (ID_Salarie) REFERENCES Salaries (ID_Salarie)
    );
    """)
    conn.commit()
    conn.close()

def create_payment_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Payment (
        ID_Payment INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Client INTEGER,
        Numero_Facture TEXT,
        Montant_Paye REAL,
        Date_Paiement TEXT,
        ID_Salarie INTEGER,
        FOREIGN KEY (ID_Client) REFERENCES Clients (ID_Client),
        FOREIGN KEY (ID_Salarie) REFERENCES Salaries (ID_Salarie)
    );
    """)
    conn.commit()
    conn.close()

def create_fournisseur_table():
    conn = mysql.connector.connect(host=host,user=user,password=password,database=database)
    cursor =  conn.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Fournisseur (
        ID_Fournisseur INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom_Fournisseur TEXT,
        Telephone TEXT,
        Email TEXT,
        Adresse TEXT,
        Ville TEXT,
        Pays TEXT
    );
    """)
    conn.commit()
    conn.close()
