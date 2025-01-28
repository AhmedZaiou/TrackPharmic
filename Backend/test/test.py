

import unittest
import json
from Dataset.achats import Achats # type: ignore





import unittest
import json

class TestClientsMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_clients.db'
        cls.clients_db = Clients()
        cls.clients_db.create_table_clients()

    def test_all_functions(self):
        # 1. Ajouter un client
        self.clients_db.ajouter_client('Alice', 'Johnson', '123456789', '0123456789', 'alicejohnson@example.com', '123 Elm St', 5000.0, 1000.0)
        client_info = json.loads(self.clients_db.extraire_client(1))
        self.assertEqual(client_info['nom'], 'Alice')
        self.assertEqual(client_info['prenom'], 'Johnson')

        # 2. Modifier un client
        self.clients_db.modifier_client(1, 'Alice', 'Johnson', '123456789', '0987654321', 'alicejohnson@newmail.com', '456 Oak St', 6000.0, 1500.0)
        client_info = json.loads(self.clients_db.extraire_client(1))
        self.assertEqual(client_info['telephone'], '0987654321')
        self.assertEqual(client_info['email'], 'alicejohnson@newmail.com')

        # 3. Ajouter du crédit à un client
        self.clients_db.ajouter_credit_client(1, 500.0)
        client_info = json.loads(self.clients_db.extraire_client(1))
        self.assertEqual(client_info['credit_actuel'], 2000.0)

        # 4. Extraire un client par ID
        client_info = json.loads(self.clients_db.extraire_client_id(1))
        self.assertEqual(client_info['nom'], 'Alice')

        # 5. Extraire un client par nom, prénom et CIN
        client_info = json.loads(self.clients_db.extraire_client_info('Alice', 'Johnson', '123456789'))
        self.assertEqual(client_info['nom'], 'Alice')

        # 6. Extraire tous les clients dont le nom contient 'Al'
        clients_info = json.loads(self.clients_db.extraire_client_nom_like('Al'))
        self.assertEqual(len(clients_info), 1)

        # 7. Extraire tous les clients
        all_clients = json.loads(self.clients_db.extraire_tous_clients())
        self.assertEqual(len(all_clients), 1)

        # 8. Extraire tous les clients avec du crédit
        self.clients_db.ajouter_client('Bob', 'Smith', '987654321', '0123456789', 'bobsmith@example.com', '789 Pine St', 7000.0, 3000.0)
        clients_with_credit = json.loads(self.clients_db.extraire_tous_client_with_credit())
        self.assertEqual(len(clients_with_credit), 2)

        # 9. Supprimer un client
        self.clients_db.supprimer_client(1)
        client_info = self.clients_db.extraire_client(1)
        self.assertIsNone(client_info)

if __name__ == '__main__':
    unittest.main()




import unittest
import json

class TestCommandesMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_commandes.db'
        cls.commandes_db = Commandes()
        cls.commandes_db.create_table_commandes()

    def test_all_functions(self):
        # 1. Ajouter une commande
        self.commandes_db.ajouter_commande(1, '2025-01-28', '2025-02-28', 'En attente', 'John Doe', 'Aspirine, Paracétamol', '2025-01-30', 1, 'Incluse')
        commande_info = json.loads(self.commandes_db.extraire_commande(1))
        self.assertEqual(commande_info['id_fournisseur'], 1)
        self.assertEqual(commande_info['statut_reception'], 'En attente')
        self.assertEqual(commande_info['receptionniste'], 'John Doe')

        # 2. Modifier la commande
        self.commandes_db.modifier_commande(1, 2, '2025-01-29', '2025-03-01', 'Livrée', 'Jane Smith', 'Aspirine, Ibuprofène', '2025-02-01', 2, 'Exclue')
        commande_info = json.loads(self.commandes_db.extraire_commande(1))
        self.assertEqual(commande_info['statut_reception'], 'Livrée')
        self.assertEqual(commande_info['produits_recus'], 'Aspirine, Ibuprofène')

        # 3. Marquer la commande comme complète
        self.commandes_db.complet_commande(1)
        commande_info = json.loads(self.commandes_db.extraire_commande(1))
        self.assertEqual(commande_info['statut_reception'], 'Complète')

        # 4. Supprimer la commande
        self.commandes_db.supprimer_commande(1)
        commande_info = self.commandes_db.extraire_commande(1)
        self.assertIsNone(commande_info)

        # 5. Ajouter deux commandes pour le test d'extraction de toutes les commandes
        self.commandes_db.ajouter_commande(1, '2025-01-28', '2025-02-28', 'En attente', 'John Doe', 'Aspirine, Paracétamol', '2025-01-30', 1, 'Incluse')
        self.commandes_db.ajouter_commande(2, '2025-01-29', '2025-03-01', 'Livrée', 'Jane Smith', 'Aspirine, Ibuprofène', '2025-02-01', 2, 'Exclue')

        all_commandes = json.loads(self.commandes_db.extraire_tous_commandes())
        self.assertEqual(len(all_commandes), 2)

if __name__ == '__main__':
    unittest.main()




import unittest
import json

class TestCreditMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_credit.db'
        cls.credit_db = Credit()
        cls.credit_db.create_table_credit()

    def test_all_functions(self):
        # 1. Ajouter un crédit
        self.credit_db.ajouter_credit(1, 'FAC001', 1000.0, 500.0, '2025-01-01', 'en cours', 1)
        credit_info = json.loads(self.credit_db.extraire_credit(1))
        self.assertEqual(credit_info['id_client'], 1)
        self.assertEqual(credit_info['montant_paye'], 1000.0)

        # 2. Modifier un crédit
        self.credit_db.modifier_credit(1, 1, 'FAC001', 1200.0, 300.0, '2025-02-01', 'en cours', 1)
        credit_info = json.loads(self.credit_db.extraire_credit(1))
        self.assertEqual(credit_info['montant_paye'], 1200.0)
        self.assertEqual(credit_info['reste_a_payer'], 300.0)

        # 3. Extraire tous les crédits
        all_credits = json.loads(self.credit_db.extraire_tous_credits())
        self.assertEqual(len(all_credits), 1)

        # 4. Extraire crédits par ID client
        credits_by_client = json.loads(self.credit_db.extraire_credit_with_id_client(1))
        self.assertEqual(len(credits_by_client), 1)

        # 5. Supprimer un crédit
        self.credit_db.supprimer_credit(1)
        credit_info = self.credit_db.extraire_credit(1)
        self.assertIsNone(credit_info)

if __name__ == '__main__':
    unittest.main()




import unittest
import json

class TestEchangesMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_echanges.db'
        cls.echanges_db = Echanges()
        cls.echanges_db.create_table_echanges()

    def test_all_functions(self):
        # 1. Ajouter un échange
        self.echanges_db.ajouter_echange(1, 1, '2025-01-01', 500.0, 'sortie', 1)
        echange_info = json.loads(self.echanges_db.extraire_echange(1))
        self.assertEqual(echange_info['id_pharmacie'], 1)

        # 2. Modifier un échange
        self.echanges_db.modifier_echange(1, 1, 1, '2025-02-01', 600.0, 'entree', 1)
        echange_info = json.loads(self.echanges_db.extraire_echange(1))
        self.assertEqual(echange_info['date_echange'], '2025-02-01')
        self.assertEqual(echange_info['total_facture'], 600.0)

        # 3. Extraire tous les échanges
        all_echanges = json.loads(self.echanges_db.extraire_tous_echanges())
        self.assertEqual(len(all_echanges), 1)

        # 4. Supprimer un échange
        self.echanges_db.supprimer_echange(1)
        echange_info = self.echanges_db.extraire_echange(1)
        self.assertIsNone(echange_info)

if __name__ == '__main__':
    unittest.main()







class TestAchatsMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_achats.db'
        cls.achats_db = Achats()
        cls.achats_db.create_table_achats()

    def test_all_functions(self):
        # 1. Ajouter un achat
        self.achats_db.ajouter_achat(1, 1, 50, 10.0, 15.0, '2025-01-28', '2026-01-28', 1)
        achat_info = json.loads(self.achats_db.extraire_achat(1))
        self.assertEqual(achat_info['id_medicament'], 1)
        self.assertEqual(achat_info['quantite_achetee'], 50)
        self.assertEqual(achat_info['prix_achat_unitaire'], 10.0)

        # 2. Modifier l'achat
        self.achats_db.modifier_achat(1, 1, 1, 60, 12.0, 18.0, '2025-02-01', '2026-02-01', 2)
        achat_info = json.loads(self.achats_db.extraire_achat(1))
        self.assertEqual(achat_info['quantite_achetee'], 60)
        self.assertEqual(achat_info['prix_achat_unitaire'], 12.0)
        self.assertEqual(achat_info['total_facture'], 1080.0)

        # 3. Supprimer l'achat
        self.achats_db.supprimer_achat(1)
        achat_info = self.achats_db.extraire_achat(1)
        self.assertIsNone(achat_info)

        # 4. Ajouter deux achats pour le test d'extraction de tous les achats
        self.achats_db.ajouter_achat(1, 1, 50, 10.0, 15.0, '2025-01-28', '2026-01-28', 1)
        self.achats_db.ajouter_achat(2, 2, 30, 8.0, 12.0, '2025-02-01', '2026-02-01', 2)

        all_achats = json.loads(self.achats_db.extraire_tous_achats())
        self.assertEqual(len(all_achats), 2)





if __name__ == '__main__':
    unittest.main()

import unittest
import json

class TestFournisseurMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_fournisseur.db'
        cls.fournisseur_db = Fournisseur(cls.db_name)
        cls.fournisseur_db.create_table_fournisseur()

    def test_all_functions(self):
        # 1. Ajouter un fournisseur
        self.fournisseur_db.ajouter_fournisseur('Fournisseur A', '0123456789', 'fournisseurA@example.com', 'Adresse A', 'Ville A', 'Pays A')
        fournisseur_info = json.loads(self.fournisseur_db.extraire_fournisseur(1))
        self.assertEqual(fournisseur_info['nom_fournisseur'], 'Fournisseur A')
        self.assertEqual(fournisseur_info['telephone'], '0123456789')

        # 2. Modifier un fournisseur
        self.fournisseur_db.modifier_fournisseur(1, 'Fournisseur B', '0987654321', 'fournisseurB@example.com', 'Adresse B', 'Ville B', 'Pays B')
        fournisseur_info = json.loads(self.fournisseur_db.extraire_fournisseur(1))
        self.assertEqual(fournisseur_info['nom_fournisseur'], 'Fournisseur B')
        self.assertEqual(fournisseur_info['telephone'], '0987654321')

        # 3. Extraire un fournisseur par son nom
        fournisseur_info_by_nom = json.loads(self.fournisseur_db.extraire_fournisseur_nom('Fournisseur B'))
        self.assertEqual(fournisseur_info_by_nom['telephone'], '0987654321')

        # 4. Extraire des fournisseurs par nom contenant une chaîne
        fournisseurs_by_nom_like = json.loads(self.fournisseur_db.extraire_fournisseur_nom_like('Fournisseur'))
        self.assertEqual(len(fournisseurs_by_nom_like), 1)

        # 5. Extraire tous les fournisseurs
        all_fournisseurs = json.loads(self.fournisseur_db.extraire_tous_fournisseurs())
        self.assertEqual(len(all_fournisseurs), 1)

        # 6. Supprimer un fournisseur
        self.fournisseur_db.supprimer_fournisseur(1)
        fournisseur_info = self.fournisseur_db.extraire_fournisseur(1)
        self.assertIsNone(fournisseur_info)

if __name__ == '__main__':
    unittest.main()

def test_medicament():
    # Création d'une instance de la classe Medicament
    medicament_db = Medicament()

    # Suppression de toutes les données pour partir sur une base propre
    medicament_db.supprimer_toute_base_donnees()

    # Création de la table
    medicament_db.create_table_medicament()

    # Ajout de médicaments
    medicament_db.ajouter_medicament(
        nom="Paracetamol",
        caracteristique="Antalgique",
        code_ean_13="1234567890123",
        generique="Non",
        prix_officine=2.5,
        prix_public=3.0,
        prix_remboursement=2.0,
        prix_hospitalier=2.8,
        substance_active="Paracetamol",
        classe_therapeutique="Analgésique",
        min_stock=10,
        stock_actuel=50
    )
    medicament_db.ajouter_medicament(
        nom="Ibuprofene",
        caracteristique="Anti-inflammatoire",
        code_ean_13="9876543210987",
        generique="Oui",
        prix_officine=4.5,
        prix_public=5.0,
        prix_remboursement=4.0,
        prix_hospitalier=4.8,
        substance_active="Ibuprofene",
        classe_therapeutique="Anti-inflammatoire",
        min_stock=5,
        stock_actuel=20
    )

    # Extraction d'un médicament par ID
    print("Extraction par ID:")
    print(medicament_db.extraire_medicament(1))  # Doit afficher les infos de Paracetamol

    # Extraction d'un médicament par code barre
    print("\nExtraction par code barre:")
    print(medicament_db.extraire_medicament_code_barre("1234567890123"))  # Paracetamol

    # Recherche avec LIKE sur le nom
    print("\nRecherche par nom (LIKE):")
    print(medicament_db.extraire_medicament_nom_like("ibu"))  # Ibuprofene

    # Extraction de tous les médicaments
    print("\nTous les médicaments:")
    print(medicament_db.extraire_tous_medicament())

    # Extraction des médicaments avec quantité minimale > 0
    print("\nMédicaments avec quantité minimale > 0:")
    print(medicament_db.extraire_medicament_quantite_minimale_sup_0())

    # Modification d'un médicament
    medicament_db.modifier_medicament(1, Stock_Actuel=30)
    print("\nMédicament modifié (ID=1):")
    print(medicament_db.extraire_medicament(1))  # Stock actuel doit être 30

    # Suppression d'un médicament
    medicament_db.supprimer_medicament(2)
    print("\nTous les médicaments après suppression (ID=2):")
    print(medicament_db.extraire_tous_medicament())  # Ibuprofene doit être supprimé

# Exécuter les tests
test_medicament()




import unittest
import json

class TestPaymentMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_payment.db'
        cls.payment_db = Payment(cls.db_name)
        cls.payment_db.create_table_payment()

    def test_all_functions(self):
        # 1. Ajouter un paiement
        self.payment_db.ajouter_payment(1, 'FACT123', 150.0, '2025-01-28', 2)
        payment_info = json.loads(self.payment_db.extraire_payment_with_id_client(1))
        self.assertEqual(payment_info[0]['numero_facture'], 'FACT123')
        self.assertEqual(payment_info[0]['montant_paye'], 150.0)

        # 2. Extraire les paiements en fonction de l'ID du client
        payments_by_client = json.loads(self.payment_db.extraire_payment_with_id_client(1))
        self.assertEqual(len(payments_by_client), 1)
        self.assertEqual(payments_by_client[0]['id_client'], 1)

if __name__ == '__main__':
    unittest.main()



import unittest
import json

class TestPharmaciesMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_pharmacies.db'
        cls.pharmacies_db = Pharmacies()
        cls.pharmacies_db.create_table_pharmacies()

    def test_all_functions(self):
        # 1. Ajouter une pharmacie
        self.pharmacies_db.ajouter_pharmacie('Pharmacie ABC', '123 Rue Principale', '0123456789', 'abcpharma@example.com', '1000', '500')
        pharmacie_info = json.loads(self.pharmacies_db.extraire_pharma_nom_like('ABC'))[0]
        self.assertEqual(pharmacie_info['nom'], 'Pharmacie ABC')

        # 2. Modifier une pharmacie
        self.pharmacies_db.modifier_pharmacie(1, 'Pharmacie XYZ', '456 Rue Secondaire', '0987654321', 'xyzpharma@example.com', '2000', '800')
        pharmacie_info = json.loads(self.pharmacies_db.extraire_pharma_nom_like('XYZ'))[0]
        self.assertEqual(pharmacie_info['nom'], 'Pharmacie XYZ')
        self.assertEqual(pharmacie_info['adresse'], '456 Rue Secondaire')

        # 3. Extraire toutes les pharmacies
        all_pharmacies = json.loads(self.pharmacies_db.extraire_tous_pharma())
        self.assertEqual(len(all_pharmacies), 1)

        # 4. Extraire des pharmacies par nom partiel
        pharmacies_info = json.loads(self.pharmacies_db.extraire_pharma_nom_like('XYZ'))
        self.assertEqual(len(pharmacies_info), 1)
        self.assertEqual(pharmacies_info[0]['nom'], 'Pharmacie XYZ')

        # 5. Supprimer une pharmacie (juste pour démonstration, bien que la méthode de suppression ne soit pas incluse)
        # self.pharmacies_db.supprimer_pharmacie(1)  # Si vous ajoutez une méthode de suppression
        # pharmacie_info = self.pharmacies_db.extraire_pharma_nom_like('XYZ')
        # self.assertEqual(len(pharmacie_info), 0)

if __name__ == '__main__':
    unittest.main()


import unittest
import json

class TestSalariesMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_salaries.db'
        cls.salaries_db = Salaries()
        cls.salaries_db.create_table_salaries()

    def test_all_functions(self):
        # 1. Ajouter un salarié
        self.salaries_db.ajouter_salarie('John', 'Doe', '123456', '0123456789', 'johndoe@example.com', '123 Main St', 'photo.jpg', 3000.0, 'CDI', '2025-01-28', 'Junior', 'passwordhash')
        salarie_info = json.loads(self.salaries_db.extraire_salarie(1))
        self.assertEqual(salarie_info['nom'], 'John')
        self.assertEqual(salarie_info['prenom'], 'Doe')

        # 2. Modifier un salarié
        self.salaries_db.modifier_salarie(1, 'John', 'Doe', '123456', '0987654321', 'johndoe@newmail.com', '456 Another St', 'newphoto.jpg', 3500.0, 'CDI', '2025-02-01', 'Senior', 'newpasswordhash')
        salarie_info = json.loads(self.salaries_db.extraire_salarie(1))
        self.assertEqual(salarie_info['telephone'], '0987654321')
        self.assertEqual(salarie_info['email'], 'johndoe@newmail.com')

        # 3. Extraire un salarié par login
        salarie_info = json.loads(self.salaries_db.extraire_salarie_login('John', 'newpasswordhash'))
        self.assertEqual(salarie_info['nom'], 'John')
        self.assertEqual(salarie_info['prenom'], 'Doe')

        # 4. Supprimer un salarié
        self.salaries_db.supprimer_salarie(1)
        salarie_info = self.salaries_db.extraire_salarie(1)
        self.assertIsNone(salarie_info)

        # 5. Ajouter deux salariés pour le test d'extraction de tous les salariés
        self.salaries_db.ajouter_salarie('Jane', 'Smith', '654321', '0123456789', 'janesmith@example.com', '789 Another St', 'photo2.jpg', 3200.0, 'CDD', '2025-02-28', 'Junior', 'passwordhash2')
        self.salaries_db.ajouter_salarie('Jack', 'White', '789012', '0123456789', 'jackwhite@example.com', '456 Main St', 'photo3.jpg', 3300.0, 'CDI', '2025-03-01', 'Senior', 'passwordhash3')

        all_salaries = json.loads(self.salaries_db.extraire_tous_salaries())
        self.assertEqual(len(all_salaries), 2)

if __name__ == '__main__':
    unittest.main()


import unittest
import json

class TestStockMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_stock.db'
        cls.stock_db = Stock()
        cls.stock_db.create_table_stock()

    def test_all_functions(self):
        # 1. Ajouter un stock
        self.stock_db.ajouter_stock(1, 1, 1, 100.0, 120.0, 110.0, '2025-01-28', '2025-12-31', 100, 50, 10, 200, '2025-01-29', '2025-01-27')
        stock_info = json.loads(self.stock_db.extraire_stock(1)) 
        self.assertEqual(stock_info['id_medicament'], 1)
        self.assertEqual(stock_info['prix_achat'], 100.0)
        self.assertEqual(stock_info['quantite_actuelle'], 50)

        # 2. Modifier le stock
        self.stock_db.modifier_stock(1, 1, 1, 1, 110.0, 130.0, 120.0, '2025-02-01', '2026-01-01', 150, 70, 20, 250, '2025-02-01', '2025-02-01')
        stock_info = json.loads(self.stock_db.extraire_stock(1))
        self.assertEqual(stock_info['prix_achat'], 110.0)
        self.assertEqual(stock_info['quantite_actuelle'], 70)
        self.assertEqual(stock_info['quantite_minimale'], 20)

        # 3. Supprimer le stock
        self.stock_db.supprimer_stock(1)
        stock_info = self.stock_db.extraire_stock(1)
        self.assertIsNone(stock_info)

        # 4. Ajouter deux stocks pour le test d'extraction avec quantite_minimale > 0
        self.stock_db.ajouter_stock(1, 1, 1, 100.0, 120.0, 110.0, '2025-01-28', '2025-12-31', 100, 50, 10, 200, '2025-01-29', '2025-01-27')
        self.stock_db.ajouter_stock(2, 2, 2, 200.0, 220.0, 210.0, '2025-02-01', '2026-12-31', 200, 80, 0, 250, '2025-02-02', '2025-02-01')

        stocks_minimale = json.loads(self.stock_db.extraire_medicament_quantite_minimale_sup_0())
        self.assertEqual(len(stocks_minimale), 1)
        self.assertEqual(stocks_minimale[0]['id_medicament'], 1)

        # 5. Extraire tous les stocks
        all_stocks = json.loads(self.stock_db.extraire_tous_stock())
        self.assertEqual(len(all_stocks), 2)

if __name__ == '__main__':
    unittest.main()



import unittest
import json

class TestVentesMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls): 
        cls.ventes_db = Ventes()
        cls.ventes_db.create_table_ventes()

    def test_all_functions(self):
        # 1. Ajouter une vente
        self.ventes_db.ajouter_vente(1, 1, 100.0, 120.0, '2025-01-28', 5, 600.0, 1, 'F001', 1, 1)
        vente_info = json.loads(self.ventes_db.extraire_vente(1))
        self.assertEqual(vente_info['id_medicament'], 1)
        self.assertEqual(vente_info['prix_achat'], 100.0)
        self.assertEqual(vente_info['quantite_vendue'], 5)

        # 2. Modifier la vente
        self.ventes_db.modifier_vente(1, 1, 1, 110.0, 130.0, '2025-02-01', 6, 780.0, 2, 'F002', 1, 1)
        vente_info = json.loads(self.ventes_db.extraire_vente(1))
        self.assertEqual(vente_info['prix_achat'], 110.0)
        self.assertEqual(vente_info['quantite_vendue'], 6)
        self.assertEqual(vente_info['total_facture'], 780.0)

        # 3. Supprimer la vente
        self.ventes_db.supprimer_vente(1)
        vente_info = self.ventes_db.extraire_vente(1)
        self.assertIsNone(vente_info)

        # 4. Ajouter deux ventes pour le test d'extraction de toutes les ventes
        self.ventes_db.ajouter_vente(1, 1, 100.0, 120.0, '2025-01-28', 5, 600.0, 1, 'F001', 1, 1)
        self.ventes_db.ajouter_vente(2, 2, 150.0, 180.0, '2025-02-01', 3, 540.0, 2, 'F002', 2, 2)

        all_ventes = json.loads(self.ventes_db.extraire_tous_ventes())
        self.assertEqual(len(all_ventes), 2)

if __name__ == '__main__':
    unittest.main()

