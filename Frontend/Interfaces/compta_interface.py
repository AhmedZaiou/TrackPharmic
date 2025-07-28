from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QFileDialog,
    QMessageBox,
)
from qtpy.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import shutil
from Backend.Dataset.credit import Credit
from Backend.Dataset.echanges import Echanges
from Backend.Dataset.payment import Payment
from Backend.Dataset.retour import Retour
from Backend.Dataset.ventes import Ventes
from datetime import datetime, timedelta
from decimal import Decimal
import calendar
from Backend.Dataset.compta_files import ComptaFilesGeneration
from dateutil.relativedelta import relativedelta
import random


class Compta_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_interface_actuel()

    def create_menu_compta(self):
        menu_layout = QHBoxLayout()
        self.compta_actuel = QPushButton("Analyse instantanée des indicateurs clés")
        self.compta_actuel.clicked.connect(self.compta_actuel_fc)
        menu_layout.addWidget(self.compta_actuel)

        self.compta_quotidiennes = QPushButton("Évolution quotidienne")
        self.compta_quotidiennes.clicked.connect(self.compta_quotidiennes_fc)
        menu_layout.addWidget(self.compta_quotidiennes)
        self.compta_mensuelles = QPushButton("Évolution mensuelles")
        self.compta_mensuelles.clicked.connect(self.compta_mensuelles_fc)
        menu_layout.addWidget(self.compta_mensuelles)
        self.telecharger_document_btn = QPushButton("Telécharger le rapport")
        self.telecharger_document_btn.clicked.connect(self.telecharger_document)
        menu_layout.addWidget(self.telecharger_document_btn)
        return menu_layout

    def compta_actuel_fc(self):
        self.show_interface_actuel()

    def compta_quotidiennes_fc(self):
        self.show_interface_qoutidiennes()

    def compta_mensuelles_fc(self):
        self.show_interface_mensuelles()

    def generer_all_data_jour(self, nb_jours=30):
        # Génère les dates des nb_jours derniers jours
        import datetime

        jours = [
            (datetime.date.today() - datetime.timedelta(days=i)).strftime("%d-%m")
            for i in range(nb_jours)
        ][::-1]

        # Génère des valeurs aléatoires pour chaque type de donnée
        credits = [random.randint(500, 5000) for _ in range(nb_jours)]
        echanges_envoyer = [random.randint(0, 2000) for _ in range(nb_jours)]
        echanges_recu = [random.randint(0, 2000) for _ in range(nb_jours)]
        paiements = [random.randint(300, 4000) for _ in range(nb_jours)]
        retours = [random.randint(0, 500) for _ in range(nb_jours)]
        ventes = [random.randint(500, 6000) for _ in range(nb_jours)]

        # Construction du dictionnaire dans le format demandé
        all_data_jour = {
            "jours": jours,
            "credits": credits,
            "echanges_envoyer": echanges_envoyer,
            "echanges_recu": echanges_recu,
            "paiements": paiements,
            "retours": retours,
            "ventes": ventes,
        }
        return all_data_jour

    def generer_all_data_mois(self, nb_jours=12):
        # Génère les dates des nb_jours derniers jours
        import datetime

        jours = [str(i + 1) for i in range(nb_jours)]

        # Génère des valeurs aléatoires pour chaque type de donnée
        credits = [random.randint(500, 5000) for _ in range(nb_jours)]
        echanges_envoyer = [random.randint(0, 2000) for _ in range(nb_jours)]
        echanges_recu = [random.randint(0, 2000) for _ in range(nb_jours)]
        paiements = [random.randint(300, 4000) for _ in range(nb_jours)]
        retours = [random.randint(0, 500) for _ in range(nb_jours)]
        ventes = [random.randint(500, 6000) for _ in range(nb_jours)]

        # Construction du dictionnaire dans le format demandé
        all_data_jour = {
            "mois": jours,
            "credits": credits,
            "echanges_envoyer": echanges_envoyer,
            "echanges_recu": echanges_recu,
            "paiements": paiements,
            "retours": retours,
            "ventes": ventes,
        }
        return all_data_jour

    def show_interface_actuel(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")
        self.main_layout = QVBoxLayout(self.vente_dash)

        titre_page = QLabel("Analyse et suivi des performances")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(titre_page)
        menu_layout = self.create_menu_compta()
        self.main_layout.addLayout(menu_layout)

        # Fetch data
        credit_jours = Credit.evolution_par_jour_moiis_courant(self.main_interface.conn)
        echanges_jours = Echanges.evolution_par_jour_moiis_courant(
            self.main_interface.conn
        )
        echanges_jours_envoyer = echanges_jours["Echange_envoyer"]
        echanges_jours_recu = echanges_jours["Echange_recu"]
        payment_jours = Payment.evolution_par_jour_moiis_courant(
            self.main_interface.conn
        )
        retour_jours = Retour.evolution_par_jour_moiis_courant(self.main_interface.conn)
        ventes_jours = Ventes.evolution_par_jour_moiis_courant(self.main_interface.conn)
        # Transform data
        credit_jours = self.transformer_donnees(credit_jours)
        echanges_jours_envoyer = self.transformer_donnees(echanges_jours_envoyer)
        echanges_jours_recu = self.transformer_donnees(echanges_jours_recu)
        payment_jours = self.transformer_donnees(payment_jours)
        retour_jours = self.transformer_donnees(retour_jours)
        ventes_jours = self.transformer_donnees(ventes_jours)

        self.all_data_jour = {
            "jours": list(credit_jours.values())[0],
            "credits": list(credit_jours.values())[1],
            "echanges_envoyer": list(echanges_jours_envoyer.values())[1],
            "echanges_recu": list(echanges_jours_recu.values())[1],
            "paiements": list(payment_jours.values())[1],
            "retours": list(retour_jours.values())[1],
            "ventes": list(ventes_jours.values())[1],
        }
        #self.all_data_jour = self.generer_all_data_jour(
        #    30
        #)  # Générer des données aléatoires pour les 30 derniers jours

        credit_mois = Credit.evolution_par_mois(self.main_interface.conn)
        echanges_mois = Echanges.evolution_par_mois(self.main_interface.conn)
        echanges_mois_envoyer = echanges_mois["Echange_envoyer"]
        echanges_mois_recu = echanges_mois["Echange_recu"]
        payment_mois = Payment.evolution_par_mois(self.main_interface.conn)
        retour_mois = Retour.evolution_par_mois(self.main_interface.conn)
        ventes_mois = Ventes.evolution_par_mois(self.main_interface.conn)

        # Transform data
        credit_mois = self.transformer_donnees_par_mois(credit_mois)
        echanges_mois_envoyer = self.transformer_donnees_par_mois(echanges_mois_envoyer)
        echanges_mois_recu = self.transformer_donnees_par_mois(echanges_mois_recu)
        payment_mois = self.transformer_donnees_par_mois(payment_mois)
        retour_mois = self.transformer_donnees_par_mois(retour_mois)
        ventes_mois = self.transformer_donnees_par_mois(ventes_mois)

        self.all_data_moi = {
            "mois": list(credit_mois.values())[0],
            "credits": list(credit_mois.values())[1],
            "echanges_envoyer": list(echanges_mois_envoyer.values())[1],
            "echanges_recu": list(echanges_mois_recu.values())[1],
            "paiements": list(payment_mois.values())[1],
            "retours": list(retour_mois.values())[1],
            "ventes": list(ventes_mois.values())[1],
        }
        #self.all_data_moi = self.generer_all_data_mois(
        #    12
        #)  # Générer des données aléatoires pour les 12 derniers mois

        aujourdhui = datetime.today().date()

        # Obtenir le jour du mois (1-31)
        jour_du_mois = aujourdhui.day - 1
        mois_du_annee = aujourdhui.month - 1

        values_to_plot_jour = [
            self.all_data_jour["credits"][jour_du_mois],
            self.all_data_jour["echanges_envoyer"][jour_du_mois],
            self.all_data_jour["echanges_recu"][jour_du_mois],
            self.all_data_jour["paiements"][jour_du_mois],
            self.all_data_jour["retours"][jour_du_mois],
            self.all_data_jour["ventes"][jour_du_mois],
        ]
        values_to_plot_mois = [
            self.all_data_moi["credits"][mois_du_annee],
            self.all_data_moi["echanges_envoyer"][mois_du_annee],
            self.all_data_moi["echanges_recu"][mois_du_annee],
            self.all_data_moi["paiements"][mois_du_annee],
            self.all_data_moi["retours"][mois_du_annee],
            self.all_data_moi["ventes"][mois_du_annee],
        ]

        values_to_plot_jour_sum = sum(values_to_plot_jour)
        values_to_plot_mois_sum = sum(values_to_plot_mois)

        self.canvas1 = self.generate_plot_actuel(
            values_to_plot_jour, "Bilan journalier"
        )
        self.canvas2 = self.generate_plot_actuel(values_to_plot_mois, "Bilan mensuel")

        self.canvas3 = self.generate_plot_actuel_deux(
            [values_to_plot_jour[0], values_to_plot_jour_sum - values_to_plot_jour[0]],
            "Crédits du jour",
        )
        self.canvas4 = self.generate_plot_actuel_deux(
            [values_to_plot_jour[1], values_to_plot_jour_sum - values_to_plot_jour[1]],
            "Échanges envoyés du jour",
        )
        self.canvas5 = self.generate_plot_actuel_deux(
            [values_to_plot_jour[2], values_to_plot_jour_sum - values_to_plot_jour[2]],
            "Échanges reçu du jour",
        )
        self.canvas6 = self.generate_plot_actuel_deux(
            [values_to_plot_jour[3], values_to_plot_jour_sum - values_to_plot_jour[3]],
            "Paiements du jour",
        )
        self.canvas7 = self.generate_plot_actuel_deux(
            [values_to_plot_jour[4], values_to_plot_jour_sum - values_to_plot_jour[4]],
            "Retours du jour",
        )
        self.canvas8 = self.generate_plot_actuel_deux(
            [values_to_plot_jour[5], values_to_plot_jour_sum - values_to_plot_jour[5]],
            "Ventes du jour",
        )

        self.canvas9 = self.generate_plot_actuel_deux(
            [values_to_plot_mois[0], values_to_plot_mois_sum - values_to_plot_mois[0]],
            "Crédits du mois",
        )
        self.canvas10 = self.generate_plot_actuel_deux(
            [values_to_plot_mois[1], values_to_plot_mois_sum - values_to_plot_mois[1]],
            "Échanges envoyés du mois",
        )
        self.canvas11 = self.generate_plot_actuel_deux(
            [values_to_plot_mois[2], values_to_plot_mois_sum - values_to_plot_mois[2]],
            "Échanges reçu du mois",
        )
        self.canvas12 = self.generate_plot_actuel_deux(
            [values_to_plot_mois[3], values_to_plot_mois_sum - values_to_plot_mois[3]],
            "Paiements du mois",
        )
        self.canvas13 = self.generate_plot_actuel_deux(
            [values_to_plot_mois[4], values_to_plot_mois_sum - values_to_plot_mois[4]],
            "Retours du mois",
        )
        self.canvas14 = self.generate_plot_actuel_deux(
            [values_to_plot_mois[5], values_to_plot_mois_sum - values_to_plot_mois[5]],
            "Ventes du mois",
        )

        # Layout principal vertical
        main_figure_layout = QVBoxLayout()

        # Ligne du haut avec 2 figures
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.canvas1)
        top_layout.addWidget(self.canvas2)

        # Ligne du bas avec 4 figures
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.canvas3)
        bottom_layout.addWidget(self.canvas4)
        bottom_layout.addWidget(self.canvas5)
        bottom_layout.addWidget(self.canvas6)
        bottom_layout.addWidget(self.canvas7)
        bottom_layout.addWidget(self.canvas8)

        bottom_layout_2 = QHBoxLayout()
        bottom_layout_2.addWidget(self.canvas9)
        bottom_layout_2.addWidget(self.canvas10)
        bottom_layout_2.addWidget(self.canvas11)
        bottom_layout_2.addWidget(self.canvas12)
        bottom_layout_2.addWidget(self.canvas13)
        bottom_layout_2.addWidget(self.canvas14)

        # Ajouter les deux lignes dans le layout principal vertical
        main_figure_layout.addLayout(top_layout)
        main_figure_layout.addLayout(bottom_layout)
        main_figure_layout.addLayout(bottom_layout_2)

        # Ajouter ce layout principal à la fenêtre (ou au widget parent)
        self.main_layout.addLayout(main_figure_layout)

        # Generate and display figures
        # self.generate_plots_quotidiennes()

        # Add the widget to the main layout
        self.main_interface.content_layout.addWidget(self.vente_dash)

    def show_interface_qoutidiennes(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")
        self.main_layout = QVBoxLayout(self.vente_dash)

        titre_page = QLabel("Analyse et suivi des performances")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(titre_page)

        menu_layout = self.create_menu_compta()
        self.main_layout.addLayout(menu_layout)

        # Fetch data
        credit_jours = Credit.evolution_par_jour_moiis_courant(self.main_interface.conn)
        echanges_jours = Echanges.evolution_par_jour_moiis_courant(
            self.main_interface.conn
        )
        echanges_jours_envoyer = echanges_jours["Echange_envoyer"]
        echanges_jours_recu = echanges_jours["Echange_recu"]
        payment_jours = Payment.evolution_par_jour_moiis_courant(
            self.main_interface.conn
        )
        retour_jours = Retour.evolution_par_jour_moiis_courant(self.main_interface.conn)
        ventes_jours = Ventes.evolution_par_jour_moiis_courant(self.main_interface.conn)

        # Transform data
        credit_jours = self.transformer_donnees(credit_jours)
        echanges_jours_envoyer = self.transformer_donnees(echanges_jours_envoyer)
        echanges_jours_recu = self.transformer_donnees(echanges_jours_recu)
        payment_jours = self.transformer_donnees(payment_jours)
        retour_jours = self.transformer_donnees(retour_jours)
        ventes_jours = self.transformer_donnees(ventes_jours)

        # Prepare data
        self.all_data_jour = {
            "jours": list(credit_jours.values())[0],
            "credits": list(credit_jours.values())[1],
            "echanges_envoyer": list(echanges_jours_envoyer.values())[1],
            "echanges_recu": list(echanges_jours_recu.values())[1],
            "paiements": list(payment_jours.values())[1],
            "retours": list(retour_jours.values())[1],
            "ventes": list(ventes_jours.values())[1],
        }

        #self.all_data_jour = self.generer_all_data_jour(
        #    30
        #)  # Générer des données aléatoires pour les 30 derniers jours

        # Generate and display figures
        self.generate_plots_quotidiennes()

        # Add the widget to the main layout
        self.main_interface.content_layout.addWidget(self.vente_dash)

    def show_interface_mensuelles(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")
        self.main_layout = QVBoxLayout(self.vente_dash)

        titre_page = QLabel("Analyse et suivi des performances")
        titre_page.setObjectName("TitrePage")
        titre_page.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(titre_page)

        menu_layout = self.create_menu_compta()
        self.main_layout.addLayout(menu_layout)

        credit_mois = Credit.evolution_par_mois(self.main_interface.conn)
        echanges_mois = Echanges.evolution_par_mois(self.main_interface.conn)
        echanges_mois_envoyer = echanges_mois["Echange_envoyer"]
        echanges_mois_recu = echanges_mois["Echange_recu"]
        payment_mois = Payment.evolution_par_mois(self.main_interface.conn)
        retour_mois = Retour.evolution_par_mois(self.main_interface.conn)
        ventes_mois = Ventes.evolution_par_mois(self.main_interface.conn)

        # Transform data
        credit_mois = self.transformer_donnees_par_mois(credit_mois)
        echanges_mois_envoyer = self.transformer_donnees_par_mois(echanges_mois_envoyer)
        echanges_mois_recu = self.transformer_donnees_par_mois(echanges_mois_recu)
        payment_mois = self.transformer_donnees_par_mois(payment_mois)
        retour_mois = self.transformer_donnees_par_mois(retour_mois)
        ventes_mois = self.transformer_donnees_par_mois(ventes_mois)

        self.all_data_moi = {
            "mois": list(credit_mois.values())[0],
            "credits": list(credit_mois.values())[1],
            "echanges_envoyer": list(echanges_mois_envoyer.values())[1],
            "echanges_recu": list(echanges_mois_recu.values())[1],
            "paiements": list(payment_mois.values())[1],
            "retours": list(retour_mois.values())[1],
            "ventes": list(ventes_mois.values())[1],
        }
        #self.all_data_moi = self.generer_all_data_mois(
        #    12
        #)  # Générer des données aléatoires pour les 12 derniers mois

        # Generate and display figures
        self.generate_plots_mensuelles()

        # Add the widget to the main layout
        self.main_interface.content_layout.addWidget(self.vente_dash)

    def telecharger_document(self):
        try:
            # 1. Génère le fichier avec ta classe métier
            chemin_fichier = ComptaFilesGeneration.extraire_vente(
                self.main_interface.conn
            )  # Suppose que cela retourne le chemin du fichier généré

            if not chemin_fichier:
                QMessageBox.warning(
                    self.main_interface, "Erreur", "La génération du fichier a échoué."
                )
                return

            # 2. Demande à l'utilisateur où enregistrer le fichier
            chemin_dest, _ = QFileDialog.getSaveFileName(
                self.main_interface,
                "Enregistrer le fichier",
                "Rapport.xlsx",
                "Fichiers Excel (*.xlsx);;Tous les fichiers (*)",
            )

            if chemin_dest:
                shutil.copy(chemin_fichier, chemin_dest)
                QMessageBox.information(
                    self.main_interface,
                    "Succès",
                    "Le document a été téléchargé avec succès.",
                )
            else:
                QMessageBox.information(
                    self.main_interface,
                    "Annulé",
                    "Téléchargement annulé par l'utilisateur.",
                )

        except Exception as e:
            QMessageBox.critical(
                self.main_interface, "Erreur", f"Une erreur est survenue :\n{str(e)}"
            )

    def transformer_donnees(self, donnees):
        data_transformee = {"jours": [], "ventes": []}
        aujourd_hui = datetime.today()
        date_debut = aujourd_hui.replace(day=1)
        dernier_jour = datetime(
            aujourd_hui.year,
            aujourd_hui.month,
            calendar.monthrange(aujourd_hui.year, aujourd_hui.month)[1],
        )

        date_fin = dernier_jour
        date_courante = date_debut
        while date_courante <= date_fin:
            date_str = date_courante.strftime("%d-%m")
            date_strP = date_courante.strftime("%Y-%m-%d")
            data_transformee["jours"].append(date_str)
            data_transformee["ventes"].append(
                float(donnees.get(date_strP, Decimal("0")))
            )
            date_courante += timedelta(days=1)
        return data_transformee

    def transformer_donnees_par_mois(self, donnees):
        data_transformee = {"mois": [], "ventes": []}
        aujourd_hui = datetime.today()
        mois_debut = datetime(aujourd_hui.year, 1, 1)
        mois_fin = aujourd_hui
        mois_courant = mois_debut
        while mois_courant <= mois_fin:
            mois_str = mois_courant.strftime("%Y-%m")
            data_transformee["mois"].append(mois_str)
            total_ventes = donnees.get(mois_str, Decimal("0"))
            data_transformee["ventes"].append(float(total_ventes))
            if mois_courant.month == 12:
                mois_courant = mois_courant.replace(year=mois_courant.year + 1, month=1)
            else:
                mois_courant = mois_courant.replace(month=mois_courant.month + 1)
        return data_transformee

    def generate_plots_quotidiennes(self):
        # Définir un style global plus lisible
        plt.style.use("bmh")
        font_properties = {"fontsize": 10}

        # --- Figure quotidienne ---
        fig1, ax1 = plt.subplots(figsize=(16, 12))
        ax1.plot(
            self.all_data_jour["jours"],
            self.all_data_jour["ventes"],
            label="Ventes",
            marker="o",
            linewidth=2,
        )
        ax1.plot(
            self.all_data_jour["jours"],
            self.all_data_jour["credits"],
            label="Crédits",
            linestyle="--",
            marker="s",
            linewidth=2,
        )
        ax1.plot(
            self.all_data_jour["jours"],
            self.all_data_jour["echanges_envoyer"],
            label="Échanges envoyés",
            linestyle="-.",
            marker="^",
            linewidth=2,
        )
        ax1.plot(
            self.all_data_jour["jours"],
            self.all_data_jour["echanges_recu"],
            label="Échanges reçus",
            linestyle=":",
            marker="v",
            linewidth=2,
        )
        ax1.plot(
            self.all_data_jour["jours"],
            self.all_data_jour["paiements"],
            label="Paiements",
            linestyle="-.",
            marker="D",
            linewidth=2,
        )
        ax1.plot(
            self.all_data_jour["jours"],
            self.all_data_jour["retours"],
            label="Retours",
            linestyle="--",
            marker="x",
            linewidth=2,
        )

        ax1.set_title(
            f" Les tendances quotidiennes pour le mois {self.all_data_jour['jours'][0].split('-')[1]}",
            fontsize=12,
            weight="bold",
        )
        ax1.set_xlabel("Jours", **font_properties)
        ax1.set_ylabel("Valeur en DH", **font_properties)
        ax1.tick_params(axis="x", rotation=45)
        ax1.legend(loc="upper left", fontsize=9)
        ax1.grid(True)
        ax1.set_facecolor("white")

        # --- Figure mensuelle ---

        # Création des canvases
        self.canvas1 = FigureCanvas(fig1)

        # Ajout à la layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas1)

        self.main_layout.addLayout(layout)

        # self.vente_dash.setLayout(layout)

    def generate_plot_actuel(self, values, titre):
        plt.style.use("bmh")
        font_properties = {"fontsize": 10}
        fig2, ax2 = plt.subplots(figsize=(4, 4))

        # Palette de couleurs personnalisée (pastel mais lisible)
        colors = ["#6A5ACD", "#20B2AA", "#FFD700", "#ADFF2F", "#FF69B4", "#ADFF2F"]
        labels = [
            "Crédits",
            "Échanges envoyés",
            "Échanges reçus",
            "Paiements",
            "Retours",
            "Ventes",
        ]
        if sum(values) == 0:
            values[-1] = 1
            ax2.pie(
                values,
                labels=labels,
                colors=colors,
                autopct="%1.1f%%",
                startangle=140,
                wedgeprops={"edgecolor": "white", "linewidth": 2},
            )
        else:
            ax2.pie(
                values,
                labels=labels,
                colors=colors,
                autopct="%1.1f%%",
                startangle=140,
                wedgeprops={"edgecolor": "white", "linewidth": 2},
            )
        ax2.set_title(titre, fontsize=14, fontweight="bold")
        ax2.axis("equal")  # Cercle parfait
        return FigureCanvas(fig2)

    def generate_plot_actuel_deux(self, values, titre):
        plt.style.use("bmh")
        fig2, ax2 = plt.subplots(figsize=(2, 2))

        # Palette de couleurs pour les bordures
        colors = ["#ADFF2F", "#E0E0E0"]

        # Si toutes les valeurs sont nulles, on met 1 pour afficher un cercle vide
        if sum(values) == 0:
            values[1] = 1

        # Création du donut avec intérieur blanc (couleur uniquement en bordure)
        wedges, texts = ax2.pie(
            values,
            colors=colors,
            startangle=140,
            wedgeprops={
                "edgecolor": "white",
                "linewidth": 2,
                "width": 0.3,
            },  # width contrôle l'épaisseur
        )

        total = values[0]
        ax2.text(
            0,
            0,
            f"{total:.2f} DHs",
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
        )

        # Titre
        ax2.set_title(titre, fontsize=7, fontweight="bold")
        ax2.axis("equal")  # Cercle parfait

        return FigureCanvas(fig2)

    def generate_plots_mensuelles(self):
        # Définir un style global plus lisible
        plt.style.use("bmh")
        font_properties = {"fontsize": 10}
        # --- Figure mensuelle ---
        fig2, ax2 = plt.subplots(figsize=(16, 12))
        ax2.plot(
            self.all_data_moi["mois"],
            self.all_data_moi["ventes"],
            label="Ventes",
            color="tab:orange",
            marker="o",
            linewidth=2,
        )
        ax2.plot(
            self.all_data_moi["mois"],
            self.all_data_moi["credits"],
            label="Crédits",
            linestyle="--",
            marker="s",
            linewidth=2,
        )
        ax2.plot(
            self.all_data_moi["mois"],
            self.all_data_moi["echanges_envoyer"],
            label="Échanges envoyés",
            linestyle="-.",
            marker="^",
            linewidth=2,
        )
        ax2.plot(
            self.all_data_moi["mois"],
            self.all_data_moi["echanges_recu"],
            label="Échanges reçus",
            linestyle=":",
            marker="v",
            linewidth=2,
        )
        ax2.plot(
            self.all_data_moi["mois"],
            self.all_data_moi["paiements"],
            label="Paiements",
            linestyle="-.",
            marker="D",
            linewidth=2,
        )
        ax2.plot(
            self.all_data_moi["mois"],
            self.all_data_moi["retours"],
            label="Retours",
            linestyle="--",
            marker="x",
            linewidth=2,
        )

        ax2.set_title(
            f"Les tendances mensuelles pour l'année {self.all_data_moi['mois'][0].split('-')[0]}",
            fontsize=12,
            weight="bold",
        )
        ax2.set_xlabel("Mois", **font_properties)
        ax2.set_ylabel("Valeur en DH", **font_properties)
        ax2.tick_params(axis="x", rotation=45)
        ax2.legend(loc="upper left", fontsize=9)
        ax2.grid(True)
        ax2.set_facecolor("white")

        self.canvas2 = FigureCanvas(fig2)

        # Ajout à la layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas2)
        self.main_layout.addLayout(layout)

        # self.vente_dash.setLayout(layout)
