from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QMessageBox,QGridLayout,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QLineEdit, QCheckBox
)
from qtpy.QtCore import Qt


from Backend.Dataset.dataset import *


class Medicament_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_ajouter_interface()

    


    def create_menu_commande(self):
        menu_layout = QHBoxLayout()
        self.ajouter_medicament = QPushButton("Ajouter Medicament")
        self.ajouter_medicament.clicked.connect(self.ajouter_medicament_fc)
        menu_layout.addWidget(self.ajouter_medicament)
        self.modifier_medicament = QPushButton("Modifier Medicament")
        self.modifier_medicament.clicked.connect(self.modifier_medicament_fc)
        menu_layout.addWidget(self.modifier_medicament)
        return menu_layout
    
    def ajouter_medicament_fc(self):
        self.show_ajouter_interface()
    def modifier_medicament_fc(self):
        self.show_modifier_interface()

    def show_ajouter_interface(self):
        self.main_interface.clear_content_frame()
        self.main_interface.keyPressEvent = self.keyPressEvent
        self.code_barre_scanner = ""

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")


        main_layout = QVBoxLayout(self.vente_dash)

        titre_page = QLabel("Gestion de medicaments")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page)

        menu_layout = self.create_menu_commande()
        main_layout.addLayout(menu_layout)





        layout = QGridLayout()

        self.code_ean_label = QLabel("Code EAN-13 :")
        layout.addWidget(self.code_ean_label , 0,0)
        self.code_ean_input = QLabel("Scanner le code barre")
        layout.addWidget(self.code_ean_input, 0,1) 

        # Labels et champs d'entrée pour chaque colonne de la table
        self.nom_label = QLabel("Nom du Médicament :")
        layout.addWidget(self.nom_label, 1,0)
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom du Médicament")
        layout.addWidget(self.nom_input, 1,1)

        self.caracteristique_label = QLabel("Caractéristique :")
        layout.addWidget(self.caracteristique_label, 2,0)
        self.caracteristique_input = QLineEdit()
        self.caracteristique_input.setPlaceholderText("Caractéristique")
        layout.addWidget(self.caracteristique_input, 2,1)

        

        self.generique_label = QLabel("Médicament Générique (Oui/Non) :")
        layout.addWidget(self.generique_label, 3,0)
        self.generique_input = QLineEdit()
        self.generique_input.setPlaceholderText("Médicament Générique (Oui/Non)")
        layout.addWidget(self.generique_input, 3,1)

        self.prix_officine_label = QLabel("Prix Officine :")
        layout.addWidget(self.prix_officine_label, 4,0)
        self.prix_officine_input = QLineEdit()
        layout.addWidget(self.prix_officine_input, 4,1)

        self.prix_public_label = QLabel("Prix Public de Vente :")
        layout.addWidget(self.prix_public_label, 5,0)
        self.prix_public_input = QLineEdit()
        layout.addWidget(self.prix_public_input, 5,1)

        self.prix_remboursement_label = QLabel("Prix Base Remboursement :")
        layout.addWidget(self.prix_remboursement_label, 6,0)
        self.prix_remboursement_input = QLineEdit()
        layout.addWidget(self.prix_remboursement_input,6,1)

        self.prix_hospitalier_label = QLabel("Prix Hospitalier :")
        layout.addWidget(self.prix_hospitalier_label,7,0)
        self.prix_hospitalier_input = QLineEdit()
        layout.addWidget(self.prix_hospitalier_input,7,1)

        self.substance_label = QLabel("Substance Active DCI :")
        layout.addWidget(self.substance_label, 8,0)
        self.substance_input = QLineEdit()
        self.substance_input.setPlaceholderText("Substance Active DCI")
        layout.addWidget(self.substance_input, 8,1)

        self.classe_label = QLabel("Classe Thérapeutique :")
        layout.addWidget(self.classe_label, 9,0)
        self.classe_input = QLineEdit()
        self.classe_input.setPlaceholderText("Classe Thérapeutique")
        layout.addWidget(self.classe_input, 9,1)


        self.min_labels = QLabel("Min in stock:")
        layout.addWidget(self.min_labels, 10,0)
        self.min_input = QLineEdit()
        layout.addWidget(self.min_input, 10,1)

        self.max_label = QLabel("Max in stock:")
        layout.addWidget(self.max_label, 11,0)
        self.max_input = QLineEdit()
        layout.addWidget(self.max_input, 11,1)

        # Bouton pour ajouter un médicament
        self.add_button = QPushButton("Ajouter Médicament")
        self.add_button.clicked.connect(self.add_medicament_to_db)
        layout.addWidget(self.add_button, 12,1)

        main_layout.addLayout(layout)




        self.main_interface.content_layout.addWidget(self.vente_dash)
    




    def keyPressEvent(self, event):
        """Gérer les entrées clavier, comme les données du lecteur de code-barres."""
        key = event.text() 

        if key == '\r' :  # Lorsque le lecteur envoie un saut de ligne
            print(self.code_barre_scanner)   
            if len(self.code_barre_scanner ) == 13:
                self.code_ean_input.setText(self.code_barre_scanner)
                self.medicament_search = extraire_medicament_code_barre(self.code_barre_scanner)
                self.code_barre_scanner = ""  # Réinitialiser pour le prochain scan 
                if self.medicament_search  is not None: 
                    QMessageBox.warning(self.main_interface, "Erreur", "Le medicament déjà exsiste, voulez vous le modifier ?")
        else:
            self.code_barre_scanner += key  # Ajouter le caractère au code en cours  


        

        
    


    def add_medicament_to_db(self):
        # Récupérer les valeurs des champs
        nom = self.nom_input.text()
        caracteristique = self.caracteristique_input.text()
        code_ean = self.code_ean_input.text()
        generique = self.generique_input.text()
        prix_officine = self.prix_officine_input.text()
        prix_public = self.prix_public_input.text()
        prix_remboursement = self.prix_remboursement_input.text()
        prix_hospitalier = self.prix_hospitalier_input.text()
        substance = self.substance_input.text()
        classe = self.classe_input.text()

        min_v = self.min_input.text()
        max_v = self.max_input.text()

        # Vérifier les champs obligatoires
        if not (nom and code_ean):
            QMessageBox.warning(self.main_interface, "Erreur", "Le nom et le code EAN-13 sont obligatoires.")
            return

        try:

            ajouter_medicament(nom, caracteristique, code_ean, generique, prix_officine, prix_public, 
                  prix_remboursement, prix_hospitalier, substance, classe, min_v, max_v)
            
            # Message de succès
            QMessageBox.information(self.main_interface, "Succès", "Médicament ajouté avec succès.")
            self.clear_fields()

        except sqlite3.IntegrityError:
            QMessageBox.warning(self.main_interface, "Erreur", "Un médicament avec ce code EAN-13 existe déjà.")
        except Exception as e:
            QMessageBox.critical(self.main_interface, "Erreur", f"Une erreur est survenue : {str(e)}")

    def clear_fields(self):
        self.nom_input.clear()
        self.caracteristique_input.clear()
        self.code_ean_input.setText("Scanner le code barre")
        self.generique_input.clear()
        self.prix_officine_input.clear()
        self.prix_public_input.clear()
        self.prix_remboursement_input.clear()
        self.prix_hospitalier_input.clear()
        self.substance_input.clear()
        self.classe_input.clear()
        self.min_input.clear()
        self.max_input.clear()
    




    def show_modifier_interface(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")


        main_layout = QVBoxLayout(self.vente_dash)

        titre_page = QLabel("Gestion de medicaments")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(titre_page)

        menu_layout = self.create_menu_commande()
        main_layout.addLayout(menu_layout)




        self.main_interface.content_layout.addWidget(self.vente_dash)
    












