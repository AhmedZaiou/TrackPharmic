from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QLineEdit,
    QHeaderView,
)
from qtpy.QtCore import Qt


from Backend.Dataset.medicament import Medicament
from Frontend.utils.utils import *


class Medicament_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_ajouter_interface()

    def create_menu_commande(self):
        menu_layout = QHBoxLayout()
        self.lister_medicament = QPushButton("Medicament")
        self.lister_medicament.clicked.connect(self.lister_medicament_fc)
        menu_layout.addWidget(self.lister_medicament)
        self.ajouter_medicament = QPushButton("Ajouter Medicament")
        self.ajouter_medicament.clicked.connect(self.ajouter_medicament_fc)
        menu_layout.addWidget(self.ajouter_medicament)
        return menu_layout

    def lister_medicament_fc(self):
        self.show_ajouter_interface()

    def ajouter_medicament_fc(self):
        self.show_modifier_interface()

    def show_ajouter_interface(self):
        self.main_interface.clear_content_frame()
        self.main_interface.keyPressEvent = self.keyPressEvent
        self.code_barre_scanner = ""
        self.medicament_search = None
        self.medicament_modif = None

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")

        main_layout = QVBoxLayout(self.vente_dash)

        titre_page = QLabel("Gestion de medicaments")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titre_page)

        menu_layout = self.create_menu_commande()
        main_layout.addLayout(menu_layout)

        liste_all_medicament = QLabel("Tous les medicaments")
        liste_new_medicament = QLabel("Nouveaux medicaments")
        liste_all_medicament.setObjectName("Titresection")
        liste_new_medicament.setObjectName("Titresection")

        self.medicament_table = QTableWidget(0, 6)  # (0 lignes, 3 colonnes)
        self.medicament_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.medicament_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Code-barre",
                "Nom",
                "Caractéristique",
                "Prix Public de Vente",
                "Min in stock",
            ]
        )
        self.remplire_table_medicamen()
        self.medicament_table.cellClicked.connect(self.afficher_medicament_depuis_table)

        # Search bar for filtering

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Chercher par 'Nom'...")
        self.search_bar.textChanged.connect(
            self.filter_table
        )  # Trigger filter when text changes
        main_layout.addWidget(liste_all_medicament)
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.medicament_table)
        main_layout.addWidget(liste_new_medicament)

        self.new_medicament_table = QTableWidget(0, 4)
        self.new_medicament_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.new_medicament_table.setHorizontalHeaderLabels(
            ["ID", "Nom", "Caractéristique", "Prix Public de Vente"]
        )
        self.remplire_table_new_medicamen()
        self.new_medicament_table.cellClicked.connect(
            self.afficher_new_medicament_depuis_table
        )
        main_layout.addWidget(self.new_medicament_table)

        self.main_interface.content_layout.addWidget(self.vente_dash)

    def show_modifier_interface(self):
        self.main_interface.clear_content_frame()
        self.main_interface.keyPressEvent = self.keyPressEvent
        self.code_barre_scanner = ""
        self.medicament_search = None

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

        # Code EAN-13
        self.code_ean_label = QLabel("Code EAN-13 :")
        layout.addWidget(self.code_ean_label, 0, 0)
        self.code_ean_input = QLineEdit()
        self.code_ean_input.setPlaceholderText("Scanner le code barre")
        layout.addWidget(self.code_ean_input, 0, 1)

        # Nom
        self.nom_label = QLabel("Nom :")
        layout.addWidget(self.nom_label, 1, 0)
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom du médicament")
        layout.addWidget(self.nom_input, 1, 1)

        # Image URL
        self.image_url_label = QLabel("Image URL :")
        layout.addWidget(self.image_url_label, 2, 0)
        self.image_url_input = QLineEdit()
        self.image_url_input.setPlaceholderText("http://...")
        layout.addWidget(self.image_url_input, 2, 1)

        # Présentation
        self.presentation_label = QLabel("Présentation :")
        layout.addWidget(self.presentation_label, 3, 0)
        self.presentation_input = QLineEdit()
        layout.addWidget(self.presentation_input, 3, 1)

        # Dosage
        self.dosage_label = QLabel("Dosage :")
        layout.addWidget(self.dosage_label, 4, 0)
        self.dosage_input = QLineEdit()
        layout.addWidget(self.dosage_input, 4, 1)

        # Distributeur ou fabriquant
        self.fabricant_label = QLabel("Distributeur/Fabriquant :")
        layout.addWidget(self.fabricant_label, 5, 0)
        self.fabricant_input = QLineEdit()
        layout.addWidget(self.fabricant_input, 5, 1)

        # Composition
        self.composition_label = QLabel("Composition :")
        layout.addWidget(self.composition_label, 6, 0)
        self.composition_input = QLineEdit()
        layout.addWidget(self.composition_input, 6, 1)

        # Classe thérapeutique
        self.classe_label = QLabel("Classe Thérapeutique :")
        layout.addWidget(self.classe_label, 7, 0)
        self.classe_input = QLineEdit()
        layout.addWidget(self.classe_input, 7, 1)

        # Statut
        self.statut_label = QLabel("Statut :")
        layout.addWidget(self.statut_label, 8, 0)
        self.statut_input = QLineEdit()
        layout.addWidget(self.statut_input, 8, 1)

        # Code ATC
        self.code_atc_label = QLabel("Code ATC :")
        layout.addWidget(self.code_atc_label, 9, 0)
        self.code_atc_input = QLineEdit()
        layout.addWidget(self.code_atc_input, 9, 1)

        # PPV
        self.ppv_label = QLabel("Prix Public de Vente (PPV) :")
        layout.addWidget(self.ppv_label, 10, 0)
        self.ppv_input = QLineEdit()
        self.ppv_input.setValidator(float_validator)
        layout.addWidget(self.ppv_input, 10, 1)

        # Prix hospitalier
        self.prix_hosp_label = QLabel("Prix Hospitalier :")
        layout.addWidget(self.prix_hosp_label, 11, 0)
        self.prix_hosp_input = QLineEdit()
        self.prix_hosp_input.setValidator(float_validator)
        layout.addWidget(self.prix_hosp_input, 11, 1)

        # Tableau
        self.tableau_label = QLabel("Tableau :")
        layout.addWidget(self.tableau_label, 12, 0)
        self.tableau_input = QLineEdit()
        layout.addWidget(self.tableau_input, 12, 1)

        # Indications
        self.indication_label = QLabel("Indication(s) :")
        layout.addWidget(self.indication_label, 13, 0)
        self.indication_input = QLineEdit()
        layout.addWidget(self.indication_input, 13, 1)

        # Min_Stock
        self.min_stock_label = QLabel("Stock Minimum :")
        layout.addWidget(self.min_stock_label, 14, 0)
        self.min_stock_input = QLineEdit()
        self.min_stock_input.setValidator(int_validator)
        layout.addWidget(self.min_stock_input, 14, 1)

        # Stock_Actuel
        self.stock_actuel_label = QLabel("Stock Actuel :")
        layout.addWidget(self.stock_actuel_label, 15, 0)
        self.stock_actuel_input = QLineEdit()
        self.stock_actuel_input.setValidator(int_validator)
        layout.addWidget(self.stock_actuel_input, 15, 1)

        # URL médicament
        self.url_medicament_label = QLabel("URL du Médicament :")
        layout.addWidget(self.url_medicament_label, 16, 0)
        self.url_medicament_input = QLineEdit()
        layout.addWidget(self.url_medicament_input, 16, 1)

        # Bouton Ajouter
        self.add_button = QPushButton("Ajouter Médicament")
        self.add_button.clicked.connect(self.add_medicament_to_db)
        layout.addWidget(self.add_button, 17, 1)

        main_layout.addLayout(layout)

        self.main_interface.content_layout.addWidget(self.vente_dash)

    def afficher_medicament_depuis_table(self, row, column):
        id = self.medicament_table.item(row, 0).text()
        medicament = Medicament.extraire_medicament(self.main_interface.conn, id)
        if medicament:
            self.show_medicament_profile(medicament)

    def afficher_new_medicament_depuis_table(self, row, column):
        id = self.new_medicament_table.item(row, 0).text()
        medicament = Medicament.extraire_medicament(self.main_interface.conn, id)
        if medicament:
            self.show_medicament_profile(medicament)

    def show_medicament_profile(self, medicament):
        self.main_interface.clear_content_frame()
        self.main_interface.keyPressEvent = self.keyPressEvent
        self.code_barre_scanner = ""
        self.medicament_search = None

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")

        main_layout = QVBoxLayout(self.vente_dash)

        titre_page = QLabel("Fiche du Médicament")
        titre_page.setObjectName("TitrePage")
        # titre_page.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titre_page)

        menu_layout = self.create_menu_commande()
        main_layout.addLayout(menu_layout)

        layout = QGridLayout()

        def add_row(label_text, value_text, row):
            label = QLabel(f"{label_text} :")
            label.setStyleSheet("font-weight: bold")
            if label_text == "Stock Minimum" or label_text == "Stock Actuel":
                value = QLabel(str(value_text))
            else:
                value = QLabel(str(value_text) if value_text else "—")
            value.setWordWrap(True)
            layout.addWidget(label, row, 0)
            layout.addWidget(value, row, 1)

        # Affichage des champs
        add_row("Code EAN-13", medicament.get("Code_EAN_13", ""), 0)
        add_row("Nom", medicament.get("Nom", ""), 1)
        add_row("Présentation", medicament.get("Présentation", ""), 2)
        add_row("Dosage", medicament.get("Dosage", ""), 3)
        add_row(
            "Distributeur/Fabriquant",
            medicament.get("Distributeur_ou_fabriquant", ""),
            4,
        )
        add_row("Composition", medicament.get("Composition", ""), 5)
        add_row("Classe thérapeutique", medicament.get("Classe_thérapeutique", ""), 6)
        add_row("Statut", medicament.get("Statut", ""), 7)
        add_row("Code ATC", medicament.get("Code_ATC", ""), 8)
        add_row("Prix Public de Vente (PPV)", medicament.get("PPV", ""), 9)
        add_row("Prix Hospitalier", medicament.get("Prix_hospitalier", ""), 10)
        add_row("Tableau", medicament.get("Tableau", ""), 11)
        add_row("Indication(s)", medicament.get("Indications", ""), 12)
        add_row("Stock Minimum", medicament.get("Min_Stock", ""), 13)
        add_row("Stock Actuel", medicament.get("Stock_Actuel", ""), 14)
        # Image si présente
        image_url = medicament.get("Image URL", "")
        if image_url:
            from PyQt5.QtGui import QPixmap
            from PyQt5.QtCore import Qt
            from urllib.request import urlopen

            try:
                image_data = urlopen(image_url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio))
                layout.addWidget(QLabel("Image :"), 16, 0)
                layout.addWidget(image_label, 16, 1)
            except:
                add_row("Image", "Image non disponible", 16)

        main_layout.addLayout(layout)

        # Bouton pour modifier le médicament
        self.modify_button = QPushButton("Modifier Médicament")
        self.modify_button.clicked.connect(
            lambda: self.modifier_medicament_inter(medicament)
        )
        main_layout.addWidget(self.modify_button)
        self.main_interface.content_layout.addWidget(self.vente_dash)

    def filter_table(self):
        # if not self.all_data:
        #    self.load_all_data()
        # Get the filter text from the search bar
        filter_text = self.search_bar.text().lower()

        # Loop through all rows and hide/show them based on the search
        for row in range(self.medicament_table.rowCount()):
            item = self.medicament_table.item(row, 1)  # Assuming column 0 is 'Nom'
            if item is not None:
                if filter_text in item.text().lower():  # Case-insensitive comparison
                    self.medicament_table.setRowHidden(row, False)
                else:
                    self.medicament_table.setRowHidden(row, True)

    def remplire_table_medicamen(self):
        try:
            medicaments = Medicament.extraire_tous_medicament(self.main_interface.conn)
            self.medicament_table.setRowCount(len(medicaments))
            for index, element in enumerate(medicaments):
                self.medicament_table.setItem(
                    index, 0, QTableWidgetItem(str(element["id_medicament"]))
                )
                self.medicament_table.setItem(
                    index, 1, QTableWidgetItem(str(element["Code_EAN_13"]))
                )
                self.medicament_table.setItem(
                    index, 2, QTableWidgetItem(str(element["Nom"]))
                )
                self.medicament_table.setItem(
                    index, 3, QTableWidgetItem(str(element["Présentation"]))
                )
                self.medicament_table.setItem(
                    index, 4, QTableWidgetItem(str(element["PPV"]))
                )
                self.medicament_table.setItem(
                    index, 5, QTableWidgetItem(str(element["Min_Stock"]))
                )
        except Exception as e:
            print(f"Erreur lors de l'extraction des médicaments : {e}")

    def remplire_table_new_medicamen(self):
        medicaments = Medicament.extraire_tous_new_medicament(self.main_interface.conn)
        self.new_medicament_table.setRowCount(len(medicaments))
        for index, element in enumerate(medicaments):
            self.new_medicament_table.setItem(
                index, 0, QTableWidgetItem(str(element["id_medicament"]))
            )

            self.new_medicament_table.setItem(
                index, 1, QTableWidgetItem(str(element["Nom"]))
            )
            self.new_medicament_table.setItem(
                index, 2, QTableWidgetItem(str(element["Présentation"]))
            )
            self.new_medicament_table.setItem(
                index, 3, QTableWidgetItem(str(element["PPV"]))
            )
            

    def keyPressEvent(self, event):
        try:
            """Gérer les entrées clavier, comme les données du lecteur de code-barres."""
            key = event.text()

            if key == "\r":  # Lorsque le lecteur envoie un saut de ligne
                if len(self.code_barre_scanner) == 13:
                    self.code_ean_input.setText(self.code_barre_scanner)
                    self.medicament_search = Medicament.extraire_medicament_code_barre(
                        self.main_interface.conn, self.code_barre_scanner
                    )
                    self.code_barre_scanner = ""  # Réinitialiser pour le prochain scan
                    if self.medicament_search is not None:
                        reply = QMessageBox.question(
                            self.main_interface,
                            "Confirmation",
                            "Le médicament existe déjà, voulez-vous le modifier ?",
                            QMessageBox.Yes | QMessageBox.No,
                        )
                        if reply == QMessageBox.Yes:
                            self.modifier_medicament_inter(self.code_barre_scanner)
            else:
                self.code_barre_scanner += key  # Ajouter le caractère au code en cours
        except:
            print("erreur")

    def modifier_medicament_inter(self, medicament):
        self.medicament_modif = medicament
        self.show_modifier_interface()
        self.code_ean_input.setText(medicament["Code_EAN_13"])
        self.nom_input.setText(medicament["Nom"])
        self.image_url_input.setText(medicament.get("Image URL", ""))
        self.presentation_input.setText(medicament["Présentation"])
        self.dosage_input.setText(medicament["Dosage"])
        self.fabricant_input.setText(medicament["Distributeur_ou_fabriquant"])
        self.composition_input.setText(medicament["Composition"])
        self.classe_input.setText(medicament["Classe_thérapeutique"])
        self.statut_input.setText(medicament["Statut"])
        self.code_atc_input.setText(medicament["Code_ATC"])
        self.ppv_input.setPlaceholderText(str(medicament["PPV"]))
        self.prix_hosp_input.setPlaceholderText(str(medicament["Prix_hospitalier"]))
        self.indication_input.setText(medicament["Indications"])
        self.min_stock_input.setText(str(medicament["Min_Stock"]))
        self.stock_actuel_input.setText(str(medicament.get("Stock_Actuel", 0)))
        self.url_medicament_input.setText(medicament.get("URL du Médicament", ""))

    def add_medicament_to_db(self):
        # Récupérer les valeurs des champs
        code_ean = self.code_ean_input.text()
        nom = self.nom_input.text()
        image_url = self.image_url_input.text()
        presentation = self.presentation_input.text()
        dosage = self.dosage_input.text()
        fabricant = self.fabricant_input.text()
        composition = self.composition_input.text()
        classe = self.classe_input.text()
        statut = self.statut_input.text()
        code_atc = self.code_atc_input.text()
        ppv = self.ppv_input.text()
        prix_hosp = self.prix_hosp_input.text()
        tableau = self.tableau_input.text()
        indications = self.indication_input.text()
        min_stock = self.min_stock_input.text()
        stock_actuel = self.stock_actuel_input.text()
        url_medicament = self.url_medicament_input.text()

        # Vérifier les champs obligatoires
        if not nom or not code_ean:
            QMessageBox.warning(
                self.main_interface,
                "Erreur",
                "Le nom et le code EAN-13 sont obligatoires.",
            )
            return

        try:
            # Conversion des valeurs numériques si nécessaire
            ppv = float(ppv) if ppv else 0.0
            prix_hosp = float(prix_hosp) if prix_hosp else 0.0
            min_stock = int(min_stock) if min_stock else 0
            stock_actuel = int(stock_actuel) if stock_actuel else 0

            # Appel à la méthode du modèle (à adapter si nécessaire)
            if self.medicament_modif is not None:
                Medicament.modifier_medicament(
                    self.main_interface.conn,
                    self.medicament_modif["id_medicament"],
                    code_ean,
                    nom,
                    image_url,
                    presentation,
                    dosage,
                    fabricant,
                    composition,
                    classe,
                    statut,
                    code_atc,
                    ppv,
                    prix_hosp,
                    tableau,
                    indications,
                    min_stock,
                    stock_actuel,
                    url_medicament,
                )
                # Message de succès
                QMessageBox.information(
                    self.main_interface, "Succès", "Médicament modifié avec succès."
                )
            else:
                Medicament.ajouter_medicament(
                    self.main_interface.conn,
                    code_ean,
                    nom,
                    image_url,
                    presentation,
                    dosage,
                    fabricant,
                    composition,
                    classe,
                    statut,
                    code_atc,
                    ppv,
                    prix_hosp,
                    tableau,
                    indications,
                    min_stock,
                    stock_actuel,
                    url_medicament,
                )

                # Message de succès
                QMessageBox.information(
                    self.main_interface, "Succès", "Médicament ajouté avec succès."
                )
            self.show_ajouter_interface()

        except Exception as e:
            QMessageBox.warning(
                self.main_interface,
                "Erreur",
                f"Erreur lors de l'ajout du médicament : {str(e)}",
            )

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

    def update_medicament_to_db(self):
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

        # Vérifier les champs obligatoires
        if not (nom and code_ean):
            QMessageBox.warning(
                self.main_interface,
                "Erreur",
                "Le nom et le code EAN-13 sont obligatoires.",
            )
            return

        try:
            medicament_data = {
                "Nom": nom,
                "Caracteristique": caracteristique,
                "Code_EAN_13": code_ean,
                "Medicament_Generique": generique,
                "Prix_Officine": prix_officine,
                "PPV": prix_public,
                "Prix_Base_Remboursement": prix_remboursement,
                "Prix_Hospitalier": prix_hospitalier,
                "Substance_Active_DCI": substance,
                "Classe_Therapeutique": classe,
                "Min_Stock": min_v,
                "Stock_Actuel": 0,
            }

            Medicament.modifier_medicament(
                self.main_interface.conn,
                self.medicament_modif["id_medicament"],
                **medicament_data,
            )
            # Message de succès
            QMessageBox.information(
                self.main_interface, "Succès", "Médicament modifié avec succès."
            )
            self.clear_fields()
            self.show_ajouter_interface()

        except Exception as e:
            QMessageBox.warning(
                self.main_interface,
                "Erreur",
                "Un médicament avec ce code EAN-13 existe déjà.",
            )
