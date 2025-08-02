import requests
from bs4 import BeautifulSoup
import pandas as pd


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



def scrapelement(url, code_barre=None, temps_sleep=3):
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
    all_a = soup.find_all("a", href=True, class_="woocommerce-LoopProduct-link")

    rows = []
    for a in all_a:
        titre = a.get_text(strip=True)  # extrait le texte, sans espacement inutile
        url   = a["href"]               # direct car href existe grâce au href=True
        rows.append({"titre": titre, "url": url})
    return rows
 

def scrap_all_pages(url_base, end_page):
    data = scrapelement(url_base)
    data_total.extend(data)
    for i in range(1, end_page + 1):
        print(f"Scraping page {i}...")
        url = f"{url_base}/page/{i}/"
        data = scrapelement(url)
        data_total.extend(data)
    return data_total
 

if __name__ == "__main__":
    data_total = []
    end_page = 226

    url_base = f"https://citymall-para.ma/categorie/visage"

    name_type = url_base.split("/")[-1]

    data_total = scrap_all_pages(url_base, end_page)
    
    df = pd.DataFrame(data_total)
    
    df.to_csv(f"/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Datascraping/scrap_no_medicament/resultats/produits_{name_type}.csv", index=False, encoding="utf‑8")
    #print(f"✅ {len(df)} produits extraits et sauvegardés.")
    