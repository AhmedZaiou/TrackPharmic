from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QGridLayout,QHeaderView, QDoubleSpinBox,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox
)
from qtpy.QtCore import Qt
from Backend.Dataset.credit import Credit
from Backend.Dataset.client import Clients
from Backend.Dataset.payment import Payment
import pandas as pd
from datetime import datetime


class Credit_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()

    def show_vente_interface(self):
        self.main_interface.clear_content_frame()

        self.credit_dash = QWidget()
        self.credit_dash.setObjectName("credit_dash")

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.credit_dash) 

        titre_page = QLabel("Gestion de credit")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page) 
 


        self.table = QTableWidget()
        self.table.setColumnCount(5)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(["Id", "Nom Prénom", "CIN", "Téléphone", "Crédit actuel"])
        self.remplir_tableau() 
        self.table.cellClicked.connect(self.credit_selected)
        main_layout.addWidget(self.table)

        self.main_interface.content_layout.addWidget(self.credit_dash)

    def remplir_tableau(self):
        # Exemple de données fictives
        credits = Clients.extraire_tous_client_with_credit() 
        credits = [ dict(i) for i in credits]  
        self.table.setRowCount(len(credits)) 
        for row, credit in enumerate(credits): 
            self.table.setItem(row, 0, QTableWidgetItem(str(credit['id_client'])))
            self.table.setItem(row, 1, QTableWidgetItem(credit['nom']+' '+credit['prenom']))
            self.table.setItem(row, 2, QTableWidgetItem(credit['cin']))
            self.table.setItem(row, 3, QTableWidgetItem(credit['telephone']))
            self.table.setItem(row, 4, QTableWidgetItem(str(credit['credit_actuel']))) 
    def credit_selected(self,row, column):
        self.id_client = self.table.item(row, 0).text() 
        self.show_payment_interface()
    


    def show_payment_interface(self):
        self.main_interface.clear_content_frame()
        self.credit_dash = QWidget()
        self.credit_dash.setObjectName("credit_dash")

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.credit_dash) 

        titre_page = QLabel("Gestion des paiements de crédit")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page) 



        table_form_layout = QGridLayout()

        self.client = Clients.extraire_client_id(self.id_client)
        self.client = dict(self.client)
        

        table_form_layout.addWidget(QLabel("Nom :"), 0,0)  
        table_form_layout.addWidget(QLabel(self.client['nom']), 0,1) 
        table_form_layout.addWidget(QLabel("Prénom :"), 0,2) 
        table_form_layout.addWidget(QLabel(self.client['prenom']), 0,3) 

        table_form_layout.addWidget(QLabel("CIN :"), 1,0)  
        table_form_layout.addWidget(QLabel(self.client['cin']), 1,1) 
        table_form_layout.addWidget(QLabel("Téléphone :"), 1,2) 
        table_form_layout.addWidget(QLabel(self.client['telephone']), 1,3) 


        table_form_layout.addWidget(QLabel("Email :"), 2,0)  
        table_form_layout.addWidget(QLabel(self.client['email']), 2,1) 
        table_form_layout.addWidget(QLabel("Adresse :"), 2,2) 
        table_form_layout.addWidget(QLabel(self.client['adresse']), 2,3) 


        table_form_layout.addWidget(QLabel("Crédit Maximum"), 3,0)  
        table_form_layout.addWidget(QLabel(str(self.client['max_credit'])), 3,1) 
        table_form_layout.addWidget(QLabel("Crédit Actuel"), 3,2) 
        table_form_layout.addWidget(QLabel(str(self.client['credit_actuel'])), 3,3) 


        self.payment_input = QDoubleSpinBox()
        self.payment_input.setMinimum(0)  # Valeur minimale
        self.payment_input.setMaximum(float(self.client['credit_actuel']))  # Valeur maximale 

        self.submit_button = QPushButton("Payer")
        self.submit_button.clicked.connect(self.add_paiment)

        table_form_layout.addWidget(QLabel("Effectuer un paiement :"), 4,0)
        table_form_layout.addWidget(self.payment_input, 4,1)  
        table_form_layout.addWidget(self.submit_button, 4,3) 
        main_layout.addLayout(table_form_layout)



        self.list_factures = QTableWidget(0, 4)
        self.list_factures.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_factures.setHorizontalHeaderLabels(["Type", "Numéro de Facture", "Total", "Date"])
        self.remplire_table()
        main_layout.addWidget(self.list_factures) 
        self.main_interface.content_layout.addWidget(self.credit_dash)

    
    def add_paiment(self):
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        montant_paye = self.payment_input.value()
        id_salarie = self.main_interface.user_session['id_salarie']
        Payment.ajouter_payment(self.id_client, int(now.timestamp()), montant_paye, now_str, id_salarie)
        Clients.ajouter_credit_client(self.id_client,  -montant_paye)
        self.show_payment_interface()

        
    def remplire_table(self):
        all_credit = Credit.extraire_credit_with_id_client(self.id_client)
        all_paiment = Payment.extraire_payment_with_id_client(self.id_client) 
        if len(all_credit) == 0:
            all_credit = pd.DataFrame(columns=['numero_facture', "reste_a_payer", "date_dernier_paiement"])
        else:
            all_credit = pd.DataFrame(all_credit)[['numero_facture', "reste_a_payer", "date_dernier_paiement"]]
        
        print(all_paiment)

        if len(all_paiment) == 0:
            all_paiment = pd.DataFrame(columns=['numero_facture', "montant_paye", "date_paiement"])
        else:
            all_paiment = pd.DataFrame(all_paiment)[['numero_facture', "montant_paye", "date_paiement"]]
        all_credit.rename(columns={'Reste_A_Payer':'Totale', "Date_Dernier_Paiement" : "Date"}, inplace=True)
        all_paiment.rename(columns={'Montant_Paye':'Totale', "Date_Paiement": "Date"},inplace=True)
        all_credit['Type'] = 'Credit'
        all_paiment['Type'] = 'Paiment'

        result = pd.concat([all_credit, all_paiment], ignore_index=True)
        print(result)
        result["date_paiement"] = pd.to_datetime(result["date_paiement"], format="%d/%m/%Y %H:%M:%S", errors="coerce")
        result=result.sort_values(by="date_paiement",  ascending=False,  ignore_index=True).reset_index()

        self.list_factures.setRowCount(len(result)) 
        for row, element in result.iterrows(): 
            self.list_factures.setItem(row, 0, QTableWidgetItem(str(element['Type'])))
            self.list_factures.setItem(row, 1, QTableWidgetItem(str(element['numero_facture'])))
            self.list_factures.setItem(row, 2, QTableWidgetItem(str(element['montant_paye'])))
            self.list_factures.setItem(row, 3, QTableWidgetItem(str(element['date_paiement']))  )
