from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QTextBrowser,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox
)
from qtpy.QtCore import Qt
import mpld3

from Frontend.Interfaces.vente_interface import Ventes

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
        fig = Ventes.get_evolution()
        image = mpld3.fig_to_html(fig)

        # Ajouter un QTextBrowser pour afficher du HTML
        html_content = f"""
        <html>
        <head><title>Comptabilité - Vue HTML</title></head>
        <body>
            <h2 style="color: blue;">Bienvenue sur le tableau de bord de la comptabilité!</h2>
            <p>Ceci est un contenu HTML simple affiché dans l'interface.</p>
        </body>
        <div>{image}</div>
        </html>
        """
        text_browser = QTextBrowser()
        text_browser.setHtml(html_content)
        main_layout.addWidget(text_browser)




        self.main_interface.content_layout.addWidget(self.vente_dash)