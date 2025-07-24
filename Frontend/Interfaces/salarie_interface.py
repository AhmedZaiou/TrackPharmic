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
from Backend.Dataset.salarie import Salaries

from Frontend.utils.utils import *


class Salarie_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()

    def show_vente_interface(self):
        self.main_interface.clear_content_frame()

        self.client_dash = QWidget()
        self.client_dash.setObjectName("client_dash")

        main_layout = QVBoxLayout(self.client_dash)

        titre_page = QLabel("Gestion des Salariés")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titre_page)
        table_form_layout = QGridLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom")
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Prénom")
        self.cin_input = QLineEdit()
        self.cin_input.setPlaceholderText("CIN")
        self.telephone_input = QLineEdit()
        self.telephone_input.setValidator(phone_validator)
        self.telephone_input.setPlaceholderText("Téléphone")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Adresse")

        self.photo = QLineEdit()
        self.photo.setPlaceholderText("Photo")
        self.salaire = QLineEdit()
        self.salaire.setPlaceholderText("Salaire (Dh)")
        self.type_contrat = QLineEdit()
        self.type_contrat.setPlaceholderText("Type contrat (CDI ou CDD)")
        self.date_embauche = QLineEdit()
        self.date_embauche.setPlaceholderText("Date d'embauche (12/12/2022)")
        self.grade = QLineEdit()
        self.grade.setPlaceholderText("Grade (admin or not)")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Mot de passe")
        self.password.setEchoMode(QLineEdit.Password)

        # Créer un bouton pour soumettre le formulaire
        self.submit_button = QPushButton("Ajouter Salarié")
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

        table_form_layout.addWidget(QLabel("Photo :"), 3, 0)
        table_form_layout.addWidget(self.photo, 3, 1)
        table_form_layout.addWidget(QLabel("Salaire (Dh) :"), 3, 2)
        table_form_layout.addWidget(self.salaire, 3, 3)
        table_form_layout.addWidget(QLabel("Type contrat :"), 4, 0)
        table_form_layout.addWidget(self.type_contrat, 4, 1)
        table_form_layout.addWidget(QLabel("Date d'embauche :"), 4, 2)
        table_form_layout.addWidget(self.date_embauche, 4, 3)

        table_form_layout.addWidget(QLabel("Grade :"), 5, 0)
        table_form_layout.addWidget(self.grade, 5, 1)
        table_form_layout.addWidget(QLabel("Mot de passe :"), 5, 2)
        table_form_layout.addWidget(self.password, 5, 3)
        table_form_layout.addWidget(self.submit_button, 6, 3)

        main_layout.addLayout(table_form_layout)

        self.list_client = QTableWidget(0, 6)
        self.list_client.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_client.setHorizontalHeaderLabels(
            ["Nom", "Prénom", "CIN", "Téléphone", "Email", "Grade"]
        )
        self.remplire_table()
        main_layout.addWidget(self.list_client)

        self.main_interface.content_layout.addWidget(self.client_dash)

    def remplire_table(self):
        all_salaries = Salaries.extraire_tous_salaries(self.main_interface.conn)
        self.list_client.setRowCount(len(all_salaries))
        for index, element in enumerate(all_salaries):
            self.list_client.setItem(index, 0, QTableWidgetItem(str(element["nom"])))
            self.list_client.setItem(index, 1, QTableWidgetItem(str(element["prenom"])))
            self.list_client.setItem(index, 2, QTableWidgetItem(str(element["cin"])))
            self.list_client.setItem(
                index, 3, QTableWidgetItem(str(element["telephone"]))
            )
            self.list_client.setItem(index, 4, QTableWidgetItem(str(element["email"])))
            self.list_client.setItem(index, 5, QTableWidgetItem(str(element["grade"])))

    def add_client(self):
        # Récupérer les valeurs des champs
        name = self.name_input.text()
        surname = self.surname_input.text()
        cin = self.cin_input.text()
        telephone = self.telephone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        salaire = self.salaire.text()
        type_contrat = self.type_contrat.text()
        photo = self.photo.text()
        date_embauche = self.date_embauche.text()  # .date().toString("yyyy-MM-dd")
        grade = self.grade.text()
        password = self.password.text()
        # Ici vous pouvez ajouter le client dans une base de données ou autre logique

        if not (name and surname and cin):
            QMessageBox.warning(
                self.main_interface,
                "Erreur",
                "Le Nom, Prènom et CIN sont obligatoires.",
            )
            return

        try:
            Salaries.ajouter_salarie(
                self.main_interface.conn,
                name,
                surname,
                cin,
                telephone,
                email,
                address,
                photo,
                salaire,
                type_contrat,
                date_embauche,
                grade,
                password,
            )
        except:
            QMessageBox.warning(self.client_dash, "Erreur", "Le CIN existe déjà.")
            return
        # Effacer les champs après soumission
        self.name_input.clear()
        self.surname_input.clear()
        self.cin_input.clear()
        self.telephone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.photo.clear()
        self.password.clear()
        self.type_contrat.clear()
        self.salaire.clear()
        self.date_embauche.clear()
        self.grade.clear()
