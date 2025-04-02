import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_medicaments(url):
    # Télécharger le contenu de la page
    response = requests.get(url,  verify=False)
    if response.status_code != 200:
        print(f"Erreur lors de l'accès à la page: {response.status_code}")
        return None

    # Parse le HTML avec BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Trouver la section des médicaments
    medicament_table = soup.find("table")  # Supposant que les médicaments sont dans une table
    if not medicament_table:
        print("Table des médicaments introuvable.")
        return None

    # Extraire les données des lignes du tableau
    medicament_data = []
    headers = [header.text.strip() for header in medicament_table.find_all("th")]

    for row in medicament_table.find_all("tr")[1:]:  # Ignorer les en-têtes
        cols = [col.text.strip() for col in row.find_all("td")]
        if cols:
            medicament_data.append(dict(zip(headers, cols)))

    return medicament_data

# URL cible
url = "https://dmp.sante.gov.ma/basesdedonnes/listes-medicaments"

list_url = [f"https://dmp.sante.gov.ma/basesdedonnes/listes-medicaments?page={i}&search=" for i in range(2,200)]
list_url.append(url)
# Scraper les données
data=[]
for url in list_url:

    data += scrape_medicaments(url)
pd.DataFrame(data).to_csv("/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/Datascraping/scrapedData/DMPdata-ppp.csv")
