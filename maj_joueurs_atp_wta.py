# extraction MAJ joueurs ATP WTA

import csv
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


URLS = {
    "ATP": "https://tennisabstract.com/reports/atpRankings.html",
    "WTA": "https://tennisabstract.com/reports/wtaRankings.html",
}
#CSV_FILENAME = '/content/drive/My Drive/joueurs.csv'
CSV_FILENAME = './data/joueurs_ATP_WTA.csv'

def initialize_driver() -> webdriver.Firefox:
    """Initialise le driver Firefox avec les options nécessaires."""
    try:
        print("Initialisation du driver Firefox...")
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(options=firefox_options)
        print("Driver Firefox initialisé avec succès")
        return driver
    except Exception as e:
        print(f"Erreur lors de l'initialisation du driver Firefox: {str(e)}")
        raise

def fetch_page_source(url: str, driver: webdriver.Firefox) -> str:
    """Récupère le contenu HTML de la page spécifiée."""
    try:
        print(f"Tentative d'accès à l'URL: {url}")
        driver.get(url)
        time.sleep(5)  # Attendre que la page se charge complètement
        print("Page chargée avec succès")
        return driver.page_source
    except Exception as e:
        print(f"Erreur lors du chargement de la page {url}: {str(e)}")
        raise

def parse_player_list(page_source: str) -> Dict[str, str]:
    """Analyse et extrait les informations de base des joueurs à partir du contenu HTML."""
    try:
        print("Analyse du contenu HTML...")
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', id='reportable')
        if not table:
            raise ValueError("Tableau des classements non trouvé")
            
        rows = table.find_all('tr')[1:]  # Ignorer la ligne d'en-tête
        print(f"Nombre de joueurs trouvés: {len(rows)}")
        
        return {row.find_all('td')[1].get_text(strip=True): row.find_all('td')[1].find('a')['href'] for row in rows}
    except Exception as e:
        print(f"Erreur lors de l'analyse du contenu HTML: {str(e)}")
        raise

def load_existing_players(filename: str) -> set:
    """Charge les joueurs existants à partir du fichier CSV."""
    try:
        print(f"Tentative de chargement des joueurs existants depuis {filename}")
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            players = {row[0] for row in reader if row}
            print(f"Nombre de joueurs existants chargés: {len(players)}")
            return players
    except FileNotFoundError:
        print(f"Fichier {filename} non trouvé. Un nouveau fichier sera créé.")
        return set()
    except Exception as e:
        print(f"Erreur lors du chargement des joueurs existants: {str(e)}")
        raise

def save_to_csv(data: Dict[str, str], filename: str, existing_players: set) -> int:
    """Enregistre la liste des joueurs et leurs liens dans un fichier CSV, en ajoutant seulement les nouveaux joueurs."""
    added_players_count = 0
    file_path = Path(filename)
    
    try:
        print(f"Tentative de sauvegarde dans {filename}")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for name, link in data.items():
                if name not in existing_players:
                    writer.writerow([name, link])
                    added_players_count += 1
        print(f"Nombre de nouveaux joueurs ajoutés: {added_players_count}")
    except FileNotFoundError:
        print(f"Fichier '{filename}' introuvable. Création d'un nouveau fichier.")
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Nom', 'Lien'])
            for name, link in data.items():
                writer.writerow([name, link])
                added_players_count += 1
    except Exception as e:
        print(f"Erreur lors de la sauvegarde dans le fichier CSV: {str(e)}")
        raise

    return added_players_count

def main():
    print("\n" + "="*50)
    print("DÉBUT DE LA MISE À JOUR DES JOUEURS ATP/WTA")
    print("="*50 + "\n")
    
    try:
        with initialize_driver() as driver:
            existing_players = load_existing_players(CSV_FILENAME)
            initial_player_count = len(existing_players)
            total_added_players = 0

            for tour, url in URLS.items():
                print(f"\nTraitement du tour {tour}...")
                page_source = fetch_page_source(url, driver)
                joueurs_dict = parse_player_list(page_source)
                added_players_count = save_to_csv(joueurs_dict, CSV_FILENAME, existing_players)
                existing_players.update(joueurs_dict.keys())
                total_added_players += added_players_count

                print(f"Tour: {tour}")
                print(f"Nombre de joueurs avant la mise à jour: {initial_player_count}")
                print(f"Nombre de nouveaux joueurs ajoutés: {added_players_count}")

            print(f"\nNombre total de nouveaux joueurs ajoutés: {total_added_players}")
            
    except Exception as e:
        print(f"\nERREUR CRITIQUE: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
        
    finally:
        print("\n" + "="*50)
        print("FIN DE LA MISE À JOUR DES JOUEURS ATP/WTA")
        print("="*50 + "\n")

if __name__ == "__main__":
    main()