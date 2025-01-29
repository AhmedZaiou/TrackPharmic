import unittest
import json
from Backend.Dataset.achat import Achats  # Assurez-vous que l'import est correct
from Backend.Dataset.client import Clients  # Assurez-vous de l'existence des classes appropriées
from Backend.Dataset.commande import Commandes
from Backend.Dataset.credit import Credit
from Backend.Dataset.echanges import Echanges
from Backend.Dataset.fournisseur import Fournisseur
from Backend.Dataset.medicament import Medicament

class TestDatabaseMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Création des bases de données pour chaque table
        cls.clients_db = Clients()
        cls.clients_db.create_table_clients()
        
        cls.commandes_db = Commandes()
        cls.commandes_db.create_table_commandes()

        cls.credit_db = Credit()
        cls.credit_db.create_table_credit()

        cls.echanges_db = Echanges()
        cls.echanges_db.create_table_echanges()

        cls.achats_db = Achats()
        cls.achats_db.create_table_achats()

        cls.fournisseur_db = Fournisseur()
        cls.fournisseur_db.create_table_fournisseur()

        cls.medicament_db = Medicament()
        cls.medicament_db.create_table_medicament()

    def test_clients(self):
        # Test des fonctions clients
        self.clients_db.ajouter_client('Alice', 'Johnson', '123456789', '0123456789', 'alicejohnson@example.com', '123 Elm St', 5000.0, 1000.0)
        client_info = json.loads(self.clients_db.extraire_client(1))
        self.assertEqual(client_info['nom'], 'Alice')
        
        self.clients_db.modifier_client(1, 'Alice', 'Johnson', '123456789', '0987654321', 'alicejohnson@newmail.com', '456 Oak St', 6000.0, 1500.0)
        client_info = json.loads(self.clients_db.extraire_client(1))
        self.assertEqual(client_info['telephone'], '0987654321')

        # Test de suppression
        self.clients_db.supprimer_client(1)
        client_info = self.clients_db.extraire_client(1)
        self.assertIsNone(client_info)

    def test_commandes(self):
        # Test des fonctions commandes
        self.commandes_db.ajouter_commande(1, '2025-01-28', '2025-02-28', 'En attente', 'John Doe', 'Aspirine, Paracétamol', '2025-01-30', 1, 'Incluse')
        commande_info = json.loads(self.commandes_db.extraire_commande(1))
        self.assertEqual(commande_info['statut_reception'], 'En attente')

        # Test de suppression
        self.commandes_db.supprimer_commande(1)
        commande_info = self.commandes_db.extraire_commande(1)
        self.assertIsNone(commande_info)

    def test_credits(self):
        # Test des fonctions crédits
        self.credit_db.ajouter_credit(1, 'FAC001', 1000.0, 500.0, '2025-01-01', 'en cours', 1)
        credit_info = json.loads(self.credit_db.extraire_credit(1))
        self.assertEqual(credit_info['montant_paye'], 1000.0)

        # Test de suppression
        self.credit_db.supprimer_credit(1)
        credit_info = self.credit_db.extraire_credit(1)
        self.assertIsNone(credit_info)

    def test_echanges(self):
        # Test des fonctions échanges
        self.echanges_db.ajouter_echange(1, 1, '2025-01-01', 500.0, 'sortie', 1)
        echange_info = json.loads(self.echanges_db.extraire_echange(1))
        self.assertEqual(echange_info['total_facture'], 500.0)

        # Test de suppression
        self.echanges_db.supprimer_echange(1)
        echange_info = self.echanges_db.extraire_echange(1)
        self.assertIsNone(echange_info)

    def test_achats(self):
        # Test des fonctions achats
        self.achats_db.ajouter_achat(1, 1, 50, 10.0, 15.0, '2025-01-28', '2026-01-28', 1)
        achat_info = json.loads(self.achats_db.extraire_achat(1))
        self.assertEqual(achat_info['prix_achat_unitaire'], 10.0)

        # Test de suppression
        self.achats_db.supprimer_achat(1)
        achat_info = self.achats_db.extraire_achat(1)
        self.assertIsNone(achat_info)

    def test_fournisseurs(self):
        # Test des fonctions fournisseurs
        self.fournisseur_db.ajouter_fournisseur('Fournisseur A', '0123456789', 'fournisseurA@example.com', 'Adresse A', 'Ville A', 'Pays A')
        fournisseur_info = json.loads(self.fournisseur_db.extraire_fournisseur(1))
        self.assertEqual(fournisseur_info['telephone'], '0123456789')

        # Test de suppression
        self.fournisseur_db.supprimer_fournisseur(1)
        fournisseur_info = self.fournisseur_db.extraire_fournisseur(1)
        self.assertIsNone(fournisseur_info)

    def test_medicament(self):
        # Test des fonctions médicaments
        self.medicament_db.ajouter_medicament(
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
        medicament_info = json.loads(self.medicament_db.extraire_medicament(1))
        self.assertEqual(medicament_info['nom'], 'Paracetamol')

        # Test de suppression
        self.medicament_db.supprimer_medicament(1)
        medicament_info = self.medicament_db.extraire_medicament(1)
        self.assertIsNone(medicament_info)

if __name__ == '__main__':
    unittest.main()
