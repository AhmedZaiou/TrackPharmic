from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QDoubleSpinBox,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QHeaderView,
)
from qtpy.QtCore import Qt
from Backend.Dataset.client import Clients
from Frontend.utils.utils import *


class Client_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()

    def show_vente_interface(self):
        self.main_interface.clear_content_frame()

        self.client_dash = QWidget()
        self.client_dash.setObjectName("client_dash")

        main_layout = QVBoxLayout(self.client_dash)

        titre_page = QLabel("Ajouter clients")
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
        self.telephone_input.setValidator(phone_validator)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Adresse")

        # Création de champs numériques pour Max_Credit et Credit_Actuel
        self.max_credit_input = QDoubleSpinBox()
        self.max_credit_input.setMinimum(0)  # Valeur minimale
        self.max_credit_input.setMaximum(100000)  # Valeur maximale

        # Créer un bouton pour soumettre le formulaire
        self.submit_button = QPushButton("Ajouter")
        self.submit_button.clicked.connect(self.add_client)

        table_form_layout.addWidget(QLabel("Nom :"), 0, 0)
        table_form_layout.addWidget(self.name_input, 0, 1)
        table_form_layout.addWidget(QLabel("Prénom :"), 0, 2)
        table_form_layout.addWidget(self.surname_input, 0, 3)
        table_form_layout.addWidget(QLabel("CIN :"), 1, 0)
        table_form_layout.addWidget(self.cin_input, 1, 1)
        table_form_layout.addWidget(QLabel("Téléphone :"), 1, 2)
        table_form_layout.addWidget(self.telephone_input, 1, 3)
        table_form_layout.addWidget(QLabel("Email :"), 2, 0)
        table_form_layout.addWidget(self.email_input, 2, 1)
        table_form_layout.addWidget(QLabel("Adresse :"), 2, 2)
        table_form_layout.addWidget(self.address_input, 2, 3)
        table_form_layout.addWidget(QLabel("Max Crédit (Dh) :"), 3, 0)
        table_form_layout.addWidget(self.max_credit_input, 3, 1)
        table_form_layout.addWidget(self.submit_button, 4, 3)

        main_layout.addLayout(table_form_layout)

        self.list_client = QTableWidget(0, 7)
        self.list_client.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_client.setHorizontalHeaderLabels(
            ["ID", "Nom", "Prénom", "CIN", "Téléphone", "Crédit Actuel", "Max Crédit"]
        )
        self.remplire_table()
        self.list_client.cellClicked.connect(self.client_selected)
        # Search bar for filtering
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Chercher par 'Nom'...")
        self.search_bar.textChanged.connect(
            self.filter_table
        )  # Trigger filter when text changes

        main_layout.addWidget(self.search_bar)

        main_layout.addWidget(self.list_client)

        self.main_interface.content_layout.addWidget(self.client_dash)

    def client_selected(self, row, column):
        id_client = self.list_client.item(row, 0).text()
        self.client = Clients.extraire_client(self.main_interface.conn, id_client)
        reply = QMessageBox.question(
            self.main_interface,
            "Confirmation de modification",
            f"Vous souhaitez modifier les informations relatives aux clients {self.client['nom']} {self.client['prenom']} ?",
            QMessageBox.Yes,
            QMessageBox.Cancel,
        )

        if reply == QMessageBox.Yes:
            self.show_update_interface()

    def filter_table(self):
        # if not self.all_data:
        #    self.load_all_data()
        # Get the filter text from the search bar
        filter_text = self.search_bar.text().lower()

        # Loop through all rows and hide/show them based on the search
        for row in range(self.list_client.rowCount()):
            item = self.list_client.item(row, 1)  # Assuming column 0 is 'Nom'
            if item is not None:
                if filter_text in item.text().lower():  # Case-insensitive comparison
                    self.list_client.setRowHidden(row, False)
                else:
                    self.list_client.setRowHidden(row, True)

    def remplire_table(self):
        all_client = Clients.extraire_tous_clients(self.main_interface.conn)
        self.list_client.setRowCount(len(all_client))
        for index, element in enumerate(all_client):
            dict_element = dict(element)
            self.list_client.setItem(
                index, 0, QTableWidgetItem(str(dict_element["id_client"]))
            )
            self.list_client.setItem(
                index, 1, QTableWidgetItem(str(dict_element["nom"]))
            )
            self.list_client.setItem(
                index, 2, QTableWidgetItem(str(dict_element["prenom"]))
            )
            self.list_client.setItem(
                index, 3, QTableWidgetItem(str(dict_element["cin"]))
            )
            self.list_client.setItem(
                index, 4, QTableWidgetItem(str(dict_element["telephone"]))
            )
            self.list_client.setItem(
                index, 5, QTableWidgetItem(str(dict_element["credit_actuel"]))
            )
            self.list_client.setItem(
                index, 6, QTableWidgetItem(str(dict_element["max_credit"]))
            )

    def add_client(self):
        # Récupérer les valeurs des champs
        name = self.name_input.text()
        surname = self.surname_input.text()
        cin = self.cin_input.text()
        telephone = self.telephone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        max_credit = self.max_credit_input.value()
        current_credit = 0
        # Ici vous pouvez ajouter le client dans une base de données ou autre logique
        if not (name and surname and cin and telephone and max_credit):
            QMessageBox.warning(
                self.main_interface,
                "Erreur",
                "Le Nom, Prènom, CIN, Téléphone et Max credit sont obligatoires.",
            )
            return
        try:
            Clients.ajouter_client(
                self.main_interface.conn,
                name,
                surname,
                cin,
                telephone,
                email,
                address,
                max_credit,
                current_credit,
            )
        except Exception as e:
            QMessageBox.warning(self.client_dash, "Erreur", "Le CIN existe déjà.")
            print(e)
            return
        self.remplire_table()
        # Effacer les champs après soumission
        self.name_input.clear()
        self.surname_input.clear()
        self.cin_input.clear()
        self.telephone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.max_credit_input.setValue(0)

    def show_update_interface(self):
        self.main_interface.clear_content_frame()

        self.client_dash = QWidget()
        self.client_dash.setObjectName("client_dash")

        main_layout = QVBoxLayout(self.client_dash)

        titre_page = QLabel("Modefier clients")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titre_page)

        table_form_layout = QGridLayout()

        # Créer les champs de saisie pour le formulaire sans 'self'
        self.name_input = QLineEdit()
        self.name_input.setText(self.client["nom"])
        self.surname_input = QLineEdit()
        self.surname_input.setText(self.client["prenom"])
        self.cin_input = QLineEdit()
        self.cin_input.setText(self.client["cin"])
        self.telephone_input = QLineEdit()
        self.telephone_input.setText(self.client["telephone"])
        self.telephone_input.setValidator(phone_validator)
        self.email_input = QLineEdit()
        self.email_input.setText(self.client["email"])
        self.address_input = QLineEdit()
        self.address_input.setText(self.client["adresse"])

        # Création de champs numériques pour Max_Credit et Credit_Actuel
        self.max_credit_input = QDoubleSpinBox()
        self.max_credit_input.setMinimum(0)  # Valeur minimale
        self.max_credit_input.setMaximum(100000)  # Valeur maximale
        self.max_credit_input.setValue(float(self.client["max_credit"]))

        # Créer un bouton pour soumettre le formulaire
        self.submit_button = QPushButton("Modefier")
        self.submit_button.clicked.connect(self.medefier_client)

        table_form_layout.addWidget(QLabel("Nom :"), 0, 0)
        table_form_layout.addWidget(self.name_input, 0, 1)
        table_form_layout.addWidget(QLabel("Prénom :"), 0, 2)
        table_form_layout.addWidget(self.surname_input, 0, 3)
        table_form_layout.addWidget(QLabel("CIN :"), 1, 0)
        table_form_layout.addWidget(self.cin_input, 1, 1)
        table_form_layout.addWidget(QLabel("Téléphone :"), 1, 2)
        table_form_layout.addWidget(self.telephone_input, 1, 3)
        table_form_layout.addWidget(QLabel("Email :"), 2, 0)
        table_form_layout.addWidget(self.email_input, 2, 1)
        table_form_layout.addWidget(QLabel("Adresse :"), 2, 2)
        table_form_layout.addWidget(self.address_input, 2, 3)
        table_form_layout.addWidget(QLabel("Max Crédit (Dh) :"), 3, 0)
        table_form_layout.addWidget(self.max_credit_input, 3, 1)
        table_form_layout.addWidget(self.submit_button, 4, 3)

        main_layout.addLayout(table_form_layout)

        self.list_client = QTableWidget(0, 7)
        self.list_client.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_client.setHorizontalHeaderLabels(
            ["ID", "Nom", "Prénom", "CIN", "Téléphone", "Crédit Actuel", "Max Crédit"]
        )
        self.remplire_table()
        self.list_client.cellClicked.connect(self.client_selected)
        # Search bar for filtering
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Chercher par 'Nom'...")
        self.search_bar.textChanged.connect(
            self.filter_table
        )  # Trigger filter when text changes

        main_layout.addWidget(self.search_bar)

        main_layout.addWidget(self.list_client)

        self.main_interface.content_layout.addWidget(self.client_dash)

    def medefier_client(self):
        # Récupérer les valeurs des champs
        name = self.name_input.text()
        surname = self.surname_input.text()
        cin = self.cin_input.text()
        telephone = self.telephone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        max_credit = self.max_credit_input.value()

        # Ici vous pouvez ajouter le client dans une base de données ou autre logique
        if not (name and surname and cin and telephone and max_credit):
            QMessageBox.warning(
                self.main_interface,
                "Erreur",
                "Le Nom, Prènom, CIN, Téléphone et Max credit sont obligatoires.",
            )
            return
        Clients.modifier_info_client(
            self.main_interface.conn,
            self.client["id_client"],
            name,
            surname,
            cin,
            telephone,
            email,
            address,
            max_credit,
        )
        self.show_vente_interface()
