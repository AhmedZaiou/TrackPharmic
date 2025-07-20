from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import json
from tqdm import tqdm

def rechercher_medicament_par_code_barres(code_barres):
    url = f"https://medicament.ma/?choice=barcode&s={code_barres}"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(), options=options)
    try:
        driver.get(url)  
        url_finale = driver.current_url 
    except Exception as e:
        print(f"Erreur : {e}")
        url_finale = None
    finally:
        driver.quit()
        return url_finale


data = pd.read_csv("codes.csv")
code_barres = {}

for code_barre in tqdm(data['code'].values, desc="Scraping des pages"):
    url = rechercher_medicament_par_code_barres(code_barre)
    code_barres[str(code_barre)] = url   
    if len(code_barres) % 100 == 0:
        with open("codee_url.json", "w", encoding="utf-8") as f:
            json.dump(code_barres, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(code_barres)} records to codee_url.json")
with open("codee_url.json", "w", encoding="utf-8") as f:
    json.dump(code_barres, f, ensure_ascii=False, indent=4)
