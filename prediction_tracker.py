"""
Système de suivi des prédictions pour amélioration continue du ML
"""

import pandas as pd
import sqlite3
from datetime import datetime
import os

class PredictionTracker:
    def __init__(self, db_path='prediction_history.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données de suivi"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_prediction TEXT,
            player1 TEXT,
            player2 TEXT,
            rank1 INTEGER,
            rank2 INTEGER,
            surface TEXT,
            tournament TEXT,
            predicted_winner TEXT,
            p1_probability REAL,
            p2_probability REAL,
            confidence REAL,
            model_type TEXT,
            actual_winner TEXT NULL,
            correct_prediction INTEGER NULL,
            date_result TEXT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_prediction(self, match_data, prediction_result):
        """Sauvegarde une prédiction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO predictions (
            date_prediction, player1, player2, rank1, rank2, surface, tournament,
            predicted_winner, p1_probability, p2_probability, confidence, model_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            match_data.get('player1', ''),
            match_data.get('player2', ''),
            match_data.get('rank1', 0),
            match_data.get('rank2', 0),
            match_data.get('surface', 'Hard'),
            match_data.get('tournament', ''),
            prediction_result.get('predicted_winner_name', ''),
            prediction_result.get('p1_probability', 0),
            prediction_result.get('p2_probability', 0),
            prediction_result.get('confidence', 0),
            prediction_result.get('model_type', 'Unknown')
        ))
        
        conn.commit()
        conn.close()
        
        return cursor.lastrowid
    
    def update_result(self, prediction_id, actual_winner):
        """Met à jour le résultat réel d'un match"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Récupérer la prédiction
        cursor.execute('SELECT predicted_winner FROM predictions WHERE id = ?', (prediction_id,))
        result = cursor.fetchone()
        
        if result:
            predicted_winner = result[0]
            correct = 1 if predicted_winner == actual_winner else 0
            
            cursor.execute('''
            UPDATE predictions 
            SET actual_winner = ?, correct_prediction = ?, date_result = ?
            WHERE id = ?
            ''', (actual_winner, correct, datetime.now().isoformat(), prediction_id))
            
            conn.commit()
        
        conn.close()
    
    def get_accuracy_stats(self, days_back=30):
        """Calcule les statistiques de précision"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
        SELECT 
            COUNT(*) as total_predictions,
            SUM(correct_prediction) as correct_predictions,
            AVG(confidence) as avg_confidence,
            model_type
        FROM predictions 
        WHERE actual_winner IS NOT NULL
        AND date_prediction >= datetime('now', '-{} days')
        GROUP BY model_type
        '''.format(days_back)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['accuracy'] = df['correct_predictions'] / df['total_predictions']
            return df
        return None
    
    def export_for_retraining(self):
        """Exporte les données pour réentraînement du modèle"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
        SELECT 
            player1, player2, rank1, rank2, surface, tournament,
            p1_probability, p2_probability, confidence,
            actual_winner, correct_prediction
        FROM predictions 
        WHERE actual_winner IS NOT NULL
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df

def example_usage():
    """Exemple d'utilisation du tracker"""
    tracker = PredictionTracker()
    
    # Exemple de sauvegarde d'une prédiction
    match_data = {
        'player1': 'Djokovic N.',
        'player2': 'Alcaraz C.',
        'rank1': 1,
        'rank2': 2,
        'surface': 'Hard',
        'tournament': 'US Open'
    }
    
    prediction_result = {
        'predicted_winner_name': 'Djokovic N.',
        'p1_probability': 0.65,
        'p2_probability': 0.35,
        'confidence': 0.65,
        'model_type': 'Real Data ML'
    }
    
    # Sauvegarder la prédiction
    pred_id = tracker.save_prediction(match_data, prediction_result)
    print(f"Prédiction sauvegardée avec ID: {pred_id}")
    
    # Simuler un résultat (à faire quand le match est terminé)
    # tracker.update_result(pred_id, 'Alcaraz C.')  # Si Alcaraz gagne
    
    # Voir les statistiques
    stats = tracker.get_accuracy_stats()
    if stats is not None:
        print("\nStatistiques de précision:")
        print(stats)

if __name__ == "__main__":
    example_usage()
