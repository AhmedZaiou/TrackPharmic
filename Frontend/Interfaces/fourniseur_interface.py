from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QGridLayout,QHeaderView,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox
)
from qtpy.QtCore import Qt

from Backend.Dataset.dataset import *


class Fournisseur_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()

    def show_vente_interface(self):
        self.main_interface.clear_content_frame()

        self.fournisseur_dash = QWidget()
        self.fournisseur_dash.setObjectName("fournisseur_dash")

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.fournisseur_dash)

        
 
        form_layout = QGridLayout()


        self.nom_input = QLineEdit()
        self.telephone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.adresse_input = QLineEdit()
        self.ville_input = QLineEdit()
        self.pays_input = QLineEdit()


        form_layout.addWidget(QLabel("Nom du Fournisseur :"), 0,0)
        form_layout.addWidget(self.nom_input , 0,1)
        form_layout.addWidget(QLabel("Téléphone :"), 1,0)
        form_layout.addWidget(self.telephone_input , 1,1)
        form_layout.addWidget(QLabel("Email :"), 2,0)
        form_layout.addWidget(self.email_input , 2,1)
        form_layout.addWidget(QLabel("Adresse :"), 3,0)
        form_layout.addWidget(self.adresse_input , 3,1)
        form_layout.addWidget(QLabel("Pays :"), 4,0)
        form_layout.addWidget(self.pays_input , 4,1)
        
        self.add_button = QPushButton("Ajouter Fournisseur")
        self.add_button.clicked.connect(self.ajouter_fournisseur)
        form_layout.addWidget(self.add_button)

        main_layout.addLayout(form_layout)


        self.table = QTableWidget()
        self.table.setColumnCount(6)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(["Nom", "Téléphone", "Email", "Adresse", "Ville", "Pays"])
        self.remplir_tableau() 
        main_layout.addWidget(self.table)

        self.main_interface.content_layout.addWidget(self.fournisseur_dash)

    def remplir_tableau(self):
        # Exemple de données fictives
        fournisseurs = extraire_tous_fournisseurs() 

        self.table.setRowCount(len(fournisseurs))


        for row, fournisseur in enumerate(fournisseurs):
            for col, data in enumerate(fournisseur[1:]):
                self.table.setItem(row, col, QTableWidgetItem(data))



    def ajouter_fournisseur(self):
        # Récupération des valeurs des champs
        nom = self.nom_input.text()
        telephone = self.telephone_input.text()
        email = self.email_input.text()
        adresse = self.adresse_input.text()
        ville = self.ville_input.text()
        pays = self.pays_input.text()
        ajouter_fournisseur(nom, telephone, email, adresse, ville, pays) 
        self.nom_input.clear()
        self.telephone_input.clear()
        self.email_input.clear()
        self.adresse_input.clear()
        self.ville_input.clear()
        self.pays_input.clear()

    


    def toggle_inputs(self):
        if self.checkbox.isChecked():
            self.amount_input.setEnabled(True)
            self.rest_a_payer.setEnabled(True)
            self.rest_a_payer_value.setEnabled(True)
        else:
            self.amount_input.setDisabled(True)
            self.rest_a_payer.setDisabled(True)
            self.rest_a_payer_value.setDisabled(True)

    def search_fournisseur(self):
        fournisseur_id = self.fournisseur_id_input.text()
        if fournisseur_id:
            # Simulation de recherche d'un fournisseur
            print(f"Recherche du fournisseur avec ID : {fournisseur_id}")
            # Exemple : remplacer par une recherche réelle
            if fournisseur_id == "123":
                self.fournisseur_status_label.setText("fournisseur : Jean Dupont")
                print("fournisseur trouvé : Jean Dupont")
            else:
                self.fournisseur_status_label.setText("fournisseur : Inconnu")
                print("fournisseur non trouvé.")
        else:
            self.fournisseur_status_label.setText("fournisseur : Anonyme")
            print("Aucun fournisseur sélectionné. Vente anonyme.")

    def process_barcode(self):
        barcode = self.barcode_input.text()
        if barcode:
            print(f"Code-barres traité : {barcode}")
            # Simuler l'ajout d'un produit au panier
            self.add_product_to_cart(barcode)
            self.barcode_input.clear()

    def add_product_to_cart(self, barcode):
        # Simule l'ajout d'un produit basé sur un code-barres
        print(f"Ajout du produit avec le code-barres {barcode} au panier.")
        row_position = self.cart_table.rowCount()
        self.cart_table.insertRow(row_position)
        self.cart_table.setItem(row_position, 0, QTableWidgetItem("Produit Exemple"))
        self.cart_table.setItem(row_position, 1, QTableWidgetItem("1"))
        self.cart_table.setItem(row_position, 2, QTableWidgetItem("10 €"))
        # Mettre à jour les totaux (exemple simplifié)
        self.update_totals(10)

    def update_totals(self, price):
        # Exemple : mettre à jour les étiquettes de sous-total, taxes et total
        current_total = int(self.total_label.text().split(":")[1].split("€")[0].strip())
        new_total = current_total + price
        self.total_label.setText(f"<b>Total : {new_total} €</b>")

    def activate_credit_mode(self):
        print("Mode Crédit activé.")
        # Logique supplémentaire pour le crédit peut être ajoutée ici

    def cancel_sale(self):
        print("Vente annulée.")

    def confirm_sale(self):
        amount = self.amount_input.text()
        print(f"Vente confirmée avec {amount} € payé maintenant.")
        # Logique de confirmation peut être ajoutée ici



