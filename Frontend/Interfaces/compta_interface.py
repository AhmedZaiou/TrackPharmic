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
)
from qtpy.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from Backend.Dataset.credit import Credit
from Backend.Dataset.echanges import Echanges
from Backend.Dataset.payment import Payment
from Backend.Dataset.retour import Retour
from Backend.Dataset.ventes import Ventes
from datetime import datetime, timedelta
from decimal import Decimal
import calendar
from dateutil.relativedelta import relativedelta


class Compta_dash:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.show_vente_interface()

    def show_vente_interface(self):
        self.main_interface.clear_content_frame()

        self.vente_dash = QWidget()
        self.vente_dash.setObjectName("vente_dash")

        # Fetch data
        credit_jours = Credit.evolution_par_jour_moiis_courant()
        credit_mois = Credit.evolution_par_mois()
        echanges_jours = Echanges.evolution_par_jour_moiis_courant()
        echanges_jours_envoyer = echanges_jours['Echange_envoyer']
        echanges_jours_recu = echanges_jours['Echange_recu'] 
        echanges_mois = Echanges.evolution_par_mois()
        echanges_mois_envoyer = echanges_mois['Echange_envoyer']
        echanges_mois_recu = echanges_mois['Echange_recu'] 
        payment_jours = Payment.evolution_par_jour_moiis_courant()
        payment_mois = Payment.evolution_par_mois()
        retour_jours = Retour.evolution_par_jour_moiis_courant()
        retour_mois = Retour.evolution_par_mois()
        ventes_jours = Ventes.evolution_par_jour_moiis_courant()
        ventes_mois = Ventes.evolution_par_mois()
        

        # Transform data
        credit_jours = self.transformer_donnees(credit_jours)
        credit_mois = self.transformer_donnees_par_mois(credit_mois)
        echanges_jours_envoyer = self.transformer_donnees(echanges_jours_envoyer)
        echanges_jours_recu = self.transformer_donnees(echanges_jours_recu)
        echanges_mois_envoyer = self.transformer_donnees_par_mois(echanges_mois_envoyer)
        echanges_mois_recu = self.transformer_donnees_par_mois(echanges_mois_recu)
        payment_jours = self.transformer_donnees(payment_jours)
        payment_mois = self.transformer_donnees_par_mois(payment_mois)
        retour_jours = self.transformer_donnees(retour_jours)
        retour_mois = self.transformer_donnees_par_mois(retour_mois)
        ventes_jours = self.transformer_donnees(ventes_jours)
        ventes_mois = self.transformer_donnees_par_mois(ventes_mois)
        

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

        self.all_data_moi = {
            "mois": list(credit_mois.values())[0],
            "credits": list(credit_mois.values())[1],
            "echanges_envoyer": list(echanges_mois_envoyer.values())[1],
            "echanges_recu": list(echanges_mois_recu.values())[1],
            "paiements": list(payment_mois.values())[1],
            "retours": list(retour_mois.values())[1],
            "ventes": list(ventes_mois.values())[1],
        }

        

        # Generate and display figures
        self.generate_plots()

        # Add the widget to the main layout
        self.main_interface.content_layout.addWidget(self.vente_dash)

    def transformer_donnees(self, donnees):
        data_transformee = {'jours': [], 'ventes': []}
        aujourd_hui = datetime.today() 
        date_debut = aujourd_hui.replace(day=1)
        dernier_jour = datetime(aujourd_hui.year, aujourd_hui.month, calendar.monthrange(aujourd_hui.year, aujourd_hui.month)[1])

        date_fin = dernier_jour 
        date_courante = date_debut 
        while date_courante <= date_fin:
            date_str = date_courante.strftime('%d-%m')
            date_strP = date_courante.strftime('%Y-%m-%d')
            data_transformee['jours'].append(date_str)
            data_transformee['ventes'].append(float(donnees.get(date_strP, Decimal('0'))))
            date_courante += timedelta(days=1)
        return data_transformee

    def transformer_donnees_par_mois(self, donnees):
        data_transformee = {'mois': [], 'ventes': []}
        aujourd_hui = datetime.today() 
        mois_debut = datetime(aujourd_hui.year, 1, 1)
        mois_fin = aujourd_hui 
        mois_courant = mois_debut
        while mois_courant <= mois_fin:
            mois_str = mois_courant.strftime('%Y-%m')
            data_transformee['mois'].append(mois_str)
            total_ventes = donnees.get(mois_str, Decimal('0'))
            data_transformee['ventes'].append(float(total_ventes))
            if mois_courant.month == 12:
                mois_courant = mois_courant.replace(year=mois_courant.year + 1, month=1)
            else:
                mois_courant = mois_courant.replace(month=mois_courant.month + 1)
        return data_transformee

    def generate_plots(self):
        # Create figures for the daily data 
        fig1, ax1 = plt.subplots()
        plt.xticks(rotation=90)
        ax1.plot(self.all_data_jour["jours"], self.all_data_jour["ventes"], label="Ventes quotidiennes", marker='o')
        ax1.plot(self.all_data_jour["jours"], self.all_data_jour["credits"], label="Crédits", linestyle='--', marker='o')
        ax1.plot(self.all_data_jour["jours"], self.all_data_jour["echanges_envoyer"], label="Échanges envoyés", linestyle='-.', marker='o')
        ax1.plot(self.all_data_jour["jours"], self.all_data_jour["echanges_recu"], label="Échanges reçus", linestyle=':', marker='o')
        ax1.plot(self.all_data_jour["jours"], self.all_data_jour["paiements"], label="Paiements", linestyle='-.', marker='o')
        ax1.plot(self.all_data_jour["jours"], self.all_data_jour["retours"], label="Retours", linestyle='--', marker='o')
        ax1.set_title("Ventes quotidiennes et autres données")
        ax1.set_xlabel("Jours")
        ax1.set_ylabel("Valeur")
        
        ax1.legend()

        # Create figures for the monthly data
        fig2, ax2 = plt.subplots()
        ax2.plot(self.all_data_moi["mois"], self.all_data_moi["ventes"], label="Ventes mensuelles", color="orange", marker='o')
        ax2.plot(self.all_data_moi["mois"], self.all_data_moi["credits"], label="Crédits mensuels", linestyle='--', marker='o')
        ax2.plot(self.all_data_moi["mois"], self.all_data_moi["echanges_envoyer"], label="Échanges envoyés mensuels", linestyle='-.', marker='o')
        ax2.plot(self.all_data_moi["mois"], self.all_data_moi["echanges_recu"], label="Échanges reçus mensuels", linestyle=':', marker='o')
        ax2.plot(self.all_data_moi["mois"], self.all_data_moi["paiements"], label="Paiements mensuels", linestyle='-.', marker='o')
        ax2.plot(self.all_data_moi["mois"], self.all_data_moi["retours"], label="Retours mensuels", linestyle='--', marker='o')
        ax2.set_title("Ventes mensuelles et autres données")
        ax2.set_xlabel("Mois")
        ax2.set_ylabel("Valeur")
        ax2.legend()

        # Create a canvas for each plot to be displayed in the Qt interface
        self.canvas1 = FigureCanvas(fig1)
        self.canvas2 = FigureCanvas(fig2)

        # Add the canvases to the layout of the interface
        layout = QVBoxLayout()

        titre_vente_q = QLabel("Ventes quotidiennes et autres données")
        titre_vente_q.setAlignment(Qt.AlignCenter)
        titre_vente_q.setObjectName("TitrePage")
        layout.addWidget(titre_vente_q) 
        layout.addWidget(self.canvas1) 
        titre_vente_m = QLabel("Ventes mensuelles et autres données")
        titre_vente_m.setAlignment(Qt.AlignCenter)
        titre_vente_m.setObjectName("TitrePage")
        layout.addWidget(titre_vente_m) 
        layout.addWidget(self.canvas2)

        # Set the layout for the vente_dash widget
        self.vente_dash.setLayout(layout)



