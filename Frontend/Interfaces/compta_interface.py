from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox
)
from qtpy.QtCore import Qt


class Compta_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()

    def show_vente_interface(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.vente_dash) 
        titre_page = QLabel("Comptabilité")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page)




        self.main_interface.content_layout.addWidget(self.vente_dash)