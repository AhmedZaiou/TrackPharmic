from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QDoubleSpinBox,
    QGridLayout,
    QHeaderView,
    QCompleter,
    QMessageBox,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QDateEdit,
)
from qtpy.QtCore import Qt, QStringListModel, QDate

from Backend.Dataset.echanges import Echanges
from Backend.Dataset.pharmacie import Pharmacies
from Backend.Dataset.stock import Stock
from Backend.Dataset.medicament import Medicament
from Backend.Dataset.salarie import Salaries
from datetime import datetime
from Frontend.utils.utils import *
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
        self.add_commande_menu = QPushButton("Envoi d'un echange")
        self.add_commande_menu.clicked.connect(self.gestion_echange)
        menu_layout.addWidget(self.add_commande_menu)
        self.add_commande_menu_recu = QPushButton("Recu un echange")
        self.add_commande_menu_recu.clicked.connect(self.gestion_echange_recus)
        menu_layout.addWidget(self.add_commande_menu_recu)  
        self.list_commande_menu = QPushButton("Pharmacie amis")
        self.list_commande_menu.clicked.connect(self.gestion_pharma)
        menu_layout.addWidget(self.list_commande_menu)

        return menu_layout
    

    def gestion_echange(self):
        self.show_principal_interface()
    def gestion_echange_recus(self):
        self.show_principal_interface_recus()


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
        self.medicament_code.setValidator(int_validator)
        self.medicament_code.setPlaceholderText("Scanner medicament")

        # Créer un bouton pour soumettre le formulaire
        self.submit_button_echange = QPushButton("Ajouter Medicament")
        self.submit_button_echange.clicked.connect(self.add_echange)

        """self.envoyer_checkbox = QCheckBox("Envoyer vers pharma")
        self.envoyer_checkbox.stateChanged.connect(self.envoyer)
        table_form_layout.addWidget(self.envoyer_checkbox, 0, 0)
        self.recevoir_checkbox = QCheckBox("Reçu de pharma")
        self.recevoir_checkbox.stateChanged.connect(self.recevoir)
        table_form_layout.addWidget(self.recevoir_checkbox, 0, 1)"""
        table_form_layout.addWidget(QLabel("Nom de pharma :"), 1, 0)
        table_form_layout.addWidget(self.name_pharma, 1, 1)
        table_form_layout.addWidget(self.medicament_code, 2, 1)
        table_form_layout.addWidget(self.submit_button_echange, 2, 0)

        main_layout.addLayout(table_form_layout)

        self.list_medicaments = QTableWidget(0, 4)
        self.list_medicaments.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.list_medicaments.setHorizontalHeaderLabels(
            ["Code Medicament", "Nom de medicament", "Quantité", "prix achat"]
        )
        main_layout.addWidget(self.list_medicaments)

        self.confirm_echange = QPushButton("Confirmer l'echange")
        self.confirm_echange.clicked.connect(self.confirm_echange_pharma)
        main_layout.addWidget(self.confirm_echange)

        self.main_interface.content_layout.addWidget(self.vente_dash)


    def show_principal_interface_list(self):
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
        self.main_interface.content_layout.addWidget(self.vente_dash)





        table_form_layout = QGridLayout()

        # Créer les champs de saisie pour le formulaire sans 'self'
        self.name_input_profil = QLabel(self.pharma['Nom']) 
        self.telephone_input_profil = QLabel(self.pharma['Téléphone'])  
        self.email_input_profil = QLabel(self.pharma['Email']) 
        self.address_input_profil = QLabel(self.pharma['Adresse'])
        self.out_input_profil = QLabel(self.pharma['Out_value']) 
        self.in_input_profil = QLabel(self.pharma['In_value'])
    

        table_form_layout.addWidget(QLabel("Nom :"), 0, 0)
        table_form_layout.addWidget(self.name_input_profil, 0, 1)
        table_form_layout.addWidget(QLabel("Téléphone :"), 0, 2)
        table_form_layout.addWidget(self.telephone_input_profil, 0, 3)
        table_form_layout.addWidget(QLabel("Email :"), 1, 0)
        table_form_layout.addWidget(self.email_input_profil, 1, 1)
        table_form_layout.addWidget(QLabel("Adresse :"), 1, 2)
        table_form_layout.addWidget(self.address_input_profil, 1, 3) 
        table_form_layout.addWidget(QLabel("Total envoyer :"), 2, 0)
        table_form_layout.addWidget(self.out_input_profil, 2, 1)
        table_form_layout.addWidget(QLabel("Total reçu :"), 2, 2)
        table_form_layout.addWidget(self.in_input_profil, 2, 3) 
        

        main_layout.addLayout(table_form_layout)

        self.list_client = QTableWidget(0, 5)
        self.list_client.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_client.setHorizontalHeaderLabels(
            ["Facture", "Date", "Total", "sens",  "Agent"]
        )
        self.remplire_table_echange()
        main_layout.addWidget(self.list_client)
        pass

    def remplire_table_echange(self):
        all_client = Echanges.extraire_tous_echanges_pharma(self.main_interface.conn,self.pharma['ID'])
        self.list_client.setRowCount(len(all_client))
        for index, element in enumerate(all_client):
            self.list_client.setItem(index, 0, QTableWidgetItem(str(element["id_facture"])))
            self.list_client.setItem(index, 1, QTableWidgetItem(str(element["date_echange"])))
            self.list_client.setItem(
                index, 2, QTableWidgetItem(str(element["total_facture"]))
            )
            sens = "Envoyer" if int(element["sens"]) == 1 else "Reçu"
            self.list_client.setItem(index, 3, QTableWidgetItem(sens))
            salarie = Salaries.extraire_salarie(self.main_interface.conn,element["id_salarie"])
            self.list_client.setItem(
                index, 4, QTableWidgetItem(str(salarie['nom'] + " "+ salarie['prenom']))
            ) 





    def show_principal_interface_recus(self):
        self.main_interface.clear_content_frame()
        self.main_interface.keyPressEvent = self.keyPressEvent_recu
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
        self.medicament_code.setValidator(int_validator)
        self.medicament_code.setPlaceholderText("Scanner medicament")



        table_form_layout.addWidget(QLabel("Nom de pharma :"), 0, 0)
        table_form_layout.addWidget(self.name_pharma, 0, 1)
        

        

        code_barre = QLabel("Code EAN 13 :")
        self.code_barre_value_ajout = QLineEdit()
        self.code_barre_value_ajout.setValidator(int_validator)
        self.code_barre_value_ajout.setPlaceholderText(" Scanner Code EAN 13")
        self.code_barre_value_ajout.setEnabled(False)

        quantite_commender = QLabel("Quantité")
        self.quantite_commender_value_ajout = QLineEdit()
        self.quantite_commender_value_ajout.setValidator(int_validator)
        self.quantite_commender_value_ajout.setPlaceholderText("Quantité commender")
        self.prix_achat_medicament_ajout = QLineEdit()
        self.prix_achat_medicament_ajout.setValidator(float_validator)
        self.prix_achat_medicament_ajout.setPlaceholderText("Prix d'achat")
        self.prix_vente_medicament_ajout = QLineEdit()
        self.prix_vente_medicament_ajout.setValidator(float_validator)
        self.prix_vente_medicament_ajout.setPlaceholderText("Prix de vente")
        self.prix_cons_medicament_ajout = QLineEdit()
        self.prix_cons_medicament_ajout.setValidator(float_validator)
        self.prix_cons_medicament_ajout.setPlaceholderText("Prix de consommation")
        self.date_expiration_medicament_ajout = QDateEdit()
        self.date_expiration_medicament_ajout.setCalendarPopup(True)
        self.date_expiration_medicament_ajout.setDate(QDate.currentDate().addYears(2))
        self.quantite_minimal_medicament_ajout = QLineEdit()
        self.quantite_minimal_medicament_ajout.setPlaceholderText("Quantité minimal")
        self.quantite_minimal_medicament_ajout.setValidator(int_validator)



        table_form_layout.addWidget(code_barre, 1, 0)
        table_form_layout.addWidget(
            self.code_barre_value_ajout, 1, 1
        )
        
        
        table_form_layout.addWidget(QLabel("Quantité minimale :"), 2, 0)
        table_form_layout.addWidget(
            self.quantite_minimal_medicament_ajout, 2, 1
        )
        table_form_layout.addWidget(quantite_commender, 3, 0)
        table_form_layout.addWidget(
            self.quantite_commender_value_ajout, 3, 1
        )
        table_form_layout.addWidget(QLabel("Date d'expiration :"), 4, 0)
        table_form_layout.addWidget(
            self.date_expiration_medicament_ajout, 4, 1
        )

        # Ajout des labels et des champs dans le layout
        table_form_layout.addWidget(QLabel("Prix d'achat :"), 5, 0)
        table_form_layout.addWidget(self.prix_achat_medicament_ajout, 5, 1)

        table_form_layout.addWidget(QLabel("Prix de vente :"), 6, 0)
        table_form_layout.addWidget(self.prix_vente_medicament_ajout, 6, 1)

        self.confirm_button_ajout = QPushButton("Confirmer l'ajout")
        self.confirm_button_ajout.clicked.connect(self.confirmation_ajout_seul)

        table_form_layout.addWidget(self.confirm_button_ajout, 7, 1)
 
 
 

        main_layout.addLayout(table_form_layout)

 

        self.list_client = QTableWidget(0, 7)
        self.list_client.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_client.setHorizontalHeaderLabels(
            ["ID","Nom", "Téléphone", "Email", "Adresse",  "Total envoyer", "Total reçu"]
        )
        self.remplire_table()
        main_layout.addWidget(self.list_client)
        

        self.main_interface.content_layout.addWidget(self.vente_dash)

    

    def confirmation_ajout_seul(self):

        if self.medicament_search is None:
            QMessageBox.warning(
                self.main_interface, "Erreur", "Veuillez selectionner un medicament"
            )
            return

        quantite_commender_value = self.quantite_commender_value_ajout.text()

        quantite_minimal_medicament = self.quantite_minimal_medicament_ajout.text()
        date_expiration_medicament = (
            self.date_expiration_medicament_ajout.date().toString("yyyy-MM-dd")
        ) 
        prix_achat_medicament = self.prix_achat_medicament_ajout.text()
        prix_vente_medicament = self.prix_vente_medicament_ajout.text()
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        reply = QMessageBox.question(
            self.main_interface,
            "Confirmation de l'échange",
            "Confirmer l'ajout ?",
            QMessageBox.Yes,
            QMessageBox.Cancel,
        )
        if reply == QMessageBox.Yes:
            Stock.ajouter_stock(self.main_interface.conn,
                self.medicament_search["id_medicament"],
                "0",
                self.main_interface.user_session["id_salarie"],
                prix_achat_medicament,
                prix_vente_medicament,
                prix_vente_medicament,
                now,
                date_expiration_medicament,
                quantite_commender_value,
                quantite_commender_value,
                quantite_minimal_medicament,
                0,
                now,
                now,
            )
            pharma = Pharmacies.extraire_pharma_nom(self.main_interface.conn,self.name_pharma.text().split("_")[0])
            id_salarie = self.main_interface.user_session["id_salarie"]
            Echanges.ajouter_echange(self.main_interface.conn,
                            pharma["id_pharmacie"],
                            0,
                            now,
                            float(prix_achat_medicament) * float(quantite_commender_value),
                            0,
                            id_salarie,
                        )
            
            # Effacer les éléments
            self.name_pharma.clear()
            self.code_barre_value_ajout.clear()
            self.quantite_commender_value_ajout.clear()
            self.prix_achat_medicament_ajout.clear()
            self.prix_vente_medicament_ajout.clear()
            self.prix_cons_medicament_ajout.clear()
            self.quantite_minimal_medicament_ajout.clear()
            self.medicament_search = None
            self.commande_current = None
        else:
            # Annuler l'ajout
            pass

    def confirm_echange_pharma(self):
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        numero_facture = int(now.timestamp())
        id_salarie = self.main_interface.user_session["id_salarie"]

        if self.producs_table.empty:
            QMessageBox.information(
                self.main_interface,
                "Aucun medicament",
                "Aucun medicament n'a été ajouté",
            )
            return
        if self.name_pharma.text() == "":
            QMessageBox.information(
                self.main_interface,
                "Aucune pharmacie",
                "Aucune pharmacie n'a été sélectionnée",
            )
            return
        pharma = Pharmacies.extraire_pharma_nom(self.main_interface.conn,self.name_pharma.text().split("_")[0])
        if pharma is None:
            QMessageBox.information(
                self.main_interface, "Pharmacie non trouvée", "Pharmacie non trouvée"
            )
            return
        pharma = dict(pharma)
        evoyer = 1
        #recu = self.recevoir_checkbox.isChecked()

        message = "Pharmacie Hajra\n"
        message += "Adresse : 123, Rue Exemple, Ville, Pays\n"
        message += "Téléphone : +212 123 456 789\n"
        message += "Bonjour,\n"
        message += "Facture n°: " + str(numero_facture) + "\n"
        message += (
            "Agent : " + str(self.main_interface.user_session["id_salarie"]) + "\n"
        )
        message += "----------------------------------------\n"
        message += "Détails de l'échange:\n"
        message += "Pharmacie : " + self.name_pharma.text() + "\n" 
        message += "----------------------------------------\n"
        message += "Produit\t\tQuantité\tPrix unitaire\tPrix total\n"
        message += "----------------------------------------\n"
        total_facture = 0
        for index, items in self.producs_table.iterrows():
            quantite_vendue = items["Quantite"]
            quantite_traiter = 0
            for prix_achat_item, quanti in zip(
                items["prix_achat"], items["list_quantity"]
            ):
                quanti_rest_to_hand = quantite_vendue - quantite_traiter
                if quanti_rest_to_hand <= quanti:
                    message += f"{items['Code_EAN_13']}\t\t{quanti_rest_to_hand}\t\t{prix_achat_item} Dh\t\t{quanti_rest_to_hand*prix_achat_item} Dh\n"
                    total_facture += quanti_rest_to_hand * prix_achat_item
                    quantite_traiter += quanti_rest_to_hand
                else:
                    quantite_traiter += quanti
                    message += f"{items['Code_EAN_13']}\t\t{quanti}\t\t{prix_achat_item} Dh\t\t{quanti*prix_achat_item} Dh\n"
                    total_facture += quanti * prix_achat_item
                if quantite_traiter >= quantite_vendue:
                    break

        message += "Total facture : " + str(total_facture) + " Dh\n"
        message += "----------------------------------------\n"
        message += "Merci pour votre échange!\n"
        message += "Date: " + now_str + "\n"

        self.producs_table.reset_index(drop=True)
        reply = QMessageBox.question(
            self.main_interface,
            "Confirmation de l'échange",
            message,
            QMessageBox.Yes,
            QMessageBox.Cancel,
        )
        if reply == QMessageBox.Yes:
            for index, items in self.producs_table.iterrows():
                id_medicament = items["id_medicament"]
                id_commande_entre = items["id_commande"]
                prix_achat = items["prix_achat"]
                prix_v = items["prix_vente"]
                prix_vente = items["PPV"]
                date_vente = now_str
                quantite_vendue = items["Quantite"]
                quantite_list = items["list_quantity"]
                total_facture = items["Prix_total"]
                ID_Stock = items["id_stock"]
                quantite_traiter = 0
                self.total_facture = 0
                for (
                    idcommande_item,
                    prix_achat_item,
                    prix_vente_item,
                    ID_Stock_item,
                    quanti,
                ) in zip(
                    id_commande_entre, prix_achat, prix_v, ID_Stock, quantite_list
                ):
                    quanti_rest_to_hand = quantite_vendue - quantite_traiter
                    
                    if quanti_rest_to_hand <= quanti:
                        
                        Stock.effectuer_vente_stock(self.main_interface.conn,ID_Stock_item, quanti_rest_to_hand)
                        Medicament.effectuer_vente_medicament(self.main_interface.conn,id_medicament, quanti_rest_to_hand)
                        Echanges.ajouter_echange(self.main_interface.conn,
                            pharma["id_pharmacie"],
                            numero_facture,
                            date_vente,
                            quanti_rest_to_hand * prix_achat_item,
                            evoyer,
                            id_salarie,
                        )
                        self.total_facture += quanti_rest_to_hand * prix_achat_item
                        quantite_traiter += quanti_rest_to_hand
                    else:
                        quantite_traiter += quanti
                        
                    
                        Stock.effectuer_vente_stock(self.main_interface.conn,ID_Stock_item, quanti)
                        Medicament.effectuer_vente_medicament(self.main_interface.conn,id_medicament, quanti)
                        Echanges.ajouter_echange(self.main_interface.conn,
                            pharma["id_pharmacie"],
                            numero_facture,
                            date_vente,
                            quanti * prix_achat_item,
                            evoyer,
                            id_salarie,
                        )
                        self.total_facture += quanti * prix_achat_item
                    if quantite_traiter >= quantite_vendue:
                        break
            QMessageBox.information(
                self.main_interface, "Echange effectué", "Echange effectué avec succès"
            )
            self.name_pharma.clear()
            self.producs_table = pd.DataFrame()
            self.update_table()

    def envoyer(self, state):
        if state == 2:
            self.recevoir_checkbox.setChecked(False)

    def recevoir(self, state):
        if state == 2:
            self.envoyer_checkbox.setChecked(False)

    def OntextChangepharma(self, text):
        if len(text) >= 3:
            self.updateCompleter_pharma(text)

    def updateCompleter_pharma(self, text):
        results = Pharmacies.extraire_pharma_nom_like(self.main_interface.conn,text)
        results = [res["nom"] for res in results]
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
        self.telephone_input.setValidator(phone_validator)
        self.telephone_input.setPlaceholderText("Téléphone")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Adresse")

        # Créer un bouton pour soumettre le formulaire
        self.submit_button = QPushButton("Ajouter Pharmacie")
        self.submit_button.clicked.connect(self.add_pharma)

        table_form_layout.addWidget(QLabel("Nom :"), 0, 0)
        table_form_layout.addWidget(self.name_input, 0, 1)
        table_form_layout.addWidget(QLabel("Téléphone :"), 0, 2)
        table_form_layout.addWidget(self.telephone_input, 0, 3)
        table_form_layout.addWidget(QLabel("Email :"), 1, 0)
        table_form_layout.addWidget(self.email_input, 1, 1)
        table_form_layout.addWidget(QLabel("Adresse :"), 1, 2)
        table_form_layout.addWidget(self.address_input, 1, 3)
        table_form_layout.addWidget(self.submit_button, 2, 3)

        main_layout.addLayout(table_form_layout)

        self.list_client = QTableWidget(0, 7)
        self.list_client.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_client.setHorizontalHeaderLabels(
            ["ID","Nom", "Téléphone", "Email", "Adresse", "Total envoyer", "Total reçu"]
        )
        self.remplire_table()
        self.list_client.cellClicked.connect(self.on_cell_clicked_pharma)
        main_layout.addWidget(self.list_client)

        self.main_interface.content_layout.addWidget(self.vente_dash)
    def on_cell_clicked_pharma(self, row, column):
        # Si la colonne 12 (Action) est cliquée

        self.pharma={
            "ID" : self.list_client.item(row, 0).text(),
            "Nom" : self.list_client.item(row, 1).text(),
            "Téléphone" : self.list_client.item(row, 2).text(),
            "Email" : self.list_client.item(row, 3).text(),
            "Adresse" : self.list_client.item(row, 4).text(),
            "Out_value" : self.list_client.item(row, 5).text(),
            "In_value" : self.list_client.item(row, 6).text(),
        }
        self.show_principal_interface_list()
        

    def remplire_table(self):
        all_client = Pharmacies.extraire_tous_pharma(self.main_interface.conn)
        self.list_client.setRowCount(len(all_client))
        for index, element in enumerate(all_client):
            self.list_client.setItem(index, 0, QTableWidgetItem(str(element["id_pharmacie"])))
            self.list_client.setItem(index, 1, QTableWidgetItem(str(element["nom"])))
            self.list_client.setItem(
                index, 2, QTableWidgetItem(str(element["telephone"]))
            )
            self.list_client.setItem(index, 3, QTableWidgetItem(str(element["email"])))
            self.list_client.setItem(
                index, 4, QTableWidgetItem(str(element["adresse"]))
            )
            self.list_client.setItem(
                index, 5, QTableWidgetItem(str(element["outvalue"]))
            )
            self.list_client.setItem(
                index, 6, QTableWidgetItem(str(element["invalue"]))
            )

    def add_pharma(self):
        # Récupérer les valeurs des champs
        name = self.name_input.text()
        telephone = self.telephone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        # Ici vous pouvez ajouter le client dans une base de données ou autre logique
        Pharmacies.ajouter_pharmacie(self.main_interface.conn,name, address, telephone, email, 0, 0)
        self.remplire_table()
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
        try:
            key = event.text()
            current_time = time.time()
            if current_time - self.last_key_time < self.barcode_delay_threshold:
                code_b = True
            self.last_key_time = current_time
            if key == "\r" and code_b:  # Lorsque le lecteur envoie un saut de ligne
                self.code_barre_scanner = self.process_barcode(self.code_barre_scanner)
                if self.code_barre_scanner != "":
                    self.add_medicament_to_echange(self.code_barre_scanner)
                    self.code_barre_scanner = ""  # Réinitialiser pour le prochain scan
            else:
                self.code_barre_scanner += key  # Ajouter le caractère au code en cours
        except:
            print("Erreur")

    def add_medicament_to_echange(self, code_barre_scanner):
        if (
            not self.producs_table.empty
            and code_barre_scanner in self.producs_table["Code_EAN_13"].values
        ):
            self.producs_table.loc[
                self.producs_table["Code_EAN_13"] == code_barre_scanner, "Quantite"
            ] += 1
            self.update_table()
        else:
            medicament = Medicament.extraire_medicament_code_barre(self.main_interface.conn,code_barre_scanner)
            if medicament is None:
                QMessageBox.information(
                    self.main_interface,
                    "Medicament non reconue",
                    "Medicament non reconue",
                )
                return
            else:
                medicament_on_dtock = Stock.extraire_medicament_id_stock(self.main_interface.conn,
                    medicament["id_medicament"]
                )
                medicament = dict(medicament)

                if medicament_on_dtock is None:
                    QMessageBox.information(
                        self.main_interface,
                        "Stock vide",
                        "Le stock de ce médicament est vide. Veuillez vérifier la disponibilité.",
                    )
                else:
                    if len(np.unique(medicament_on_dtock["prix_vente"])) > 1:
                        QMessageBox.information(
                            self.main_interface,
                            "Atention le prix de ce medicament à changer",
                            "Atention le prix de ce medicament à changer, Merci de séparer les facture en cas de quantité superieur a 1",
                        )

                    medicament["Quantite"] = 1
                    medicament["PPV"] = medicament_on_dtock[
                        "prix_achat"
                    ][0]
                    medicament["prix_vente"] = medicament_on_dtock["prix_vente"]
                    medicament["date_expiration"] = medicament_on_dtock[
                        "date_expiration"
                    ][0]
                    medicament["quantite_actuelle"] = medicament["Stock_Actuel"]
                    medicament["id_commande"] = medicament_on_dtock["id_commande"]
                    medicament["list_quantity"] = medicament_on_dtock["list_quantity"]
                    medicament["prix_achat"] = medicament_on_dtock["prix_achat"]
                    medicament["id_stock"] = medicament_on_dtock["id_stock"]
                    medicament["Prix_total"] = (
                        medicament["Quantite"] * medicament["prix_achat"]
                    )
                    df = pd.DataFrame([medicament])
                    if self.producs_table.empty:
                        self.producs_table = df
                    else:
                        self.producs_table = pd.concat(
                            [self.producs_table, df], ignore_index=True
                        )
                    self.producs_table["Prix_total"] = self.producs_table[
                        "Prix_total"
                    ].round(2)
                    self.update_table()

    def update_table(self):
        self.list_medicaments.setRowCount(len(self.producs_table))
        for row, product in self.producs_table.iterrows():
            self.list_medicaments.setItem(
                row, 0, QTableWidgetItem(str(product["Code_EAN_13"]))
            )
            self.list_medicaments.setItem(row, 1, QTableWidgetItem(str(product["Nom"])))
            line_edit = QSpinBox()
            line_edit.setValue(product["Quantite"])
            line_edit.editingFinished.connect(
                lambda row=row: self.update_quantity(row, line_edit.text())
            )
            self.list_medicaments.setCellWidget(row, 2, line_edit)
            self.list_medicaments.setItem(
                row, 3, QTableWidgetItem(str(product["prix_achat"][0]))
            )

    def update_quantity(self, row, new_value):
        new_quantity = int(new_value)
        self.producs_table.loc[row, "Quantite"] = new_quantity
        self.update_table()



    def keyPressEvent_recu(self, event):
        try:
            key = event.text()
            current_time = time.time()
            if current_time - self.last_key_time < self.barcode_delay_threshold:
                code_b = True
            else:
                code_b = False
            self.last_key_time = current_time
            if key == "\r" and code_b:  # Lorsque le lecteur envoie un saut de ligne
                self.code_barre_scanner = self.process_barcode(self.code_barre_scanner)
                if self.code_barre_scanner != "":
                    self.code_barre_value_ajout.setText(self.code_barre_scanner)
                    self.remplir_medicament_cases(self.code_barre_scanner)
                    self.code_barre_scanner = ""  # Réinitialiser pour le prochain scan
            else:
                self.code_barre_scanner += key  # Ajouter le caractère au code en cours
        except:
            print("erreur")

    def remplir_medicament_cases(self, code_barre_scanner):
        self.medicament_search = Medicament.extraire_medicament_code_barre(self.main_interface.conn,
            code_barre_scanner
        )
        if self.medicament_search is None:
            QMessageBox.warning(
                self.main_interface,
                "Erreur",
                "Le medicament n'exsiste pas, voulez vous l'ajouter ?",
            )
        else:
            self.medicament_search = dict(self.medicament_search)
            print(self.medicament_search)
            
