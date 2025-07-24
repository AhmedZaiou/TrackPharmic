from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
)
from qtpy.QtCore import Qt

from Backend.Dataset.ventes import Ventes
from Backend.Dataset.credit import Credit
from Backend.Dataset.payment import Payment
from Backend.Dataset.retour import Retour


class AffichageFacture:
    def __init__(self, main_interface, numero_facture):
        self.main_interface = main_interface
        self.numero_facture = (
            numero_facture  # facture_data contient les infos à afficher
        )
        self.vente = Ventes.extraire_ventes_par_numero_facture(
            self.main_interface.conn, self.numero_facture
        )
        self.payment = Payment.extraire_paiements_par_numero_facture(
            self.main_interface.conn, self.numero_facture
        )
        self.credit = Credit.extraire_credits_par_numero_facture(
            self.main_interface.conn, self.numero_facture
        )
        self.retour = Retour.extraire_retours_par_numero_facture(
            self.main_interface.conn, self.numero_facture
        )

        self.show_facture_interface()

    def show_facture_interface(self):
        self.main_interface.clear_content_frame()

        self.facture_widget = QWidget()
        self.facture_widget.setObjectName("facture_widget")
        main_layout = QVBoxLayout(self.facture_widget)

        # --- En-tête de la facture ---
        titre_label = QLabel("Facture")
        titre_label.setObjectName("TitrePage")
        titre_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titre_label)

        # --- Informations client et facture ---
        infos_layout = QVBoxLayout()

        client_nom = QLabel(f"Client : {self.facture_data['client_nom']}")
        date_facture = QLabel(f"Date : {self.facture_data['date']}")
        numero_facture = QLabel(f"Facture N° : {self.facture_data['numero']}")

        infos_layout.addWidget(client_nom)
        infos_layout.addWidget(date_facture)
        infos_layout.addWidget(numero_facture)

        main_layout.addLayout(infos_layout)

        # --- Détail des produits ---
        self.table_widget_facture = QTableWidget()
        self.table_widget_facture.setColumnCount(4)
        self.table_widget_facture.setHorizontalHeaderLabels(
            ["Produit", "Quantité", "Prix Unitaire", "Total"]
        )
        self.table_widget_facture.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.remplir_table_produits()

        main_layout.addWidget(self.table_widget_facture)

        # --- Total général ---
        total_general = QLabel(f"Total à payer : {self.facture_data['total']} MAD")
        total_general.setAlignment(Qt.AlignRight)
        total_general.setObjectName("TotalGeneral")
        main_layout.addWidget(total_general)

        self.main_interface.content_layout.addWidget(self.facture_widget)

    def remplir_table_produits(self):
        produits = self.facture_data["produits"]  # Liste de dictionnaires
        self.table_widget_facture.setRowCount(len(produits))
        for index, produit in enumerate(produits):
            self.table_widget_facture.setItem(
                index, 0, QTableWidgetItem(produit["nom"])
            )
            self.table_widget_facture.setItem(
                index, 1, QTableWidgetItem(str(produit["quantite"]))
            )
            self.table_widget_facture.setItem(
                index, 2, QTableWidgetItem(f"{produit['prix_unitaire']}")
            )
            total_ligne = produit["quantite"] * produit["prix_unitaire"]
            self.table_widget_facture.setItem(
                index, 3, QTableWidgetItem(f"{total_ligne}")
            )
