from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox
)
from qtpy.QtCore import Qt


class Acceuil_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()

    def show_vente_interface(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.vente_dash)

        top_layout = QHBoxLayout()

        # Section Client
        client_layout = QVBoxLayout()
        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Rechercher client par ID")
        self.search_client_button = QPushButton("Rechercher")
        self.search_client_button.clicked.connect(self.search_client)
        self.add_client_button = QPushButton("Nouveau client")
        self.add_client_button.clicked.connect(self.search_client)

        self.client_status_label = QLabel("Client : Anonyme")
        self.client_max_credit = QLabel("Max_credit : 100")
        self.client_credit_actuel = QLabel("Credit Actuel : 0")


        client_layout.addWidget(self.client_id_input)
        client_layout.addWidget(self.search_client_button)
        client_layout.addWidget(self.add_client_button)
        client_layout.addWidget(self.client_status_label)
        client_layout.addWidget(self.client_max_credit)
        client_layout.addWidget(self.client_credit_actuel)
        

        # Zone d'entrée pour le code-barres
        barcode_layout = QVBoxLayout()
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Entrez le code-barres ou scannez ici")
        self.barcode_input.returnPressed.connect(self.process_barcode)
        self.product_table = QTableWidget(0, 3)  # (0 lignes, 3 colonnes)
        self.product_table.setHorizontalHeaderLabels(["Code barre","Nom", "Prix", "Caractéristique"])
        barcode_layout.addWidget(self.product_table)





        self.add_to_cart_button = QPushButton("Ajouter au panier")
        self.add_to_cart_button.clicked.connect(self.process_barcode)
        barcode_layout.addWidget(self.barcode_input)
        barcode_layout.addWidget(self.add_to_cart_button)

        top_layout.addLayout(barcode_layout)
        top_layout.addLayout(client_layout)

        main_layout.addLayout(top_layout)




        # Liste des produits
        

        # Panier
        self.cart_table = QTableWidget(0, 3)
        self.cart_table.setHorizontalHeaderLabels(["Code barre","Nom", "Quantité", "Prix total"])
        main_layout.addWidget(self.cart_table)

        # Totaux
        totals_layout = QHBoxLayout()
        self.subtotal_label = QLabel("Sous-total : 0 Dh")
        self.tax_label = QLabel("Taxes : 0 Dh")
        self.total_label = QLabel("<b>Total : 0 Dh</b>")
        totals_layout.addWidget(self.subtotal_label)
        totals_layout.addWidget(self.tax_label)
        totals_layout.addWidget(self.total_label)
        main_layout.addLayout(totals_layout)

        # Paiement
        payment_layout = QHBoxLayout()
        self.checkbox = QCheckBox('Crédit ?', self.main_interface)
        self.checkbox.stateChanged.connect(self.toggle_inputs)
        

        payment_layout.addWidget(self.checkbox)

        # Montant à payer
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Montant à payer maintenant")
        payment_layout.addWidget(self.amount_input) 

        self.rest_a_payer = QLabel("Réste à payer après :")
        self.rest_a_payer_value = QLineEdit()

        payment_layout.addWidget(self.rest_a_payer) 
        payment_layout.addWidget(self.rest_a_payer_value) 
        self.toggle_inputs()

        

        # Bouton pour annuler
        

        main_layout.addLayout(payment_layout)

        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.cancel_sale)
        main_layout.addWidget(self.cancel_button)

        # Actions
        self.confirm_button = QPushButton("Confirmer la vente")
        main_layout.addWidget(self.confirm_button)

        # Assign layout to central widget
        self.main_interface.content_layout.addWidget(self.vente_dash)

        # Connecter les signaux
        self.confirm_button.clicked.connect(self.confirm_sale)
    


    def toggle_inputs(self):
        if self.checkbox.isChecked():
            self.amount_input.setEnabled(True)
            self.rest_a_payer.setEnabled(True)
            self.rest_a_payer_value.setEnabled(True)
        else:
            self.amount_input.setDisabled(True)
            self.rest_a_payer.setDisabled(True)
            self.rest_a_payer_value.setDisabled(True)

    def search_client(self):
        client_id = self.client_id_input.text()
        if client_id:
            # Simulation de recherche d'un client
            print(f"Recherche du client avec ID : {client_id}")
            # Exemple : remplacer par une recherche réelle
            if client_id == "123":
                self.client_status_label.setText("Client : Jean Dupont")
                print("Client trouvé : Jean Dupont")
            else:
                self.client_status_label.setText("Client : Inconnu")
                print("Client non trouvé.")
        else:
            self.client_status_label.setText("Client : Anonyme")
            print("Aucun client sélectionné. Vente anonyme.")

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



