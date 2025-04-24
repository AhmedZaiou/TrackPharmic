from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCompleter,
    QSpinBox,
    QHeaderView,
    QMessageBox,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
)
from qtpy.QtCore import Qt, QStringListModel
from Backend.Dataset.medicament import Medicament
from Backend.Dataset.stock import Stock
from Backend.Dataset.ventes import Ventes
from Backend.Dataset.credit import Credit

from Backend.Dataset.client import Clients
from Backend.Dataset.commande_client import CommandeClient
from Frontend.utils.utils import *
from decimal import Decimal

from datetime import datetime

import pandas as pd
import numpy as np
import time
from io import BytesIO
import base64

import tempfile
import os
from xhtml2pdf import pisa
import barcode
from barcode.writer import ImageWriter
from PIL import Image

import subprocess
sumatra_path = r"C:\Users\dikster\AppData\Local\SumatraPDF\SumatraPDF.exe"

if os.name == 'nt': 
    import win32api
    import win32print

class Vente_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()
        self.client_info = {
            "id_client": 0,
            "nom": "Anonyme",
            "prenom": "Anonyme",
            "cin": "Anonyme",
            "telephone": "06666666666",
            "email": "email@email.ext",
            "Adresse": "Anonyme",
            "max_credit": 0,
            "credit_actuel": 0,
        }
        self.list_od_commande = None
        self.producs_table = pd.DataFrame()
        self.last_key_time = time.time()
        self.barcode_delay_threshold = 0.1
        self.code_b = False

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

        # Section Client
        client_layout = QGridLayout()
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

        self.client_status_label = QLabel("None")
        self.client_cin_label = QLabel(" None")
        self.client_max_credit = QLabel(" None")
        self.client_credit_actuel = QLabel(" None")

        self.client_status_label_ = QLabel("Client : ")
        self.client_cin_label_ = QLabel("CIN : ")
        self.client_max_credit_ = QLabel("Max_credit : ")
        self.client_credit_actuel_ = QLabel("Credit Actuel : ")

        client_layout.addWidget(self.client_id_input, 0, 0)
        client_layout.addWidget(self.search_client_button, 0, 1)
        client_layout.addWidget(self.add_client_button, 0, 2)


        # section commande :
        self.label_commande = QLabel("Numéro commande : ")
        self.commande_id_input = QLineEdit() 
        self.commande_id_input.setPlaceholderText("Rechercher commande par ID")
        self.commande_id_input.setValidator(int_validator)
        self.commande_id_input.textChanged.connect(self.OntextChangeCommande)

        self.completer_commande = QCompleter()
        self.completer_commande.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_commande.setCompletionMode(QCompleter.PopupCompletion)
        self.commande_id_input.setCompleter(self.completer_commande)
        self.completer_commande.activated.connect(self.selectionner_Commande) 

        self.montant_facture_commande_label = QLabel("Montant facture : ")
        self.montant_facture_commande_value = QLabel("None")

        self.montant_payer_commande_label = QLabel("Montant payer : ")
        self.montant_payer_commande_value = QLabel("None")

        self.montant_rest_commande_label = QLabel("Montant rester : ")
        self.montant_rest_commande_value = QLabel("None")


        self.search_commande = QPushButton("Cherche commande")
        self.search_commande.clicked.connect(self.search_commande_button)

        commande_layout_tab = QGridLayout()
        commande_layout_tab.addWidget(self.label_commande, 0, 0)
        commande_layout_tab.addWidget(self.commande_id_input, 0, 1)
        commande_layout_tab.addWidget(self.search_commande, 0, 2)
        commande_layout_tab.addWidget(self.montant_facture_commande_label, 1, 0)
        commande_layout_tab.addWidget(self.montant_facture_commande_value, 1, 1)
        commande_layout_tab.addWidget(self.montant_facture_commande_label, 2, 0)
        commande_layout_tab.addWidget(self.montant_facture_commande_value, 2, 1)
        commande_layout_tab.addWidget(self.montant_payer_commande_label, 3, 0) 
        commande_layout_tab.addWidget(self.montant_payer_commande_value, 3, 1)
        commande_layout_tab.addWidget(self.montant_rest_commande_label, 4, 0)
        commande_layout_tab.addWidget(self.montant_rest_commande_value,4, 1) 

        # Zone d'entrée pour le code-barres
        barcode_layout = QHBoxLayout()
        self.barcode_input = QLineEdit()
        self.barcode_input.setValidator(int_validator)
        self.barcode_input.setPlaceholderText("Entrez le code-barres ou scannez ici")
        self.barcode_input.returnPressed.connect(self.process_barcode_manuel)

        self.add_to_cart_button = QPushButton("Ajouter au panier")
        self.add_to_cart_button.clicked.connect(self.ajouter_panier)
        barcode_layout.addWidget(self.barcode_input)
        barcode_layout.addWidget(self.add_to_cart_button)

        main_layout.addLayout(barcode_layout)
        # Liste des produits

        # Panier
        self.cart_table = QTableWidget(0, 8)
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.cart_table.setHorizontalHeaderLabels(
            [
                "Code EAN 13",
                "Nom",
                "Caractéristique",
                "Stock",
                "Prix unité",
                "Quantité",
                "Date d'expiration",
                "Prix total",
            ]
        )
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

        client_layout_tab = QGridLayout()
        client_layout_tab.addWidget(self.client_status_label_, 1, 0)
        client_layout_tab.addWidget(self.client_status_label, 1, 1)
        client_layout_tab.addWidget(self.client_cin_label_, 1, 2)
        client_layout_tab.addWidget(self.client_cin_label, 1, 3)
        client_layout_tab.addWidget(self.client_max_credit_, 2, 0)
        client_layout_tab.addWidget(self.client_max_credit, 2, 1)
        client_layout_tab.addWidget(self.client_credit_actuel_, 2, 2)
        client_layout_tab.addWidget(self.client_credit_actuel, 2, 3)





        aditional_information  = QHBoxLayout()
        main_layout.addLayout(client_layout)
        aditional_information.addLayout(client_layout_tab, 1)
        aditional_information.addLayout(commande_layout_tab, 1)
        main_layout.addLayout(aditional_information)

        # Paiement
        payment_layout = QHBoxLayout()
        self.checkbox = QCheckBox("Crédit ?", self.main_interface)
        self.checkbox.stateChanged.connect(self.toggle_inputs)

        payment_layout.addWidget(self.checkbox)
        # Montant à payer
        self.amount_input = QLineEdit()
        self.amount_input.setValidator(float_validator)
        self.amount_input.setPlaceholderText("Montant à payer maintenant")
        payment_layout.addWidget(self.amount_input)
 
        self.toggle_inputs()

        # Bouton pour annuler

        main_layout.addLayout(payment_layout)

        button_layout = QHBoxLayout()

        # Actions
        self.confirm_button = QPushButton("Confirmer la vente")
        button_layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.cancel_sale)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

        # Assign layout to central widget
        self.main_interface.content_layout.addWidget(self.vente_dash)

        # Connecter les signaux
        self.confirm_button.clicked.connect(self.confirm_sale)
    
    def search_commande_button(self, code_commande = None):
        if not code_commande: 
            code_commande = self.commande_id_input.text() 
        else:
            if len(code_commande) == 13:
                code_commande = code_commande[2:-1]          

        self.list_od_commande = CommandeClient.get_commande(code_commande) 
        self.commande_id_input.setText(code_commande)
        self.montant_facture_commande_value.setText(str(self.list_od_commande[0]['total_facture_calculer']))
        self.montant_payer_commande_value.setText(str(self.list_od_commande[0]['to_pay_now']))
        self.montant_rest_commande_value.setText(str(self.list_od_commande[0]['total_facture_calculer'] - self.list_od_commande[0]['to_pay_now']))
    
        

    def OntextChangeClient(self, text):
        if len(text) >= 3:
            self.updateCompleter_fournisseur(text)
    
    def OntextChangeCommande(self, text):
        if len(text) >= 3:
            self.updateCompleter_fournisseur(text)

    def updateCompleter_fournisseur(self, text):
        results = Clients.extraire_client_nom_like(text)
        results = ["_".join(res.values()) for res in results]
        model = QStringListModel(results)
        self.completer_client.setModel(model)

    def selectionner_client(self, text):
        print(text)
    
    def selectionner_Commande(self, text):
        print(text)

    def toggle_inputs(self):
        if self.checkbox.isChecked():
            if (
                self.client_info["nom"] == "Anonyme"
                and self.client_info["prenom"] == "Anonyme"
                and self.client_info["cin"] == "Anonyme"
            ):
                QMessageBox.information(
                    self.main_interface,
                    "Merci de choisire un client avant d'activer l'option credit",
                    "Merci de choisire un client avant d'activer l'option credit",
                )
                self.checkbox.setChecked(False)
            else:
                self.amount_input.setEnabled(True) 
        else:
            self.amount_input.setDisabled(True) 

    def search_client(self):
        client_id = self.client_id_input.text()
        if "_" not in client_id:
            self.client_status_label.setText("None")
            self.client_cin_label.setText("None")
            self.client_max_credit.setText("None")
            self.client_credit_actuel.setText("None")

            self.client_info = None
        else:
            nom, prenom, cin = client_id.split("_")
            self.client_info = Clients.extraire_client_info(nom, prenom, cin)
            self.client_status_label.setText(
                f"{self.client_info['nom']} {self.client_info['prenom']} "
            )
            self.client_cin_label.setText(f"{self.client_info['cin']}")
            self.client_max_credit.setText(f"{self.client_info['max_credit']} Dh")
            self.client_credit_actuel.setText(f"{self.client_info['credit_actuel']} Dh")

    def process_barcode(self, codebare):
        if len(codebare) >= 13:
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
            self.cart_table.setItem(
                row, 0, QTableWidgetItem(str(product["Code_EAN_13"]))
            )
            self.cart_table.setItem(row, 1, QTableWidgetItem(str(product["Nom"])))
            self.cart_table.setItem(
                row, 2, QTableWidgetItem(str(product["Caracteristique"]))
            )
            self.cart_table.setItem(
                row, 3, QTableWidgetItem(str(product["quantite_actuelle"]))
            )
            self.cart_table.setItem(
                row, 4, QTableWidgetItem(str(product["Prix_Public_de_Vente"]))
            )
            line_edit = QSpinBox()
            line_edit.setValue(product["Quantite"])
            line_edit.editingFinished.connect(
                lambda row=row: self.update_quantity(row, line_edit.text())
            )
            self.cart_table.setCellWidget(row, 5, line_edit)
            self.cart_table.setItem(
                row, 6, QTableWidgetItem(str(product["date_expiration"]))
            )
            self.cart_table.setItem(
                row, 7, QTableWidgetItem(str(product["Prix_total"]))
            )

        self.subtotal_label.setText(
            f"Sous-total : {self.producs_table['Prix_total'].sum()} Dh"
        )
        self.total_label.setText(
            f"<b>Total : {self.producs_table['Prix_total'].sum()} Dh</b>"
        )

        self.barcode_input.clear()

    def update_quantity(self, row, new_value):
        new_quantity = int(new_value)
        self.producs_table.loc[row, "Quantite"] = new_quantity
        self.producs_table.loc[row, "Prix_total"] = (
            new_quantity * self.producs_table.loc[row, "Prix_Public_de_Vente"]
        )
        self.producs_table = self.producs_table[self.producs_table["Quantite"] != 0]
        self.update_table()

    def add_medicament_to_vente(self, code_barre_scanner):
        if (
            not self.producs_table.empty
            and code_barre_scanner in self.producs_table["Code_EAN_13"].values
        ):
            self.producs_table.loc[
                self.producs_table["Code_EAN_13"] == code_barre_scanner, "Quantite"
            ] += 1
            self.producs_table.loc[
                self.producs_table["Code_EAN_13"] == code_barre_scanner, "Prix_total"
            ] += self.producs_table.loc[
                self.producs_table["Code_EAN_13"] == code_barre_scanner,
                "Prix_Public_de_Vente",
            ]
            self.update_table()
        else:
            medicament = Medicament.extraire_medicament_code_barre(code_barre_scanner)

            if medicament is None:
                QMessageBox.information(
                    self.main_interface,
                    "Medicament non reconue",
                    "Medicament non reconue",
                )
                return
            else:
                medicament_on_dtock = Stock.extraire_medicament_id_stock(
                    medicament["ID_Medicament"]
                ) 

                if medicament_on_dtock is None:
                    message = (
                                f"<div style='border: 1px solid red; padding: 15px; border-radius: 8px;'>"
                                f"<h2 style='color: red;'>Attention : le stock du médicament '{medicament['Nom']}' est épuisé.</h2>"
                                f"<p><strong>Caractéristiques :</strong> {medicament['Caracteristique']}</p>"
                                f"<p><strong>Prix public :</strong> {medicament['Prix_Public_De_Vente']} MAD</p>"
                                f"<p>Veuillez vérifier la disponibilité. Vous pouvez passer une commande depuis la section <strong>'Commandes'</strong>.</p>"
                                f"</div>"
                            )
                    QMessageBox.information(
                        self.main_interface,
                        "Stock vide",
                        message,   
                    )
                else:
                    if len(np.unique(medicament_on_dtock["prix_vente"])) > 1:
                        QMessageBox.information(
                            self.main_interface,
                            "Atention le prix de ce medicament à changer",
                            "Atention le prix de ce medicament à changer, Merci de séparer les facture en cas de quantité superieur a 1",
                        )

                    medicament["Quantite"] = 1
                    medicament["Prix_Public_de_Vente"] = medicament_on_dtock[
                        "prix_vente"
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
                        medicament["Quantite"] * medicament["Prix_Public_de_Vente"]
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

    def keyPressEvent(self, event):
        try:
            key = event.text()
            current_time = time.time()
            if current_time - self.last_key_time < self.barcode_delay_threshold:
                self.code_b = True
            self.last_key_time = current_time
            if key == "\r" and self.code_b:  # Lorsque le lecteur envoie un saut de ligne
                self.code_barre_scanner = self.process_barcode(self.code_barre_scanner)
                if self.code_barre_scanner != "" and   self.code_barre_scanner[:2] == "10":
                    self.search_commande_button(self.code_barre_scanner)
                elif self.code_barre_scanner != "" :
                    self.add_medicament_to_vente(self.code_barre_scanner)
                    self.code_barre_scanner = ""  # Réinitialiser pour le prochain scan
                self.code_b = False
            else:
                self.code_barre_scanner += key  # Ajouter le caractère au code en cours
        except:
            print('Erreur')

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
        reply = QMessageBox.question(
            self.main_interface,
            "Annulation de vente",
            "Êtes-vous sûr de vouloir annuler la vente ?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            QMessageBox.information(
                self.main_interface,
                "Annulation de vente",
                "La vente a été annulée avec succès.",
            )
            self.main_interface = Vente_dash(self.main_interface)

    def generate_barcode(self, barcode_data): 
        options = {
        'module_width': 200 / 1000,  # Adjust module width (barcode thickness)
        'module_height':2.5,  # Barcode height
        'font_size': 3,  # Font size for the label (you can adjust this)
        'text_distance': 2,  # Distance between the barcode and text
        'quiet_zone': 1,  # Quiet zone (padding) around the barcode
        } 
        barcode_format = barcode.get_barcode_class('EAN13')  # Barcode format (EAN13 in this case)
        barcode_instance = barcode_format(barcode_data, writer=ImageWriter())

        # Save the barcode as an image file
        barcode_image = barcode_instance.render(options)  # Generate the barcode image
        # Save the barcode to a BytesIO object 

        # Resize the image  
        buffered = BytesIO()
        barcode_image.save(buffered, format="PNG")
        # Convert the image to base64
        barcode_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return barcode_base64

    def confirm_sale(self):
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        id_client = 0 if self.client_info is None else self.client_info["id_client"]
        numero_facture = int(now.timestamp())
        
        id_salarie = self.main_interface.user_session["id_salarie"]
 
        if self.producs_table.empty :
            QMessageBox.warning(
                self.main_interface,
                "Erreur",
                "Le panier est vide.",
            )
            return
        
        message = f"""
            <!DOCTYPE html>
            <html>
            <body>
                <h2>RACHAD TAZA</h2>
                <p><strong>Adresse :</strong> Hay Rachad, Bloc2, n:75, Taza</p>
                <p><strong>Téléphone :</strong> 0535285298, 0680061368</p>  
                <p>Facture n°: {numero_facture}</p>
                <p><strong>Agent :</strong> {self.main_interface.user_session['id_salarie']}</p>
                <hr>
                """
        
        if self.client_info['nom'] != "Anonyme":
            message += f"""
                    <h4>Client:</h4>
                    <p><strong>Nom :</strong> {self.client_info['nom']} {self.client_info['prenom']}</p>
                    <p><strong>CIN :</strong> {self.client_info['cin']}</p>
                    <p><strong>Crédit Actuel :</strong> {self.client_info['credit_actuel']} Dh</p>
                    """
        message  += "<h4>Détails de la vente:</h4>"
        list_facture = []
        for index, items in self.producs_table.iterrows():
                id_medicament = items["ID_Medicament"]
                nom_medicament = items["Nom"]
                id_commande_entre = items["id_commande"]
                prix_achat = items["prix_achat"]
                prix_v = items["prix_vente"]
                prix_vente = items["Prix_Public_de_Vente"]
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
                        list_facture.append([items['Code_EAN_13'],
                            id_medicament,
                            idcommande_item,
                            prix_achat_item,
                            prix_vente_item,
                            date_vente,
                            quanti_rest_to_hand,
                            id_client,
                            numero_facture,
                            id_salarie,
                            ID_Stock_item, 
                            nom_medicament]
                        )
                        
                        self.total_facture += prix_vente_item * quanti_rest_to_hand
                        quantite_traiter += quanti_rest_to_hand
                    else:
                        quantite_traiter += quanti
                        list_facture.append([items['Code_EAN_13'],
                            id_medicament,
                            idcommande_item,
                            prix_achat_item,
                            prix_vente_item,
                            date_vente,
                            quanti,
                            id_client,
                            numero_facture,
                            id_salarie,
                            ID_Stock_item,
                            nom_medicament]
                        )
                        
                        self.total_facture += prix_vente_item * quanti
                    if quantite_traiter >= quantite_vendue:
                        break

        total_facture_calculer = 0 if self.list_od_commande is None or len(self.list_od_commande)==0 else -float(self.list_od_commande[0]['to_pay_now'])

        message+= "<hr>"
        
        for item in list_facture: 
            message  += f"{item[-1]} <br>"
            message += f"{item[0]}   &nbsp;&nbsp; {item[6]} x  &nbsp;&nbsp; {item[4]} Dh <br><br>"
            total_facture_calculer += round(float(item[4]*item[6] ), 2)
        
        if self.checkbox.isChecked():
            to_pay_now = round(float(self.amount_input.text()), 2)
        else:
            to_pay_now = round(float(total_facture_calculer), 2)  
        if (
            float(total_facture_calculer) - float(to_pay_now) + float(self.client_info["credit_actuel"])
            > float(self.client_info["max_credit"])
        ):
            QMessageBox.information(
                self.main_interface,
                "Credit insuffisant",
                "Pas possible de faire cette vente, le credit du client est insuffisant",
            )
            return

        self.producs_table.reset_index(drop=True)
        
        barcode_data = f'{matricul_pharma}{numero_facture}0'
        
        image_base64 = self.generate_barcode(barcode_data)
        if self.list_od_commande is not None:
            message +=  f""" 
                    <p><strong> Commande N°::</strong> {self.list_od_commande[0]['numero_facture']}</p>
                    <p><strong>Montant payé :</strong> {round(float(self.list_od_commande[0]['to_pay_now']),2)} Dh</p>

                    """
        message +=  f""" 

                <hr>

                <p><strong>Total facture :</strong> {round(float(total_facture_calculer),2)} Dh</p>
                <p><strong>Montant payé :</strong> {round(float(to_pay_now),2)} Dh</p>
                <p><strong>Reste à payer :</strong> {round(float(total_facture_calculer - to_pay_now),2)} Dh</p>
                <hr>
                <p><img src="data:image/png;base64,{image_base64}" alt="Logo" style="max-width:10px;max-height:15px;"></p>
                <p><em>Merci pour votre achat!</em></p>
                <p><strong>Date :</strong> {now_str}</p>
            </body>
            </html>
            """

        
        reply =  confirm_sale(self.main_interface,"Confirmation de vente", message )
        if reply == QMessageBox.Yes:
            for  items in list_facture:
                total = self.ajouter_vente_with_all_operation(
                            items[1],
                            items[2],
                            items[3],
                            items[4],
                            items[5],
                            items[6],
                            items[7],
                            items[8],
                            items[9],
                            items[10],
                        )

            if self.checkbox.isChecked():
                to_pay_now = self.amount_input.text()
                self.ajouter_credit_with_all_operation(
                    id_client,
                    numero_facture,
                    to_pay_now,
                    total_facture_calculer,
                    now_str,
                    "in progresse",
                    id_salarie,
                )
            self.print_ticket(message)

            QMessageBox.information(
                self.main_interface,
                "Confirmation de vente",
                "Vente confirmée avec succès!",
            )
            self.commande_id_input.clear()
            self.montant_facture_commande_value.setText("")
            self.montant_payer_commande_value.setText("")
            self.montant_rest_commande_value.setText("")
            

            self.client_id_input.clear()
            self.barcode_input.clear()
            self.cart_table.clearContents()
            self.cart_table.setRowCount(0)
            self.subtotal_label.setText("Sous-total : 0 Dh")
            self.tax_label.setText("Taxes : 0 Dh")
            self.total_label.setText("<b>Total : 0 Dh</b>")
            self.checkbox.setChecked(False)
            self.amount_input.clear() 
            self.producs_table = pd.DataFrame()
    
    def print_ticket(self, message_html):
        print("Conversion du ticket HTML en PDF...")
        pdf_path = "output.pdf"

        with open("output.pdf", "w+b") as f:
            pisa.CreatePDF(message_html, dest=f)
        
        if os.name == 'nt':  # 'nt' indique Windows 
            cmd = [sumatra_path, "-print-to-default", "-print-settings", "fit", pdf_path]
            subprocess.run(cmd, shell=False)

            #win32api.ShellExecute(0, "print", pdf_path, None, ".", 0)
        else:
            os.system(f"lp {pdf_path}")

    def ajouter_vente_with_all_operation(
        self,
        id_medicament,
        idcommande_item,
        prix_achat_item,
        prix_vente_item,
        date_vente,
        quanti,
        id_client,
        numero_facture,
        id_salarie,
        ID_Stock_item,
    ):
        if self.list_od_commande is not None:
            CommandeClient.modifier_statut_commande_client(
                self.list_od_commande[0]['numero_facture'], numero_facture
            )
        Ventes.ajouter_vente(
            id_medicament,
            idcommande_item,
            prix_achat_item,
            prix_vente_item,
            date_vente,
            quanti,
            quanti * prix_vente_item,
            id_client,
            numero_facture,
            id_salarie,
            ID_Stock_item,
        )
        Stock.effectuer_vente_stock(ID_Stock_item, quanti)
        Medicament.effectuer_vente_medicament(id_medicament, quanti)
        return quanti * prix_vente_item
        # todo : supprimer du stock

    def ajouter_credit_with_all_operation(
        self,
        id_client,
        numero_facture,
        to_pay_now,
        total_facture,
        now_str,
        status,
        id_salarie,
    ):
        Credit.ajouter_credit(
            id_client,
            numero_facture,
            to_pay_now,
            total_facture - int(to_pay_now),
            now_str,
            status,
            id_salarie,
        )
        Clients.ajouter_credit_client(id_client, total_facture - int(to_pay_now))
