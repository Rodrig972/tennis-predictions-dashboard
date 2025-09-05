"""
Entraîneur ML utilisant les vraies données historiques
"""

import pandas as pd
import numpy as np
import sqlite3
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from datetime import datetime

def load_historical_data():
    """Charge toutes les données historiques depuis les bases SQLite"""
    print("Chargement des données historiques...")
    
    all_matches = []
    
    # Charger ATP et WTA de 2020 à 2024 (données récentes plus pertinentes)
    years = [2020, 2021, 2022, 2023, 2024]
    circuits = ['atp', 'wta']
    
    for circuit in circuits:
        for year in years:
            db_path = f'Data_Base_Tennis/{circuit}_{year}.db'
            if os.path.exists(db_path):
                try:
                    conn = sqlite3.connect(db_path)
                    
                    # Lire les données avec les vraies colonnes
                    query = """
                    SELECT 
                        Winner, Loser, WRank, LRank,
                        W1, L1, W2, L2, W3, L3,
                        Surface, Series, Comment,
                        B365W, B365L, AvgW, AvgL
                    FROM data 
                    WHERE Comment IS NULL OR Comment != 'Walkover'
                    AND WRank IS NOT NULL 
                    AND LRank IS NOT NULL
                    AND WRank > 0 AND LRank > 0
                    AND WRank < 500 AND LRank < 500
                    """
                    
                    df = pd.read_sql_query(query, conn)
                    df['Circuit'] = circuit.upper()
                    df['Year'] = year
                    
                    all_matches.append(df)
                    print(f"  {circuit.upper()} {year}: {len(df)} matchs")
                    
                    conn.close()
                    
                except Exception as e:
                    print(f"  Erreur {circuit} {year}: {e}")
    
    if not all_matches:
        print("Aucune donnée trouvée!")
        return None
    
    # Combiner toutes les données
    combined_df = pd.concat(all_matches, ignore_index=True)
    print(f"\nTotal: {len(combined_df)} matchs historiques")
    
    return combined_df

def prepare_features(df):
    """Prépare les caractéristiques pour l'entraînement ML"""
    print("Préparation des caractéristiques...")
    
    # Nettoyer les données
    df = df.dropna(subset=['WRank', 'LRank', 'W1', 'L1'])
    
    # Dans cette structure, Winner a toujours gagné (target = 1)
    # On va créer des exemples pour les deux joueurs
    matches_data = []
    
    for _, row in df.iterrows():
        # Match 1: Winner vs Loser (Winner gagne = 1)
        matches_data.append({
            'Player1': row['Winner'],
            'Player2': row['Loser'], 
            'Rank1': row['WRank'],
            'Rank2': row['LRank'],
            'Surface': row['Surface'],
            'Series': row['Series'],
            'Odds1': row.get('AvgW', 2.0),
            'Odds2': row.get('AvgL', 2.0),
            'Circuit': row['Circuit'],
            'Target': 1  # Winner gagne
        })
        
        # Match 2: Loser vs Winner (Winner gagne = 0, donc Loser gagne = 1)
        matches_data.append({
            'Player1': row['Loser'],
            'Player2': row['Winner'],
            'Rank1': row['LRank'], 
            'Rank2': row['WRank'],
            'Surface': row['Surface'],
            'Series': row['Series'],
            'Odds1': row.get('AvgL', 2.0),
            'Odds2': row.get('AvgW', 2.0),
            'Circuit': row['Circuit'],
            'Target': 0  # Loser ne gagne pas contre Winner
        })
    
    # Convertir en DataFrame
    expanded_df = pd.DataFrame(matches_data)
    
    # Créer les caractéristiques
    features = []
    targets = []
    
    for _, row in expanded_df.iterrows():
        try:
            # Caractéristiques de base
            rank1 = float(row['Rank1'])
            rank2 = float(row['Rank2'])
            
            # Skip si classements aberrants
            if rank1 > 500 or rank2 > 500:
                continue
            
            # Différence de classement
            rank_diff = rank1 - rank2
            
            # Avantage du classement (plus le classement est bas, mieux c'est)
            rank_advantage = (rank2 - rank1) / max(rank1, rank2)
            
            # Surface encoding
            surface_map = {'Hard': 0, 'Clay': 1, 'Grass': 2, 'Indoor': 0}
            surface = surface_map.get(row.get('Surface', 'Hard'), 0)
            
            # Circuit encoding
            circuit = 1 if row['Circuit'] == 'ATP' else 0
            
            # Cotes si disponibles
            odds1 = row.get('Odds1', 2.0)
            odds2 = row.get('Odds2', 2.0)
            
            if pd.notna(odds1) and pd.notna(odds2) and odds1 > 0 and odds2 > 0:
                odds_advantage = (odds2 - odds1) / (odds1 + odds2)
            else:
                odds_advantage = 0
            
            feature_vector = [
                rank1,                    # Classement joueur 1
                rank2,                    # Classement joueur 2
                rank_diff,                # Différence de classement
                rank_advantage,           # Avantage relatif du classement
                surface,                  # Type de surface
                circuit,                  # ATP vs WTA
                odds_advantage,           # Avantage selon les cotes
                min(rank1, rank2),        # Meilleur classement
                max(rank1, rank2),        # Moins bon classement
                abs(rank_diff)            # Différence absolue
            ]
            
            features.append(feature_vector)
            targets.append(row['Target'])
            
        except Exception as e:
            continue
    
    feature_names = [
        'rank1', 'rank2', 'rank_diff', 'rank_advantage', 
        'surface', 'circuit', 'odds_advantage',
        'best_rank', 'worst_rank', 'abs_rank_diff'
    ]
    
    X = np.array(features)
    y = np.array(targets)
    
    print(f"Caractéristiques préparées: {len(X)} matchs valides")
    return X, y, feature_names

def train_real_ml_model():
    """Entraîne le modèle ML avec les vraies données"""
    print("=== ENTRAINEMENT ML AVEC DONNEES REELLES ===")
    
    # Charger les données historiques
    df = load_historical_data()
    if df is None:
        return None, 0
    
    # Préparer les caractéristiques
    X, y, feature_names = prepare_features(df)
    
    if len(X) == 0:
        print("Aucune donnée valide pour l'entraînement!")
        return None, 0
    
    # Division train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Entraînement: {len(X_train)} matchs")
    print(f"Test: {len(X_test)} matchs")
    
    # Entraîner le modèle Random Forest
    print("\nEntraînement du modèle Random Forest...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Évaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n=== RESULTATS ===")
    print(f"Précision: {accuracy:.1%}")
    print(f"Données d'entraînement: {len(X_train)} matchs")
    print(f"Données de test: {len(X_test)} matchs")
    
    # Rapport détaillé
    print("\nRapport de classification:")
    print(classification_report(y_test, y_pred, 
                              target_names=['Joueur 2 gagne', 'Joueur 1 gagne']))
    
    # Importance des caractéristiques
    print("\nImportance des caractéristiques:")
    for name, importance in zip(feature_names, model.feature_importances_):
        print(f"  {name}: {importance:.3f}")
    
    # Sauvegarder le modèle
    os.makedirs('./ml_models', exist_ok=True)
    
    model_path = './ml_models/real_tennis_model.joblib'
    joblib.dump(model, model_path)
    print(f"\nModèle sauvegardé: {model_path}")
    
    feature_names_path = './ml_models/real_feature_names.joblib'
    joblib.dump(feature_names, feature_names_path)
    print(f"Caractéristiques sauvegardées: {feature_names_path}")
    
    return model, accuracy

def predict_with_real_model(rank1, rank2, surface='Hard', circuit='ATP', odds1=None, odds2=None):
    """Fait une prédiction avec le modèle entraîné sur vraies données"""
    try:
        model_path = './ml_models/real_tennis_model.joblib'
        feature_names_path = './ml_models/real_feature_names.joblib'
        
        if not os.path.exists(model_path):
            print("Modèle réel non trouvé. Entraînez d'abord avec train_real_ml_model()")
            return None
        
        model = joblib.load(model_path)
        
        # Préparer les caractéristiques
        rank_diff = rank1 - rank2
        rank_advantage = (rank2 - rank1) / max(rank1, rank2)
        
        surface_map = {'Hard': 0, 'Clay': 1, 'Grass': 2, 'Indoor': 0}
        surface_encoded = surface_map.get(surface, 0)
        
        circuit_encoded = 1 if circuit == 'ATP' else 0
        
        if odds1 and odds2:
            odds_advantage = (odds2 - odds1) / (odds1 + odds2)
        else:
            odds_advantage = 0
        
        features = np.array([[
            rank1, rank2, rank_diff, rank_advantage,
            surface_encoded, circuit_encoded, odds_advantage,
            min(rank1, rank2), max(rank1, rank2), abs(rank_diff)
        ]])
        
        # Prédiction
        prob = model.predict_proba(features)[0]
        winner = model.predict(features)[0]
        
        return {
            'p1_probability': prob[1],
            'p2_probability': prob[0], 
            'predicted_winner': int(winner),
            'confidence': max(prob),
            'model_type': 'Real Data ML'
        }
        
    except Exception as e:
        print(f"Erreur prédiction: {e}")
        return None

if __name__ == "__main__":
    # Entraîner le modèle avec les vraies données
    model, accuracy = train_real_ml_model()
    
    if model:
        print(f"\nModele ML entraine avec VRAIES donnees!")
        print(f"Precision: {accuracy:.1%}")
        print(f"Modele sauvegarde dans ml_models/")
        
        # Test de prédiction
        print(f"\n=== TEST DE PREDICTION ===")
        result = predict_with_real_model(
            rank1=10, rank2=50, 
            surface='Hard', circuit='ATP'
        )
        
        if result:
            print(f"Joueur 1 (rank 10) vs Joueur 2 (rank 50)")
            print(f"Probabilite J1: {result['p1_probability']:.1%}")
            print(f"Probabilite J2: {result['p2_probability']:.1%}")
            print(f"Gagnant predit: Joueur {result['predicted_winner'] + 1}")
            print(f"Confiance: {result['confidence']:.1%}")
    else:
        print("Echec de l'entrainement du modele")
