from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QHeaderView,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QTextEdit,
    QMessageBox,
)
from qtpy.QtCore import Qt
from Backend.Dataset.client import Clients
from Backend.Dataset.payment import Payment
from Backend.Dataset.credit import Credit
from Backend.Dataset.retour import Retour
from Backend.Dataset.ventes import Ventes
from Backend.Dataset.medicament import Medicament
from decimal import Decimal

import pandas as pd
from datetime import datetime


class Credit_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()

    def show_vente_interface(self):
        self.main_interface.clear_content_frame()

        self.credit_dash = QWidget()
        self.credit_dash.setObjectName("credit_dash")

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.credit_dash)

        titre_page = QLabel("Gestion de credit")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titre_page)

        self.table = QTableWidget()
        self.table.setColumnCount(5)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(
            ["Id", "Nom Prénom", "CIN", "Téléphone", "Crédit actuel"]
        )
        self.remplir_tableau()
        self.table.cellClicked.connect(self.credit_selected)

        # Search bar for filtering
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Chercher par 'Nom'...")
        self.search_bar.textChanged.connect(
            self.filter_table
        )  # Trigger filter when text changes

        main_layout.addWidget(self.search_bar)

        main_layout.addWidget(self.table)

        self.main_interface.content_layout.addWidget(self.credit_dash)

    def filter_table(self):
        # if not self.all_data:
        #    self.load_all_data()
        # Get the filter text from the search bar
        filter_text = self.search_bar.text().lower()

        # Loop through all rows and hide/show them based on the search
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)  # Assuming column 0 is 'Nom'
            if item is not None:
                if filter_text in item.text().lower():  # Case-insensitive comparison
                    self.table.setRowHidden(row, False)
                else:
                    self.table.setRowHidden(row, True)

    def remplir_tableau(self):
        # Exemple de données fictives
        credits = Clients.extraire_tous_clients_with_credit(self.main_interface.conn)
        credits = [dict(i) for i in credits]
        self.table.setRowCount(len(credits))
        for row, credit in enumerate(credits):
            self.table.setItem(row, 0, QTableWidgetItem(str(credit["id_client"])))
            self.table.setItem(
                row, 1, QTableWidgetItem(credit["nom"] + " " + credit["prenom"])
            )
            self.table.setItem(row, 2, QTableWidgetItem(credit["cin"]))
            self.table.setItem(row, 3, QTableWidgetItem(credit["telephone"]))
            self.table.setItem(row, 4, QTableWidgetItem(str(credit["credit_actuel"])))

    def credit_selected(self, row, column):
        self.id_client = self.table.item(row, 0).text()
        self.show_payment_interface()

    def show_payment_interface(self):
        self.main_interface.clear_content_frame()
        self.credit_dash = QWidget()
        self.credit_dash.setObjectName("credit_dash")

        # Widget central
        # Layout principal
        main_layout = QVBoxLayout(self.credit_dash)

        titre_page = QLabel("Gestion des paiements de crédit")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titre_page)

        table_form_layout = QGridLayout()

        self.client = Clients.extraire_client(self.main_interface.conn, self.id_client)
        self.client = dict(self.client)

        table_form_layout.addWidget(QLabel("Nom :"), 0, 0)
        table_form_layout.addWidget(QLabel(self.client["nom"]), 0, 1)
        table_form_layout.addWidget(QLabel("Prénom :"), 0, 2)
        table_form_layout.addWidget(QLabel(self.client["prenom"]), 0, 3)

        table_form_layout.addWidget(QLabel("CIN :"), 1, 0)
        table_form_layout.addWidget(QLabel(self.client["cin"]), 1, 1)
        table_form_layout.addWidget(QLabel("Téléphone :"), 1, 2)
        table_form_layout.addWidget(QLabel(self.client["telephone"]), 1, 3)

        table_form_layout.addWidget(QLabel("Email :"), 2, 0)
        table_form_layout.addWidget(QLabel(self.client["email"]), 2, 1)
        table_form_layout.addWidget(QLabel("Adresse :"), 2, 2)
        table_form_layout.addWidget(QLabel(self.client["adresse"]), 2, 3)

        table_form_layout.addWidget(QLabel("Crédit Maximum"), 3, 0)
        table_form_layout.addWidget(QLabel(str(self.client["max_credit"])), 3, 1)
        table_form_layout.addWidget(QLabel("Crédit Actuel"), 3, 2)
        table_form_layout.addWidget(QLabel(str(self.client["credit_actuel"])), 3, 3)

        self.payment_input = QDoubleSpinBox()
        self.payment_input.setMinimum(0)  # Valeur minimale
        self.payment_input.setMaximum(
            float(self.client["credit_actuel"])
        )  # Valeur maximale

        self.submit_button = QPushButton("Payer")
        self.submit_button.clicked.connect(self.add_paiment)

        table_form_layout.addWidget(QLabel("Effectuer un paiement :"), 4, 0)
        table_form_layout.addWidget(self.payment_input, 4, 1)
        table_form_layout.addWidget(self.submit_button, 4, 3)
        main_layout.addLayout(table_form_layout)

        self.list_factures = QTableWidget(0, 4)
        self.list_factures.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list_factures.setHorizontalHeaderLabels(
            ["Type", "Numéro de Facture", "Total", "Date"]
        )
        self.remplire_table()
        main_layout.addWidget(self.list_factures)
        self.main_interface.content_layout.addWidget(self.credit_dash)
        self.list_factures.cellClicked.connect(self.show_facture)

        # add click

    def show_facture(self, row, column):
        numero_facture = self.list_factures.item(row, 1).text()
        if self.list_factures.item(row, 0).text() != "Credit":
            return
        vente = Ventes.extraire_ventes_par_numero_facture(
            self.main_interface.conn, numero_facture
        )
        payment = Payment.extraire_paiements_par_numero_facture(
            self.main_interface.conn, numero_facture
        )
        credit = Credit.extraire_credits_par_numero_facture(
            self.main_interface.conn, numero_facture
        )
        retour = Retour.extraire_retours_par_numero_facture(
            self.main_interface.conn, numero_facture
        )

        client = Clients.extraire_client(
            self.main_interface.conn, vente[0]["id_client"]
        )

        # Construction du message
        message = f"""
        <!DOCTYPE html>
        <html>
        <body>
            <h2>RACHAD TAZA</h2>
            <p><strong>Adresse :</strong> Hay Rachad, Bloc2, n:75, Taza</p>
            <p><strong>Téléphone :</strong> 0535285298, 0680061368</p>  
            <p>Facture n°: {numero_facture}</p>
            <p><strong>Agent :</strong> {vente[0]['id_salarie']}</p>
            <hr>
        """

        if client["nom"] != "Anonyme":
            message += f"""
            <h4>Client:</h4>
            <p><strong>Nom :</strong> {client['nom']} {client['prenom']}</p>
            <p><strong>CIN :</strong> {client['cin']}</p>
            <p><strong>Crédit Actuel :</strong> {client['credit_actuel']} Dh</p>
            <hr>
            """

        message += """
            <h4>Détails de la vente:</h4>
            <table border="1" cellspacing="0" cellpadding="5">
            <tr>
                <th>Produit</th>
                <th>Qu</th>
                <th>PU</th>
                <th>Total</th>
            </tr>
        """
        total_facture_calculer = 0

        for item in vente:
            medicament = Medicament.extraire_medicament(
                self.main_interface.conn, item["id_medicament"]
            )
            message += f"<tr><td>{medicament['Nom']}</td><td>{item['quantite_vendue']}</td><td>{item['prix_vente']} Dh</td><td>{item['quantite_vendue']*item['prix_vente']} Dh</td></tr>"
            total_facture_calculer += item["quantite_vendue"] * item["prix_vente"]
        message += """
            </table>
            <hr> 
        """

        message1 = """ 
            <h4>Paiements:</h4>
            <pre>
        """
        if payment:
            for p in payment:
                message1 += f"  - Paiement: {p}\n"
        else:
            message1 += "  Aucun paiement enregistré.\n"

        message1 += """
            </pre>
            <h4>Crédits:</h4>
            <pre>
        """

        message1 += """ 
            <table border="1" cellspacing="0" cellpadding="5">
            <tr>
                <th>Montant payé</th>
                <th>Reste</th>
                <th>Date dernier paiement</th>
                <th>Statut </th>
            </tr>
        """
        rest_a_payer = 0
        for c in credit:
            message1 += f"<tr><td>{c['montant_paye']} Dh</td><td>{c['reste_a_payer']} Dh</td><td>{c['date_dernier_paiement']} Dh</td><td>{c['statut']} </td></tr>"
            rest_a_payer += c["reste_a_payer"]
        message1 += """
                    </table>
                    <hr> 
                """
        message1 += """
            </pre>
            <h4>Retours:</h4>
            <pre>
        """
        if retour:
            for r in retour:
                message1 += f"  - Retour: {r}\n"
        else:
            message1 += "  Aucun retour enregistré.\n"

        message += f"""
            </pre>
            <hr>
            <p><strong>Total facture :</strong> {total_facture_calculer} Dh</p>
            <p><strong>Montant payé :</strong> {0} Dh</p>
            <p><strong>Reste à payer :</strong> {rest_a_payer} Dh</p>
            <hr> 
            <p><em>Merci pour votre achat!</em></p>
            <p><strong>Date :</strong> {vente[0]['date_vente']}</p>
        </body>
        </html>
        """

        # Affichage
        QMessageBox.information(self.main_interface, "Crédit insuffisant", message)

    def add_paiment(self):
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        montant_paye = self.payment_input.value()
        id_salarie = self.main_interface.user_session["id_salarie"]
        Payment.ajouter_payment(
            self.main_interface.conn,
            self.id_client,
            int(now.timestamp()),
            montant_paye,
            now_str,
            id_salarie,
        )
        Clients.ajouter_credit_client(
            self.main_interface.conn, self.id_client, -montant_paye
        )
        self.show_payment_interface()

    def remplire_table(self):
        all_credit = Credit.extraire_credit_with_id_client(
            self.main_interface.conn, self.id_client
        )
        all_paiment = Payment.extraire_payment_with_id_client(
            self.main_interface.conn, self.id_client
        )
        if len(all_credit) == 0:
            all_credit = pd.DataFrame(
                columns=["numero_facture", "reste_a_payer", "date_dernier_paiement"]
            )
        else:
            all_credit = pd.DataFrame(all_credit)[
                ["numero_facture", "reste_a_payer", "date_dernier_paiement"]
            ]

        if len(all_paiment) == 0:
            all_paiment = pd.DataFrame(
                columns=["numero_facture", "montant_paye", "date_paiement"]
            )
        else:
            all_paiment = pd.DataFrame(all_paiment)[
                ["numero_facture", "montant_paye", "date_paiement"]
            ]
        all_credit.rename(
            columns={"reste_a_payer": "Totale", "date_dernier_paiement": "Date"},
            inplace=True,
        )
        all_paiment.rename(
            columns={"montant_paye": "Totale", "date_paiement": "Date"}, inplace=True
        )
        all_credit["Type"] = "Credit"
        all_paiment["Type"] = "Paiment"

        result = pd.concat([all_credit, all_paiment], ignore_index=True)
        result["Date"] = pd.to_datetime(
            result["Date"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
        )
        result = result.sort_values(
            by="Date", ascending=False, ignore_index=True
        ).reset_index()

        self.list_factures.setRowCount(len(result))
        for row, element in result.iterrows():
            self.list_factures.setItem(row, 0, QTableWidgetItem(str(element["Type"])))
            self.list_factures.setItem(
                row, 1, QTableWidgetItem(str(element["numero_facture"]))
            )
            self.list_factures.setItem(row, 2, QTableWidgetItem(str(element["Totale"])))
            self.list_factures.setItem(row, 3, QTableWidgetItem(str(element["Date"])))
