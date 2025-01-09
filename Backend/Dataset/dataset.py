 
import sqlite3
from Frontend.utils.utils import *


# Fonction : create_table_medicament
def create_table_medicament():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Medicament (
                ID_Medicament INTEGER PRIMARY KEY AUTOINCREMENT,
                Nom TEXT,
                caracteristique TEXT,
                Code_EAN_13 TEXT UNIQUE,
                Medicament_GENERIQUE TEXT,
                Prix_Officine TEXT,
                Prix_Public_de_Vente REAL,
                Prix_base_remboursement REAL,
                Prix_Hospitalier REAL,
                Substance_active_DCI TEXT,
                Classe_Therapeutique TEXT
            )
        """)

def ajouter_medicament(nom, caracteristique, code_ean_13, medicament_generique, prix_officine, prix_public_de_vente,
                       prix_base_remboursement, prix_hospitalier, substance_active_dci, classe_therapeutique):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Medicament (
                Nom, caracteristique, Code_EAN_13, Medicament_GENERIQUE, Prix_Officine, Prix_Public_de_Vente,
                Prix_base_remboursement, Prix_Hospitalier, Substance_active_DCI, Classe_Therapeutique
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, caracteristique, code_ean_13, medicament_generique, prix_officine, prix_public_de_vente,
              prix_base_remboursement, prix_hospitalier, substance_active_dci, classe_therapeutique))


def supprimer_medicament(id_medicament):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Medicament WHERE ID_Medicament = ?", (id_medicament,))


def modifier_medicament(id_medicament, nom, caracteristique, code_ean_13, medicament_generique, prix_officine,
                        prix_public_de_vente, prix_base_remboursement, prix_hospitalier, substance_active_dci,
                        classe_therapeutique):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Medicament SET
                Nom = ?, caracteristique = ?, Code_EAN_13 = ?, Medicament_GENERIQUE = ?, Prix_Officine = ?,
                Prix_Public_de_Vente = ?, Prix_base_remboursement = ?, Prix_Hospitalier = ?, Substance_active_DCI = ?,
                Classe_Therapeutique = ?
            WHERE ID_Medicament = ?
        """, (nom, caracteristique, code_ean_13, medicament_generique, prix_officine, prix_public_de_vente,
              prix_base_remboursement, prix_hospitalier, substance_active_dci, classe_therapeutique, id_medicament))


def extraire_medicament(id_medicament):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE ID_Medicament = ?", (id_medicament,))
        return cursor.fetchone()

def extraire_medicament_code_barre(code_barre):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament WHERE Code_EAN_13 = ?", (code_barre,))
        return cursor.fetchone()


def extraire_tous_medicament():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament")
        return cursor.fetchall()





 

# Fonction : create_table_stock
def create_table_stock():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Stock (
                ID_Stock INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Medicament INTEGER NOT NULL,
                ID_Commande INTEGER,
                Prix_Achat REAL,
                Prix_Vente REAL,
                Prix_Conseille REAL,
                Date_Achat TEXT,
                Date_Expiration TEXT,
                Stock_Initial INTEGER,
                Quantite_Actuelle INTEGER,
                Quantite_Minimale INTEGER,
                Quantite_Maximale INTEGER,
                Quantite_Commandee INTEGER,
                Date_Reception TEXT,
                Date_Derniere_Sortie TEXT,
                FOREIGN KEY(ID_Medicament) REFERENCES Medicament(ID_Medicament)
            )
        """)

# Fonction : ajouter_stock
def ajouter_stock(id_medicament, id_commande, prix_achat, prix_vente, prix_conseille, date_achat, date_expiration,
                  stock_initial, quantite_actuelle, quantite_minimale, quantite_maximale, quantite_commandee,
                  date_reception, date_derniere_sortie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Stock (
                ID_Medicament, ID_Commande, Prix_Achat, Prix_Vente, Prix_Conseille,
                Date_Achat, Date_Expiration, Stock_Initial, Quantite_Actuelle,
                Quantite_Minimale, Quantite_Maximale, Quantite_Commandee,
                Date_Reception, Date_Derniere_Sortie
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_medicament, id_commande, prix_achat, prix_vente, prix_conseille, date_achat, date_expiration,
              stock_initial, quantite_actuelle, quantite_minimale, quantite_maximale, quantite_commandee,
              date_reception, date_derniere_sortie))

# Fonction : supprimer_stock
def supprimer_stock(id_stock):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Stock WHERE ID_Stock = ?", (id_stock,))

# Fonction : modifier_stock
def modifier_stock(id_stock, id_medicament, id_commande, prix_achat, prix_vente, prix_conseille, date_achat,
                   date_expiration, stock_initial, quantite_actuelle, quantite_minimale, quantite_maximale,
                   quantite_commandee, date_reception, date_derniere_sortie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Stock SET
                ID_Medicament = ?, ID_Commande = ?, Prix_Achat = ?, Prix_Vente = ?, Prix_Conseille = ?,
                Date_Achat = ?, Date_Expiration = ?, Stock_Initial = ?, Quantite_Actuelle = ?,
                Quantite_Minimale = ?, Quantite_Maximale = ?, Quantite_Commandee = ?,
                Date_Reception = ?, Date_Derniere_Sortie = ?
            WHERE ID_Stock = ?
        """, (id_medicament, id_commande, prix_achat, prix_vente, prix_conseille, date_achat, date_expiration,
              stock_initial, quantite_actuelle, quantite_minimale, quantite_maximale, quantite_commandee,
              date_reception, date_derniere_sortie, id_stock))

# Fonction : extraire_stock
def extraire_stock(id_stock):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Stock WHERE ID_Stock = ?", (id_stock,))
        return cursor.fetchone()

# Fonction : extraire_tous_stock
def extraire_tous_stock():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Stock")
        return cursor.fetchall()



 

# Fonction : create_table_ventes
def create_table_ventes():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ventes (
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
            )
        """)

# Fonction : ajouter_vente
def ajouter_vente(id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture,
                  id_client, numero_facture, id_salarie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Ventes (
                ID_Medicament, ID_Commande_Entre, Prix_Achat, Prix_Vente, Date_Vente,
                Quantite_Vendue, Total_Facture, ID_Client, Numero_Facture, ID_Salarie
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture,
              id_client, numero_facture, id_salarie))

# Fonction : supprimer_vente
def supprimer_vente(id_vente):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ventes WHERE ID_Vente = ?", (id_vente,))

# Fonction : modifier_vente
def modifier_vente(id_vente, id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue,
                   total_facture, id_client, numero_facture, id_salarie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Ventes SET
                ID_Medicament = ?, ID_Commande_Entre = ?, Prix_Achat = ?, Prix_Vente = ?, Date_Vente = ?,
                Quantite_Vendue = ?, Total_Facture = ?, ID_Client = ?, Numero_Facture = ?, ID_Salarie = ?
            WHERE ID_Vente = ?
        """, (id_medicament, id_commande_entre, prix_achat, prix_vente, date_vente, quantite_vendue, total_facture,
              id_client, numero_facture, id_salarie, id_vente))

# Fonction : extraire_vente
def extraire_vente(id_vente):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ventes WHERE ID_Vente = ?", (id_vente,))
        return cursor.fetchone()

# Fonction : extraire_tous_ventes
def extraire_tous_ventes():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ventes")
        return cursor.fetchall()


 

# Fonction : create_table_achats
def create_table_achats():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Achats (
                ID_Achat INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Medicament INTEGER NOT NULL,
                ID_Fournisseur INTEGER NOT NULL,
                Quantite_Achetee INTEGER,
                Prix_Achat_Unitaire REAL,
                Prix_Vente_Unitaire REAL,
                Date_Achat TEXT,
                Date_Expiration TEXT,
                ID_Salarie INTEGER,
                FOREIGN KEY(ID_Medicament) REFERENCES Medicament(ID_Medicament),
                FOREIGN KEY(ID_Fournisseur) REFERENCES Fournisseur(ID_Fournisseur)
            )
        """)

# Fonction : ajouter_achat
def ajouter_achat(id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, 
                  date_achat, date_expiration, id_salarie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Achats (
                ID_Medicament, ID_Fournisseur, Quantite_Achetee, Prix_Achat_Unitaire, Prix_Vente_Unitaire, 
                Date_Achat, Date_Expiration, ID_Salarie
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, 
              date_achat, date_expiration, id_salarie))

# Fonction : supprimer_achat
def supprimer_achat(id_achat):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Achats WHERE ID_Achat = ?", (id_achat,))

# Fonction : modifier_achat
def modifier_achat(id_achat, id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire,
                   date_achat, date_expiration, id_salarie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Achats SET 
                ID_Medicament = ?, ID_Fournisseur = ?, Quantite_Achetee = ?, Prix_Achat_Unitaire = ?, 
                Prix_Vente_Unitaire = ?, Date_Achat = ?, Date_Expiration = ?, ID_Salarie = ?
            WHERE ID_Achat = ?
        """, (id_medicament, id_fournisseur, quantite_achetee, prix_achat_unitaire, prix_vente_unitaire, 
              date_achat, date_expiration, id_salarie, id_achat))

# Fonction : extraire_achat
def extraire_achat(id_achat):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Achats WHERE ID_Achat = ?", (id_achat,))
        return cursor.fetchone()

# Fonction : extraire_tous_achats
def extraire_tous_achats():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Achats")
        return cursor.fetchall()




 

# Fonction : create_table_commandes
def create_table_commandes():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
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
            )
        """)

# Fonction : ajouter_commande
def ajouter_commande(liste_produits, id_fournisseur, date_commande, date_reception_prev, statut_reception, 
                     receptionniste, produits_reçus, date_reception, id_salarie, status_incl):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Commandes (
                Liste_Produits, ID_Fournisseur, Date_Commande, Date_Reception_Prevue, Statut_Reception, 
                Receptionniste, Produits_Reçus, Date_Reception, ID_Salarie, Status_Incl
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (liste_produits, id_fournisseur, date_commande, date_reception_prev, statut_reception, 
              receptionniste, produits_reçus, date_reception, id_salarie, status_incl))

# Fonction : supprimer_commande
def supprimer_commande(id_commande):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Commandes WHERE ID_Commande = ?", (id_commande,))

# Fonction : modifier_commande
def modifier_commande(id_commande, liste_produits, id_fournisseur, date_commande, date_reception_prev, 
                      statut_reception, receptionniste, produits_reçus, date_reception, id_salarie, status_incl):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Commandes SET 
                Liste_Produits = ?, ID_Fournisseur = ?, Date_Commande = ?, Date_Reception_Prevue = ?, 
                Statut_Reception = ?, Receptionniste = ?, Produits_Reçus = ?, Date_Reception = ?, 
                ID_Salarie = ?, Status_Incl = ? 
            WHERE ID_Commande = ?
        """, (liste_produits, id_fournisseur, date_commande, date_reception_prev, statut_reception, 
              receptionniste, produits_reçus, date_reception, id_salarie, status_incl, id_commande))

# Fonction : extraire_commande
def extraire_commande(id_commande):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Commandes WHERE ID_Commande = ?", (id_commande,))
        return cursor.fetchone()

# Fonction : extraire_tous_commandes
def extraire_tous_commandes():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Commandes")
        return cursor.fetchall()



 

# Fonction : create_table_salaries
def create_table_salaries():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Salaries (
                ID_Salarie INTEGER PRIMARY KEY AUTOINCREMENT,
                Nom TEXT NOT NULL,
                Prenom TEXT NOT NULL,
                CIN TEXT NOT NULL,
                Photo TEXT,
                Salaire REAL NOT NULL,
                Type_Contrat TEXT NOT NULL,
                Jours_Travail INTEGER NOT NULL,
                Date_Embauche TEXT NOT NULL,
                Grade TEXT NOT NULL
            )
        """)

# Fonction : ajouter_salarie
def ajouter_salarie(nom, prenom, cin, photo, salaire, type_contrat, jours_travail, date_embauche, grade):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Salaries (Nom, Prenom, CIN, Photo, Salaire, Type_Contrat, Jours_Travail, Date_Embauche, Grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, prenom, cin, photo, salaire, type_contrat, jours_travail, date_embauche, grade))

# Fonction : supprimer_salarie
def supprimer_salarie(id_salarie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Salaries WHERE ID_Salarie = ?", (id_salarie,))

# Fonction : modifier_salarie
def modifier_salarie(id_salarie, nom, prenom, cin, photo, salaire, type_contrat, jours_travail, date_embauche, grade):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Salaries SET
                Nom = ?, Prenom = ?, CIN = ?, Photo = ?, Salaire = ?, Type_Contrat = ?, Jours_Travail = ?, 
                Date_Embauche = ?, Grade = ?
            WHERE ID_Salarie = ?
        """, (nom, prenom, cin, photo, salaire, type_contrat, jours_travail, date_embauche, grade, id_salarie))

# Fonction : extraire_salarie
def extraire_salarie(id_salarie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Salaries WHERE ID_Salarie = ?", (id_salarie,))
        return cursor.fetchone()

# Fonction : extraire_tous_salaries
def extraire_tous_salaries():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Salaries")
        return cursor.fetchall()

 

# Fonction : create_table_clients
def create_table_clients():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clients (
                ID_Client INTEGER PRIMARY KEY AUTOINCREMENT,
                Nom TEXT NOT NULL,
                Prenom TEXT NOT NULL,
                CIN TEXT NOT NULL,
                Telephone TEXT,
                Email TEXT,
                Adresse TEXT,
                Max_Credit REAL NOT NULL,
                Credit_Actuel REAL NOT NULL
            )
        """)

# Fonction : ajouter_client
def ajouter_client(nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Clients (Nom, Prenom, CIN, Telephone, Email, Adresse, Max_Credit, Credit_Actuel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel))

# Fonction : supprimer_client
def supprimer_client(id_client):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clients WHERE ID_Client = ?", (id_client,))

# Fonction : modifier_client
def modifier_client(id_client, nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Clients SET
                Nom = ?, Prenom = ?, CIN = ?, Telephone = ?, Email = ?, Adresse = ?, Max_Credit = ?, 
                Credit_Actuel = ?
            WHERE ID_Client = ?
        """, (nom, prenom, cin, telephone, email, adresse, max_credit, credit_actuel, id_client))

# Fonction : extraire_client
def extraire_client(id_client):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients WHERE ID_Client = ?", (id_client,))
        return cursor.fetchone()

# Fonction : extraire_tous_clients
def extraire_tous_clients():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clients")
        return cursor.fetchall()


 

# Fonction : create_table_echanges
def create_table_echanges():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Echanges (
                ID_Echange INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Pharmacie INTEGER NOT NULL,
                Liste_Produits TEXT NOT NULL,
                Date_Echange TEXT NOT NULL,
                Total_Facture REAL NOT NULL,
                Demandeur TEXT NOT NULL,
                ID_Salarie INTEGER NOT NULL
            )
        """)

# Fonction : ajouter_echange
def ajouter_echange(id_pharmacie, liste_produits, date_echange, total_facture, demandeur, id_salarie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Echanges (ID_Pharmacie, Liste_Produits, Date_Echange, Total_Facture, Demandeur, ID_Salarie)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_pharmacie, liste_produits, date_echange, total_facture, demandeur, id_salarie))

# Fonction : supprimer_echange
def supprimer_echange(id_echange):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Echanges WHERE ID_Echange = ?", (id_echange,))

# Fonction : modifier_echange
def modifier_echange(id_echange, id_pharmacie, liste_produits, date_echange, total_facture, demandeur, id_salarie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Echanges SET
                ID_Pharmacie = ?, Liste_Produits = ?, Date_Echange = ?, Total_Facture = ?, Demandeur = ?, ID_Salarie = ?
            WHERE ID_Echange = ?
        """, (id_pharmacie, liste_produits, date_echange, total_facture, demandeur, id_salarie, id_echange))

# Fonction : extraire_echange
def extraire_echange(id_echange):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Echanges WHERE ID_Echange = ?", (id_echange,))
        return cursor.fetchone()

# Fonction : extraire_tous_echanges
def extraire_tous_echanges():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Echanges")
        return cursor.fetchall()
 

# Fonction : create_table_credit
def create_table_credit():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Credit (
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
        """)

# Fonction : ajouter_credit
def ajouter_credit(id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Credit (ID_Client, Numero_Facture, Montant_Paye, Reste_A_Payer, Date_Dernier_Paiement, Statut, ID_Salarie)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie))

# Fonction : supprimer_credit
def supprimer_credit(id_credit):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Credit WHERE ID_Credit = ?", (id_credit,))

# Fonction : modifier_credit
def modifier_credit(id_credit, id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Credit SET 
                ID_Client = ?, Numero_Facture = ?, Montant_Paye = ?, Reste_A_Payer = ?, 
                Date_Dernier_Paiement = ?, Statut = ?, ID_Salarie = ? 
            WHERE ID_Credit = ?
        """, (id_client, numero_facture, montant_paye, reste_a_payer, date_dernier_paiement, statut, id_salarie, id_credit))

# Fonction : extraire_credit
def extraire_credit(id_credit):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Credit WHERE ID_Credit = ?", (id_credit,))
        return cursor.fetchone()

# Fonction : extraire_tous_credits
def extraire_tous_credits():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Credit")
        return cursor.fetchall()



 

# Fonction : create_table_fournisseur
def create_table_fournisseur():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Fournisseurs (
                ID_Fournisseur INTEGER PRIMARY KEY AUTOINCREMENT,
                Nom_Fournisseur TEXT NOT NULL,
                Telephone TEXT,
                Email TEXT,
                Adresse TEXT,
                Ville TEXT,
                Pays TEXT
            )
        """)

# Fonction : ajouter_fournisseur
def ajouter_fournisseur(nom_fournisseur, telephone, email, adresse, ville, pays):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Fournisseurs (Nom_Fournisseur, Telephone, Email, Adresse, Ville, Pays)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom_fournisseur, telephone, email, adresse, ville, pays))

# Fonction : supprimer_fournisseur
def supprimer_fournisseur(id_fournisseur):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Fournisseurs WHERE ID_Fournisseur = ?", (id_fournisseur,))

# Fonction : modifier_fournisseur
def modifier_fournisseur(id_fournisseur, nom_fournisseur, telephone, email, adresse, ville, pays):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Fournisseurs SET 
                Nom_Fournisseur = ?, Telephone = ?, Email = ?, Adresse = ?, Ville = ?, Pays = ? 
            WHERE ID_Fournisseur = ?
        """, (nom_fournisseur, telephone, email, adresse, ville, pays, id_fournisseur))

# Fonction : extraire_fournisseur
def extraire_fournisseur(id_fournisseur):
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseurs WHERE ID_Fournisseur = ?", (id_fournisseur,))
        return cursor.fetchone()

# Fonction : extraire_tous_fournisseurs
def extraire_tous_fournisseurs():
    with sqlite3.connect( dataset) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseurs")
        return cursor.fetchall()
