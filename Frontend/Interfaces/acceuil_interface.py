from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QHeaderView,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox
)
from qtpy.QtCore import Qt


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
        widget_medicament_expiration_layout = QVBoxLayout(widget_medicament_expiration)
        self.table_widget_medicament_expiration = QTableWidget()
        self.table_widget_medicament_expiration.setColumnCount(3)
        self.table_widget_medicament_expiration.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget_medicament_expiration.setHorizontalHeaderLabels(["Nom médicament", "Date expiration", "Quantité"])
        self.populate_table() 
        widget_medicament_expiration_layout.addWidget(self.table_widget_medicament_expiration)
        main_layout.addWidget(widget_medicament_expiration)

        # Deuxième widget: Liste des commandes en cours
        widget_commend_en_cours = QWidget()
        widget_commend_en_cours_layout = QVBoxLayout(widget_commend_en_cours)
        self.table_widget_commend_en_cours = QTableWidget()
        self.table_widget_commend_en_cours.setColumnCount(4)
        self.table_widget_commend_en_cours.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget_commend_en_cours.setHorizontalHeaderLabels(["Date commande", "Fournisseur", "Status", "Quantité"])
        self.populate_commande_table()
        widget_commend_en_cours_layout.addWidget(self.table_widget_commend_en_cours)
        main_layout.addWidget(widget_commend_en_cours)

        # Troisième widget: Médicaments avec disponibilité de stock < min stock
        widget_disponibilite = QWidget()
        widget_disponibilite_layout = QVBoxLayout(widget_disponibilite)
        self.table_widget_disponibilite = QTableWidget()
        self.table_widget_disponibilite.setColumnCount(3)
        self.table_widget_disponibilite.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget_disponibilite.setHorizontalHeaderLabels(["Nom médicament", "Quantité", "Min Quantité"])
        self.populate_disponibilite_table() 


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
    


    def populate_table(self):
            # Clear existing data
            self.table_widget_medicament_expiration.setRowCount(0)

            # Get the data for the table (replace with your own data retrieval logic)
            data = []#get_medicament_expiration_data()

            # Populate the table with data
            for row, item in enumerate(data):
                self.table_widget_medicament_expiration.insertRow(row)
                for col, value in enumerate(item):
                    self.table_widget_medicament_expiration.setItem(row, col, QTableWidgetItem(str(value)))
    def populate_commande_table(self):
        pass
    def populate_disponibilite_table(self):
        pass
