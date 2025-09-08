#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import json
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def get_prediction_stats():
    """Récupère les statistiques des prédictions depuis la base de données"""
    try:
        conn = sqlite3.connect('predictions.db')
        cursor = conn.cursor()
        
        # Statistiques globales
        cursor.execute("SELECT COUNT(*) FROM predictions")
        total_predictions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM predictions WHERE resultat_reel IS NOT NULL")
        predictions_with_results = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction_correcte = 1")
        correct_predictions = cursor.fetchone()[0]
        
        # Taux de réussite
        success_rate = (correct_predictions / predictions_with_results * 100) if predictions_with_results > 0 else 0
        
        # Confiance moyenne
        cursor.execute("SELECT AVG(confiance_pct) FROM predictions")
        avg_confidence = cursor.fetchone()[0] or 0
        
        # Nombre de tournois uniques
        cursor.execute("SELECT COUNT(DISTINCT tournoi) FROM predictions")
        unique_tournaments = cursor.fetchone()[0]
        
        # Statistiques par tournoi
        cursor.execute("""
            SELECT tournoi, 
                   COUNT(*) as total, 
                   SUM(CASE WHEN resultat_reel IS NOT NULL THEN 1 ELSE 0 END) as avec_resultats,
                   SUM(CASE WHEN prediction_correcte = 1 THEN 1 ELSE 0 END) as correctes
            FROM predictions 
            GROUP BY tournoi 
            ORDER BY total DESC
        """)
        tournament_stats = cursor.fetchall()
        
        # Prédictions récentes avec résultats
        cursor.execute("""
            SELECT joueur_1, joueur_2, gagnant_predit, resultat_reel, 
                   prediction_correcte, confiance_pct, date_prediction
            FROM predictions 
            WHERE resultat_reel IS NOT NULL 
            ORDER BY date_prediction DESC 
            LIMIT 10
        """)
        recent_predictions = cursor.fetchall()
        
        conn.close()
        
        # Formatage des données
        tournament_data = []
        for row in tournament_stats:
            tournament, total, avec_resultats, correctes = row
            rate = (correctes / avec_resultats * 100) if avec_resultats > 0 else None
            tournament_data.append({
                'tournament': tournament,
                'total': total,
                'with_results': avec_resultats,
                'correct': correctes,
                'success_rate': rate
            })
        
        recent_data = []
        for row in recent_predictions:
            joueur_1, joueur_2, predit, reel, correct, confiance, date = row
            recent_data.append({
                'match': f"{joueur_1} vs {joueur_2}",
                'predicted': predit,
                'actual': reel,
                'correct': bool(correct),
                'confidence': confiance,
                'date': date
            })
        
        return {
            'global_stats': {
                'total_predictions': total_predictions,
                'predictions_with_results': predictions_with_results,
                'correct_predictions': correct_predictions,
                'success_rate': round(success_rate, 1),
                'avg_confidence': round(avg_confidence, 1),
                'unique_tournaments': unique_tournaments
            },
            'tournament_stats': tournament_data,
            'recent_predictions': recent_data
        }
        
    except Exception as e:
        print(f"Erreur lors de la récupération des statistiques: {e}")
        return None

@app.route('/api/stats')
def api_stats():
    """API endpoint pour récupérer les statistiques"""
    stats = get_prediction_stats()
    if stats:
        return jsonify(stats)
    else:
        return jsonify({'error': 'Erreur lors de la récupération des statistiques'}), 500

@app.route('/api/health')
def health_check():
    """Endpoint de vérification de santé"""
    return jsonify({'status': 'OK', 'message': 'API Stats Tennis fonctionnelle'})

if __name__ == '__main__':
    # Vérifier que la base de données existe
    if not os.path.exists('predictions.db'):
        print("Attention: predictions.db non trouvée!")
    
    print("API Stats Tennis demarree sur http://localhost:5001")
    print("Endpoint statistiques: http://localhost:5001/api/stats")
    app.run(host='0.0.0.0', port=5001, debug=True)
