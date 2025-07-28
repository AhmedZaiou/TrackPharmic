from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenuBar,
    QMenu,
    QAction,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtCore import QTimer
from qtpy.QtCore import Qt, QSize
from qtpy.QtGui import QPixmap, QIcon
import threading
import time
from Frontend.utils.utils import *
from Backend.Dataset.salarie import Salaries
from Backend.Comptabilite.cloturecaisse import *
import os
import pymysql
from Frontend.utils.utils import *


class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(name_application)
        self.setGeometry(100, 100, 1200, 800)  # merci de remplire
        self.showFullScreen()
        self.setStyleSheet(set_styles())
        # self.show_main_interface()
        self.show_login_interface()
        self.setFocusPolicy(Qt.StrongFocus)
        self.conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )

        t = threading.Thread(target=self.update_value, daemon=True)
        t.start()

    def update_value(self):
        while True:
            try:
                # Vérifie si la connexion est toujours valide
                self.conn.ping(reconnect=True)
            except Exception:
                print("Reconnexion MySQL...")
                self.conn = pymysql.connect(
                    host=host, user=user, password=password, database=database
                )            
            time.sleep(3)

    def create_database(self):
        import json
        from Backend.Dataset.client import (
            Clients,
        )  # Assurez-vous de l'existence des classes appropriées
        from Backend.Dataset.commande import Commandes
        from Backend.Dataset.credit import Credit
        from Backend.Dataset.echanges import Echanges
        from Backend.Dataset.fournisseur import Fournisseur
        from Backend.Dataset.medicament import Medicament
        from Backend.Dataset.salarie import Salaries
        from Backend.Dataset.stock import Stock
        from Backend.Dataset.payment import Payment
        from Backend.Dataset.pharmacie import Pharmacies
        from Backend.Dataset.ventes import Ventes
        from Backend.Dataset.retour import Retour
        from Backend.Dataset.commande_client import CommandeClient

        # Medicament.supprimer_toute_base_donnees()

        Clients.create_table_clients(self.conn)
        Stock.create_table_stock(self.conn)
        Commandes.create_table_commandes(self.conn)
        Credit.create_table_credit(self.conn)
        Echanges.create_table_echanges(self.conn)
        Fournisseur.create_table_fournisseur(self.conn)
        Medicament.create_table_medicament(self.conn)
        Payment.create_table_payment(self.conn)
        Pharmacies.create_table_pharmacies(self.conn)
        Ventes.create_table_ventes(self.conn)
        Salaries.create_table_salaries(self.conn)
        Retour.create_table_retours(self.conn)
        CommandeClient.create_table_commandes_client(self.conn)
        Salaries.ajouter_salarie(
            self.conn,
            "user",
            "prenom",
            "cin",
            "telephone",
            "email",
            "adresse",
            "photo",
            "salaire",
            "type_contrat",
            "date_embauche",
            "admin",
            "user",
        )

    def show_login_interface(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setObjectName("widgetGeneral")
        self.central_widget = QWidget()
        self.central_widget.setObjectName("widgetGeneral")

        self.main_layout_p = QVBoxLayout(self.central_widget)

        self.setCentralWidget(self.central_widget)

        self.central_widget = QWidget()
        self.central_widget.setObjectName("main")

        self.main_layout = QVBoxLayout(self.central_widget)

        # Ajouter le logo de l'application
        self.logo_label = QLabel()
        pixmap = QPixmap(
            app_logo
        )  # Remplacez "path_to_logo_image" par le chemin de votre image
        pixmap = pixmap.scaled(
            550, 550, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )  # Réduire la taille du logo
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setObjectName("logo")
        self.main_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        # Ajouter le titre de l'application
        self.title_label = QLabel(Name_pharma)
        self.title_label.setObjectName("titlelogo")

        # Créer un widget pour contenir le logo et le titre
        logo_title_widget = QWidget()
        logo_title_layout = QHBoxLayout(logo_title_widget)
        logo_title_layout.addWidget(self.logo_label)
        logo_title_layout.addWidget(self.title_label)
        logo_title_widget.setObjectName("logoTitle")

        self.main_layout.addWidget(logo_title_widget, alignment=Qt.AlignCenter)

        # Page de connexion
        self.login_frame = QFrame()
        self.login_frame.setFixedSize(400, 400)  # Frame carrée avec taille fixe
        self.main_layout.addWidget(self.login_frame, alignment=Qt.AlignCenter)
        self.login_frame.setObjectName("loginframe")
        # Layout de la frame de connexion
        self.login_layout = QVBoxLayout(self.login_frame)
        self.connexion = QLabel("Connexion")
        self.connexion.setObjectName("connexionlab")
        self.login_layout.addWidget(self.connexion)
        self.user_label = QLabel("Utilisateur :")
        self.login_layout.addWidget(self.user_label)
        self.user_entry = QLineEdit()
        self.user_entry.setPlaceholderText("Entrez votre nom d'utilisateur")
        self.login_layout.addWidget(self.user_entry)

        self.password_label = QLabel("Mot de passe :")
        self.login_layout.addWidget(self.password_label)

        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setPlaceholderText("Entrez votre mot de passe")
        self.login_layout.addWidget(self.password_entry)

        self.login_button = QPushButton("Se connecter")
        self.login_button.clicked.connect(self.login)
        self.login_button.setObjectName("buttconexion")
        self.login_layout.addWidget(self.login_button)

        self.main_layout_p.addWidget(self.central_widget)

    def login(self):
        login = self.user_entry.text()
        password = self.password_entry.text()
        self.user_session = Salaries.extraire_salarie_login(self.conn, login, password)
        if self.user_session is None:
            QMessageBox.information(
                self, "Erreur de connexion", "Mot de passe ou utilisateur incorrect"
            )
        elif self.user_session["grade"] == "admin":
            self.show_main_interface()
        else:
            self.show_main_interface_salarie()

    def show_main_interface(self):
        # Widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.current_input = ""

        self.central_widget.setObjectName("widgetGeneral")

        self.main_layout = QVBoxLayout(self.central_widget)

        self.top_menu_frame = QFrame(self)
        self.top_menu_frame.setObjectName("topmenu")
        self.top_menu_frame.setFixedHeight(100)  # Hauteur du menu vertical
        self.main_layout.addWidget(self.top_menu_frame)

        self.top_menu_layout = QHBoxLayout(self.top_menu_frame)

        profile_widget = QWidget()
        profile_widget.setObjectName("profilewidget")
        profile_layout = QHBoxLayout(profile_widget)

        # Ajouter une image de profil
        profile_image = QLabel()
        if not os.path.isfile(self.user_session["photo"]):
            self.user_session["photo"] = profile_salarie
        pixmap = QPixmap(
            self.user_session["photo"]
        )  # Remplacez par le chemin de votre image
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        profile_image.setPixmap(pixmap)
        profile_image.setAlignment(Qt.AlignCenter)

        # Ajouter un nom de profil
        profile_name = QLabel(
            str(self.user_session["nom"] + " " + self.user_session["prenom"])
        )
        profile_name.setAlignment(Qt.AlignCenter)
        profile_name.setStyleSheet("font-size: 14px; font-weight: bold; align: left;")

        # Ajouter l'image et le nom au layout
        profile_layout.addWidget(profile_image)
        profile_layout.addWidget(profile_name)

        # Ajouter le widget de profil au menu gauche
        self.top_menu_layout.addWidget(profile_widget)

        self.deconexion_bouton = self.create_button_with_icon(
            "Déconnexion", deconexion_logo
        )
        self.salarie_bouton = self.create_button_with_icon(
            "Gesion Salariés", salare_logo
        )
        self.kpi_bouton = self.create_button_with_icon(
            "Comptabilité de la pharmacie", kpi_logo
        )
        self.medicament_bouton = self.create_button_with_icon(
            "Gestion des médicaments", medicament_logo
        )
        self.fournisseur_bouton = self.create_button_with_icon(
            "Gestion des fournisseurs", fournisseur_logo
        )

        self.list_stock_bouton = self.create_button_with_icon(
            "Disponibilité en stock", stock_gestion_logo
        )

        self.fournisseur_bouton.clicked.connect(self.fournisseur_click)
        self.medicament_bouton.clicked.connect(self.medicament_click)
        self.salarie_bouton.clicked.connect(self.salarie_click)
        self.kpi_bouton.clicked.connect(self.compta_click)
        self.deconexion_bouton.clicked.connect(self.deconexion_click)

        self.base_widget = QWidget()
        self.base_layout = QHBoxLayout(self.base_widget)

        # Frame pour menu gauche (vertical)
        self.left_menu_frame = QFrame(self)
        self.left_menu_frame.setFixedWidth(100)
        self.base_layout.addWidget(self.left_menu_frame)
        self.left_menu_frame.setObjectName("leftmenu")

        # Layout pour menu gauche
        self.left_menu_layout = QVBoxLayout(self.left_menu_frame)

        self.acceuil_bouton = self.create_button_with_icon("Acceuil", acceuil_logo)
        self.commande_bouton = self.create_button_with_icon(
            "Gestion des commandes", commande_client_logo
        )
        self.commande_Client_bouton = self.create_button_with_icon(
            "Gestion des commandes Clients", commande_logo
        )
        self.credit_bouton = self.create_button_with_icon(
            "Gestion des crédits", credit_logo
        )
        self.vente_bouton = self.create_button_with_icon(
            "Gestion des ventes", vente_logo
        )
        self.retour_bouton = self.create_button_with_icon(
            "Gestion des retours", retour_logo
        )

        self.client_bouton = self.create_button_with_icon(
            "Gestion des clients", client_logo
        )
        self.echange_bouton = self.create_button_with_icon(
            "Gestion des échanges", echange_logo
        )
        self.stock_bouton = self.create_button_with_icon("Gestion de stock", stock_logo)
        self.ferme_bouton = self.create_button_with_icon(
            "Cloturé la caisse", ferme_logo
        )

        self.acceuil_bouton.clicked.connect(self.acceuil_click)
        self.commande_bouton.clicked.connect(self.commande_click)
        self.commande_Client_bouton.clicked.connect(self.commande_client_click)
        self.credit_bouton.clicked.connect(self.credit_click)
        self.vente_bouton.clicked.connect(self.vente_click)
        self.retour_bouton.clicked.connect(self.retour_click)
        self.client_bouton.clicked.connect(self.client_click)
        self.echange_bouton.clicked.connect(self.echange_click)
        self.stock_bouton.clicked.connect(self.stock_click)
        self.ferme_bouton.clicked.connect(self.cloture_clic)

        self.list_stock_bouton.clicked.connect(self.list_stock_click)

        # Ajouter des boutons dans le menu vertical du haut
        self.top_menu_layout.addWidget(self.acceuil_bouton)
        self.top_menu_layout.addWidget(self.fournisseur_bouton)
        self.top_menu_layout.addWidget(self.commande_bouton)
        self.top_menu_layout.addWidget(self.list_stock_bouton)
        self.top_menu_layout.addWidget(self.stock_bouton)
        self.top_menu_layout.addWidget(self.medicament_bouton)
        self.top_menu_layout.addWidget(self.salarie_bouton)
        self.top_menu_layout.addWidget(self.kpi_bouton)
        self.top_menu_layout.addWidget(self.deconexion_bouton)

        # Ajouter des boutons dans le menu gauche
        self.left_menu_layout.addWidget(self.vente_bouton)
        self.left_menu_layout.addWidget(self.commande_Client_bouton)
        self.left_menu_layout.addWidget(self.retour_bouton)
        self.left_menu_layout.addWidget(self.credit_bouton)
        self.left_menu_layout.addWidget(self.client_bouton)
        self.left_menu_layout.addWidget(self.echange_bouton)
        self.left_menu_layout.addWidget(self.ferme_bouton)

        # Frame pour contenu principal
        self.content_frame = QFrame(self)
        self.base_layout.addWidget(self.content_frame)

        # Layout pour contenu principal
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.addWidget(QLabel("Contenu principal ici"))
        self.content_frame.setObjectName("contentframe")

        self.main_layout.addWidget(self.base_widget)

        # Créer les menus (Menu horizontal en haut et menu latéral)
        self.create_menus()
        self.acceuil_click()

    def show_main_interface_salarie(self):
        # Widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.current_input = ""

        self.central_widget.setObjectName("widgetGeneral")

        self.main_layout = QVBoxLayout(self.central_widget)

        self.top_menu_frame = QFrame(self)
        self.top_menu_frame.setObjectName("topmenu")
        self.top_menu_frame.setFixedHeight(100)  # Hauteur du menu vertical
        self.main_layout.addWidget(self.top_menu_frame)

        self.top_menu_layout = QHBoxLayout(self.top_menu_frame)

        profile_widget = QWidget()
        profile_widget.setObjectName("profilewidget")
        profile_layout = QHBoxLayout(profile_widget)

        # Ajouter une image de profil
        profile_image = QLabel()
        if not os.path.isfile(self.user_session["photo"]):
            self.user_session["photo"] = profile_salarie
        pixmap = QPixmap(
            self.user_session["photo"]
        )  # Remplacez par le chemin de votre image
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        profile_image.setPixmap(pixmap)
        profile_image.setAlignment(Qt.AlignCenter)

        # Ajouter un nom de profil
        profile_name = QLabel(
            str(self.user_session["nom"] + " " + self.user_session["prenom"])
        )
        profile_name.setAlignment(Qt.AlignCenter)
        profile_name.setStyleSheet("font-size: 14px; font-weight: bold; align: left;")

        # Ajouter l'image et le nom au layout
        profile_layout.addWidget(profile_image)
        profile_layout.addWidget(profile_name)

        # Ajouter le widget de profil au menu gauche
        self.top_menu_layout.addWidget(profile_widget)

        self.deconexion_bouton = self.create_button_with_icon(
            "Déconnexion", deconexion_logo
        )
        self.medicament_bouton = self.create_button_with_icon(
            "Gestion des médicaments", medicament_logo
        )
        self.fournisseur_bouton = self.create_button_with_icon(
            "Gestion des fournisseurs", fournisseur_logo
        )
        self.list_stock_bouton = self.create_button_with_icon(
            "Disponibilité en stock", stock_gestion_logo
        )

        self.fournisseur_bouton.clicked.connect(self.fournisseur_click)
        self.medicament_bouton.clicked.connect(self.medicament_click)
        self.deconexion_bouton.clicked.connect(self.deconexion_click)
        self.list_stock_bouton.clicked.connect(self.list_stock_click)

        self.base_widget = QWidget()
        self.base_layout = QHBoxLayout(self.base_widget)

        # Frame pour menu gauche (vertical)
        self.left_menu_frame = QFrame(self)
        self.left_menu_frame.setFixedWidth(100)
        self.base_layout.addWidget(self.left_menu_frame)
        self.left_menu_frame.setObjectName("leftmenu")

        # Layout pour menu gauche
        self.left_menu_layout = QVBoxLayout(self.left_menu_frame)

        self.acceuil_bouton = self.create_button_with_icon("Acceuil", acceuil_logo)
        self.commande_bouton = self.create_button_with_icon(
            "Gestion des commandes", commande_client_logo
        )
        self.credit_bouton = self.create_button_with_icon(
            "Gestion des crédits", credit_logo
        )
        self.vente_bouton = self.create_button_with_icon(
            "Gestion des ventes", vente_logo
        )
        self.commande_Client_bouton = self.create_button_with_icon(
            "Gestion des commandes Clients", commande_logo
        )
        self.retour_bouton = self.create_button_with_icon(
            "Gestion des retours", retour_logo
        )
        self.client_bouton = self.create_button_with_icon(
            "Gestion des clients", client_logo
        )
        self.echange_bouton = self.create_button_with_icon(
            "Gestion des échanges", echange_logo
        )
        self.stock_bouton = self.create_button_with_icon("Gestion de stock", stock_logo)
        self.ferme_bouton = self.create_button_with_icon(
            "Cloturé la caisse", ferme_logo
        )

        self.acceuil_bouton.clicked.connect(self.acceuil_click)
        self.commande_bouton.clicked.connect(self.commande_click)
        self.commande_Client_bouton.clicked.connect(self.commande_client_click)
        self.credit_bouton.clicked.connect(self.credit_click)
        self.vente_bouton.clicked.connect(self.vente_click)
        self.client_bouton.clicked.connect(self.client_click)
        self.echange_bouton.clicked.connect(self.echange_click)
        self.stock_bouton.clicked.connect(self.stock_click)
        self.ferme_bouton.clicked.connect(self.cloture_clic)
        self.retour_bouton.clicked.connect(self.retour_click)

        # Ajouter des boutons dans le menu vertical du haut
        self.top_menu_layout.addWidget(self.acceuil_bouton)
        self.top_menu_layout.addWidget(self.fournisseur_bouton)
        self.top_menu_layout.addWidget(self.commande_bouton)
        self.top_menu_layout.addWidget(self.list_stock_bouton)
        self.top_menu_layout.addWidget(self.stock_bouton)
        self.top_menu_layout.addWidget(self.medicament_bouton)
        self.top_menu_layout.addWidget(self.deconexion_bouton)

        # Ajouter des boutons dans le menu gauche
        self.left_menu_layout.addWidget(self.vente_bouton)
        self.left_menu_layout.addWidget(self.commande_Client_bouton)
        self.left_menu_layout.addWidget(self.retour_bouton)
        self.left_menu_layout.addWidget(self.credit_bouton)
        self.left_menu_layout.addWidget(self.client_bouton)
        self.left_menu_layout.addWidget(self.echange_bouton)
        self.left_menu_layout.addWidget(self.ferme_bouton)

        # Frame pour contenu principal
        self.content_frame = QFrame(self)
        self.base_layout.addWidget(self.content_frame)

        # Layout pour contenu principal
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.addWidget(QLabel("Contenu principal ici"))
        self.content_frame.setObjectName("contentframe")

        self.main_layout.addWidget(self.base_widget)

        # Créer les menus (Menu horizontal en haut et menu latéral)
        self.create_menus()
        self.acceuil_click()

    def keyPressEvent(self, event):
        """Gérer les entrées clavier, comme les données du lecteur de code-barres."""
        pass

    def acceuil_click(self):
        from .acceuil_interface import Acceuil_dash

        self.main_interface = Acceuil_dash(self)

    def client_click(self):
        from .client_interface import Client_dash

        self.main_interface = Client_dash(self)

    def commande_click(self):
        from .comande_interface import Commande_dash

        self.main_interface = Commande_dash(self)

    def commande_client_click(self):
        from .commande_client import Commande_client

        self.main_interface = Commande_client(self)

    def credit_click(self):
        from .credit_interface import Credit_dash

        self.main_interface = Credit_dash(self)

    def echange_click(self):
        from .echange_interface import Echange_dash

        self.main_interface = Echange_dash(self)

    def cloture_clic(self):
        reply = QMessageBox.question(
            self,
            "Confirmation de cloture",
            "Merci de confirlé la cloture de la journée",
            QMessageBox.Yes,
            QMessageBox.Cancel,
        )

        if reply == QMessageBox.Yes:
            caisse = Caisse(self.conn)
            caisse.fermeture_de_caisse()

    def medicament_click(self):
        from .medicament_interface import Medicament_dash

        self.main_interface = Medicament_dash(self)

    def salarie_click(self):
        from .salarie_interface import Salarie_dash

        self.main_interface = Salarie_dash(self)

    def stock_click(self):
        from .stock_interface import Stock_dash

        self.main_interface = Stock_dash(self)

    def vente_click(self):
        from .vente_interface import Vente_dash

        self.main_interface = Vente_dash(self)

    def retour_click(self):
        from .retour_interface import Retour_dash

        self.main_interface = Retour_dash(self)

    def compta_click(self):
        from .compta_interface import Compta_dash

        self.main_interface = Compta_dash(self)

    def fournisseur_click(self):
        from .fourniseur_interface import Fournisseur_dash

        self.main_interface = Fournisseur_dash(self)

    def medicament_click(self):
        from .medicament_interface import Medicament_dash

        self.main_interface = Medicament_dash(self)

    def list_stock_click(self):
        from .stock_element_interface import List_stock_dash

        self.main_interface = List_stock_dash(self)

    def deconexion_click(self):
        self.close()

    def create_button_with_icon(self, text, icon_path):
        # Créer un bouton avec une image
        button = QPushButton("")
        button.setObjectName("ButtonWithLogo")
        button.setToolTip(text)
        icon = QIcon(icon_path)

        if not icon.isNull():  # Vérifie si l'icône est valide
            button.setIcon(icon)
            button.setIconSize(QSize(32, 32))  # Définit la taille de l'icône
        else:
            print(f"L'image '{icon_path}' n'a pas été trouvée ou est invalide.")

        def handle_click():


            app = QApplication.instance()

            # Désactiver toute l'application
            for widget in app.allWidgets():
                widget.setEnabled(False)
            cooldown_s = 1

            # Réactiver après cooldown (converti en ms)
            QTimer.singleShot(int(cooldown_s * 1000), lambda: [
                w.setEnabled(True) for w in app.allWidgets()
            ])

        button.clicked.connect(handle_click)
        return button

    def create_menus(self):
        # Menu barre supérieure (horizontal)
        menubar = self.menuBar()

        # Créer le menu "Fichier"
        file_menu = menubar.addMenu("Fichier")
        open_action = QAction("Ouvrir", self)
        file_menu.addAction(open_action)
        save_action = QAction("Sauvegarder", self)
        file_menu.addAction(save_action)
        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Créer le menu "Édition"
        edit_menu = menubar.addMenu("Édition")
        cut_action = QAction("Couper", self)
        edit_menu.addAction(cut_action)
        copy_action = QAction("Copier", self)
        edit_menu.addAction(copy_action)
        paste_action = QAction("Coller", self)
        edit_menu.addAction(paste_action)

        # Créer le menu "Aide"
        help_menu = menubar.addMenu("Aide")
        about_action = QAction("À propos", self)
        help_menu.addAction(about_action)

    def clear_content_frame(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
