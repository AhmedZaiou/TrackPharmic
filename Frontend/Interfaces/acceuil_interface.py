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

from Backend.Dataset.stock import Stock
from Backend.Dataset.medicament import Medicament


class Acceuil_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()

    def show_vente_interface(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")
        main_layout = QVBoxLayout(self.vente_dash)

        # Premier widget: Tableau des médicaments avec date d'expiration < 2 mois
        widget_medicament_expiration = QWidget()
        label_titre = QLabel("Médicaments expirant dans moins de 2 mois") 
        label_titre.setObjectName("TitrePage")
        label_titre.setAlignment(Qt.AlignCenter)
        widget_medicament_expiration_layout = QVBoxLayout(widget_medicament_expiration)
        self.table_widget_medicament_expiration = QTableWidget()
        self.table_widget_medicament_expiration.setColumnCount(4)
        self.table_widget_medicament_expiration.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table_widget_medicament_expiration.setHorizontalHeaderLabels(
            ["Code médicament", "Nom médicament", "Date expiration", "Quantité"]
        )
        self.remplire_table_expiration()
        widget_medicament_expiration_layout.addWidget(label_titre)
        widget_medicament_expiration_layout.addWidget(
            self.table_widget_medicament_expiration
        )
        main_layout.addWidget(widget_medicament_expiration)

        # Troisième widget: Médicaments avec disponibilité de stock < min stock
        widget_disponibilite = QWidget()
        label_titre_disponibilite = QLabel(
            "Médicaments en dessous du stock minimal requis"
        )
        label_titre_disponibilite.setObjectName("TitrePage")
        label_titre_disponibilite.setAlignment(Qt.AlignCenter)
        widget_disponibilite_layout = QVBoxLayout(widget_disponibilite)
        self.table_widget_disponibilite = QTableWidget()
        self.table_widget_disponibilite.setColumnCount(4)
        self.table_widget_disponibilite.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table_widget_disponibilite.setHorizontalHeaderLabels(
            ["Code médicament", "Nom médicament", "Quantité", "Min Quantité"]
        )
        self.remplire_table_quantit_minim()

        widget_disponibilite_layout.addWidget(label_titre_disponibilite)
        widget_disponibilite_layout.addWidget(self.table_widget_disponibilite)
        main_layout.addWidget(widget_disponibilite)

        # Quatrième widget: Nombre de ventes effectuées aujourd'hui
        widget_statistique = QWidget()
        widget_statistique_layout = QVBoxLayout(widget_statistique)
        label_widget_statistique = QLabel()
        # Set the label text with the number of sales made today
        # ...
        widget_statistique_layout.addWidget(label_widget_statistique)
        main_layout.addWidget(widget_statistique)

        self.main_interface.content_layout.addWidget(self.vente_dash)

    def remplire_table_expiration(self):
        data = Stock.extraire_tous_medicament_with_expiration_date_minim() 
        self.table_widget_medicament_expiration.setRowCount(len(data))
        for index, element in enumerate(data):
            dict_element = dict(element)
            self.table_widget_medicament_expiration.setItem(
                index, 0, QTableWidgetItem(str(dict_element["Code_EAN_13"]))
            )
            self.table_widget_medicament_expiration.setItem(
                index, 1, QTableWidgetItem(str(dict_element["Nom"]))
            )
            self.table_widget_medicament_expiration.setItem(
                index, 2, QTableWidgetItem(str(dict_element["date_expiration"]))
            )
            self.table_widget_medicament_expiration.setItem(
                index, 3, QTableWidgetItem(str(dict_element["quantite_actuelle"]))
            )

    def remplire_table_quantit_minim(self):
        data = Medicament.extraire_medicament_quantite_minimale_repture()
        self.table_widget_disponibilite.setRowCount(len(data))
        for index, element in enumerate(data):
            dict_element = dict(element)
            self.table_widget_disponibilite.setItem(
                index, 0, QTableWidgetItem(str(dict_element["Code_EAN_13"]))
            )
            self.table_widget_disponibilite.setItem(
                index, 1, QTableWidgetItem(str(dict_element["Nom"]))
            )
            self.table_widget_disponibilite.setItem(
                index, 3, QTableWidgetItem(str(dict_element["Stock_Actuel"]))
            )
            self.table_widget_disponibilite.setItem(
                index, 3, QTableWidgetItem(str(dict_element["Min_Stock"]))
            )
