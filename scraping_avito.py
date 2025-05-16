from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

# --- Configuration du navigateur
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

# --- Liste pour stocker les données
annonces = []

# --- Limite de pages
MAX_PAGES = 300

# --- Boucle sur les pages
for page in range(1, MAX_PAGES + 1):
    print(f"Scraping page {page}...")
    url = f"https://www.avito.ma/fr/maroc/voitures-à_vendre?o={page}"
    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    ads = soup.select("a.sc-1jge648-0")

    if not ads:
        print("Plus d'annonces trouvées, arrêt.")
        break

    for ad in ads:
        try:
            lien = "https://www.avito.ma" + ad["href"]
            titre = ad.select_one("p[title]").text.strip()

            ville_el = ad.select_one("p:-soup-contains('dans')")
            ville = ville_el.text.strip() if ville_el else ""

            prix_el = ad.select_one("p span span")
            prix = prix_el.text.strip().replace("\u202f", "").replace("DH", "").strip() if prix_el else ""

            specs = ad.select("span.sc-1s278lr-0 span span")
            annee = specs[0].text.strip() if len(specs) > 0 else ""
            boite = specs[1].text.strip() if len(specs) > 1 else ""
            carburant = specs[2].text.strip() if len(specs) > 2 else ""

            annonces.append({
                "Titre": titre,
                "Ville": ville,
                "Prix": prix,
                "Année": annee,
                "Boîte": boite,
                "Carburant": carburant,
                "Lien": lien
            })
        except Exception as e:
            print("Erreur dans une annonce :", e)

# --- Sauvegarde dans un fichier CSV
if annonces:
    with open("annonces_avito.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=annonces[0].keys())
        writer.writeheader()
        writer.writerows(annonces)

    print(f"{len(annonces)} annonces enregistrées dans annonces_avito.csv")
else:
    print("Aucune annonce trouvée.")

# --- Fermeture du navigateur
driver.quit()
