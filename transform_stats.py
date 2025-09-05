import pandas as pd
import os
import time
import sqlite3
from datetime import datetime
import re
import csv

def calculer_forme_recente(pourc_vict_last_10, pourc_vict_last_50):
    try:
        if pd.isna(pourc_vict_last_10) or pd.isna(pourc_vict_last_50):
            return "Non disponible"
        pourc_vict_last_10 = float(pourc_vict_last_10)
        pourc_vict_last_50 = float(pourc_vict_last_50)
        if pourc_vict_last_10 > pourc_vict_last_50 + 10:
            return "Excellente"
        elif pourc_vict_last_10 > pourc_vict_last_50:
            return "Bonne"
        elif pourc_vict_last_10 < pourc_vict_last_50 - 10:
            return "Mauvaise"
        else:
            return "Stable"
    except (ValueError, TypeError):
        return "Non disponible"

def determiner_surface_preferee(pourc_vict_car, pourc_vict_surf):
    try:
        if pd.isna(pourc_vict_car) or pd.isna(pourc_vict_surf):
            return "Non disponible"
        pourc_vict_car = float(pourc_vict_car)
        pourc_vict_surf = float(pourc_vict_surf)
        if pourc_vict_car > pourc_vict_surf + 5:
            return "Terre battue"
        elif pourc_vict_surf > pourc_vict_car + 5:
            return "Dur"
        else:
            return "Polyvalent"
    except (ValueError, TypeError):
        return "Non disponible"

def calculer_confiance(pourc_vict_last_10, pourc_serv_last_game, pourc_bb_sauvées):
    try:
        if pd.isna(pourc_vict_last_10) or pd.isna(pourc_serv_last_game) or pd.isna(pourc_bb_sauvées):
            return None
        pourc_vict_last_10 = float(pourc_vict_last_10)
        pourc_serv_last_game = float(pourc_serv_last_game)
        pourc_bb_sauvées = float(pourc_bb_sauvées)
        return (pourc_vict_last_10 + pourc_serv_last_game + pourc_bb_sauvées) / 3
    except (ValueError, TypeError):
        return None

def determiner_tendance(pourc_vict_last_10, pourc_vict_car):
    try:
        if pd.isna(pourc_vict_last_10) or pd.isna(pourc_vict_car):
            return "Non disponible"
        pourc_vict_last_10 = float(pourc_vict_last_10)
        pourc_vict_car = float(pourc_vict_car)
        if pourc_vict_last_10 > pourc_vict_car + 5:
            return "Progression"
        elif pourc_vict_last_10 < pourc_vict_car - 5:
            return "Régression"
        else:
            return "Stable"
    except (ValueError, TypeError):
        return "Non disponible"

def format_date_values(df, date_column='Date', format_type="dd/mm/yy"):
    """
    Reformate la colonne 'Date' d'un DataFrame au format spécifié.
    
    Args:
        df (DataFrame): Le DataFrame pandas contenant les dates à formater
        date_column (str): Nom de la colonne contenant les dates
        format_type (str): Type de format de date ('dd/mm/yy')
        
    Returns:
        DataFrame: Le DataFrame avec les dates reformatées
    """
    if date_column not in df.columns:
        print(f"Avertissement: Le DataFrame ne contient pas de colonne '{date_column}'.")
        return df
    
    print(f"Formatage des dates en cours vers le format: {format_type.upper()}")
    
    def format_single_date(date_str):
        """Formate une date individuelle du format '10.07.' vers '10/07/25'."""
        try:
            if pd.isna(date_str) or not isinstance(date_str, str):
                return date_str
            
            # Nettoyer la chaîne et enlever les points finaux
            date_str = date_str.strip().rstrip('.')
            
            # Vérifier si c'est au format attendu (JJ.MM)
            if re.match(r'^\d{2}\.\d{2}$', date_str):
                day, month = date_str.split('.')
                current_year = datetime.now().year
                formatted_date = f"{day}/{month}/{str(current_year)[-2:]}"
                print(f"Date formatée: {date_str} -> {formatted_date}")
                return formatted_date
            else:
                # Si ce n'est pas le format attendu, retourner tel quel
                return date_str
        except Exception as e:
            print(f"Erreur formatage date '{date_str}': {e}")
            return date_str
    
    # Appliquer le formatage à chaque valeur de la colonne
    df[date_column] = df[date_column].apply(format_single_date)
    
    return df

def init_database():
    """Initialise la base de données SQLite et crée les tables nécessaires."""
    db_path = './data/tennis_stats.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Créer la table des joueurs si elle n'existe pas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS joueurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        classement INTEGER,
        pays TEXT,
        age INTEGER,
        lien_photo TEXT,
        lien_tennisexplorer TEXT,
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Créer la table des statistiques si elle n'existe pas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS statistiques (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        joueur_id INTEGER,
        date_match DATE,
        heure_match TIME,
        tournoi TEXT,
        round TEXT,
        nom TEXT,
        classement INTEGER,
        pourc_vict_car REAL,
        pourc_vict_surf REAL,
        h2h_ratio_car REAL,
        h2h_ratio_1_an REAL,
        h2h_ratio_surf REAL,
        h2h_sets_gagnes INTEGER,
        pourc_vict_car_1_an_car REAL,
        pourc_vict_car_1_an_surf REAL,
        pourc_vict_last_50 REAL,
        pourc_vict_last_10 REAL,
        nb_matchs_joues_30j INTEGER,
        duree_tournoi INTEGER,
        favori_lose REAL,
        outsider_win REAL,
        pourc_serv_last_game REAL,
        pourc_pts_winfirst_serv REAL,
        pourc_bb_sauvees REAL,
        cotes TEXT,
        h2h TEXT,
        lien_photo TEXT,
        pays TEXT,
        age INTEGER,
        lien_tennisexplorer TEXT,
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (joueur_id) REFERENCES joueurs(id)
    )
        
 
    
      
    ''')
    
    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès.")

def save_to_database(df):
    """Sauvegarde les données dans la base de données SQLite existante."""
    db_path = './data/tennis_stats.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        try:
            # Vérifier si le joueur existe déjà
            cursor.execute('SELECT id FROM joueurs WHERE nom = ?', (row['Nom'],))
            result = cursor.fetchone()
            
            if result is None:
                # Insérer le nouveau joueur
                cursor.execute('''
                INSERT INTO joueurs (nom, classement, pays, age, lien_photo, lien_tennisexplorer)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    row['Nom'],
                    row['Classement'],
                    row['Pays'],
                    row['Age'],
                    row['Lien Photo'],
                    row['Lien TennisExplorer']
                ))
                joueur_id = cursor.lastrowid
            else:
                joueur_id = result[0]
            
            # Formater la date si elle existe
            date_match = None
            if pd.notna(row['Date']):
                try:
                    # Si la date est déjà au bon format (dd/mm/yy), l'utiliser directement
                    if isinstance(row['Date'], str) and re.match(r'^\d{2}/\d{2}/\d{2}$', row['Date']):
                        date_match = row['Date']
                    # Si la date est au format JJ.MM. (avec point final)
                    elif isinstance(row['Date'], str) and re.match(r'^\d{2}\.\d{2}\.$', row['Date'].strip()):
                        current_year = datetime.now().year
                        # Extraire le jour et le mois
                        day, month = row['Date'].strip('.').split('.')
                        date_str = f"{day}/{month}/{str(current_year)[-2:]}"
                        date_match = date_str
                    # Si la date est au format JJ.MM (sans point final)
                    elif isinstance(row['Date'], str) and re.match(r'^\d{2}\.\d{2}$', row['Date'].strip()):
                        current_year = datetime.now().year
                        # Extraire le jour et le mois
                        day, month = row['Date'].split('.')
                        date_str = f"{day}/{month}/{str(current_year)[-2:]}"
                        date_match = date_str
                    else:
                        # Essayer de parser la date dans d'autres formats
                        date_obj = pd.to_datetime(row['Date'])
                        date_match = date_obj.strftime('%d/%m/%y')
                except Exception as e:
                    print(f"Erreur lors du formatage de la date '{row['Date']}': {e}")
            
            # Vérifier si cette statistique existe déjà
            cursor.execute('''
            SELECT id FROM statistiques 
            WHERE joueur_id = ? AND date_match = ? AND tournoi = ? AND round = ?
            ''', (joueur_id, date_match, row['Tournoi'], row['Round']))
            
            if cursor.fetchone() is None:
                # Insérer les nouvelles statistiques
                cursor.execute('''
                INSERT INTO statistiques (
                    joueur_id, date_match, heure_match, tournoi, round, nom, classement,
                    pourc_vict_car, pourc_vict_surf, h2h_ratio_car, h2h_ratio_1_an,
                    h2h_ratio_surf, h2h_sets_gagnes, pourc_vict_car_1_an_car,
                    pourc_vict_car_1_an_surf, pourc_vict_last_50, pourc_vict_last_10,
                    nb_matchs_joues_30j, duree_tournoi, favori_lose, outsider_win,
                    pourc_serv_last_game, pourc_pts_winfirst_serv, pourc_bb_sauvees,
                    forme_recente, surface_preferee, confiance, tendance, cotes, h2h,
                    lien_photo, pays, age, lien_tennisexplorer
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    joueur_id, date_match, row['Heure'], row['Tournoi'], row['Round'],
                    row['Nom'], row['Classement'], row['Pourc_vict_car'], row['Pourc_vict_surf'],
                    row['H2H_ratio_car'], row['H2H_ratio_1_an'], row['H2H_ratio_surf'],
                    row['H2H_sets_gagnés'], row['Pourc_vict_car_1_an_car'],
                    row['Pourc_vict_car_1_an_surf'], row['Pourc_vict_last_50'],
                    row['Pourc_vict_last_10'], row['Nb_matchs_joués_30j'],
                    row['Durée_tournoi'], row['Favori_lose'], row['Outsider_win'],
                    row['Pourc_serv_last_game'], row['Pourc_pts_winfirst_serv'],
                    row['Pourc_bb_sauvées'], row['Forme_recente'], row['Surface_preferee'],
                    row['Confiance'], row['Tendance'], row['Côtes'], row['H2H'],
                    row['Lien Photo'], row['Pays'], row['Age'], row['Lien TennisExplorer']
                ))
                print(f"Nouvelles statistiques ajoutées pour {row['Nom']}")
            else:
                print(f"Statistiques déjà existantes pour {row['Nom']} à cette date")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des données pour {row['Nom']}: {str(e)}")
            continue
    
    conn.commit()
    conn.close()
    print("Données sauvegardées dans la base de données avec succès.")

def load_player_names():
    """
    Charge les noms des joueurs depuis new_list_players.csv et crée un dictionnaire
    de correspondance entre les noms simples et les noms formatés.
    """
    player_names = {}
    try:
        with open('./data/new_list_players.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row:  # Ignorer les lignes vides
                    continue
                formatted_name = row[0]
                # Extraire le nom de famille et l'initiale
                parts = formatted_name.split()
                if len(parts) > 1:
                    last_name = ' '.join(parts[:-1])  # Nom de famille
                    initial = parts[-1]  # Initiale
                    # Stocker le nom formaté avec l'initiale
                    player_names[last_name.lower()] = formatted_name
    except Exception as e:
        print(f"Erreur lors du chargement des noms des joueurs: {str(e)}")
    return player_names

def handle_similar_names_in_tournament(df, player_names):
    """
    Harmonise tous les noms avec le mapping player_names, puis gère les doublons dans chaque tournoi.
    """
    # Nettoyer les espaces dans les noms
    df['Nom'] = df['Nom'].astype(str).str.strip()

    # Appliquer le mapping player_names à tous les noms
    def map_name(name):
        base_name = name.lower()
        return player_names.get(base_name, name)
    df['Nom'] = df['Nom'].apply(map_name)

    # Gérer les doublons dans chaque tournoi
    for tournament in df['Tournoi'].unique():
        tournament_df = df[df['Tournoi'] == tournament]
        name_counts = tournament_df['Nom'].value_counts()
        duplicate_names = name_counts[name_counts > 1].index
        for name in duplicate_names:
            name_rows = tournament_df[tournament_df['Nom'] == name].sort_values('Classement')
            for i, (idx, row) in enumerate(name_rows.iterrows()):
                # Si le nom a déjà une initiale, on ne touche pas
                parts = name.split()
                if len(parts) > 1 and parts[-1].endswith('.'):
                    continue
                # Sinon, on ajoute une initiale selon l'ordre
                if i == 0:
                    df.at[idx, 'Nom'] = f"{name} M."
                else:
                    df.at[idx, 'Nom'] = f"{name} E."
    return df

def transform_stats():
    # Initialiser la base de données
    init_database()
    
    # Charger les noms des joueurs
    player_names = load_player_names()
    
    # Lire le fichier Excel
    df = pd.read_excel('./data/Stats_tournois_en_cours.xlsx')
    
    # Appliquer le formatage des noms
    df = handle_similar_names_in_tournament(df, player_names)
    
    # Chemins des fichiers
    input_file = './data/Result_data_export.xlsx'
    output_file = './data/Stats_tournois_en_cours.xlsx'
    
    try:
        # Vérifier si le fichier d'entrée existe
        if not os.path.exists(input_file):
            print(f"Erreur: Le fichier {input_file} n'existe pas.")
            return
            
        # Lire tous les onglets du fichier Excel
        xls = pd.ExcelFile(input_file)
        print(f"Onglets trouvés: {xls.sheet_names}")
        
        all_data = []
        
        # Parcourir chaque onglet
        for sheet_name in xls.sheet_names:
            print(f"\nTraitement de l'onglet: {sheet_name}")
            
            # Lire l'onglet
            df = pd.read_excel(input_file, sheet_name=sheet_name)
            print(f"Nombre de colonnes: {len(df.columns)}")
            print(f"Colonnes disponibles: {df.columns.tolist()}")
            
            # Formater les dates si la colonne existe
            if 'Date' in df.columns:
                print("\nDates avant formatage:")
                print(df['Date'].head())
                df = format_date_values(df, date_column='Date')
                print("\nDates après formatage:")
                print(df['Date'].head())
                
                # Ajouter l'année en cours
                current_year = datetime.now().year
                df['Année'] = current_year
            
            # Afficher les premières lignes pour debug
            print("\nPremières lignes du DataFrame:")
            print(df.head())
            
            # Vérifier si le DataFrame a des données
            if df.empty:
                print(f"Attention: L'onglet {sheet_name} est vide")
                continue
                
            # Créer un nouveau DataFrame pour stocker les données transformées
            transformed_data = []
            
            # Parcourir toutes les colonnes
            for col in df.columns:
                print(f"\nTraitement de la colonne: {col}")
                
                # Extraire les données de la colonne
                player_data = df[col]
                
                # Vérifier si la ligne contient des données de joueur (pas un en-tête)
                if player_data.iloc[0] == 'Match' or player_data.iloc[0] == 'Tableau':
                    print("Ligne d'en-tête détectée, passage à la suivante")
                    continue
                
                print(f"Données du joueur: {player_data.iloc[2] if len(player_data) > 2 else 'Non disponible'}")
                
                # Vérifier si les données du joueur sont valides
                if len(player_data) <= 2 or pd.isna(player_data.iloc[2]):
                    print("Données du joueur non valides, passage au suivant")
                    continue
                    
                try:
                    # Extraire les informations supplémentaires
                    cotes = player_data.iloc[23] if len(player_data) > 23 else None
                    date = player_data.iloc[25] if len(player_data) > 25 else None
                    heure = player_data.iloc[26] if len(player_data) > 26 else None
                    lien_photo = player_data.iloc[29] if len(player_data) > 29 else None
                    pays = player_data.iloc[32] if len(player_data) > 32 else None
                    age = player_data.iloc[33] if len(player_data) > 33 else None
                    round_info = player_data.iloc[36] if len(player_data) > 36 else None
                    lien_tennisexplorer = player_data.iloc[31] if len(player_data) > 31 else None
                    H2H = player_data.iloc[28] if len(player_data) > 28 else None
                    
                    # Extraire et convertir le classement
                    classement = player_data.iloc[3] if len(player_data) > 3 else None
                    if classement is not None:
                        try:
                            classement = int(float(classement))
                            print(f"Classement converti pour {player_data.iloc[2]}: {classement}")
                        except (ValueError, TypeError):
                            print(f"Erreur de conversion du classement pour {player_data.iloc[2]}: {classement}")
                            classement = None
                    
                    # Créer une nouvelle ligne avec les données du joueur
                    new_row = {
                        'Id': None,
                        'Date': date,
                        'Heure': heure,
                        'Tournoi': sheet_name,
                        'Round': round_info,
                        'Nom': player_data.iloc[2],
                        'Classement': classement,
                        'Pourc_vict_car': player_data.iloc[4] if len(player_data) > 4 else None,
                        'Pourc_vict_surf': player_data.iloc[5] if len(player_data) > 5 else None,
                        'H2H_ratio_car': player_data.iloc[6] if len(player_data) > 6 else None,
                        'H2H_ratio_1_an': player_data.iloc[7] if len(player_data) > 7 else None,
                        'H2H_ratio_surf': player_data.iloc[8] if len(player_data) > 8 else None,
                        'H2H_sets_gagnés': player_data.iloc[9] if len(player_data) > 9 else None,
                        'Pourc_vict_car_1_an_car': player_data.iloc[10] if len(player_data) > 10 else None,
                        'Pourc_vict_car_1_an_surf': player_data.iloc[11] if len(player_data) > 11 else None,
                        'Pourc_vict_last_50': player_data.iloc[12] if len(player_data) > 12 else None,
                        'Pourc_vict_last_10': player_data.iloc[13] if len(player_data) > 13 else None,
                        'Nb_matchs_joués_30j': player_data.iloc[14] if len(player_data) > 14 else None,
                        'Durée_tournoi': player_data.iloc[15] if len(player_data) > 15 else None,
                        'Favori_lose': player_data.iloc[16] if len(player_data) > 16 else None,
                        'Outsider_win': player_data.iloc[17] if len(player_data) > 17 else None,
                        'Pourc_serv_last_game': player_data.iloc[18] if len(player_data) > 18 else None,
                        'Pourc_pts_winfirst_serv': player_data.iloc[19] if len(player_data) > 19 else None,
                        'Pourc_bb_sauvées': player_data.iloc[20] if len(player_data) > 20 else None,
                        'Forme_recente': calculer_forme_recente(
                            player_data.iloc[13] if len(player_data) > 13 else None,
                            player_data.iloc[12] if len(player_data) > 12 else None
                        ),
                        'Surface_preferee': determiner_surface_preferee(
                            player_data.iloc[4] if len(player_data) > 4 else None,
                            player_data.iloc[5] if len(player_data) > 5 else None
                        ),
                        'Confiance': calculer_confiance(
                            player_data.iloc[13] if len(player_data) > 13 else None,
                            player_data.iloc[18] if len(player_data) > 18 else None,
                            player_data.iloc[20] if len(player_data) > 20 else None
                        ),
                        'Tendance': determiner_tendance(
                            player_data.iloc[13] if len(player_data) > 13 else None,
                            player_data.iloc[4] if len(player_data) > 4 else None
                        ),
                        'Côtes': cotes,
                        'H2H': H2H,
                        'Lien Photo': lien_photo,
                        'Pays': pays,
                        'Age': age,
                        'Lien TennisExplorer': lien_tennisexplorer
                    }
                    transformed_data.append(new_row)
                    print(f"Ajout des données pour le joueur: {new_row['Nom']} (Classement: {new_row['Classement']})")
                except Exception as e:
                    print(f"Erreur lors de la création de la ligne: {str(e)}")
                    continue
            
            # Ajouter les données transformées à la liste principale
            all_data.extend(transformed_data)
            print(f"Nombre de lignes ajoutées pour cet onglet: {len(transformed_data)}")
        
        # Créer un DataFrame final avec toutes les données
        final_df = pd.DataFrame(all_data)
        
        # Réorganiser les colonnes dans l'ordre souhaité
        columns_order = [
            'Id', 'Date', 'Heure', 'Tournoi', 'Round', 'Nom', 'Classement',
            'Pourc_vict_car', 'Pourc_vict_surf', 'H2H_ratio_car', 'H2H_ratio_1_an',
            'H2H_ratio_surf', 'H2H_sets_gagnés', 'Pourc_vict_car_1_an_car',
            'Pourc_vict_car_1_an_surf', 'Pourc_vict_last_50', 'Pourc_vict_last_10',
            'Nb_matchs_joués_30j', 'Durée_tournoi', 'Favori_lose', 'Outsider_win',
            'Pourc_serv_last_game', 'Pourc_pts_winfirst_serv', 'Pourc_bb_sauvées',
            'Forme_recente', 'Surface_preferee', 'Confiance', 'Tendance',
            'Côtes', 'H2H', 'Lien Photo', 'Pays', 'Age', 'Lien TennisExplorer'
        ]
        final_df = final_df[columns_order]

        # --- AJOUT : formatage systématique de la colonne 'Date' ---
        def format_single_date(date_str):
            try:
                if pd.isna(date_str) or not isinstance(date_str, str):
                    return date_str
                date_str = date_str.strip().rstrip('.')
                # Format JJ.MM
                if re.match(r'^\d{2}\.\d{2}$', date_str):
                    day, month = date_str.split('.')
                    current_year = datetime.now().year
                    return f"{day}/{month}/{str(current_year)[-2:]}"
                # Format JJ.MM.
                if re.match(r'^\d{2}\.\d{2}\.$', date_str):
                    day, month = date_str.strip('.').split('.')
                    current_year = datetime.now().year
                    return f"{day}/{month}/{str(current_year)[-2:]}"
                # Format déjà correct
                if re.match(r'^\d{2}/\d{2}/\d{2}$', date_str):
                    return date_str
                return date_str
            except Exception as e:
                print(f"Erreur formatage date '{date_str}': {e}")
                return date_str
        if 'Date' in final_df.columns:
            final_df['Date'] = final_df['Date'].apply(format_single_date)
            # Forcer le type string pour éviter la conversion automatique en datetime
            final_df['Date'] = final_df['Date'].astype(str)
        # --- FIN AJOUT ---

        print(f"\nNombre total de lignes dans le DataFrame final: {len(final_df)}")
        print("\nTypes des colonnes dans le DataFrame final:")
        print(final_df.dtypes)
        print("\nValeurs uniques de classement:")
        print(final_df['Classement'].unique())
        
        if len(final_df) > 0:
            # Sauvegarder dans la base de données
            print("Sauvegarde des données dans la base de données...")
            save_to_database(final_df)
            print("Données sauvegardées dans la base de données avec succès.")
            
            # Vérifier si le fichier de sortie existe déjà
            if os.path.exists(output_file):
                try:
                    # Essayer de supprimer le fichier existant
                    os.remove(output_file)
                    print(f"Fichier existant {output_file} supprimé")
                except PermissionError:
                    print(f"Erreur: Impossible de supprimer le fichier {output_file}. Veuillez fermer le fichier s'il est ouvert.")
                    return
                except Exception as e:
                    print(f"Erreur lors de la suppression du fichier: {str(e)}")
                    return
            
            # Essayer d'écrire le fichier avec plusieurs tentatives
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    # S'assurer que la colonne Date reste au format string JJ/MM/AA
                    if 'Date' in final_df.columns:
                        # Convertir en string pour éviter la conversion automatique en datetime
                        final_df['Date'] = final_df['Date'].astype(str)
                    
                    # Sauvegarder dans Excel
                    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                        final_df.to_excel(writer, index=False, sheet_name='StatsJoueurs')
                    
                    print(f"Transformation terminée. Le fichier a été sauvegardé sous {output_file}")
                    break
                except PermissionError:
                    if attempt < max_attempts - 1:
                        print(f"Tentative {attempt + 1} échouée. Veuillez fermer le fichier s'il est ouvert. Nouvelle tentative dans 2 secondes...")
                        time.sleep(2)
                    else:
                        print("Erreur: Impossible d'écrire dans le fichier après plusieurs tentatives. Veuillez fermer le fichier s'il est ouvert.")
                except Exception as e:
                    print(f"Une erreur s'est produite lors de l'écriture du fichier: {str(e)}")
                    break
        else:
            print("Aucune donnée n'a été transformée. Le fichier de sortie n'a pas été créé.")
        
    except Exception as e:
        print(f"Une erreur s'est produite: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    transform_stats()