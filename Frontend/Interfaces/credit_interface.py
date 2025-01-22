from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QGridLayout,QHeaderView, QDoubleSpinBox,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox
)
from qtpy.QtCore import Qt
from Backend.Dataset.dataset import *
import pandas as pd


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
        self.table.setHorizontalHeaderLabels(["Id","Nom Prenom", "CIN" ,"Téléphone", "Credit actuel"])
        self.remplir_tableau() 
        self.table.cellClicked.connect(self.credit_selected)
        main_layout.addWidget(self.table)

        self.main_interface.content_layout.addWidget(self.credit_dash)

    def remplir_tableau(self):
        # Exemple de données fictives
        credits = extraire_tous_client_with_credit() 
        credits = [ dict(i) for i in credits]  
        self.table.setRowCount(len(credits)) 
        for row, credit in enumerate(credits): 
            self.table.setItem(row, 0, QTableWidgetItem(str(credit['ID_Client'])))
            self.table.setItem(row, 1, QTableWidgetItem(credit['Nom']+' '+credit['Prenom']))
            self.table.setItem(row, 2, QTableWidgetItem(credit['CIN']))
            self.table.setItem(row, 3, QTableWidgetItem(credit['Telephone']))
            self.table.setItem(row, 4, QTableWidgetItem(str(credit['Credit_Actuel']))) 
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

        titre_page = QLabel("Gestion de payment credit")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page) 



        table_form_layout = QGridLayout()

        self.client = extraire_client_id(self.id_client)
        self.client = dict(self.client)
        

        table_form_layout.addWidget(QLabel("Nom :"), 0,0)  
        table_form_layout.addWidget(QLabel(self.client['Nom']), 0,1) 
        table_form_layout.addWidget(QLabel("Prénom :"), 0,2) 
        table_form_layout.addWidget(QLabel(self.client['Prenom']), 0,3) 

        table_form_layout.addWidget(QLabel("CIN :"), 1,0)  
        table_form_layout.addWidget(QLabel(self.client['CIN']), 1,1) 
        table_form_layout.addWidget(QLabel("Téléphone :"), 1,2) 
        table_form_layout.addWidget(QLabel(self.client['Telephone']), 1,3) 


        table_form_layout.addWidget(QLabel("Email :"), 2,0)  
        table_form_layout.addWidget(QLabel(self.client['Email']), 2,1) 
        table_form_layout.addWidget(QLabel("Adresse :"), 2,2) 
        table_form_layout.addWidget(QLabel(self.client['Adresse']), 2,3) 


        table_form_layout.addWidget(QLabel("Max Credit"), 3,0)  
        table_form_layout.addWidget(QLabel(str(self.client['Max_Credit'])), 3,1) 
        table_form_layout.addWidget(QLabel("Credit Actuel"), 3,2) 
        table_form_layout.addWidget(QLabel(str(self.client['Credit_Actuel'])), 3,3) 


        self.payment_input = QDoubleSpinBox()
        self.payment_input.setMinimum(0)  # Valeur minimale
        self.payment_input.setMaximum(float(self.client['Credit_Actuel']))  # Valeur maximale 

        self.submit_button = QPushButton("Payer")
        self.submit_button.clicked.connect(self.add_paiment)

        table_form_layout.addWidget(QLabel("Effectuer un paiement :"), 4,0)  
        table_form_layout.addWidget(self.payment_input, 4,1)  
        table_form_layout.addWidget(self.submit_button, 4,3) 
        main_layout.addLayout(table_form_layout)



        self.list_factures = QTableWidget(0, 4)
        self.list_factures.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_factures.setHorizontalHeaderLabels(["Type","Numero Facture","Totale", 'Date'])
        self.remplire_table()
        main_layout.addWidget(self.list_factures) 
        self.main_interface.content_layout.addWidget(self.credit_dash)

    
    def add_paiment(self):
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        montant_paye = self.payment_input.value()
        id_salarie = self.main_interface.user_session['ID_Salarie']
        ajouter_payment(self.id_client, int(now.timestamp()), montant_paye, now_str, id_salarie)
        ajouter_credit_client(self.id_client,  -montant_paye)
        self.show_payment_interface()

        
    def remplire_table(self):
        all_credit = extraire_credit_with_id_client(self.id_client)
        all_paiment = extraire_paiment_with_id_client(self.id_client)

        all_credit = pd.DataFrame([dict(credit) for credit in all_credit])[['Numero_Facture', "Reste_A_Payer", "Date_Dernier_Paiement"]]
        all_paiment = pd.DataFrame([dict(pay) for pay in all_paiment])[['Numero_Facture', "Montant_Paye", "Date_Paiement"]]
        all_credit.rename(columns={'Reste_A_Payer':'Totale', "Date_Dernier_Paiement" : "Date"}, inplace=True)
        all_paiment.rename(columns={'Montant_Paye':'Totale', "Date_Paiement": "Date"},inplace=True)
        all_credit['Type'] = 'Credit'
        all_paiment['Type'] = 'Paiment'

        result = pd.concat([all_credit, all_paiment], ignore_index=True)
        result["Date"] = pd.to_datetime(result["Date"], format="%d/%m/%Y %H:%M:%S", errors="coerce")
        result=result.sort_values(by="Date",  ascending=False,  ignore_index=True).reset_index()

        self.list_factures.setRowCount(len(result)) 
        for row, element in result.iterrows(): 
            self.list_factures.setItem(row, 0, QTableWidgetItem(str(element['Type'])))
            self.list_factures.setItem(row, 1, QTableWidgetItem(element['Numero_Facture']))
            self.list_factures.setItem(row, 2, QTableWidgetItem(str(element['Totale'])))
            self.list_factures.setItem(row, 3, QTableWidgetItem(str(element['Date']))  )

  



    
 