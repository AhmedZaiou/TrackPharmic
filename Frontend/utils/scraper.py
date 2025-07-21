from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSignal
from Backend.Datascraping.extraire_medicament import Scraper_medicament
from Backend.Dataset.medicament import Medicament
from Backend.Dataset.todo_task import Todo_Task
import threading
import time 



def actualiser_medicament(conn):
    if Todo_Task.test_scrapper(conn):  
        data = Scraper_medicament.scrap_new_medicament()
        
        for key in data:  
            if Medicament.test_existance_url(conn,data[key].get('url')):
                continue
            Code_EAN_13 = data[key].get('Code_EAN_13')
            Nom = data[key].get('Nom')
            Image_URL = data[key].get('Image URL')
            Présentation = data[key].get('Présentation')
            Dosage = data[key].get('Dosage')
            Distributeur_ou_fabriquant = data[key].get('Distributeur ou fabriquant')
            Composition = data[key].get('Composition')
            Classe_thérapeutique = data[key].get('Classe thérapeutique')
            Statut = data[key].get('Statut')
            Code_ATC = data[key].get('Code ATC')
            PPV = data[key].get('PPV')
            Prix_hospitalier =  data[key].get('Prix hospitalier')
            Tableau =   data[key].get('Tableau')
            Indications =   data[key].get('Indication(s)') 
            Min_Stock   = 0
            Stock_Actuel =  0
            url_medicament = data[key].get('url')
            Medicament.ajouter_medicament(conn,Code_EAN_13,
                Nom,
                Image_URL,
                Présentation,
                Dosage,
                Distributeur_ou_fabriquant,
                Composition,
                Classe_thérapeutique,
                Statut,
                Code_ATC,
                PPV,
                Prix_hospitalier,
                Tableau,
                Indications,
                Min_Stock,
                Stock_Actuel,
                url_medicament) 
        Todo_Task.scraper_today() 


from PyQt5.QtCore import QThread

class Worker(QThread):

    def __init__(self, conn):
        super().__init__()
        self.conn = conn
    def run(self):
        actualiser_medicament(self.conn) 