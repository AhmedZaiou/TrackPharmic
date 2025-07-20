from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

from Backend.Dataset.medicament import Medicament

class Scraper_medicament:
    @staticmethod
    def get_medicament_codeBarre(code_barre):
        url = f"https://medicament.ma/?choice=barcode&s={code_barre}"
        return Scraper_medicament.scrap_medicament(url=url, code_barre = code_barre)
    
    @staticmethod
    def scrap_medicament(url, code_barre = None , temps_sleep=3):
        options = Options()
        options.add_argument('--headless')  # mode sans interface
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Initialisation du navigateur
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(temps_sleep)

        html = driver.page_source 
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')
        data = {}
        h3_tag = soup.find("h3")
        data["Code_EAN_13"] = code_barre if code_barre else None
        data["Nom"] = h3_tag.get_text(strip=True) if h3_tag else None 
        img_tag = soup.select_one("div.only-mobile img")
        data["Image URL"] = img_tag["src"] if img_tag else None
        rows = soup.select("table.table-details tr")
        for row in rows:
            field = row.find("td", class_="field")
            value = row.find("td", class_="value")
            if field and value:
                key = field.get_text(strip=True)
                val = value.get_text(strip=True)
                data[key] = val
        def parse_prix(prix_str):
            """Convertit une chaîne de type '36.20 dhs' en float 36.20"""
            if prix_str:
                return float(prix_str.replace('dhs', '').strip())
            return None
        data["PPV"] = parse_prix(data.get("PPV"))
        data["Prix hospitalier"] = parse_prix(data.get("Prix hospitalier"))
        data["url"] = url 
        return data 
    

    @staticmethod
    def scrap_new_medicament():

        url = f"https://medicament.ma/"
        options = Options()
        options.add_argument('--headless')  # mode sans interface
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Initialisation du navigateur
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)

        html = driver.page_source 
        driver.quit() 

        soup = BeautifulSoup(html, 'html.parser')
    
        results = {}

        # Sélection des lignes du tableau
        rows = soup.select('table.table.table-striped tbody tr')
        for row in rows: 
            link_tag = row.find('a')
            url_medicament = link_tag['href']
            full_url = "https://medicament.ma" + url_medicament if url_medicament.startswith('/') else url_medicament
            results[full_url] = Scraper_medicament.scrap_medicament(url=full_url)
            
        return results
            









