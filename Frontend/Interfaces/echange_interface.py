from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QDoubleSpinBox,QGridLayout,QHeaderView,QCompleter,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox
)
from qtpy.QtCore import Qt, QStringListModel

from Backend.Dataset.dataset import *


class Echange_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_principal_interface()
    


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
        self.list_medicament_data = []

        # Créer les champs de saisie pour le formulaire sans 'self'
        self.name_pharma = QLineEdit() 
        self.name_pharma.textChanged.connect(self.OntextChangepharma)

        self.completer_pharma = QCompleter()
        self.completer_pharma.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_pharma.setCompletionMode(QCompleter.PopupCompletion)
        self.name_pharma.setCompleter(self.completer_pharma)
        self.completer_pharma.activated.connect(self.selectionner_pharma)

        self.medicament_code = QLineEdit()
        self.quantite = QLineEdit()
        self.prix = QLineEdit()
 

        # Créer un bouton pour soumettre le formulaire
        self.submit_button_echange = QPushButton("Ajouter ajouter Medicament")
        self.submit_button_echange.clicked.connect(self.add_echange)


        table_form_layout.addWidget(QLabel("Nom de pharma :"), 0,0) 
        table_form_layout.addWidget(self.name_pharma, 0,1)   
        table_form_layout.addWidget(QLabel("Scanner medicament :"), 0,2) 
        table_form_layout.addWidget(self.medicament_code, 0,3) 
        table_form_layout.addWidget(QLabel("Quantité :"), 1,0) 
        table_form_layout.addWidget(self.quantite, 1,1)
        table_form_layout.addWidget(QLabel("Prix  :"), 1,2) 
        table_form_layout.addWidget(self.prix, 1,3)   
        table_form_layout.addWidget(self.submit_button_echange, 2,3)  

        main_layout.addLayout(table_form_layout) 

        self.list_medicaments = QTableWidget(0, 4)
        self.list_medicaments.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_medicaments.setHorizontalHeaderLabels(["Code Medicament","Nom de medicament", "Quantité", "prix achat"])
        main_layout.addWidget(self.list_medicaments)

        self.confirm_echange = QPushButton("Confirmer l'echange")
        main_layout.addWidget(self.confirm_echange)





        self.main_interface.content_layout.addWidget(self.vente_dash)
    
    def OntextChangepharma(self,text):
        if len(text) >= 3:
            self.updateCompleter_pharma(text)

    def updateCompleter_pharma(self, text): 
        results = extraire_pharma_nom_like(text)   
        results = ["_".join(res) for res in results]
        model = QStringListModel(results)  
        self.completer_pharma.setModel(model) 
    def selectionner_pharma(self, text):
        print(text)
    


    def show_gestion_pharma_interface(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.vente_dash) 
        titre_page = QLabel("Gestion d'echanges : Ajouter et lister les pharmacies")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page)


        menu_layout = self.create_menu_commande()
        main_layout.addLayout(menu_layout)

        table_form_layout = QGridLayout() 

        # Créer les champs de saisie pour le formulaire sans 'self'
        self.name_input = QLineEdit() 
        self.telephone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()


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
        self.list_client.setHorizontalHeaderLabels(["Nom","Téléphone","Email","Adresse", "Crédit Actuel", "Max Crédit"])
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
        quantite = self.quantite.text()
        prix = self.prix.text() 
        # Ici vous pouvez ajouter le client dans une base de données ou autre logique 
        self.list_medicament_data.append({'id' :name, "code_med" : code_med , "quantite" : quantite,"prix":prix })
        self.remplire_table_echange()
        # Effacer les champs après soumission 
        self.medicament_code.clear()
        self.quantite.clear()
        self.prix.clear() 
    
    def remplire_table_echange(self): 
        self.list_medicaments.setRowCount(len(self.list_medicament_data))
        for index,element in enumerate(self.list_medicament_data): 
            self.list_medicaments.setItem(index, 0, QTableWidgetItem(str(element['id']))) 
            self.list_medicaments.setItem(index, 1, QTableWidgetItem(str(element['code_med']))) 
            self.list_medicaments.setItem(index, 2, QTableWidgetItem(str(element['quantite']))) 
            self.list_medicaments.setItem(index, 3, QTableWidgetItem(str(element['prix'])))  