"""
Entraîneur ML simplifié utilisant les données actuelles
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

def create_sample_training_data():
    """Crée des données d'entraînement basées sur les matchs actuels"""
    print("Creation de donnees d'entrainement simulees...")
    
    # Données simulées basées sur des statistiques réelles
    np.random.seed(42)
    n_matches = 1000
    
    data = []
    for i in range(n_matches):
        # Caractéristiques des joueurs
        p1_rank = np.random.randint(1, 200)
        p2_rank = np.random.randint(1, 200)
        
        # Probabilité basée sur le classement
        rank_diff = p1_rank - p2_rank
        base_prob = 0.5 + (rank_diff * -0.002)  # Meilleur classement = probabilité plus élevée
        base_prob = max(0.1, min(0.9, base_prob))
        
        # Ajout de bruit pour réalisme
        win_prob = base_prob + np.random.normal(0, 0.1)
        win_prob = max(0.1, min(0.9, win_prob))
        
        # Résultat du match (1 si joueur 1 gagne, 0 sinon)
        winner = 1 if np.random.random() < win_prob else 0
        
        # Caractéristiques d'entrée
        features = [
            p1_rank,
            p2_rank,
            abs(p1_rank - p2_rank),  # Différence de classement
            np.random.uniform(0.4, 0.8),  # % victoires récentes J1
            np.random.uniform(0.4, 0.8),  # % victoires récentes J2
            np.random.randint(0, 10),     # H2H J1
            np.random.randint(0, 10),     # H2H J2
            np.random.choice([0, 1, 2]),  # Surface (0=Hard, 1=Clay, 2=Grass)
        ]
        
        data.append(features + [winner])
    
    columns = [
        'p1_rank', 'p2_rank', 'rank_diff', 'p1_recent_win_pct', 
        'p2_recent_win_pct', 'h2h_p1', 'h2h_p2', 'surface', 'winner'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    return df

def train_simple_ml_model():
    """Entraîne un modèle ML simple"""
    print("=== ENTRAINEMENT ML SIMPLIFIE ===")
    
    # Créer les données d'entraînement
    df = create_sample_training_data()
    print(f"Donnees creees: {len(df)} matchs")
    
    # Préparer les caractéristiques et cibles
    feature_columns = ['p1_rank', 'p2_rank', 'rank_diff', 'p1_recent_win_pct', 
                      'p2_recent_win_pct', 'h2h_p1', 'h2h_p2', 'surface']
    
    X = df[feature_columns]
    y = df['winner']
    
    # Division train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entraîner le modèle
    print("Entrainement du modele Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Évaluer le modèle
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Precision du modele: {accuracy:.3f}")
    
    # Sauvegarder le modèle
    os.makedirs('./ml_models', exist_ok=True)
    model_path = './ml_models/simple_tennis_model.joblib'
    joblib.dump(model, model_path)
    print(f"Modele sauvegarde: {model_path}")
    
    # Sauvegarder les noms des caractéristiques
    feature_names_path = './ml_models/feature_names.joblib'
    joblib.dump(feature_columns, feature_names_path)
    print(f"Caracteristiques sauvegardees: {feature_names_path}")
    
    return model, accuracy

def predict_with_simple_model(p1_rank, p2_rank, p1_recent_pct=0.6, p2_recent_pct=0.6, 
                             h2h_p1=0, h2h_p2=0, surface=0):
    """Fait une prédiction avec le modèle simple"""
    try:
        model_path = './ml_models/simple_tennis_model.joblib'
        if not os.path.exists(model_path):
            return None
        
        model = joblib.load(model_path)
        
        # Préparer les caractéristiques
        features = np.array([[
            p1_rank, p2_rank, abs(p1_rank - p2_rank),
            p1_recent_pct, p2_recent_pct, h2h_p1, h2h_p2, surface
        ]])
        
        # Prédiction
        prob = model.predict_proba(features)[0]
        winner = model.predict(features)[0]
        
        return {
            'p1_probability': prob[1],  # Probabilité que joueur 1 gagne
            'p2_probability': prob[0],  # Probabilité que joueur 2 gagne
            'predicted_winner': int(winner),
            'confidence': max(prob)
        }
        
    except Exception as e:
        print(f"Erreur prediction: {e}")
        return None

if __name__ == "__main__":
    # Entraîner le modèle
    model, accuracy = train_simple_ml_model()
    
    print(f"\nModele entraine avec succes!")
    print(f"Precision: {accuracy:.1%}")
    
    # Test de prédiction
    print("\n=== TEST DE PREDICTION ===")
    result = predict_with_simple_model(p1_rank=10, p2_rank=50)
    if result:
        print(f"Joueur 1 (rank 10) vs Joueur 2 (rank 50)")
        print(f"Probabilite J1: {result['p1_probability']:.1%}")
        print(f"Probabilite J2: {result['p2_probability']:.1%}")
        print(f"Gagnant predit: Joueur {result['predicted_winner'] + 1}")
        print(f"Confiance: {result['confidence']:.1%}")
