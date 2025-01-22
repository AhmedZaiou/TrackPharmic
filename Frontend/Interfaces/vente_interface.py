from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QCompleter,QSpinBox,QHeaderView,QMessageBox,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox
)
from qtpy.QtCore import Qt, QStringListModel
from Backend.Dataset.dataset import *
import pandas as pd
import numpy as np
import time


class Vente_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()
        self.client_info = None
        self.producs_table = pd.DataFrame()
        self.last_key_time = time.time()
        self.barcode_delay_threshold = 0.1 



    def show_vente_interface(self):
        self.code_barre_scanner = ""
        self.main_interface.keyPressEvent = self.keyPressEvent
        
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")
        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.vente_dash)

        titre_page = QLabel("Gestion de Ventes")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page) 

        top_layout = QHBoxLayout()
        # Section Client
        client_layout = QVBoxLayout()
        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Rechercher client par Nom")

        self.client_id_input.textChanged.connect(self.OntextChangeClient)

        self.completer_client = QCompleter()
        self.completer_client.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_client.setCompletionMode(QCompleter.PopupCompletion)
        self.client_id_input.setCompleter(self.completer_client)
        self.completer_client.activated.connect(self.selectionner_client)


        self.search_client_button = QPushButton("Rechercher")
        self.search_client_button.clicked.connect(self.search_client)
        self.add_client_button = QPushButton("Nouveau client")
        self.add_client_button.clicked.connect(self.search_client)

        self.client_status_label = QLabel("Client : None")
        self.client_cin_label = QLabel("CIN : None")
        self.client_max_credit = QLabel("Max_credit : None")
        self.client_credit_actuel = QLabel("Credit Actuel : None")

        client_layout.addWidget(self.client_id_input)
        client_layout.addWidget(self.search_client_button)
        client_layout.addWidget(self.add_client_button)
        client_layout.addWidget(self.client_status_label)
        client_layout.addWidget(self.client_cin_label)
        client_layout.addWidget(self.client_max_credit)
        client_layout.addWidget(self.client_credit_actuel)
        

        # Zone d'entrée pour le code-barres
        barcode_layout = QVBoxLayout()
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Entrez le code-barres ou scannez ici")
        self.barcode_input.returnPressed.connect(self.process_barcode_manuel) 

        self.add_to_cart_button = QPushButton("Ajouter au panier")
        self.add_to_cart_button.clicked.connect(self.ajouter_panier)
        barcode_layout.addWidget(self.barcode_input)
        barcode_layout.addWidget(self.add_to_cart_button)

        top_layout.addLayout(barcode_layout)
        top_layout.addLayout(client_layout)

        main_layout.addLayout(top_layout) 
        # Liste des produits
        

        # Panier
        self.cart_table = QTableWidget(0, 8)
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        columns = ["Nom" , "caracteristique", "Code_EAN_13" , "Medicament_GENERIQUE", "Prix_Officine" ,
                "Prix_Public_de_Vente" , "Prix_base_remboursement" , "Prix_Hospitalier" , "Substance_active_DCI" ,
                "Classe_Therapeutique" ]
        
        self.cart_table.setHorizontalHeaderLabels(["Code EAN 13","Nom","Caracteristique","Stock","Prix unité", "Quantité", "Date_Expiration", "Prix total"])
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
    
    def OntextChangeClient(self, text):
        if len(text) >= 3:
            self.updateCompleter_fournisseur(text)
    
    def updateCompleter_fournisseur(self, text): 
        results = extraire_client_nom_like(text)  
        results = ["_".join(res) for res in results]
        model = QStringListModel(results)  
        self.completer_client.setModel(model) 
    


    def selectionner_client(self, text):
        print(text)

    def toggle_inputs(self):

        if self.checkbox.isChecked():
            if self.client_info == None: 
                QMessageBox.information(self.main_interface, "Merci de choisire un client avant d'activer l'option credit", "Merci de choisire un client avant d'activer l'option credit")
                self.checkbox.setChecked(False)
            else:
                self.amount_input.setEnabled(True)
                self.rest_a_payer.setEnabled(True)
                self.rest_a_payer_value.setEnabled(True)
        else:
            self.amount_input.setDisabled(True)
            self.rest_a_payer.setDisabled(True)
            self.rest_a_payer_value.setDisabled(True)

    def search_client(self):
        client_id = self.client_id_input.text()
        if '_' not in client_id:
            print('merci de remplire les informations du client dans la bare de recherche ')
            self.client_status_label.setText("Client : None")
            self.client_cin_label.setText("CIN : None")
            self.client_max_credit.setText("Max_credit : None")
            self.client_credit_actuel.setText("Credit Actuel : None")

            self.client_info = None
        else:
            nom,prenom,cin = client_id.split('_') 
            self.client_info = dict(extraire_client_info(nom,prenom,cin))
            self.client_status_label.setText(f"Client : {self.client_info['Nom']} {self.client_info['Prenom']} ")
            self.client_cin_label.setText(f"CIN : {self.client_info['CIN']}")
            self.client_max_credit.setText(f"Max_credit : {self.client_info['Max_Credit']} Dh")
            self.client_credit_actuel.setText(f"Credit Actuel : {self.client_info['Credit_Actuel']} Dh")




    def process_barcode(self, codebare):
        if len(codebare) > 13:
            return codebare[-13:]
        return ""

    def ajouter_panier(self): 
        code = self.barcode_input.text()
        code = self.process_barcode(code) 
        if len(code) == 13:
            self.add_medicament_to_vente(code)

    def update_table(self): 
        self.cart_table.setRowCount(len(self.producs_table))
        for row, product in self.producs_table.iterrows():   
            self.cart_table.setItem(row, 0, QTableWidgetItem(str(product['Code_EAN_13']))) 
            self.cart_table.setItem(row, 1, QTableWidgetItem(str(product['Nom']))) 
            self.cart_table.setItem(row, 2, QTableWidgetItem(str(product['caracteristique']))) 
            self.cart_table.setItem(row, 3, QTableWidgetItem(str(product['Quantite_Actuelle']))) 
            self.cart_table.setItem(row, 4, QTableWidgetItem(str(product['Prix_Public_de_Vente']))) 
            line_edit = QSpinBox()
            line_edit.setValue(product['Quantite'])
            line_edit.editingFinished.connect(lambda row=row: self.update_quantity(row, line_edit.text()))
            self.cart_table.setCellWidget(row, 5, line_edit) 
            self.cart_table.setItem(row, 6, QTableWidgetItem(str(product['Date_Expiration']))) 
            self.cart_table.setItem(row, 7, QTableWidgetItem(str(product['Prix_total'])))  
        
        self.subtotal_label.setText(f"Sous-total : {self.producs_table['Prix_total'].sum()} Dh") 
        self.total_label.setText(f"<b>Total : {self.producs_table['Prix_total'].sum()} Dh</b>")

        self.barcode_input.clear()

    def update_quantity(self, row, new_value): 
        new_quantity = int(new_value) 
        self.producs_table.loc[row,"Quantite"] = new_quantity 
        self.producs_table.loc[row,"Prix_total"] = new_quantity * self.producs_table.loc[row,"Prix_Public_de_Vente"]
        self.update_table() 
    


    def add_medicament_to_vente(self,code_barre_scanner):

        if  not self.producs_table.empty and code_barre_scanner in self.producs_table["Code_EAN_13"].values:
            self.producs_table.loc[self.producs_table['Code_EAN_13'] == code_barre_scanner, 'Quantite'] += 1
            self.producs_table.loc[self.producs_table['Code_EAN_13'] == code_barre_scanner, 'Prix_total'] += self.producs_table.loc[self.producs_table['Code_EAN_13'] == code_barre_scanner, 'Prix_Public_de_Vente']
        else:
            print(code_barre_scanner)
            medicament  = extraire_medicament_code_barre(code_barre_scanner)
            if medicament is None:
                QMessageBox.information(self.main_interface, "Medicament non reconue", "Medicament non reconue")
                return 
            else: 
                medicament_on_dtock = extraire_medicament_id_stock(medicament['ID_Medicament']) 
                medicament = dict(medicament)  


                if medicament_on_dtock is None:
                    QMessageBox.information(self.main_interface, "stock vide", "Stock vide")
                else:  
                    if len(np.unique(medicament_on_dtock['Prix_Vente']))>1:
                        QMessageBox.information(self.main_interface, "Atention le prix de ce medicament à changer", "Atention le prix de ce medicament à changer, Merci de séparer les facture en cas de quantité superieur a 1")
                    
                    medicament["Quantite"]  = 1
                    medicament['Prix_Public_de_Vente'] = medicament_on_dtock['Prix_Vente'][0]
                    medicament['Prix_Vente'] = medicament_on_dtock['Prix_Vente']
                    medicament['Date_Expiration'] = medicament_on_dtock['Date_Expiration'][0]
                    medicament['Quantite_Actuelle'] = medicament_on_dtock['Quantite_Actuelle']
                    medicament['ID_Commande'] = medicament_on_dtock['ID_Commande']
                    medicament['list_quantity'] = medicament_on_dtock['list_quantity']
                    medicament['Prix_Achat'] = medicament_on_dtock['Prix_Achat']
                    medicament['ID_Stock'] = medicament_on_dtock['ID_Stock']
                    medicament["Prix_total"]  = medicament["Quantite"] * medicament['Prix_Public_de_Vente']
                    df = pd.DataFrame([medicament])
                    if self.producs_table.empty :
                        self.producs_table = df 
                    else:
                        self.producs_table = pd.concat([self.producs_table, df], ignore_index=True)
                    self.producs_table['Prix_total']=self.producs_table['Prix_total'].round(2)
        self.update_table()
        
    
    def keyPressEvent(self, event): 
        key = event.text() 
        current_time = time.time()
        if current_time - self.last_key_time < self.barcode_delay_threshold:
            print("saisie de code bare", self.code_barre_scanner)   
            code_b = True
        self.last_key_time = current_time 
        

        if key == '\r' and code_b:  # Lorsque le lecteur envoie un saut de ligne  
            self.code_barre_scanner = self.process_barcode(self.code_barre_scanner)
            if self.code_barre_scanner  != "":
                self.add_medicament_to_vente(self.code_barre_scanner)
                self.code_barre_scanner = ""  # Réinitialiser pour le prochain scan                  
                 
        else:
            self.code_barre_scanner += key  # Ajouter le caractère au code en cours 

        

    def process_barcode_manuel(self):
        pass
        

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
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")

        for index, items in self.producs_table.iterrows():
            id_medicament = items['ID_Medicament']
            id_commande_entre = items['ID_Commande']
            prix_achat = items['Prix_Achat']
            prix_v = items['Prix_Vente']
            prix_vente = items['Prix_Public_de_Vente']
            date_vente = now_str
            quantite_vendue = items['Quantite'] 
            quantite_list= items['list_quantity']  
            total_facture = items['Prix_total']
            ID_Stock = items['ID_Stock']
            id_client = 0 if self.client_info is None else self.client_info['ID_Client']
            numero_facture = int(now.timestamp())
            id_salarie = self.main_interface.user_session['ID_Salarie']
            quantite_traiter = 0
            self.total_facture = 0
            for idcommande_item, prix_achat_item, prix_vente_item, ID_Stock_item, quanti in zip(id_commande_entre, prix_achat, prix_v , ID_Stock, quantite_list) :
                quanti_rest_to_hand = quantite_vendue - quantite_traiter
                if  quanti_rest_to_hand <= quanti:
                    totale = self.ajouter_vente_with_all_operation(id_medicament, idcommande_item, prix_achat_item, prix_vente_item, date_vente, quanti_rest_to_hand, 
                    id_client, numero_facture, id_salarie) 
                    self.total_facture+=totale
                    quantite_traiter += quanti_rest_to_hand 
                else: 
                    quantite_traiter+=quanti
                    totale = self.ajouter_vente_with_all_operation(id_medicament, idcommande_item, prix_achat_item, prix_vente_item, date_vente, quanti, 
                    id_client, numero_facture, id_salarie) 
                    self.total_facture+=totale
                if quantite_traiter >= quantite_vendue:
                    break 
        credit = False
        if self.checkbox.isChecked():
            credit = True
            to_pay_now = self.amount_input.text()  
            self.ajouter_credit_with_all_operation(id_client, numero_facture, to_pay_now, self.total_facture, now_str, 'in progresse', id_salarie)
            
        


    def ajouter_vente_with_all_operation(self, id_medicament, idcommande_item, prix_achat_item, prix_vente_item, date_vente, quanti, id_client, numero_facture, id_salarie):
        ajouter_vente(id_medicament, idcommande_item, prix_achat_item, prix_vente_item, date_vente, quanti, quanti * prix_vente_item, id_client, numero_facture, id_salarie) 
        return quanti * prix_vente_item
        # todo : supprimer du stock 
    def ajouter_credit_with_all_operation(self, id_client, numero_facture, to_pay_now, total_facture, now_str, status, id_salarie):
        ajouter_credit(id_client, numero_facture, to_pay_now,  total_facture-int(to_pay_now), now_str, status, id_salarie)
        ajouter_credit_client(id_client,  total_facture-int(to_pay_now))


    

        



