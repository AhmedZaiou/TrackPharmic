from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSpinBox,
    QHeaderView,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QMessageBox,
)
from qtpy.QtCore import Qt, QDate
import ast
from datetime import datetime
import time
from Backend.Dataset.stock import Stock
from Backend.Dataset.medicament import Medicament
from Backend.Dataset.retour import Retour

from Frontend.utils.utils import *


class Retour_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface

        self.show_add_stock_interface_saisie_libre()

        self.last_time = time.time()
        self.commande_deja_traiter_list = []
        self.last_key_time = time.time()
        self.barcode_delay_threshold = 0.1
        self.code_barre_scanner = ""

    def show_add_stock_interface_saisie_libre(self):
        self.main_interface.clear_content_frame()
        self.main_interface.keyPressEvent = self.keyPressEventLibre
        self.medicament_search = None
        self.commande_current = None

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")
        self.code_barre_scanner = ""

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.vente_dash)

        titre_page = QLabel("Gestion de retour")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titre_page)

        formul_layout = QVBoxLayout()

        self.formulaire_widget = QWidget()

        validation_layout_fournisseur = QGridLayout(self.formulaire_widget)

        code_barre = QLabel("Code EAN 13 :")
        self.code_barre_value_ajout = QLineEdit()
        self.code_barre_value_ajout.setPlaceholderText(" Scanner Code EAN 13")

        numero_facture = QLabel("Numéro du facture:")
        self.numero_facture = QLineEdit()
        self.numero_facture.setValidator(int_validator)
        self.numero_facture.setPlaceholderText("Numéro facture")

        client_iden = QLabel("Nom de client:")
        self.client_iden = QLineEdit()
        self.client_iden.setPlaceholderText("Nom de client")

        quantite_commender = QLabel("Quantité")
        self.quantite_commender_value_ajout = QLineEdit()
        self.quantite_commender_value_ajout.setValidator(int_validator)
        self.quantite_commender_value_ajout.setPlaceholderText("Quantité de retour")
        self.prix_achat_medicament_ajout = QLineEdit()
        self.prix_achat_medicament_ajout.setValidator(float_validator)
        self.prix_achat_medicament_ajout.setPlaceholderText("Prix de produit")

        self.date_expiration_medicament_ajout = QDateEdit()
        self.date_expiration_medicament_ajout.setCalendarPopup(True)
        self.date_expiration_medicament_ajout.setDate(QDate.currentDate().addYears(2))

        validation_layout_fournisseur.addWidget(client_iden, 0, 0)
        validation_layout_fournisseur.addWidget(self.client_iden, 0, 1)
        validation_layout_fournisseur.addWidget(numero_facture, 0, 2)
        validation_layout_fournisseur.addWidget(self.numero_facture, 0, 3)

        validation_layout_fournisseur.addWidget(code_barre, 1, 0)
        validation_layout_fournisseur.addWidget(self.code_barre_value_ajout, 1, 1)

        validation_layout_fournisseur.addWidget(quantite_commender, 1, 2)
        validation_layout_fournisseur.addWidget(
            self.quantite_commender_value_ajout, 1, 3
        )
        validation_layout_fournisseur.addWidget(QLabel("Date d'expiration :"), 2, 0)
        validation_layout_fournisseur.addWidget(
            self.date_expiration_medicament_ajout, 2, 1
        )

        # Ajout des labels et des champs dans le layout
        validation_layout_fournisseur.addWidget(QLabel("Prix de produit :"), 2, 2)
        validation_layout_fournisseur.addWidget(self.prix_achat_medicament_ajout, 2, 3)

        self.confirm_button_ajout = QPushButton("Confirmer l'ajout")
        self.confirm_button_ajout.clicked.connect(self.confirmation_retour_seul)

        validation_layout_fournisseur.addWidget(self.confirm_button_ajout, 4, 3)

        formul_layout.addWidget(self.formulaire_widget)

        main_layout.addLayout(formul_layout)


        self.medicament_table = QTableWidget(0, 4)  # (0 lignes, 3 colonnes)
        self.medicament_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.medicament_table.setHorizontalHeaderLabels(["Numéro facture", "Nom","Quantité","Date"])
        self.remplire_table_retour()
        

        # Search bar for filtering
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Chercher par 'Numéro facture'...")
        self.search_bar.textChanged.connect(self.filter_table)  # Trigger filter when text changes

        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.medicament_table)

        self.main_interface.content_layout.addWidget(self.vente_dash)
    def filter_table(self):
        #if not self.all_data:
        #    self.load_all_data()
        # Get the filter text from the search bar
        filter_text = self.search_bar.text().lower()

        # Loop through all rows and hide/show them based on the search
        for row in range(self.medicament_table.rowCount()):
            item = self.medicament_table.item(row, 0)  # Assuming column 0 is 'Nom'
            if item is not None:
                if filter_text in item.text().lower():  # Case-insensitive comparison
                    self.medicament_table.setRowHidden(row, False)
                else:
                    self.medicament_table.setRowHidden(row, True)
    def remplire_table_retour(self):
        medicaments = Retour.extraire_tous_table_retours(self.main_interface.conn)
        self.medicament_table.setRowCount(len(medicaments))
        for index, element in enumerate(medicaments): 
            self.medicament_table.setItem(
                index, 0, QTableWidgetItem(str(element["numero_facture"]))
            )
            self.medicament_table.setItem(
                index, 1, QTableWidgetItem(str(element["nom_medicament"]))
            )
            self.medicament_table.setItem(
                index, 2, QTableWidgetItem(str(element["quantite_retour"]))
            )
            self.medicament_table.setItem(
                index, 3, QTableWidgetItem(str(element["date_retour"]))
            ) 

    def confirmation_retour_seul(self):
        quantite_commender_retour = self.quantite_commender_value_ajout.text()
        date_expiration_medicament = self.date_expiration_medicament_ajout.date().toString(
            "yyyy-MM-dd"
        )
        prix_achat_retour = self.prix_achat_medicament_ajout.text()
        code_barre_value_ajout = self.code_barre_value_ajout.text()
        numero_facture = self.numero_facture.text()
        client_iden = self.client_iden.text()

        self.medicament_search = Medicament.extraire_medicament_code_barre(self.main_interface.conn,
            code_barre_value_ajout
        )
        if (
            not self.medicament_search
            or not prix_achat_retour
            or not quantite_commender_retour
            or not date_expiration_medicament
        ):
            QMessageBox.information(
                self.main_interface,
                "Information incomplete",
                "Merci de remplire les informations",
            )
            return
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        reply = QMessageBox.question(
            self.main_interface,
            "Confirmation de retour",
            "Confirmer le retour ?",
            QMessageBox.Yes,
            QMessageBox.Cancel,
        )
        if reply == QMessageBox.Yes:
            Retour.ajouter_retour(self.main_interface.conn,
                self.medicament_search["id_medicament"],
                prix_achat_retour,
                now,
                quantite_commender_retour,
                numero_facture,
                self.main_interface.user_session["id_salarie"],
            )

            Stock.ajouter_stock(self.main_interface.conn,
                self.medicament_search["id_medicament"],
                0,
                self.main_interface.user_session["id_salarie"],
                prix_achat_retour,
                prix_achat_retour,
                prix_achat_retour,
                now,
                date_expiration_medicament,
                0,
                quantite_commender_retour,
                quantite_commender_retour,
                quantite_commender_retour,
                now,
                now,
            )

            self.main_interface = Retour_dash(self.main_interface)

    def keyPressEventLibre(self, event):
        """Gérer les entrées clavier, comme les données du lecteur de code-barres."""
        pass
