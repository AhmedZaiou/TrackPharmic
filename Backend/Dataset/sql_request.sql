-- Table Medicament
CREATE TABLE IF NOT EXISTS Medicament (
    id_medicament INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    caracteristique TEXT,
    code_ean_13 VARCHAR(13) UNIQUE,
    medicament_generique BOOLEAN DEFAULT 0,
    prix_officine REAL,
    prix_public_de_vente REAL,
    prix_base_remboursement REAL,
    prix_hospitalier REAL,
    substance_active_dci TEXT,
    classe_therapeutique TEXT,
    min_stock INTEGER DEFAULT 0,
    stock_actuel INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table Stock
CREATE TABLE IF NOT EXISTS Stock (
    id_stock INTEGER PRIMARY KEY AUTOINCREMENT,
    id_medicament INTEGER NOT NULL,
    id_commande INTEGER,
    id_salarie INTEGER,
    prix_achat REAL,
    prix_vente REAL,
    prix_conseille REAL,
    date_achat DATE,
    date_expiration DATE,
    stock_initial INTEGER DEFAULT 0,
    quantite_actuelle INTEGER DEFAULT 0,
    quantite_minimale INTEGER DEFAULT 0,
    quantite_maximale INTEGER,
    date_reception DATE,
    date_derniere_sortie DATE,
    FOREIGN KEY (id_medicament) REFERENCES Medicament (id_medicament) ON DELETE CASCADE,
    FOREIGN KEY (id_commande) REFERENCES Commandes (id_commande),
    FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
);

-- Table Ventes
CREATE TABLE IF NOT EXISTS Ventes (
    id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
    id_medicament INTEGER NOT NULL,
    id_commande_entre INTEGER,
    prix_achat REAL,
    prix_vente REAL,
    date_vente DATE NOT NULL,
    quantite_vendue INTEGER DEFAULT 0,
    total_facture REAL,
    id_client INTEGER,
    numero_facture VARCHAR(50),
    id_salarie INTEGER,
    id_stock_item INTEGER,
    FOREIGN KEY (id_medicament) REFERENCES Medicament (id_medicament),
    FOREIGN KEY (id_commande_entre) REFERENCES Commandes (id_commande),
    FOREIGN KEY (id_client) REFERENCES Clients (id_client),
    FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie),
    FOREIGN KEY (id_stock_item) REFERENCES Stock (id_stock)
);

-- Table Achats
CREATE TABLE IF NOT EXISTS Achats (
    id_achat INTEGER PRIMARY KEY AUTOINCREMENT,
    id_medicament INTEGER NOT NULL,
    id_fournisseur INTEGER,
    quantite_achetee INTEGER DEFAULT 0,
    prix_achat_unitaire REAL,
    prix_vente_unitaire REAL,
    date_achat DATE NOT NULL,
    date_expiration DATE,
    id_salarie INTEGER,
    FOREIGN KEY (id_medicament) REFERENCES Medicament (id_medicament),
    FOREIGN KEY (id_fournisseur) REFERENCES Fournisseur (id_fournisseur),
    FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
);

-- Table Commandes
CREATE TABLE IF NOT EXISTS Commandes (
    id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
    id_fournisseur INTEGER,
    date_commande DATE NOT NULL,
    date_reception_prev DATE,
    statut_reception TEXT,
    receptionniste VARCHAR(100),
    produits_recus TEXT,
    date_reception DATE,
    id_salarie INTEGER,
    status_incl TEXT,
    FOREIGN KEY (id_fournisseur) REFERENCES Fournisseur (id_fournisseur),
    FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
);

-- Table Salaries
CREATE TABLE IF NOT EXISTS Salaries (
    id_salarie INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    cin VARCHAR(20) UNIQUE,
    telephone VARCHAR(15),
    email VARCHAR(100),
    adresse TEXT,
    photo TEXT,
    salaire REAL,
    type_contrat VARCHAR(50),
    date_embauche DATE,
    grade VARCHAR(50),
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table Clients
CREATE TABLE IF NOT EXISTS Clients (
    id_client INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    cin VARCHAR(20) UNIQUE,
    telephone VARCHAR(15),
    email VARCHAR(100),
    adresse TEXT,
    max_credit REAL,
    credit_actuel REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table Pharmacies
CREATE TABLE IF NOT EXISTS Pharmacies (
    id_pharmacie INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100),
    adresse TEXT,
    telephone VARCHAR(15),
    email VARCHAR(100),
    outvalue TEXT,
    invalue TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table Echanges
CREATE TABLE IF NOT EXISTS Echanges (
    id_echange INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pharmacie INTEGER,
    id_facture INTEGER,
    date_echange DATE NOT NULL,
    total_facture REAL,
    sens VARCHAR(10),
    id_salarie INTEGER,
    FOREIGN KEY (id_pharmacie) REFERENCES Pharmacies (id_pharmacie),
    FOREIGN KEY (id_facture) REFERENCES Ventes (id_vente),
    FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
);

-- Table Credit
CREATE TABLE IF NOT EXISTS Credit (
    id_credit INTEGER PRIMARY KEY AUTOINCREMENT,
    id_client INTEGER,
    numero_facture VARCHAR(50),
    montant_paye REAL,
    reste_a_payer REAL,
    date_dernier_paiement DATE,
    statut TEXT,
    id_salarie INTEGER,
    FOREIGN KEY (id_client) REFERENCES Clients (id_client),
    FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
);

-- Table Payment
CREATE TABLE IF NOT EXISTS Payment (
    id_payment INTEGER PRIMARY KEY AUTOINCREMENT,
    id_client INTEGER,
    numero_facture VARCHAR(50),
    montant_paye REAL,
    date_paiement DATE NOT NULL,
    id_salarie INTEGER,
    FOREIGN KEY (id_client) REFERENCES Clients (id_client),
    FOREIGN KEY (id_salarie) REFERENCES Salaries (id_salarie)
);

-- Table Fournisseur
CREATE TABLE IF NOT EXISTS Fournisseur (
    id_fournisseur INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_fournisseur VARCHAR(100),
    telephone VARCHAR(15),
    email VARCHAR(100),
    adresse TEXT,
    ville VARCHAR(50),
    pays VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
