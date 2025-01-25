from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QDoubleSpinBox,QGridLayout,QHeaderView,QCompleter,QMessageBox,QSpinBox,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox
)
from qtpy.QtCore import Qt, QStringListModel

from Backend.Dataset.dataset import *
import pandas as pd
import time
import numpy as np

class Echange_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_principal_interface() 
        self.producs_table = pd.DataFrame()
        self.last_key_time = time.time()
        self.barcode_delay_threshold = 0.1 
        self.code_barre_scanner = ""
    


    def create_menu_commande(self):
        menu_layout = QHBoxLayout()
        self.add_commande_menu = QPushButton("gestion echange")
        self.add_commande_menu.clicked.connect(self.gestion_echange)
        menu_layout.addWidget(self.add_commande_menu)
        self.list_commande_menu = QPushButton(" gestion pharma")
        self.list_commande_menu.clicked.connect(self.gestion_pharma)
        menu_layout.addWidget(self.list_commande_menu)
        return menu_layout
    

    def gestion_echange(self):
        self.show_principal_interface()
    def gestion_pharma(self):
        self.show_gestion_pharma_interface()

    def show_principal_interface(self):
        self.main_interface.clear_content_frame()
        self.main_interface.keyPressEvent = self.keyPressEvent
        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash") 
        main_layout = QVBoxLayout(self.vente_dash) 
        titre_page = QLabel("Gestion d'echanges")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page)
        menu_layout = self.create_menu_commande()
        main_layout.addLayout(menu_layout)

        table_form_layout = QGridLayout()  

        # Créer les champs de saisie pour le formulaire sans 'self'
        self.name_pharma = QLineEdit() 
        self.name_pharma.setPlaceholderText("Nom de la pharmacie")
        self.name_pharma.textChanged.connect(self.OntextChangepharma)
        self.nom_pharma_s = QLabel("Aucune pharma sélectionnée")
        self.completer_pharma = QCompleter()
        self.completer_pharma.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_pharma.setCompletionMode(QCompleter.PopupCompletion)

        self.completer_pharma.activated.connect(self.selectionner_pharma)
        self.name_pharma.setCompleter(self.completer_pharma)

        self.medicament_code = QLineEdit()
        self.medicament_code.setPlaceholderText("Scanner medicament")
        self.quantite = QLineEdit()
        self.prix = QLineEdit()
 

        # Créer un bouton pour soumettre le formulaire
        self.submit_button_echange = QPushButton("Ajouter Medicament")
        self.submit_button_echange.clicked.connect(self.add_echange)

        self.envoyer_checkbox = QCheckBox("Envoyer vers pharma")
        self.envoyer_checkbox.stateChanged.connect(self.envoyer)
        table_form_layout.addWidget(self.envoyer_checkbox, 0,0)
        self.recevoir_checkbox = QCheckBox("Reçu de pharma")
        self.recevoir_checkbox.stateChanged.connect(self.recevoir)
        table_form_layout.addWidget(self.recevoir_checkbox, 0,1)
        table_form_layout.addWidget(QLabel("Nom de pharma :"), 1,0) 
        table_form_layout.addWidget(self.name_pharma, 1,1)    
        table_form_layout.addWidget(self.medicament_code, 2,1)  
        table_form_layout.addWidget(self.submit_button_echange, 2,0)  
        

        
        main_layout.addLayout(table_form_layout) 

        self.list_medicaments = QTableWidget(0, 4)
        self.list_medicaments.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_medicaments.setHorizontalHeaderLabels(["Code Medicament","Nom de medicament", "Quantité", "prix achat"])
        main_layout.addWidget(self.list_medicaments)

        self.confirm_echange = QPushButton("Confirmer l'echange")
        self.confirm_echange.clicked.connect(self.confirm_echange_pharma)
        main_layout.addWidget(self.confirm_echange)





        self.main_interface.content_layout.addWidget(self.vente_dash)
    def confirm_echange_pharma(self):
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        numero_facture = int(now.timestamp())
        id_salarie = self.main_interface.user_session['ID_Salarie']




        if self.producs_table.empty:
            QMessageBox.information(self.main_interface, "Aucun medicament", "Aucun medicament n'a été ajouté")
            return
        if self.name_pharma.text() == "":
            QMessageBox.information(self.main_interface, "Aucune pharmacie", "Aucune pharmacie n'a été sélectionnée")
            return
        pharma = extraire_pharma_nom(self.name_pharma.text().split("_")[0])
        if pharma is None:
            QMessageBox.information(self.main_interface, "Pharmacie non trouvée", "Pharmacie non trouvée")
            return
        pharma = dict(pharma)
        evoyer = self.envoyer_checkbox.isChecked()
        recu = self.recevoir_checkbox.isChecked()



        message = "Pharmacie Hajra\n"
        message += "Adresse : 123, Rue Exemple, Ville, Pays\n"
        message += "Téléphone : +212 123 456 789\n"
        message += "Bonjour,\n"
        message += "Facture n°: " + str(numero_facture) + "\n"
        message += "Agent : " + str(self.main_interface.user_session['ID_Salarie'])+ "\n"
        message += "----------------------------------------\n"
        message += "Détails de l'échange:\n"
        message += "Pharmacie : " + self.name_pharma.text() + "\n"
        message += "Envoyer : " + str(self.envoyer_checkbox.isChecked()) + "\n"
        message += "Reçu : " + str(self.recevoir_checkbox.isChecked()) + "\n"
        message += "----------------------------------------\n"
        message += "Produit\t\tQuantité\tPrix unitaire\tPrix total\n"
        message += "----------------------------------------\n"
        total_facture = 0
        for index, items in self.producs_table.iterrows():
            quantite_vendue = items['Quantite']
            quantite_traiter = 0  
            for  prix_achat_item, quanti in zip( items['Prix_Achat'], items['list_quantity']  ) :
                    quanti_rest_to_hand = quantite_vendue - quantite_traiter
                    if  quanti_rest_to_hand <= quanti:
                        message += f"{items['Code_EAN_13']}\t\t{quanti_rest_to_hand}\t\t{prix_achat_item} Dh\t\t{quanti_rest_to_hand*prix_achat_item} Dh\n" 
                        total_facture+=quanti_rest_to_hand * prix_achat_item
                        quantite_traiter += quanti_rest_to_hand 
                    else:
                        quantite_traiter+=quanti
                        message += f"{items['Code_EAN_13']}\t\t{quanti}\t\t{prix_achat_item} Dh\t\t{quanti*prix_achat_item} Dh\n" 
                        total_facture+=quanti * prix_achat_item
                    if quantite_traiter >= quantite_vendue:
                        break  

        message +="Total facture : " + str(total_facture) + " Dh\n"
        message += "----------------------------------------\n"
        message += "Merci pour votre échange!\n" 
        message += "Date: " + now_str + "\n"


        self.producs_table.reset_index(drop=True) 
        reply = QMessageBox.question(self.main_interface, "Confirmation de l'échange", message,
                    QMessageBox.Yes, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
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
                quantite_traiter = 0
                self.total_facture = 0
                for idcommande_item, prix_achat_item, prix_vente_item, ID_Stock_item, quanti in zip(id_commande_entre, prix_achat, prix_v , ID_Stock, quantite_list) :
                    quanti_rest_to_hand = quantite_vendue - quantite_traiter
                    if  quanti_rest_to_hand <= quanti:
                        ajouter_vente(id_medicament, idcommande_item, prix_achat_item, prix_achat_item, date_vente, quanti_rest_to_hand, quanti_rest_to_hand * prix_achat_item, pharma['ID_Pharmacie'], numero_facture, id_salarie) 
                        ajouter_echange(pharma['ID_Pharmacie'], numero_facture, date_vente, quanti_rest_to_hand * prix_achat_item, evoyer, id_salarie)
                        self.total_facture+=quanti_rest_to_hand * prix_achat_item
                        quantite_traiter += quanti_rest_to_hand 
                    else:
                        quantite_traiter+=quanti
                        ajouter_vente(id_medicament, idcommande_item, prix_achat_item, prix_achat_item, date_vente, quanti, quanti * prix_achat_item, pharma['ID_Pharmacie'], numero_facture, id_salarie) 
                        ajouter_echange(pharma['ID_Pharmacie'], numero_facture, date_vente, quanti * prix_achat_item, evoyer, id_salarie)
                        self.total_facture+=quanti * prix_achat_item
                    if quantite_traiter >= quantite_vendue:
                        break  
            QMessageBox.information(self.main_interface, "Echange effectué", "Echange effectué avec succès")
            
    def envoyer(self, state):  
        if state == 2:
            self.recevoir_checkbox.setChecked(False)
        
    def recevoir(self, state):
        if state == 2:
            self.envoyer_checkbox.setChecked(False)
    
    def OntextChangepharma(self,text):
        if len(text) >= 3:
            self.updateCompleter_pharma(text)

    def updateCompleter_pharma(self, text): 
        results = extraire_pharma_nom_like(text)   
        results = ["_".join(res) for res in results]
        model = QStringListModel(results)  
        self.completer_pharma.setModel(model) 

    def selectionner_pharma(self, text):
        self.nom_pharma_s.setText(text)
    


    def show_gestion_pharma_interface(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.vente_dash) 
        titre_page = QLabel("Gestion d'échanges : Ajouter et lister les pharmacies")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page)


        menu_layout = self.create_menu_commande()
        main_layout.addLayout(menu_layout)

        table_form_layout = QGridLayout() 

        # Créer les champs de saisie pour le formulaire sans 'self'
        self.name_input = QLineEdit() 
        self.name_input.setPlaceholderText("Nom")
        self.telephone_input = QLineEdit()
        self.telephone_input.setPlaceholderText("Téléphone")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Adresse")


        # Créer un bouton pour soumettre le formulaire
        self.submit_button = QPushButton("Ajouter Pharmacie") 
        self.submit_button.clicked.connect(self.add_pharma)


        table_form_layout.addWidget(QLabel("Nom :"), 0,0) 
        table_form_layout.addWidget(self.name_input, 0,1)   
        table_form_layout.addWidget(QLabel("Téléphone :"), 0,2) 
        table_form_layout.addWidget(self.telephone_input, 0,3) 
        table_form_layout.addWidget(QLabel("Email :"), 1,0) 
        table_form_layout.addWidget(self.email_input, 1,1) 
        table_form_layout.addWidget(QLabel("Adresse :"), 1,2) 
        table_form_layout.addWidget(self.address_input, 1,3)   
        table_form_layout.addWidget(self.submit_button, 2,3)  



        main_layout.addLayout(table_form_layout) 

        self.list_client = QTableWidget(0, 6)
        self.list_client.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_client.setHorizontalHeaderLabels(["Nom","Téléphone","Email","Adresse", "Crédit Actuel", "Crédit Maximum"])
        self.remplire_table()
        main_layout.addWidget(self.list_client)
    

        self.main_interface.content_layout.addWidget(self.vente_dash)


    def remplire_table(self):
        all_client = extraire_tous_pharma()
        self.list_client.setRowCount(len(all_client))
        for index,element in enumerate(all_client):
            dict_element = dict(element)
            self.list_client.setItem(index, 0, QTableWidgetItem(str(dict_element['Nom']))) 
            self.list_client.setItem(index, 1, QTableWidgetItem(str(dict_element['telephone']))) 
            self.list_client.setItem(index, 2, QTableWidgetItem(str(dict_element['email']))) 
            self.list_client.setItem(index, 3, QTableWidgetItem(str(dict_element['adresse']))) 
            self.list_client.setItem(index, 4, QTableWidgetItem(str(dict_element['outvalue']))) 
            self.list_client.setItem(index, 5, QTableWidgetItem(str(dict_element['invalue']))) 

    def add_pharma(self):
        # Récupérer les valeurs des champs
        name = self.name_input.text() 
        telephone = self.telephone_input.text()
        email = self.email_input.text()
        address = self.address_input.text() 
        # Ici vous pouvez ajouter le client dans une base de données ou autre logique 
        ajouter_pharmacie(name, address, telephone, email, 0, 0) 
        # Effacer les champs après soumission
        self.name_input.clear() 
        self.telephone_input.clear()
        self.email_input.clear()
        self.address_input.clear() 
    

    def add_echange(self):
        # Récupérer les valeurs des champs
        name = self.name_pharma.text() 
        code_med = self.medicament_code.text()
        self.add_medicament_to_echange(code_med)
        # Effacer les champs après soumission 
        self.medicament_code.clear() 

    def process_barcode(self, codebare):
        if len(codebare) >= 13:
            return codebare[-13:]
        return ""

    def keyPressEvent(self, event):  
        key = event.text() 
        current_time = time.time()
        if current_time - self.last_key_time < self.barcode_delay_threshold:  
            code_b = True
        self.last_key_time = current_time 
        if key == '\r' and code_b:  # Lorsque le lecteur envoie un saut de ligne   
            self.code_barre_scanner = self.process_barcode(self.code_barre_scanner) 
            if self.code_barre_scanner != "":
                self.add_medicament_to_echange(self.code_barre_scanner)
                self.code_barre_scanner = ""  # Réinitialiser pour le prochain scan                  
        else:
            self.code_barre_scanner += key  # Ajouter le caractère au code en cours 
    
    def add_medicament_to_echange(self,code_barre_scanner): 
        if  not self.producs_table.empty and code_barre_scanner in self.producs_table["Code_EAN_13"].values:
            self.producs_table.loc[self.producs_table['Code_EAN_13'] == code_barre_scanner, 'Quantite'] += 1
            self.update_table()
        else: 
            medicament  = extraire_medicament_code_barre(code_barre_scanner)
            if medicament is None:
                QMessageBox.information(self.main_interface, "Medicament non reconue", "Medicament non reconue")
                return 
            else: 
                medicament_on_dtock = extraire_medicament_id_stock(medicament['ID_Medicament']) 
                medicament = dict(medicament)  

                if medicament_on_dtock is None:
                    QMessageBox.information(self.main_interface, "Stock vide", "Le stock de ce médicament est vide. Veuillez vérifier la disponibilité.")
                else:  
                    if len(np.unique(medicament_on_dtock['Prix_Vente']))>1:
                        QMessageBox.information(self.main_interface, "Atention le prix de ce medicament à changer", "Atention le prix de ce medicament à changer, Merci de séparer les facture en cas de quantité superieur a 1")
                    
                    medicament["Quantite"]  = 1
                    medicament['Prix_Public_de_Vente'] = medicament_on_dtock['Prix_Achat'][0]
                    medicament['Prix_Vente'] = medicament_on_dtock['Prix_Vente']
                    medicament['Date_Expiration'] = medicament_on_dtock['Date_Expiration'][0]
                    medicament['Quantite_Actuelle'] = medicament_on_dtock['Quantite_Actuelle']
                    medicament['ID_Commande'] = medicament_on_dtock['ID_Commande']
                    medicament['list_quantity'] = medicament_on_dtock['list_quantity']
                    medicament['Prix_Achat'] = medicament_on_dtock['Prix_Achat']
                    medicament['ID_Stock'] = medicament_on_dtock['ID_Stock']
                    medicament["Prix_total"]  = medicament["Quantite"] * medicament['Prix_Achat']
                    df = pd.DataFrame([medicament])
                    if self.producs_table.empty :
                        self.producs_table = df 
                    else:
                        self.producs_table = pd.concat([self.producs_table, df], ignore_index=True)
                    self.producs_table['Prix_total']=self.producs_table['Prix_total'].round(2)
                    self.update_table()
    def update_table(self): 
        self.list_medicaments.setRowCount(len(self.producs_table))
        for row, product in self.producs_table.iterrows():   
            self.list_medicaments.setItem(row, 0, QTableWidgetItem(str(product['Code_EAN_13']))) 
            self.list_medicaments.setItem(row, 1, QTableWidgetItem(str(product['Nom'])))   
            line_edit = QSpinBox()
            line_edit.setValue(product['Quantite'])
            line_edit.editingFinished.connect(lambda row=row: self.update_quantity(row, line_edit.text()))
            self.list_medicaments.setCellWidget(row, 2, line_edit) 
            self.list_medicaments.setItem(row, 3, QTableWidgetItem(str(product['Prix_Achat'][0])))  
    
    def update_quantity(self, row, new_value): 
        new_quantity = int(new_value) 
        self.producs_table.loc[row,"Quantite"] = new_quantity  
        self.update_table() 
         
 