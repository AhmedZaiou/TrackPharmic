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
from Backend.Dataset.commande_client import CommandeClient
from decimal import Decimal
from Backend.Dataset.client import Clients

from Frontend.utils.utils import *

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

if os.name == 'nt': 
    import win32api
    import win32print

class Commande_client:
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

        titre_page = QLabel("Commande Client")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titre_page)

        # Zone d'entrée pour le code-barres
        barcode_layout = QHBoxLayout()

        self.barcode_input = QLineEdit()
        self.barcode_input.setValidator(int_validator)
        self.barcode_input.setPlaceholderText("Entrez le code-barres ou scannez ici")
        self.barcode_input.returnPressed.connect(self.process_barcode_manuel)

        self.name_medicament_input = QLineEdit() 
        self.name_medicament_input.setPlaceholderText("Entrez le nom du medicament") 
        self.name_medicament_input.textChanged.connect(self.search_medicament)
        self.name_medicament_input.textChanged.connect(self.update_completer)

        self.completer_client = QCompleter()
        self.completer_client.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_client.setCompletionMode(QCompleter.PopupCompletion)
        self.name_medicament_input.setCompleter(self.completer_client)
        self.completer_client.activated.connect(self.selectionner_client)

        self.add_to_cart_button = QPushButton("Ajouter au panier")
        self.add_to_cart_button.clicked.connect(self.ajouter_panier)
        barcode_layout.addWidget(self.barcode_input)
        barcode_layout.addWidget(self.name_medicament_input)
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


        # Paiement
        payment_layout = QHBoxLayout()
        self.checkbox = QCheckBox("Ne payer qu'une partie ?", self.main_interface)
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


        # Connecter les signaux
        self.confirm_button.clicked.connect(self.confirm_sale)



        self.table = QTableWidget()
        self.table.setColumnCount(5)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(
            ["Numéro de facture", "Date de vente", "Total payé", "Total de la facture", "Réste à payer"] 
        )
        self.remplir_tableau()
        # Search bar for filtering
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Chercher par 'date'...")
        self.search_bar.textChanged.connect(self.filter_table)  # Trigger filter when text changes

        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.table)
        self.table.cellClicked.connect(self.show_facture)

        # Assign layout to central widget
        self.main_interface.content_layout.addWidget(self.vente_dash)
    
    def show_facture(self, row, column):
        numero_facture = self.table.item(row, 0).text() 
        commande = CommandeClient.get_commande(numero_facture) 

        message = f"""
            <!DOCTYPE html>
            <html>
            <body>
                <h2>RACHAD TAZA</h2>
                <p><strong>Adresse :</strong> Hay Rachad, Bloc2, n:75, Taza</p>
                <p><strong>Téléphone :</strong> 0535285298, 0680061368</p>  
                <p>Commande n°: {numero_facture}</p>
                <p><strong>Agent :</strong> {self.main_interface.user_session['id_salarie']}</p>
                <hr>
                """
        
        message += f"""

                <h4>Détails de la vente:</h4>
                <table border="1" cellspacing="0" cellpadding="5">
                <tr>
                    <th>Produit</th>
                    <th>Qu</th>
                    <th>PU</th>
                    <th>Total</th>
                </tr>"""

        total_facture_calculer = 0
        for  items in commande: 
                
                id_medicament = items["id_medicament"]
                nom_medicament = items["nom_medicament"] 
                prix_vente = items["prix_vente"]  # même chose
                date_vente = items["now_str"]
                quantite_vendue = items["quantite_vendue"]  
                to_pay_now = items["to_pay_now"]   
                message += f"<tr><td>{nom_medicament}</td><td>{prix_vente}</td><td>{quantite_vendue} Dh</td><td>{quantite_vendue*prix_vente} Dh</td></tr>"
                total_facture_calculer += quantite_vendue*prix_vente
        

        self.producs_table.reset_index(drop=True)
        
        barcode_data = f'{matricul_pharma}{numero_facture}0'
        
        image_base64 = self.generate_barcode(barcode_data)
        message +=  f"""
                </table>

                <p><strong>Total facture :</strong> {total_facture_calculer} Dh</p>
                <p><strong>Montant payé :</strong> {to_pay_now} Dh</p>
                <p><strong>Reste à payer :</strong> {total_facture_calculer - float(to_pay_now)} Dh</p>
                <hr>
                <p><img src="data:image/png;base64,{image_base64}" alt="Logo" style="max-width:10px;max-height:15px;"></p>
                <p><em>Merci pour votre achat!</em></p>
                <p><strong>Date :</strong> {date_vente}</p>
            </body>
            </html>
            """ 
        # Affichage
        QMessageBox.information(
            self.main_interface,
            "Crédit insuffisant",
            message
        )  


    def filter_table(self):
        #if not self.all_data:
        #    self.load_all_data()
        # Get the filter text from the search bar
        filter_text = self.search_bar.text().lower()

        # Loop through all rows and hide/show them based on the search
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)  # Assuming column 0 is 'Nom'
            if item is not None:
                if filter_text in item.text().lower():  # Case-insensitive comparison
                    self.table.setRowHidden(row, False)
                else:
                    self.table.setRowHidden(row, True) 

    def remplir_tableau(self):
        # Exemple de données fictives
        commandes = CommandeClient.get_all_commandes_client()

        self.table.setRowCount(len(commandes))
        for row, comm in enumerate(commandes):
            self.table.setItem(row, 0, QTableWidgetItem(comm["numero_facture"]))
            self.table.setItem(row, 1, QTableWidgetItem(comm["date_vente"].strftime("%d/%m/%Y %H:%M:%S")))
            self.table.setItem(row, 2, QTableWidgetItem(str(comm["to_pay_now"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(comm["total_facture_calculer"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(float(comm["total_facture_calculer"]) - float(comm["to_pay_now"])))) 
    
    def search_medicament(self, text):
        if len(text) >= 3:
            results = Medicament.extraire_medicament_nom_like(text) 
            list_res = []
            for res in results:
                list_res.append(f"{res['Nom']}, {res['Caracteristique']}, Prix : {res['Prix_Public_De_Vente']} Dh. {res['Code_EAN_13']}")  
            model = QStringListModel(list_res)
            self.completer_client.setModel(model)
    def update_completer(self, text):
        if "Prix :" in text and 'Dh.' in text:
            code_bare = text.split(' ')[-1]
            self.add_medicament_to_vente(code_bare)
            self.name_medicament_input.clear()



    def OntextChangeClient(self, text):
        if len(text) >= 3:
            self.updateCompleter_fournisseur(text)

    def updateCompleter_fournisseur(self, text):
        results = Clients.extraire_client_nom_like(text)
        results = ["_".join(res.values()) for res in results]
        model = QStringListModel(results)
        self.completer_client.setModel(model)

    def selectionner_client(self, text):
        print(text)

    def toggle_inputs(self):
        if self.checkbox.isChecked(): 
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
                row, 3, QTableWidgetItem(str(1))
            )
            self.cart_table.setItem(
                row, 4, QTableWidgetItem(str(product["Prix_Public_De_Vente"]))
            )
            line_edit = QSpinBox()
            line_edit.setValue(product["Quantite"])
            line_edit.editingFinished.connect(
                lambda row=row: self.update_quantity(row, line_edit.text())
            )
            self.cart_table.setCellWidget(row, 5, line_edit)
            self.cart_table.setItem(
                row, 6, QTableWidgetItem(str('En cours'))
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
            new_quantity * self.producs_table.loc[row, "Prix_Public_De_Vente"]
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
                "Prix_Public_De_Vente",
            ]
            self.update_table()
        else:
            medicament = Medicament.extraire_medicament_code_barre(code_barre_scanner)
            medicament["Quantite"] = 1
            medicament["Prix_total"] = medicament["Prix_Public_De_Vente"]
            
            if medicament is None:
                QMessageBox.information(
                    self.main_interface,
                    "Medicament non reconue",
                    "Medicament non reconue",
                )
                return
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
                if self.code_barre_scanner != "":
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
            self.main_interface = Commande_client(self.main_interface)

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
                <p>Commande n°: {numero_facture}</p>
                <p><strong>Agent :</strong> {self.main_interface.user_session['id_salarie']}</p>
                <hr>
                """
        
        if self.client_info['nom'] != "Anonyme":
            message += f"""
                    <h4>Client:</h4>
                    <p><strong>Nom :</strong> {self.client_info['nom']} {self.client_info['prenom']}</p>
                    <p><strong>CIN :</strong> {self.client_info['cin']}</p>
                    <p><strong>Crédit Actuel :</strong> {self.client_info['credit_actuel']} Dh</p>
                    <hr>
                    """
        message += f""" 
                <h4>Détails de la commande:</h4>
                """
        list_facture = []
        for index, items in self.producs_table.iterrows(): 
                
                id_medicament = items["ID_Medicament"]
                nom_medicament = items["Nom"]
                prix_achat = items["Prix_Hospitalier"]  # tu n'avais pas "prix_achat", donc je prends "Prix_Hospitalier"
                prix_v = items["Prix_Public_De_Vente"]
                prix_vente = items["Prix_Public_De_Vente"]  # même chose
                date_vente = now_str
                quantite_vendue = items["Quantite"]
                quantite_list = items.get("list_quantity", [])  # au cas où "list_quantity" n'existe pas, pour éviter une erreur
                total_facture = items["Prix_total"]
                ID_Stock = items.get("ID_Stock", None)  # tu n'avais pas "id_stock" dans ton dict exemple
                quantite_traiter = 0
                self.total_facture = 0
                list_facture.append([items['Code_EAN_13'],
                            id_medicament, 
                            prix_vente,
                            date_vente,
                            quantite_vendue,
                            id_client,
                            numero_facture,
                            id_salarie, 
                            nom_medicament]
                        )

        total_facture_calculer = 0
        for item in list_facture: 
            message  += f"{item[-1]} <br>"
            message += f"{item[0]}   &nbsp;&nbsp; {item[4]} x  &nbsp;&nbsp; {item[2]} Dh <br><br>" 
            total_facture_calculer += item[2]*item[4]
        
        if self.checkbox.isChecked():
            to_pay_now = self.amount_input.text()
        else:
            to_pay_now = total_facture_calculer 

        self.producs_table.reset_index(drop=True)
        
        barcode_data = f'{matricul_pharma}{numero_facture}0'
        
        image_base64 = self.generate_barcode(barcode_data)
        message +=  f""" <hr>
                <p><strong>Total facture :</strong> {total_facture_calculer} Dh</p>
                <p><strong>Montant payé :</strong> {to_pay_now} Dh</p>
                <p><strong>Reste à payer :</strong> {total_facture_calculer - Decimal(to_pay_now)} Dh</p>
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
                if self.checkbox.isChecked():
                    to_pay_now = self.amount_input.text()
                else:
                    to_pay_now = total_facture_calculer
                CommandeClient.ajouter_commande_client(
                    items[6],
                    items[0], 
                    items[1], 
                    items[2], 
                    items[3], 
                    items[4],
                    items[5], 
                    items[7], 
                    items[8], 
                    to_pay_now, 
                    total_facture_calculer, 
                    now_str, 
                    "in progresse",
                    )


                
            self.print_ticket(message)

            QMessageBox.information(
                self.main_interface,
                "Confirmation de vente",
                "Vente confirmée avec succès!",
            )
 
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
            win32api.ShellExecute(0, "print", pdf_path, None, ".", 0)
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
