from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QGridLayout,QDoubleSpinBox,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox, QHeaderView
)
from qtpy.QtCore import Qt
from Backend.Dataset.dataset import *




class Client_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()

    def show_vente_interface(self):
        self.main_interface.clear_content_frame()

        self.client_dash = QWidget()
        self.client_dash.setObjectName("client_dash")

        main_layout = QVBoxLayout(self.client_dash)

        titre_page = QLabel("Gestion des clients")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page) 
        
        table_form_layout = QGridLayout() 
        
        
        # Créer les champs de saisie pour le formulaire sans 'self'
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom")
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Prénom")
        self.cin_input = QLineEdit()
        self.cin_input.setPlaceholderText("CIN")
        self.telephone_input = QLineEdit()
        self.telephone_input.setPlaceholderText("Téléphone")
        self.telephone_input.setValidator(int_validator)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Adresse")

        # Création de champs numériques pour Max_Credit et Credit_Actuel
        self.max_credit_input = QDoubleSpinBox()
        self.max_credit_input.setMinimum(0)  # Valeur minimale
        self.max_credit_input.setMaximum(100000)  # Valeur maximale 

        self.current_credit_input = QDoubleSpinBox()
        self.current_credit_input.setMinimum(0)  # Valeur minimale
        self.current_credit_input.setMaximum(100000)  # Valeur maximale 

        # Créer un bouton pour soumettre le formulaire
        self.submit_button = QPushButton("Ajouter")
        self.submit_button.clicked.connect(self.add_client)


        table_form_layout.addWidget(QLabel("Nom :"), 0,0) 
        table_form_layout.addWidget(self.name_input, 0,1) 
        table_form_layout.addWidget(QLabel("Prénom :"), 0,2) 
        table_form_layout.addWidget(self.surname_input, 0,3) 
        table_form_layout.addWidget(QLabel("CIN :"), 1,0) 
        table_form_layout.addWidget(self.cin_input, 1,1) 
        table_form_layout.addWidget(QLabel("Téléphone :"), 1,2) 
        table_form_layout.addWidget(self.telephone_input, 1,3) 
        table_form_layout.addWidget(QLabel("Email :"), 2,0) 
        table_form_layout.addWidget(self.email_input, 2,1) 
        table_form_layout.addWidget(QLabel("Adresse :"), 2,2) 
        table_form_layout.addWidget(self.address_input, 2,3) 
        table_form_layout.addWidget(QLabel("Max Crédit (Dh) :"), 3,0) 
        table_form_layout.addWidget(self.max_credit_input, 3,1) 
        table_form_layout.addWidget(QLabel("Crédit Actuel (Dh) :"), 3,2) 
        table_form_layout.addWidget(self.current_credit_input, 3,3)  
        table_form_layout.addWidget(self.submit_button, 4,3)  


        main_layout.addLayout(table_form_layout)



        self.list_client = QTableWidget(0, 6)
        self.list_client.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_client.setHorizontalHeaderLabels(["Nom", "Prénom", "CIN", "Téléphone", "Crédit Actuel", "Max Crédit"])
        self.remplire_table()
        main_layout.addWidget(self.list_client)



        self.main_interface.content_layout.addWidget(self.client_dash)

    

    def remplire_table(self):
        all_client = extraire_tous_clients()
        self.list_client.setRowCount(len(all_client))
        for index,element in enumerate(all_client):
            dict_element = dict(element)
            self.list_client.setItem(index, 0, QTableWidgetItem(str(dict_element['Nom']))) 
            self.list_client.setItem(index, 1, QTableWidgetItem(str(dict_element['Prenom']))) 
            self.list_client.setItem(index, 2, QTableWidgetItem(str(dict_element['CIN']))) 
            self.list_client.setItem(index, 3, QTableWidgetItem(str(dict_element['Telephone']))) 
            self.list_client.setItem(index, 4, QTableWidgetItem(str(dict_element['Credit_Actuel']))) 
            self.list_client.setItem(index, 5, QTableWidgetItem(str(dict_element['Max_Credit']))) 

    def add_client(self):
        # Récupérer les valeurs des champs
        name = self.name_input.text()
        surname = self.surname_input.text()
        cin = self.cin_input.text()
        telephone = self.telephone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        max_credit = self.max_credit_input.value()
        current_credit = self.current_credit_input.value()
        # Ici vous pouvez ajouter le client dans une base de données ou autre logique 
        ajouter_client(name, surname, cin, telephone, email, address, max_credit, current_credit)
        self.remplire_table()
        # Effacer les champs après soumission
        self.name_input.clear()
        self.surname_input.clear()
        self.cin_input.clear()
        self.telephone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.max_credit_input.setValue(0)
        self.current_credit_input.setValue(0)

         
        
 