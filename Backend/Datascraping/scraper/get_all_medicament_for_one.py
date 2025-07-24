from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd

# Configuration des options du navigateur


def scrap_page_url(url, temps_sleep=3):
    options = Options()
    options.add_argument("--headless")  # Exécution en mode sans interface graphique
    # Initialisation du navigateur
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(temps_sleep)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")
    soup_tbody = soup.find("tbody")
    rows = soup_tbody.find_all("tr") if soup_tbody else []
    list_of_medicaments = []
    for i in range(len(rows)):
        scoup_row = rows[i]
        a_tag = scoup_row.find("a")
        url = a_tag["href"]
        details_span = a_tag.find("span", class_="details")
        name = details_span.contents[0].strip()
        small_span = details_span.find("span", class_="small")
        details = small_span.text.strip()
        medicament_info = {"url": url, "name": name, "details": details}
        list_of_medicaments.append(medicament_info)
    return list_of_medicaments


alphabet = [chr(i) for i in range(ord("A"), ord("Z") + 1)]

list_of_medicaments_complete = []
list_of_medicaments_complete_traited = []
for alpha in alphabet:
    for i in range(1, 1000):
        print(f"Traitement de la page {i} pour la lettre {alpha}")
        url = f"https://medicament.ma/listing-des-medicaments/page/{i}/?lettre={alpha}"
        try:
            list_of_medicaments = scrap_page_url(url)
        except:
            print(f"Erreur lors de la récupération de la page {url}")
            break
        list_of_medicaments_complete_traited.append((alpha, i))
        if len(list_of_medicaments) == 0:
            break
        else:
            list_of_medicaments_complete.extend(list_of_medicaments)

print(len(list_of_medicaments_complete))
pd.DataFrame(list_of_medicaments_complete).to_csv(
    "medicaments.csv", index=False, encoding="utf-8-sig"
)
with open("medicaments_traiter.txt", "w", encoding="utf-8") as f:
    for item in list_of_medicaments_complete_traited:
        f.write(str(item) + "\n")
