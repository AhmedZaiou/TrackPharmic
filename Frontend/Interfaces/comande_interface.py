from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QCompleter,
    QSpinBox,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QHeaderView,
)
from qtpy.QtCore import Qt, QStringListModel
from datetime import datetime
import time

from Backend.Dataset.commande import Commandes
from Backend.Dataset.fournisseur import Fournisseur
from Backend.Dataset.medicament import Medicament


from Frontend.utils.utils import *


class Commande_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_commande_interface()
        self.commande = []
        self.info_fourniseur = None
        self.code_barre_scanner = ""
        self.last_key_time = time.time()
        self.barcode_delay_threshold = 0.1
        self.main_interface.keyPressEvent = self.keyPressEvent

    def create_menu_commande(self):
        menu_layout = QHBoxLayout()
        """self.add_commande_menu = QPushButton("Passer commande")
        self.add_commande_menu.clicked.connect(self.add_commande)
        menu_layout.addWidget(self.add_commande_menu)
        self.list_commande_menu = QPushButton("lister commande")
        self.list_commande_menu.clicked.connect(self.commande_entrack)
        menu_layout.addWidget(self.list_commande_menu)"""
        return menu_layout

    def show_commande_interface(self):
        self.main_interface.clear_content_frame()

        self.principale_dash_add = QWidget()
        self.principale_dash_add.setObjectName("principalDash")

        # Widget central
        # Layout principal
        main_layout_add = QVBoxLayout(self.principale_dash_add)

        titre_page = QLabel("Passer des commandes")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        main_layout_add.addWidget(titre_page)

        menu_layout = self.create_menu_commande()
        main_layout_add.addLayout(menu_layout)

        add_commande_layout = QVBoxLayout()
        # Section Fournisseur
        fournisseur_layout = QGridLayout()
        self.fournisseur_input = QLineEdit()
        self.fournisseur_input.setPlaceholderText("Rechercher fournisseur par Nom")

        self.fournisseur_input.textChanged.connect(self.OntextChangeFournisseur)

        self.completer_fournisseur = QCompleter()
        self.completer_fournisseur.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_fournisseur.setCompletionMode(QCompleter.PopupCompletion)
        self.fournisseur_input.setCompleter(self.completer_fournisseur)
        self.completer_fournisseur.activated.connect(self.selectionner_fournisseur)

        self.add_fournisseur_button = QPushButton("Nouveau fournisseur")
        self.add_fournisseur_button.clicked.connect(self.create_fournisseur)

        self.fournisseur_status_label = QLabel("Fournisseur : ")
        self.fournisseur_activite_label = QLabel("Email : ")

        self.fournisseur_max_credit = QLabel("Téléphone : ")
        self.fournisseur_credit_actuel = QLabel("Adresse : ")

        self.fournisseur_status_label.setText("Fournisseur : Nom Fournisseur")
        self.fournisseur_activite_label.setText("Email : Email Fournisseur")
        self.fournisseur_max_credit.setText("Téléphone : Téléphone Fournisseur")
        self.fournisseur_credit_actuel.setText("Adresse : Adresse Fournisseur")
        fournisseur_layout.addWidget(self.fournisseur_input, 0, 0)
        fournisseur_layout.addWidget(self.add_fournisseur_button, 0, 1)

        fournisseur_layout.addWidget(self.fournisseur_status_label, 1, 0)
        fournisseur_layout.addWidget(self.fournisseur_activite_label, 1, 1)

        fournisseur_layout.addWidget(self.fournisseur_max_credit, 2, 0)
        fournisseur_layout.addWidget(self.fournisseur_credit_actuel, 2, 1)

        self.inclure_checkbox = QCheckBox("Important")
        fournisseur_layout.addWidget(self.inclure_checkbox, 3, 0)

        add_commande_layout.addLayout(fournisseur_layout)

        # Zone d'entrée pour le code-barres
        barcode_layout = QGridLayout()
        self.barcode_input = QLineEdit()
        self.barcode_input.setValidator(int_validator)
        self.barcode_input.setPlaceholderText("Entrez le code-barres ou scannez ici")

        self.nom_medicament = QLineEdit()
        self.nom_medicament.setPlaceholderText(
            "Entrez le nom du médicament ici"
        )  # Updated placeholder text to be in French
        self.barcode_input.returnPressed.connect(self.process_barcode)
        self.nom_medicament.textChanged.connect(self.onTextChanged)

        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.nom_medicament.setCompleter(self.completer)

        self.quantite_input = QSpinBox()
        self.quantite_input.setRange(1, 10000)

        self.add_to_cart_button = QPushButton("Ajouter au panier")
        self.add_to_cart_button.clicked.connect(self.ajouter_medi_to_commande)

        barcode_layout.addWidget(self.barcode_input, 0, 0)
        barcode_layout.addWidget(self.nom_medicament, 0, 1)
        barcode_layout.addWidget(QLabel("Quantité : "), 0, 2)
        barcode_layout.addWidget(self.quantite_input, 0, 3)
        barcode_layout.addWidget(self.add_to_cart_button, 0, 4)
        add_commande_layout.addLayout(barcode_layout)
        main_layout_add.addLayout(add_commande_layout)

        self.product_table = QTableWidget(0, 3)  # (0 lignes, 3 colonnes)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.product_table.setHorizontalHeaderLabels(["Code-barre", "Nom", "Quantité"])
        main_layout_add.addWidget(self.product_table)

        button_layout = QGridLayout()
        self.confirmation_button = QPushButton("Confirmer la commande")
        self.confirmation_button.clicked.connect(self.confirmation_function)
        self.confirmation_button.clicked.connect(self.confirmation_function)

        self.annuler_button = QPushButton("Annuler la commande")
        self.annuler_button.clicked.connect(self.annuler_fonction)

        button_layout.addWidget(self.confirmation_button, 0, 0)
        button_layout.addWidget(self.annuler_button, 0, 1)
        main_layout_add.addLayout(button_layout)

        self.main_interface.content_layout.addWidget(self.principale_dash_add)

    def selectionner_fournisseur(self, text):
        data = Fournisseur.extraire_fournisseur_nom(text)

        self.fournisseur_status_label.setText(
            f"Fournisseur : {data['nom_fournisseur']}"
        )
        self.fournisseur_activite_label.setText(f"Email : {data['email']}")

        self.fournisseur_max_credit.setText(f"Téléphone : {data['telephone']}")
        self.fournisseur_credit_actuel.setText(f"Adresse : {data['adresse']}")
        self.info_fourniseur = data

    def OntextChangeFournisseur(self, text):
        if len(text) >= 3:
            self.updateCompleter_fournisseur(text)

    def updateCompleter_fournisseur(self, text):
        results = Fournisseur.extraire_fournisseur_nom_like(text)
        results = [item["nom_fournisseur"] for item in results]
        model = QStringListModel(results)
        self.completer_fournisseur.setModel(model)

    def onTextChanged(self, text):
        if len(text) >= 5:
            self.updateCompleter(text)

    def updateCompleter(self, text):
        results = Medicament.extraire_medicament_nom_like_name(text)
        model = QStringListModel(results)
        self.completer.setModel(model)

    def ajouter_medi_to_commande(self):
        code_barre = self.barcode_input.text()
        nom_medicament = self.nom_medicament.text()
        quantite = self.quantite_input.value()

        if code_barre == "" and nom_medicament == "":
            QMessageBox.information(
                self.main_interface,
                "Merci de sélectionner un médicament",
                "Merci de sélectionner un médicament avant d'ajouter au panier.",
            )
        else:
            self.commande.append([code_barre, nom_medicament, quantite])
            test_existance = False
            for item in self.commande: 
                if item[0] == code_barre:
                    item[2] += 1
                    test_existance = True
                    break
            if not test_existance:
                self.commande.append([code_barre, nom_medicament, quantite])
            self.product_table.setRowCount(len(self.commande))
            for row, product in enumerate(self.commande):
                for col, data in enumerate(product):
                    self.product_table.setItem(row, col, QTableWidgetItem(str(data)))
        self.barcode_input.clear()
        self.nom_medicament.clear()
        self.quantite_input.setValue(1)

    def ajouter_medi_to_commande_code(self, code_barre_scanner):
        medicament = Medicament.extraire_medicament_code_barre(code_barre_scanner)
        if medicament is None:
            QMessageBox.information(
                self.main_interface, "Medicament non reconue", "Medicament non reconue"
            )
            return
        else:
            medicament = dict(medicament)
            #self.commande.append([code_barre_scanner, medicament["Nom"], 1])

            test_existance = False
            for item in self.commande: 
                if item[0] == code_barre_scanner:
                    item[2] += 1
                    test_existance = True
                    break
            if not test_existance:
                self.commande.append([code_barre_scanner, medicament["Nom"], 1])

            self.product_table.setRowCount(len(self.commande))
            for row, product in enumerate(self.commande):
                for col, data in enumerate(product):
                    self.product_table.setItem(row, col, QTableWidgetItem(str(data)))

    def confirmation_function(self):
        if self.info_fourniseur is None:
            QMessageBox.information(
                self.main_interface,
                "Merci de sélectionner un fournisseur",
                "Merci de sélectionner un fournisseur avant de confirmer la commande.",
            )
            return
        if len(self.commande) == 0:
            QMessageBox.information(
                self.main_interface,
                "Merci de sélectionner des médicaments",
                "Merci de sélectionner des médicaments",
            )
            return
        id_salarie = self.main_interface.user_session["id_salarie"]
        if self.inclure_checkbox.isChecked:
            Commandes.ajouter_commande(
                str(self.commande),
                self.info_fourniseur["id_fournisseur"],
                datetime.now(),
                datetime.now(),
                "en cours",
                None,
                None,
                None,
                id_salarie,
                False,
            )
        else:
            Commandes.ajouter_commande(
                str(self.commande),
                self.info_fourniseur["id_fournisseur"],
                datetime.now(),
                datetime.now(),
                "en cours",
                None,
                None,
                None,
                id_salarie,
                True,
            )

        QMessageBox.information(
            self.main_interface,
            "La commande a été enregistrée avec succès",
            "La commande a été enregistrée avec succès",
        )
        self.actualiser_commande()

    def annuler_fonction(self):
        confirmation = QMessageBox.question(
            self.main_interface,
            "Confirmation",
            "Êtes-vous sûr de vouloir annuler la commande ?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.Yes:
            self.main_interface = Commande_dash(self.main_interface)

    def actualiser_commande(self):
        self.commande = []
        self.product_table.setRowCount(0)
        self.barcode_input.clear()
        self.nom_medicament.clear()
        self.fournisseur_input.clear()
        self.quantite_input.setValue(1)
        self.info_fourniseur = None
        self.fournisseur_status_label.setText(f"Fournisseur : ")
        self.fournisseur_activite_label.setText(f"Email :  ")

        self.fournisseur_max_credit.setText(f"Téléphone :  ")
        self.fournisseur_credit_actuel.setText(f"Adresse :  ")

    def show_list_commande_interface(self):
        self.main_interface.clear_content_frame()

        self.principale_dash = QWidget()
        self.principale_dash.setObjectName("principalDash")

        main_layout = QVBoxLayout(self.principale_dash)

        titre_page = QLabel("Gestion des comandes")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titre_page)

        menu_layout = self.create_menu_commande()
        main_layout.addLayout(menu_layout)

        # Panier
        self.cart_table = QTableWidget(0, 6)
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cart_table.setHorizontalHeaderLabels(
            [
                "Code commande",
                "Fournisseur",
                "Date de commande",
                "Noms des médicaments",
                "Statut commande",
                "Traiter",
            ]
        )
        main_layout.addWidget(self.cart_table)

        self.charger_carte_table()

        # Assign layout to central widget
        self.main_interface.content_layout.addWidget(self.principale_dash)

        # Connecter les signaux

    def commande_entrack(self):
        self.show_list_commande_interface()

    def add_commande(self):
        self.show_commande_interface()

    def toggle_inputs(self):
        if self.checkbox.isChecked():
            self.amount_input.setEnabled(True)
            self.rest_a_payer.setEnabled(True)
            self.rest_a_payer_value.setEnabled(True)
        else:
            self.amount_input.setDisabled(True)
            self.rest_a_payer.setDisabled(True)
            self.rest_a_payer_value.setDisabled(True)

    def create_fournisseur(self):
        from Frontend.Interfaces.fourniseur_interface import Fournisseur_dash

        self.main_interface = Fournisseur_dash(self.main_interface)

    def process_barcode(self, codebare):
        if len(codebare) >= 13:
            return codebare[-13:]
        return ""

    def charger_carte_table(self):
        data = Commandes.extraire_tous_commandes_table()
        self.cart_table.setRowCount(len(data))
        for row, product in enumerate(data):
            self.cart_table.setItem(
                row, 0, QTableWidgetItem(str(product["id_commande"]))
            )
            fournissuer = Fournisseur.extraire_fournisseur(product["id_fournisseur"])
            self.cart_table.setItem(
                row, 1, QTableWidgetItem(fournissuer["nom_fournisseur"])
            )
            self.cart_table.setItem(
                row, 2, QTableWidgetItem(str(product["date_commande"]))
            )
            self.cart_table.setItem(row, 3, QTableWidgetItem(product["Liste_Produits"]))
            self.cart_table.setItem(
                row, 3, QTableWidgetItem(product["statut_reception"])
            )
            self.cart_table.setItem(row, 3, QTableWidgetItem(product["status_incl"]))

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
                    self.ajouter_medi_to_commande_code(self.code_barre_scanner)
                    self.code_barre_scanner = ""  # Réinitialiser pour le prochain scan

            else:
                self.code_barre_scanner += key  # Ajouter le caractère au code en cours
        except:
            print("erreur")
