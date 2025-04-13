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


class List_stock_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()

    def show_vente_interface(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")
        main_layout = QVBoxLayout(self.vente_dash)

        label_titre = QLabel("Liste des médicaments existants dans le stock") 
        label_titre.setObjectName("TitrePage")
        label_titre.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label_titre)

        # Premier widget: Tableau des médicaments avec date d'expiration < 2 mois
        widget_medicament_expiration = QWidget()
        widget_medicament_expiration_layout = QVBoxLayout(widget_medicament_expiration)
        self.table_widget_medicament_expiration = QTableWidget()
        self.table_widget_medicament_expiration.setColumnCount(4)
        self.table_widget_medicament_expiration.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table_widget_medicament_expiration.setHorizontalHeaderLabels(
            ["Code médicament", "Nom médicament", "Date expiration", "Quantité"]
        )
        self.populate_table() 

        # Search bar for filtering
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Chercher par 'Nom médicament'...")
        self.search_bar.textChanged.connect(self.filter_table)  # Trigger filter when text changes

        main_layout.addWidget(self.search_bar)
        widget_medicament_expiration_layout.addWidget(
            self.table_widget_medicament_expiration
        )
        main_layout.addWidget(widget_medicament_expiration)

        # Quatrième widget: Nombre de ventes effectuées aujourd'hui
        widget_statistique = QWidget()
        widget_statistique_layout = QVBoxLayout(widget_statistique)
        label_widget_statistique = QLabel()
        # Set the label text with the number of sales made today
        # ...
        widget_statistique_layout.addWidget(label_widget_statistique)
        main_layout.addWidget(widget_statistique)

        self.main_interface.content_layout.addWidget(self.vente_dash)
    def filter_table(self):
        #if not self.all_data:
        #    self.load_all_data()
        # Get the filter text from the search bar
        filter_text = self.search_bar.text().lower()

        # Loop through all rows and hide/show them based on the search
        for row in range(self.table_widget_medicament_expiration.rowCount()):
            item = self.table_widget_medicament_expiration.item(row, 1)  # Assuming column 0 is 'Nom'
            if item is not None:
                if filter_text in item.text().lower():  # Case-insensitive comparison
                    self.table_widget_medicament_expiration.setRowHidden(row, False)
                else:
                    self.table_widget_medicament_expiration.setRowHidden(row, True)

    def populate_table(self):
        data = Stock.extraire_stock_medicament()
        self.table_widget_medicament_expiration.setRowCount(len(data))
        for index, element in enumerate(data):
            self.table_widget_medicament_expiration.setItem(
                index, 0, QTableWidgetItem(str(element["Code_EAN_13"]))
            )
            self.table_widget_medicament_expiration.setItem(
                index, 1, QTableWidgetItem(str(element["Nom"]))
            )
            self.table_widget_medicament_expiration.setItem(
                index, 2, QTableWidgetItem(str(element["date_expiration"]))
            )
            self.table_widget_medicament_expiration.setItem(
                index, 3, QTableWidgetItem(str(element["quantite_actuelle"]))
            )

    def populate_disponibilite_table(self):
        pass
