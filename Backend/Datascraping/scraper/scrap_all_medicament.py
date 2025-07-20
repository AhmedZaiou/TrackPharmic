from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd
import json
from tqdm import tqdm
from Backend.Datascraping.extraire_medicament import Scraper_medicament

all_medicaments = pd.read_csv('medicaments.csv', encoding='utf-8-sig')
all_data_medicaments = {}
all_not = []
for url in tqdm(all_medicaments['url'].values, desc="Scraping des pages"):
    try:
        all_data_medicaments[url] = Scraper_medicament.scrap_medicament(url)
    except :
        all_not.append(url)
    if len(all_data_medicaments) % 10 == 0:
        with open("medicament_info.json", "w", encoding="utf-8") as f:
            json.dump(all_data_medicaments, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(all_data_medicaments)} records to medicament_info.json")
    
all_data_medicaments['Not'] = all_not
with open("medicament_info.json", "w", encoding="utf-8") as f:
    json.dump(all_data_medicaments, f, ensure_ascii=False, indent=4)