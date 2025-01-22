
from qtpy.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QFrame, QLabel, QLineEdit
from qtpy.QtCore import Qt,QSize
from qtpy.QtGui import QPixmap, QIcon 


from Frontend.utils.utils import *
from Backend.Dataset.dataset import *


class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(name_application)
        self.setGeometry(100, 100, 1200, 800) # merci de remplire 
        #self.showFullScreen()
        self.setStyleSheet(set_styles())
        #self.show_main_interface()
        self.show_login_interface()
        self.setFocusPolicy(Qt.StrongFocus)
     

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

        
 
        # Page de connexion
        self.login_frame = QFrame()
        self.login_frame.setFixedSize(400, 400)  # Frame carrée avec taille fixe 
        self.main_layout.addWidget(self.login_frame, alignment=Qt.AlignCenter)
        self.login_frame.setObjectName("loginframe")
        # Layout de la frame de connexion
        self.login_layout = QVBoxLayout(self.login_frame)
        self.connexion = QLabel("Connexion")
        self.connexion.setObjectName('connexionlab')
        self.login_layout.addWidget(self.connexion )
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
        self.user_session = extraire_salarie_login(login, password)
        if self.user_session is None:
            print("mot de passe erreur") 

        else: 
            self.show_main_interface()  
    

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
        profile_layout = QHBoxLayout(profile_widget)

        # Ajouter une image de profil
        profile_image = QLabel()
        pixmap = QPixmap(self.user_session['Photo'])  # Remplacez par le chemin de votre image
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        profile_image.setPixmap(pixmap)
        profile_image.setAlignment(Qt.AlignCenter)

        # Ajouter un nom de profil
        profile_name = QLabel(str(self.user_session['Nom']+" "+self.user_session['Prenom'])) 
        profile_name.setAlignment(Qt.AlignCenter)
        profile_name.setStyleSheet("font-size: 14px; font-weight: bold;")

        # Ajouter l'image et le nom au layout
        profile_layout.addWidget(profile_image)
        profile_layout.addWidget(profile_name)

        # Ajouter le widget de profil au menu gauche
        self.top_menu_layout.addWidget(profile_widget)

        self.deconexion_bouton = self.create_button_with_icon("", deconexion_logo)
        self.salarie_bouton = self.create_button_with_icon("", salare_logo)
        self.kpi_bouton = self.create_button_with_icon("", kpi_logo)
        self.medicament_bouton = self.create_button_with_icon("", medicament_logo)
        self.fournisseur_bouton = self.create_button_with_icon("", fournisseur_logo)

        self.top_menu_layout.addWidget(self.fournisseur_bouton)
        self.top_menu_layout.addWidget(self.medicament_bouton)

        self.top_menu_layout.addWidget(self.salarie_bouton)
        self.top_menu_layout.addWidget(self.kpi_bouton)
        # Ajouter des boutons dans le menu vertical du haut 
        self.top_menu_layout.addWidget(self.deconexion_bouton)

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

        self.acceuil_bouton = self.create_button_with_icon("", acceuil_logo)
        self.commande_bouton = self.create_button_with_icon("", commande_logo)
        self.credit_bouton = self.create_button_with_icon("", credit_logo)
        self.vente_bouton = self.create_button_with_icon("", vente_logo)
        self.client_bouton = self.create_button_with_icon("", client_logo)
        self.echange_bouton = self.create_button_with_icon("", echange_logo)
        self.stock_bouton = self.create_button_with_icon("", stock_logo)
        self.ferme_bouton = self.create_button_with_icon("", ferme_logo)

        self.acceuil_bouton.clicked.connect(self.acceuil_click)
        self.commande_bouton.clicked.connect(self.commande_click)
        self.credit_bouton.clicked.connect(self.credit_click)
        self.vente_bouton.clicked.connect(self.vente_click)
        self.client_bouton.clicked.connect(self.client_click)
        self.echange_bouton.clicked.connect(self.echange_click)
        self.stock_bouton.clicked.connect(self.stock_click)
        self.ferme_bouton.clicked.connect(self.stock_click)


        # Ajouter des boutons dans le menu gauche
        self.left_menu_layout.addWidget(self.acceuil_bouton)
        self.left_menu_layout.addWidget(self.vente_bouton)
        self.left_menu_layout.addWidget(self.commande_bouton)
        self.left_menu_layout.addWidget(self.credit_bouton)
        self.left_menu_layout.addWidget(self.client_bouton)
        self.left_menu_layout.addWidget(self.echange_bouton)
        self.left_menu_layout.addWidget(self.stock_bouton)
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
        
    def credit_click(self):
        from .credit_interface import Credit_dash
        self.main_interface = Credit_dash(self) 
    def echange_click(self):
        from .echange_interface import Echange_dash
        self.main_interface = Echange_dash(self) 
        
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
    def compta_click(self):
        from .compta_interface import Compta_dash
        self.main_interface = Compta_dash(self)
    def fournisseur_click(self):
        from .fourniseur_interface import Fournisseur_dash
        self.main_interface = Fournisseur_dash(self)
    def medicament_click(self):
        from .medicament_interface import Medicament_dash
        self.main_interface = Medicament_dash(self)
    def deconexion_click(self): 
        self.close() 
    
    def create_button_with_icon(self, text, icon_path):
        # Créer un bouton avec une image
        button = QPushButton(text)
        button.setObjectName("ButtonWithLogo")
        icon = QIcon(icon_path)

        if not icon.isNull():  # Vérifie si l'icône est valide
            button.setIcon(icon)
            button.setIconSize(QSize(32, 32))  # Définit la taille de l'icône
        else:
            print(f"L'image '{icon_path}' n'a pas été trouvée ou est invalide.")
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
    


    def show_main_interface_salarie(self):
        # Widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)  
        self.central_widget.setObjectName("widgetGeneral")

        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)

        # Frame pour menu haut (vertical)
        self.top_menu_frame = QFrame(self)
        self.top_menu_frame.setFixedHeight(100)  # Hauteur du menu vertical
        self.main_layout.addWidget(self.top_menu_frame)

        self.top_menu_frame.setObjectName("topmenu")

        # Layout pour menu haut
        self.top_menu_layout = QHBoxLayout(self.top_menu_frame)

        profile_widget = QWidget()
        profile_layout = QHBoxLayout(profile_widget)
        # Ajouter une image de profil
        profile_image = QLabel()
        pixmap = QPixmap(self.user_session['Photo'])  # Remplacez par le chemin de votre image
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        profile_image.setPixmap(pixmap)
        profile_image.setAlignment(Qt.AlignCenter)

        # Ajouter un nom de profil
        profile_name = QLabel(str(self.user_session['Nom']+" "+self.user_session['Prenom'])) 
        profile_name.setAlignment(Qt.AlignCenter)
        profile_name.setStyleSheet("font-size: 14px; font-weight: bold;")

        # Ajouter l'image et le nom au layout
        profile_layout.addWidget(profile_image)
        profile_layout.addWidget(profile_name)

        # Ajouter le widget de profil au menu gauche
        self.top_menu_layout.addWidget(profile_widget)


        # Ajouter des boutons dans le menu vertical du haut 
        self.top_menu_layout.addWidget(QPushButton("Déconnexion"))


        self.base_widget = QWidget()
        self.base_layout = QHBoxLayout(self.base_widget)

        # Frame pour menu gauche (vertical)
        self.left_menu_frame = QFrame(self)
        self.left_menu_frame.setFixedWidth(100)
        self.base_layout.addWidget(self.left_menu_frame)
        self.left_menu_frame.setObjectName("leftmenu")

        # Layout pour menu gauche
        self.left_menu_layout = QVBoxLayout(self.left_menu_frame)


        acceuil_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/logoacceuil.png"
        commande_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/commandelogo.png"
        credit_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/creditlogo.png"
        vente_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/ventelogo.svg"
        client_logo = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Frontend/images/ventelogo.svg"



        self.acceuil_bouton = self.create_button_with_icon("", acceuil_logo)
        self.commande_bouton = self.create_button_with_icon("", commande_logo)
        self.credit_bouton = self.create_button_with_icon("", credit_logo)
        self.vente_bouton = self.create_button_with_icon("", vente_logo)
        self.client_bouton = self.create_button_with_icon("", client_logo)

        self.acceuil_bouton.clicked.connect(self.acceuil_click)


        # Ajouter des boutons dans le menu gauche
        self.left_menu_layout.addWidget(self.acceuil_bouton)
        self.left_menu_layout.addWidget(self.vente_bouton)
        self.left_menu_layout.addWidget(self.commande_bouton)
        self.left_menu_layout.addWidget(self.credit_bouton)
        self.left_menu_layout.addWidget(self.client_bouton)

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
    
