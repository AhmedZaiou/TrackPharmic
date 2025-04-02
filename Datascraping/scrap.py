import requests
import urllib3
import certifi
import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib3
import os
from bs4 import BeautifulSoup

# Disable SSL warnings (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://ammps.sante.gov.ma/recherche-medicaments?page="

def get_total_pages():
    """Fetch the total number of pages from pagination."""
    response = requests.get(BASE_URL + "1", verify=False)  # Disable SSL verification
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pagination = soup.select_one("ul.pagination")
        if pagination:
            pages = [int(a.text) for a in pagination.find_all("a") if a.text.isdigit()]
            return max(pages) if pages else 1
    return 1  # Default to 1 page if pagination is not found
def save_html(page_number, soup):
    """Sauvegarde le contenu HTML dans un fichier."""
    file_path = os.path.join("./pages", f"page_{page_number}.html")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(soup.prettify())
def scrape_page(page_number):
    """Scrape a single page and extract medicine data."""
    url = BASE_URL + str(page_number)
    response = requests.get(url, verify=False)  # Disable SSL verification
    if response.status_code != 200:
        print(f"Failed to fetch page {page_number}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("table tbody tr")
    save_html(page_number, soup)  # Sauvegarde du HTML

    data = []
    for row in rows:
        cols = [col.text.strip() for col in row.find_all("td")]
        if cols:
            data.append(cols)
    
    return data

def main():
    """Scrape all pages and save the data to a CSV file."""
    total_pages = get_total_pages()
    print(f"Total pages found: {total_pages}")

    all_data = []
    for page in range(1, total_pages + 1):
        print(f"Scraping page {page}...")
        page_data = scrape_page(page)
        print(page_data)
        all_data.extend(page_data)

    # Save data to CSV
    df = pd.DataFrame(all_data, columns=["Column1", "Column2", "Column3", "Column4"])  # Adjust column names
    df.to_csv("medicines_data.csv", index=False, encoding="utf-8")
    print("Scraping complete! Data saved to `medicines_data.csv`.")

if __name__ == "__main__":
    main()
