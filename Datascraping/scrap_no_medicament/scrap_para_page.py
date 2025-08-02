import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

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
import os
from tqdm import tqdm   


def scrape_page(url, code_barre=None, temps_sleep=3):
    options = Options()
    options.add_argument("--headless")  # mode sans interface
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialisation du navigateur
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(temps_sleep)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    #class="woocommerce-LoopProduct-link woocommerce-loop-product__link"
    product_main = soup.find("div", class_="product-main")
    product_footer = soup.find("div", class_="product-footer")

    data = {}

    h1 = product_main.select_one("h1.product_title")
    data["titre"] = h1.get_text(strip=True) if h1 else None
    price_tag = product_main.select_one(".price-wrapper .woocommerce-Price-amount.amount bdi")
    if price_tag:
        raw = price_tag.get_text(strip=True)
        # ex: "185,00 MAD"
        # scission nombre + devise
        parts = raw.replace("\u00A0", " ").split(" ")
        if len(parts) >= 2:
            prix = parts[0].replace(",", ".").strip()
            dev = parts[-1].strip()
        else:
            prix = raw
            dev = None
        data["prix"] = prix
        data["devise"] = dev
    else:
        data["prix"] = data["devise"] = None
    
    code = product_main.select_one("span.stl_codenum")
    data["code_bar"] = code.get_text(strip=True) if code else None

    if data["code_bar"] == 'N/A' :
        data["code_bar"]  = product_main.select_one("span.sku").get_text(strip=True)
    

    # 5. Catégories et étiquettes
    data["categories"] = "\n".join([
        a.get_text(strip=True) for a in product_main.select("span.posted_in a[rel='tag']")
    ])
    data["tags"] = "\n".join([
        a.get_text(strip=True) for a in product_main.select("span.tagged_as a[rel='tag']")
    ])
    # 6. Images (grandes) depuis la galerie
    images = []
    for img in soup.select(".woocommerce-product-gallery__image a img"):
        # essaie data-large_image puis data-src ou src
        url = (
            img.get("data-large_image")
            or img.get("data-src")
            or img.get("src")
            or img.get("data-thumb")
        )
        if url and url not in images:
            images.append(url)
    data["images"] = images[0] if len(images)>0 else None

    # 2. Paragraphes de description
    descriptions = "\n".join([p.get_text(strip=True) for p in product_footer.find_all("p", class_="font_7") if p.get_text(strip=True)])

    # 3. Caractéristiques
    caracteristiques = "\n".join([p.get_text(strip=True) for p in product_footer.find_all("p", class_="font_6")])

    data["descriptions"] = descriptions
    data["caracteristiques"] = caracteristiques
    data["url"] = url


    return data






 


 

if __name__ == "__main__":

    dossier = "/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Datascraping/scrap_no_medicament/resultats"
    dfs = []
    # Parcours de tous les fichiers CSV
    for nom_fichier in os.listdir(dossier):
        if nom_fichier.endswith(".csv"):
            chemin_fichier = os.path.join(dossier, nom_fichier)
            df = pd.read_csv(chemin_fichier)   
            dfs.append(df)
    
    df_concat = pd.concat(dfs, ignore_index=True)

    for url in tqdm(df_concat['url'].values[26:]):
        try:
            data_total = scrape_page(url) 

            if data_total['code_bar'] != 'N/A':
                # save json
                with open(f"/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Datascraping/scrap_no_medicament/results_jsons/{data_total['code_bar']}.json", "w") as f:
                    json.dump(data_total, f, ensure_ascii=False, indent=4)
            else:
                with open(f"/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Datascraping/scrap_no_medicament/results_jsons/{data_total['titre']}.json", "w") as f:
                    json.dump(data_total, f, ensure_ascii=False, indent=4) 
        except Exception as e:
            print(f"Erreur lors du traitement de l'URL {url}: {e}")
            continue
         

 