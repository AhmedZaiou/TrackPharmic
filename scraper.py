from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd
import json
import numpy as np
from tqdm import tqdm
from Backend.Datascraping.extraire_medicament import Scraper_medicament

from Backend.Dataset.medicament import Medicament

"""all_medicaments = pd.read_csv('/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Backend/Datascraping/scraper/medicaments.csv', encoding='utf-8-sig')
all_data_medicaments = {}
all_not = []
for url in tqdm(all_medicaments['url'].values, desc="Scraping des pages"):
    try:
        all_data_medicaments[url] = Scraper_medicament.scrap_medicament(url)
    except :
        all_not.append(url)
    if len(all_data_medicaments) % 10 == 0:
        with open("/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Backend/Datascraping/scraper/medicament_info.json", "w", encoding="utf-8") as f:
            json.dump(all_data_medicaments, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(all_data_medicaments)} records to medicament_info.json")
    
all_data_medicaments['Not'] = all_not
with open("/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Backend/Datascraping/scraper/medicament_info.json", "w", encoding="utf-8") as f:
    json.dump(all_data_medicaments, f, ensure_ascii=False, indent=4)"""

data_path = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Backend/Datascraping/scraper/medicament_info.json"
with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

codes_url = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Backend/Datascraping/scraper/codee_url.json"
with open(codes_url, "r", encoding="utf-8") as f:
    codes_url_data = json.load(f)

codes_url_data = {codes_url_data[k]: k for k in codes_url_data}

data.pop('Not', None)

new_data = []
for i in data:
    try:
        data[i]["Code_EAN_13"] = codes_url_data[i] if i in codes_url_data else None
    except:
        print(i)
    new_data.append(data[i])
pand_data = pd.DataFrame(new_data)


pand_data["Min_Stock"] = 0
pand_data["Stock_Actuel"] = 0
pand_data = pand_data[["Code_EAN_13", "Nom", "Image URL","Présentation","Dosage", "Distributeur ou fabriquant", "Composition", "Classe thérapeutique","Statut",
                       "Code ATC","PPV", "Prix hospitalier","Tableau", "Indication(s)","Min_Stock","Stock_Actuel","url"]]


pand_data.rename(columns={"Image URL": "Image_URL", 'Distributeur ou fabriquant': "Distributeur_ou_fabriquant", "Classe thérapeutique": "Classe_thérapeutique","Code ATC": "Code_ATC","Prix hospitalier": "Prix_hospitalier", "Indication(s)": "Indications", "url" : "url_medicament"}, inplace=True)
pand_data.to_csv("/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Backend/Datascraping/scraper/medicament_info_with_Codes.csv", index=False, encoding='utf-8-sig')

pand_data.replace({np.nan: None}, inplace=True)
Medicament.ajouter_medicament_data_frame(pand_data)



