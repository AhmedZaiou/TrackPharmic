from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,QSpinBox,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox, QMessageBox
)
from qtpy.QtCore import Qt
import ast


from datetime import datetime

import time



from Backend.Dataset.dataset import *


class Stock_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.main_interface.keyPressEvent = self.keyPressEvent
        self.show_reception_interface()

        self.last_time = time.time()
        self.commande_deja_traiter_list = []

    


    def create_menu_commande(self):
        menu_layout = QHBoxLayout()
        self.reception_commande = QPushButton("Reception d'une commande")
        self.reception_commande.clicked.connect(self.reception_commande_fc)
        menu_layout.addWidget(self.reception_commande)
        self.add_stock_menu = QPushButton("Ajouter dans le stock")
        self.add_stock_menu.clicked.connect(self.add_stock_menu_fc)
        menu_layout.addWidget(self.add_stock_menu)
        return menu_layout

    def reception_commande_fc(self):
        self.show_reception_interface()
    def add_stock_menu_fc(self):
        self.show_add_stock_interface()

    def show_reception_interface(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.vente_dash)
 
        titre_page = QLabel("Gestion de Stock")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page)

        menu_layout = self.create_menu_commande()
        main_layout.addLayout(menu_layout)


        self.cart_table = QTableWidget(0, 8)
        self.cart_table.setHorizontalHeaderLabels(["Code commande","Fourniseur", "Date de comande", "Noms des medicaments",  "Statue commande", "Traiter"])
        self.cart_table.cellClicked.connect(self.commande_select)
        main_layout.addWidget(self.cart_table)
        self.charger_carte_table()














        









        self.main_interface.content_layout.addWidget(self.vente_dash)





    def show_add_stock_interface(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")
        self.code_barre_scanner = ""

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.vente_dash)
 
        titre_page = QLabel("Gestion de Stock")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page)

        menu_layout = self.create_menu_commande()
        main_layout.addLayout(menu_layout)




        formul_layout = QHBoxLayout()

        self.formulaire_widget = QWidget()







        validation_layout_fournisseur = QGridLayout(self.formulaire_widget)
        date_commande = QLabel('Date du commande :')
        self.date_commande_value = QLabel("")
        fournisseur_name = QLabel("Nom de fournisseur : ")
        self.fournisseur_name_value = QLabel("")

        statue_commande = QLabel("Statue de Commande")
        self.statue_commande_value = QLabel("")

        code_barre = QLabel('Code EAN 13 :')
        self.code_barre_value = QLineEdit()
        medicament_name = QLabel("Nom de medicament : ")
        self.medicament_name_value = QLabel("")

        quantite_commender = QLabel("Quantité")
        self.quantite_commender_value = QSpinBox()
        self.quantite_commender_value.setRange(1, 10000)

        self.suivant_medicament = QLabel("Suivant >")
        self.precedent_medicament = QLabel("< Precedent")





        validation_layout_fournisseur.addWidget(fournisseur_name, 0,0)
        validation_layout_fournisseur.addWidget(self.fournisseur_name_value, 0,1)
        validation_layout_fournisseur.addWidget(date_commande, 1,0)
        validation_layout_fournisseur.addWidget(self.date_commande_value, 1,1)
        validation_layout_fournisseur.addWidget(statue_commande, 2,0)
        validation_layout_fournisseur.addWidget(self.statue_commande_value, 2,1)  

        validation_layout_fournisseur.addWidget(code_barre, 3,0)
        validation_layout_fournisseur.addWidget(self.code_barre_value, 3,1)
        validation_layout_fournisseur.addWidget(medicament_name, 4,0)
        validation_layout_fournisseur.addWidget(self.medicament_name_value, 4,1) 
        validation_layout_fournisseur.addWidget(quantite_commender, 6,0)
        validation_layout_fournisseur.addWidget(self.quantite_commender_value, 6,1)  





        self.prix_achat_medicament = QLineEdit()
        self.prix_vente_medicament = QLineEdit()
        self.prix_cons_medicament = QLineEdit()
        self.date_expiration_medicament = QLineEdit()

        self.quantite_maximal_medicament = QLineEdit()
        self.quantite_minimal_medicament = QLineEdit()


         # Ajout des labels et des champs dans le layout
        validation_layout_fournisseur.addWidget(QLabel("Prix d'achat :"), 7, 0)
        validation_layout_fournisseur.addWidget(self.prix_achat_medicament, 7, 1)

        validation_layout_fournisseur.addWidget(QLabel("Prix de vente :"), 8, 0)
        validation_layout_fournisseur.addWidget(self.prix_vente_medicament, 8, 1)

        

        validation_layout_fournisseur.addWidget(QLabel("Date d'expiration :"), 9, 0)
        validation_layout_fournisseur.addWidget(self.date_expiration_medicament, 9, 1)

        validation_layout_fournisseur.addWidget(QLabel("Quantité maximale :"), 10, 0)
        validation_layout_fournisseur.addWidget(self.quantite_maximal_medicament, 10, 1)

        validation_layout_fournisseur.addWidget(QLabel("Quantité minimale :"), 11, 0)
        validation_layout_fournisseur.addWidget(self.quantite_minimal_medicament, 11, 1)




        self.confirm_button = QPushButton("Confirmer l'ajout") 
        self.confirm_button.clicked.connect(self.confirmation_ajout)

        validation_layout_fournisseur.addWidget(self.confirm_button, 12, 1) 

        formul_layout.addWidget(self.formulaire_widget) 

        self.situation_widget = QWidget()
        situation_layout = QVBoxLayout(self.situation_widget)

        self.medicament_commande_list = QTableWidget(0, 3)
        self.medicament_commande_list.setHorizontalHeaderLabels(["Code EAN 13","Nom Medicament", "Quantité"])

        situation_layout.addWidget(self.medicament_commande_list)

        self.medicament_traiter_commande_list = QTableWidget(0, 3)
        self.medicament_traiter_commande_list.setHorizontalHeaderLabels(["Code EAN 13","Nom Medicament", "Quantité"])

        situation_layout.addWidget(self.medicament_traiter_commande_list)


        formul_layout.addWidget(self.situation_widget)



        button_layout = QGridLayout()
        self.supprission_button = QPushButton("Supprimer la commande")
        button_layout.addWidget(self.supprission_button, 0,0)


        self.finalisation_button = QPushButton("finaliser la commande")
        self.finalisation_button.clicked.connect(self.finaliser_commande)
        button_layout.addWidget(self.finalisation_button,0,1)
        
        main_layout.addLayout(formul_layout)
        main_layout.addLayout(button_layout)

        self.main_interface.content_layout.addWidget(self.vente_dash)
    


    def remplire_medicament_deja_traiter(self):
        id_commande = self.commande_current["ID_Commande"]

        self.medicament_traiter_commande_list.setRowCount(len(self.commande_deja_traiter_list))
        for id,item in  enumerate(self.commande_deja_traiter_list):
            self.medicament_traiter_commande_list.setItem(id, 0, QTableWidgetItem(str(item[0])))
            self.medicament_traiter_commande_list.setItem(id, 1, QTableWidgetItem(str(item[1])))
            self.medicament_traiter_commande_list.setItem(id, 2, QTableWidgetItem(str(item[2])))
    
    def finaliser_commande(self):
        complet_commande(self.commande_current['ID_Commande'], self.main_interface.user_session['ID_Salarie'])





        

    
    def confirmation_ajout(self):
        print(self.commande_current)
        print(self.medicament_search)
        quantite_minimal_medicament = self.quantite_minimal_medicament.text()
        quantite_maximal_medicament = self.quantite_maximal_medicament.text()

        date_expiration_medicament = self.date_expiration_medicament.text()
        prix_achat_medicament = self.prix_achat_medicament.text()
        prix_vente_medicament = self.prix_vente_medicament.text()
        quantite_commender_value = self.quantite_commender_value.value()


        self.commande_deja_traiter_list.append([self.medicament_search['Code_EAN_13'],self.medicament_search['Nom'], self.quantite_commender_value.value()])
        self.remplire_medicament_deja_traiter()


        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")


        ajouter_stock(self.medicament_search['ID_Medicament'], self.commande_current['ID_Commande'], self.main_interface.user_session['ID_Salarie'], prix_achat_medicament, prix_vente_medicament, prix_vente_medicament, now, date_expiration_medicament,
                  quantite_commender_value, quantite_commender_value, quantite_commender_value, quantite_commender_value,
                  now, now) 
        




    def charger_carte_table(self):
        self.commande_en_cours  = extraire_tous_commandes_table()  
        self.cart_table.setRowCount(len(self.commande_en_cours ))
        for row, product in enumerate(self.commande_en_cours):  
            product = dict(product) 
            self.cart_table.setItem(row, 0, QTableWidgetItem(str(product['ID_Commande']))) 
            self.cart_table.setItem(row, 1, QTableWidgetItem(str(product['ID_Fournisseur']))) 
            self.cart_table.setItem(row, 2, QTableWidgetItem(str(product['Date_Commande']))) 
            self.cart_table.setItem(row, 3, QTableWidgetItem(str(product['Liste_Produits']))) 
            self.cart_table.setItem(row, 4, QTableWidgetItem(str(product['Statut_Reception'])))  


    def commande_select(self, row, column):
        self.show_add_stock_interface()

        self.commande_current = dict(self.commande_en_cours[row])
        self.fournisseur_selectionner = extraire_fournisseur(self.commande_current['ID_Fournisseur'])

        self.fournisseur_name_value.setText(str(self.fournisseur_selectionner[1]))
        self.date_commande_value.setText(str(self.commande_current['Date_Commande']))
        self.statue_commande_value.setText(str(self.commande_current['Statut_Reception']))

        self.list_product_commande = ast.literal_eval(self.commande_current['Liste_Produits'])

        self.medicament_commande_list.setRowCount(len(self.list_product_commande))
        for id,item in  enumerate(self.list_product_commande):
            self.medicament_commande_list.setItem(id, 0, QTableWidgetItem(str(item[0])))
            self.medicament_commande_list.setItem(id, 1, QTableWidgetItem(str(item[1])))
            self.medicament_commande_list.setItem(id, 2, QTableWidgetItem(str(item[2])))
        
        self.remplire_medicament_deja_traiter()
        
        self.item_id = 0
        self.number_items = len(self.list_product_commande)
        if self.number_items >0:
            self.code_barre_value.setText(str(self.list_product_commande[self.item_id][0]))
            self.medicament_name_value.setText(str(self.list_product_commande[self.item_id][1]))
            self.quantite_commender_value.setValue(self.list_product_commande[self.item_id][2])
    



    def keyPressEvent(self, event):
        """Gérer les entrées clavier, comme les données du lecteur de code-barres."""
        key = event.text() 
        '''current_time = time.time()
        time_diff = current_time - self.last_time
        self.last_time = current_time
        if time_diff < 0.14 :'''  
        #self.code_barre_value.setFocus() 
        if key == '\r' :  # Lorsque le lecteur envoie un saut de ligne

            #if len(self.code_barre_scanner ) == 13:
            print("pass",self.code_barre_scanner ) 
            self.code_barre_value.setText(self.code_barre_scanner)
            self.remplir_medicament_cases(self.code_barre_scanner)
            self.code_barre_scanner = ""  # Réinitialiser pour le prochain scan 
        else:
            self.code_barre_scanner += key  # Ajouter le caractère au code en cours 

     
    def remplir_medicament_cases(self, code_barre_scanner):
        self.medicament_search = extraire_medicament_code_barre(code_barre_scanner)  
        if self.medicament_search is None:
            QMessageBox.warning(self.main_interface, "Erreur", "Le medicament n'exsiste pas, voulez vous l'ajouter ?")
        else:
            self.medicament_search = dict(self.medicament_search)
            self.quantite_maximal_medicament.setText(str(self.medicament_search["max_stock"] ))
            self.quantite_minimal_medicament.setText(str(self.medicament_search["min_stock"] ) ) 
            self.prix_vente_medicament.setText(str(self.medicament_search["Prix_Public_de_Vente"] ))



        





        

