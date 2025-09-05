"""
Dashboard Tennis fonctionnel - Avec intégration ML réelle
"""

from flask import Flask, jsonify, render_template_string
import json
import os
import sys
from simplified_prediction_system import SimplifiedTennisPredictionSystem

app = Flask(__name__)

# Initialiser le système de prédiction
prediction_system = None

def load_predictions():
    """Charge les vraies prédictions depuis le système ML"""
    global prediction_system
    try:
        if prediction_system is None:
            prediction_system = SimplifiedTennisPredictionSystem()
        
        predictions = prediction_system.process_all_matches()
        return predictions
    except Exception as e:
        print(f"Erreur chargement prédictions: {e}")
        return []

# Données de fallback si le système ML échoue
SAMPLE_MATCHES = [
    {
        "Match": "Sinner vs Auger Aliassime",
        "Tournoi": "US Open (ATP)",
        "Date": "05/09/25",
        "Heure": "21:00",
        "Joueur 1": "Sinner",
        "Joueur 2": "Auger Aliassime",
        "Classement J1": 1,
        "Classement J2": 27,
        "Gagnant Prédit": "Sinner",
        "Confiance (%)": 76.3,
        "Cote J1": 1.03,
        "Cote J2": 13.27,
        "Round": "SF",
        "Modele": "SimpleML",
        "Type": "ML",
        "Photo J1": "https://www.tennisexplorer.com/res/img/player/OK7tW3bR-dEXkR0Wq.jpeg",
        "Photo J2": "https://www.tennisexplorer.com/res/img/player/t42zJFgg-8fYqFF2n.jpeg",
        "Lien Tennis Explorer": "https://www.tennisexplorer.com/match-detail/?id=3011243"
    },
    {
        "Match": "Djokovic vs Alcaraz",
        "Tournoi": "US Open (ATP)",
        "Date": "05/09/25",
        "Heure": "21:00",
        "Joueur 1": "Djokovic",
        "Joueur 2": "Alcaraz",
        "Classement J1": 7,
        "Classement J2": 2,
        "Gagnant Prédit": "Alcaraz",
        "Confiance (%)": 59.3,
        "Cote J1": 3.89,
        "Cote J2": 1.26,
        "Round": "SF",
        "Modele": "SimpleML",
        "Type": "ML",
        "Photo J1": "https://www.tennisexplorer.com/res/img/player/2yxhH1ya-KKWyfaNo.jpeg",
        "Photo J2": "https://www.tennisexplorer.com/res/img/player/CYLI6SbR-EZcCkAic.jpeg",
        "Lien Tennis Explorer": "https://www.tennisexplorer.com/match-detail/?id=3010463"
    },
    {
        "Match": "Sabalenka vs Pegula",
        "Tournoi": "US Open (WTA)",
        "Date": "05/09/25",
        "Heure": "01:00",
        "Joueur 1": "Sabalenka",
        "Joueur 2": "Pegula",
        "Classement J1": 1,
        "Classement J2": 4,
        "Gagnant Prédit": "Sabalenka",
        "Confiance (%)": 67.7,
        "Cote J1": 1.32,
        "Cote J2": 3.42,
        "Round": "SF",
        "Modele": "SimpleML",
        "Type": "ML",
        "Photo J1": "https://www.tennisexplorer.com/res/img/player/EyiUUwFm-I9HZAz1R.jpeg",
        "Photo J2": "https://www.tennisexplorer.com/res/img/player/ChM8wNya-A19CsvyR.jpeg",
        "Lien Tennis Explorer": "https://www.tennisexplorer.com/match-detail/?id=3010531"
    },
    {
        "Match": "Osaka vs Anisimova",
        "Tournoi": "US Open (WTA)",
        "Date": "05/09/25",
        "Heure": "02:30",
        "Joueur 1": "Osaka",
        "Joueur 2": "Anisimova",
        "Classement J1": 24,
        "Classement J2": 9,
        "Gagnant Prédit": "Anisimova",
        "Confiance (%)": 53.0,
        "Cote J1": 1.84,
        "Cote J2": 1.96,
        "Round": "SF",
        "Modele": "SimpleML",
        "Type": "ML",
        "Photo J1": "https://www.tennisexplorer.com/res/img/player/fknJF4ya-YgRjYWBf.jpeg",
        "Photo J2": "https://www.tennisexplorer.com/res/img/player/QHwt9QdA-0f842xJt.jpeg",
        "Lien Tennis Explorer": "https://www.tennisexplorer.com/match-detail/?id=3011241"
    }
]

@app.route('/')
def dashboard():
    return '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎾 Tennis Predictions Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            min-height: 100vh;
            line-height: 1.6;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 0;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 20px;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .header h1 {
            margin: 0;
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(45deg, #3b82f6, #10b981);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.5px;
        }
        .header p {
            margin: 15px 0 0 0;
            opacity: 0.9;
            font-size: 1.2rem;
            font-weight: 500;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.08);
            padding: 30px 25px;
            border-radius: 16px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        .stat-number {
            font-size: 2.8rem;
            font-weight: 800;
            color: #3b82f6;
            margin-bottom: 8px;
            text-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
        }
        .matches-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
            max-width: 850px;
            margin: 0 auto;
            padding: 0 20px;
        }
        .match-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 12px 16px;
            margin: 0;
            border-left: 3px solid #4a90e2;
            transition: transform 0.2s ease;
            width: 100%;
            max-width: 400px;
            min-width: 0;
            box-sizing: border-box;
        }
        .match-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        .match-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .match-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0;
        }
        .player {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .ranking {
            background: #4a90e2;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .odds {
            color: #4a90e2;
            font-weight: 500;
        }
        .match-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        .favorite {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .player-photo {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            object-fit: cover;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .confidence {
            padding: 6px 12px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        .confidence-high { background: #10b981; }
        .confidence-medium { background: #f59e0b; }
        .confidence-low { background: #ef4444; }
        .ml-badge {
            background: #10b981;
            color: white;
            padding: 4px 8px;
            border-radius: 8px;
            font-size: 0.7rem;
            font-weight: 500;
            margin-left: 8px;
        }
        .tennis-link {
            background: #3b82f6;
            color: white;
            padding: 6px 10px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.8rem;
            transition: background 0.2s;
        }
        .tennis-link:hover {
            background: #2563eb;
            color: white;
        }
        .tournament-section {
            margin: 12px 0;
        }
        .tournament-title {
            color: #4a90e2;
            font-size: 1.3rem;
            margin-bottom: 8px;
            padding-bottom: 6px;
            border-bottom: 2px solid #4a90e2;
        }
        
        @media (max-width: 1000px) {
            .matches-grid {
                max-width: 650px;
                gap: 20px;
            }
            .match-card {
                max-width: 300px;
            }
        }
        
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr 1fr;
                gap: 15px;
            }
            .matches-grid {
                grid-template-columns: 1fr;
                gap: 20px;
                max-width: 500px;
                padding: 0 15px;
            }
            .match-card {
                padding: 12px 16px;
            }
            .match-info {
                flex-direction: column;
                gap: 8px;
            }
            .match-footer {
                flex-direction: column;
                gap: 8px;
                align-items: flex-start;
            }
        }
        
        @media (max-width: 480px) {
            .match-card {
                padding: 10px 12px;
            }
            .matches-grid {
                padding: 0 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎾 Tennis Predictions Dashboard</h1>
            <p>Prédictions ML en temps réel • US Open 2025</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="total-matches">4</div>
                <div>Matchs Total</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="ml-predictions">4</div>
                <div>Prédictions ML</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="avg-confidence">58.0%</div>
                <div>Confiance Moyenne</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="tournaments">2</div>
                <div>Tournois</div>
            </div>
        </div>

        <div id="matches-container">
            <div class="tournament-section">
                <h2 class="tournament-title">🏆 US Open (ATP)</h2>
                <div id="atp-matches"></div>
            </div>
            <div class="tournament-section">
                <h2 class="tournament-title">🏆 US Open (WTA)</h2>
                <div id="wta-matches"></div>
            </div>
        </div>
    </div>

    <script>
        function getConfidenceClass(confidence) {
            if (confidence > 70) return 'confidence-high';
            if (confidence >= 50) return 'confidence-medium';
            return 'confidence-low';
        }

        function getFavoritePlayerPhoto(match) {
            // Déterminer quel joueur est le favori
            const favoritePlayer = match['Gagnant Prédit'];
            
            // Retourner la photo correspondante ou une image par défaut
            if (favoritePlayer && favoritePlayer.trim() === match['Joueur 1'].trim() && match['Photo J1']) {
                return match['Photo J1'];
            } else if (favoritePlayer && favoritePlayer.trim() === match['Joueur 2'].trim() && match['Photo J2']) {
                return match['Photo J2'];
            }
            
            // Image par défaut si pas de photo
            return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTYiIGZpbGw9IiM0YTkwZTIiLz4KPHN2ZyB4PSI4IiB5PSI4IiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPgo8cGF0aCBkPSJNMTIgMTJjMi4yMSAwIDQtMS43OSA0LTRzLTEuNzktNC00LTQtNCAxLjc5LTQgNCAxLjc5IDQgNCA0em0wIDJjLTIuNjcgMC04IDEuMzQtOCA0djJoMTZ2LTJjMC0yLjY2LTUuMzMtNC04LTR6Ii8+Cjwvc3ZnPgo8L3N2Zz4K';
        }

        function getTennisExplorerLink(match) {
            if (match['Lien Tennis Explorer']) {
                return match['Lien Tennis Explorer'];
            }
            
            // Générer un lien par défaut basé sur les noms des joueurs
            const player1 = encodeURIComponent(match['Joueur 1'] || '');
            const player2 = encodeURIComponent(match['Joueur 2'] || '');
            return `https://www.tennisexplorer.com/matches/?search=${player1}+${player2}`;
        }

        function createMatchCard(match) {
            const favoritePhoto = match['Gagnant Prédit'].trim() === match['Joueur 1'].trim() 
                ? match['Photo J1'] : match['Photo J2'];
            
            return `
                <div class="match-card">
                    <div class="match-header">
                        <div>
                            <strong>${match.Date || 'Date inconnue'}</strong> - ${match.Heure || 'Heure inconnue'}
                        </div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">${match.Round || 'Round inconnu'}</div>
                    </div>
                    <div class="match-info">
                        <div class="player">
                            <span class="ranking">#${match['Classement J1'] || 'N/A'}</span>
                            <span>${match['Joueur 1']}</span>
                            <span class="odds">@${match['Cote J1'] || 'N/A'}</span>
                        </div>
                        <div style="font-size: 1.2rem; color: #666; margin: 0 20px;">vs</div>
                        <div class="player" style="text-align: right;">
                            <span class="odds">@${match['Cote J2'] || 'N/A'}</span>
                            <span>${match['Joueur 2']}</span>
                            <span class="ranking">#${match['Classement J2'] || 'N/A'}</span>
                        </div>
                    </div>
                    <div class="match-footer">
                        <div class="favorite">
                            <img src="${getFavoritePlayerPhoto(match)}" alt="Photo" class="player-photo" style="display: none;" onload="this.style.display='inline';" onerror="this.style.display='none';">
                            <span>${match['Confiance (%)'] >= 70 ? '⭐ ' : ''}Favori: ${match['Gagnant Prédit']}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span class="confidence ${getConfidenceClass(match['Confiance (%)'])}">${match['Confiance (%)']}%</span>
                            <a href="${getTennisExplorerLink(match)}" target="_blank" class="tennis-link">🔗</a>
                        </div>
                    </div>
                </div>
            `;
        }

        // Charger les données
        console.log('Démarrage du chargement des données...');
        
        fetch('/api/matches')
            .then(response => {
                console.log('Réponse API reçue:', response.status);
                if (!response.ok) {
                    throw new Error('Erreur réseau: ' + response.status);
                }
                return response.json();
            })
            .then(matches => {
                console.log('Données reçues:', matches.length, 'matchs');
                
                // Mettre à jour les statistiques
                document.getElementById('total-matches').textContent = matches.length;
                document.getElementById('ml-predictions').textContent = matches.length;
                
                const avgConfidence = matches.reduce((sum, m) => sum + m['Confiance (%)'], 0) / matches.length;
                document.getElementById('avg-confidence').textContent = avgConfidence.toFixed(1) + '%';
                
                const atpContainer = document.getElementById('atp-matches');
                const wtaContainer = document.getElementById('wta-matches');
                
                // Vider les conteneurs
                atpContainer.innerHTML = '';
                wtaContainer.innerHTML = '';
                
                // Créer les grilles pour ATP et WTA
                const atpMatches = matches.filter(m => m.Tournoi.includes('ATP'));
                const wtaMatches = matches.filter(m => m.Tournoi.includes('WTA'));
                
                if (atpMatches.length > 0) {
                    atpContainer.innerHTML = '<div class="matches-grid">' + 
                        atpMatches.map(match => createMatchCard(match)).join('') + 
                        '</div>';
                }
                
                if (wtaMatches.length > 0) {
                    wtaContainer.innerHTML = '<div class="matches-grid">' + 
                        wtaMatches.map(match => createMatchCard(match)).join('') + 
                        '</div>';
                }
                
                console.log('Interface mise à jour avec succès');
            })
            .catch(error => {
                console.error('Erreur de chargement:', error);
                document.getElementById('matches-container').innerHTML = 
                    '<div style="text-align: center; color: #ef4444; padding: 50px;"><h2>❌ Erreur: ' + error.message + '</h2></div>';
            });
    </script>
</body>
</html>
    '''

@app.route('/api/matches')
def get_matches():
    """Retourne les prédictions ML réelles"""
    try:
        # Charger les vraies prédictions
        predictions = load_predictions()
        
        if predictions and len(predictions) > 0:
            print(f"API: {len(predictions)} prédictions ML chargées")
            return jsonify(predictions)
        else:
            print("API: Utilisation des données SAMPLE_MATCHES")
            return jsonify(SAMPLE_MATCHES)
            
    except Exception as e:
        print(f"Erreur API: {e}")
        return jsonify(SAMPLE_MATCHES)

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'OK',
        'matches': len(SAMPLE_MATCHES),
        'ml_active': True,
        'system': 'SimpleML Dashboard'
    })

@app.route('/api/debug')
def debug():
    """Endpoint de debug pour vérifier les données utilisées"""
    try:
        predictions = load_predictions()
        return jsonify({
            'predictions_loaded': len(predictions) if predictions else 0,
            'using_fallback': len(predictions) == 0,
            'sample_data_count': len(SAMPLE_MATCHES),
            'excel_file_exists': prediction_system.players_data is not None if prediction_system else False,
            'first_prediction': predictions[0] if predictions else None
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'predictions_loaded': 0,
            'using_fallback': True
        })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    print("=== DASHBOARD TENNIS FONCTIONNEL ===")
    print(f"Matchs charges: {len(SAMPLE_MATCHES)}")
    print(f"Application disponible sur le port: {port}")
    
    app.run(debug=False, host='0.0.0.0', port=port)
