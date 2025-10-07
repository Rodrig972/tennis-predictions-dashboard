"""
Dashboard Tennis fonctionnel - Avec intégration ML réelle
"""

from flask import Flask, render_template_string, jsonify, make_response
import pandas as pd
import json
from datetime import datetime
import os
from player_nationalities import get_player_nationality, get_country_flag_emoji
from ultimate_prediction_system import UltimateTennisPredictionSystem

app = Flask(__name__)

# Initialiser le système de prédiction
prediction_system = None
cached_predictions = None

def load_predictions():
    """Charge les vraies prédictions depuis le système ML ultime"""
    global prediction_system
    try:
        if prediction_system is None:
            prediction_system = UltimateTennisPredictionSystem()
        
        predictions = prediction_system.process_all_matches()
        print(f"Prédictions ML Ultimate chargées: {len(predictions)}")
        
        # Debug: afficher les premiers matchs
        if predictions:
            print("Premiers matchs chargés:")
            for i, match in enumerate(predictions[:3]):
                print(f"  {i+1}. {match['Match']} - {match['Tournoi']}")
        
        return predictions
    except Exception as e:
        print(f"Erreur chargement prédictions Ultimate: {e}")
        import traceback
        traceback.print_exc()
        return []

# Données de fallback si le système ML échoue - SYNCHRONISÉES avec les vraies données
SAMPLE_MATCHES = [
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
        "Confiance (%)": 58.7,
        "Cote J1": 3.86,
        "Cote J2": 1.27,
        "Round": "SF",
        "Modele": "Real ML (67.2%)",
        "Type": "ML",
        "Photo J1": "https://www.tennisexplorer.com/res/img/player/2yxhH1ya-KKWyfaNo.jpeg",
        "Photo J2": "https://www.tennisexplorer.com/res/img/player/CYLI6SbR-EZcCkAic.jpeg",
        "Lien Tennis Explorer": "https://www.tennisexplorer.com/match-detail/?id=3010463"
    },
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
        "Confiance (%)": 75.5,
        "Cote J1": 1.03,
        "Cote J2": 14.3,
        "Round": "SF",
        "Modele": "Real ML (67.2%)",
        "Type": "ML",
        "Photo J1": "https://www.tennisexplorer.com/res/img/player/OK7tW3bR-dEXkR0Wq.jpeg",
        "Photo J2": "https://www.tennisexplorer.com/res/img/player/t42zJFgg-8fYqFF2n.jpeg",
        "Lien Tennis Explorer": "https://www.tennisexplorer.com/match-detail/?id=3011243"
    },
    {
        "Match": "Sabalenka vs Anisimova",
        "Tournoi": "US Open (WTA)",
        "Date": "05/09/25",
        "Heure": "01:00",
        "Joueur 1": "Sabalenka",
        "Joueur 2": "Anisimova",
        "Classement J1": 1,
        "Classement J2": 9,
        "Gagnant Prédit": "Sabalenka",
        "Confiance (%)": 70.5,
        "Cote J1": 1.47,
        "Cote J2": 2.72,
        "Round": "SF",
        "Modele": "Real ML (67.2%)",
        "Type": "ML",
        "Photo J1": "https://www.tennisexplorer.com/res/img/player/EyiUUwFm-I9HZAz1R.jpeg",
        "Photo J2": "https://www.tennisexplorer.com/res/img/player/QHwt9QdA-0f842xJt.jpeg",
        "Lien Tennis Explorer": "https://www.tennisexplorer.com/match-detail/?id=3010531"
    }
]

@app.route('/')
def dashboard():
    # Force no-cache headers
    from flask import make_response
    try:
        """Page principale - dashboard dynamique avec données Excel en temps réel"""
        # Charger les prédictions Excel en temps réel
        predictions = load_predictions()
        
        # Convertir les types numpy en types Python pour la sérialisation JSON
        def convert_numpy_types(obj):
            if hasattr(obj, 'item'):  # numpy scalars
                return obj.item()
            elif isinstance(obj, dict):
                return {k: convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(v) for v in obj]
            return obj
        
        # Ajouter les drapeaux des pays et l'avantage domicile aux prédictions
        for prediction in predictions:
            # Drapeaux des joueurs
            j1_nationality = get_player_nationality(prediction.get('Joueur 1', ''))
            j2_nationality = get_player_nationality(prediction.get('Joueur 2', ''))
            
            prediction['Drapeau J1'] = get_country_flag_emoji(j1_nationality) if j1_nationality else ''
            prediction['Drapeau J2'] = get_country_flag_emoji(j2_nationality) if j2_nationality else ''
            prediction['Pays J1'] = j1_nationality or ''
            prediction['Pays J2'] = j2_nationality or ''
            
            # Avantage domicile
            from player_nationalities import is_home_advantage
            tournoi = prediction.get('Tournoi', '')
            j1_home = is_home_advantage(prediction.get('Joueur 1', ''), tournoi)
            j2_home = is_home_advantage(prediction.get('Joueur 2', ''), tournoi)
            
            prediction['Avantage Domicile J1'] = j1_home
            prediction['Avantage Domicile J2'] = j2_home
        
        predictions_clean = convert_numpy_types(predictions)
        predictions_json = json.dumps(predictions_clean, ensure_ascii=False)
        
        # Calculer le nombre de tournois uniques
        tournois_uniques = set()
        for prediction in predictions:
            if 'Tournoi' in prediction:
                tournois_uniques.add(prediction['Tournoi'])
        nb_tournois = len(tournois_uniques)
        
        # Créer le HTML avec les données en temps réel et timestamp pour forcer le refresh
        timestamp = datetime.now().strftime('%H:%M:%S')
        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎾 Tennis Predictions Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            color: #f8fafc; min-height: 100vh; margin: 0;
        }}
        .match-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.5);
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 30px 20px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.8rem; margin-bottom: 15px; color: #38bdf8; font-weight: 700; letter-spacing: -0.025em; }}
        .stats {{ 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; margin-bottom: 30px;
        }}
        .stat-card {{ 
            background: rgba(15, 23, 42, 0.8); padding: 24px; border-radius: 16px; border: 1px solid rgba(148, 163, 184, 0.1); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); transition: all 0.3s ease;
            text-align: center; backdrop-filter: blur(10px);
        }}
        .stat-number {{ font-size: 2.2rem; font-weight: 800; color: #38bdf8; margin-bottom: 8px; }}
        .matches-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; max-width: 1200px; margin: 0 auto; }}
        .match-card {{ 
            background: rgba(15, 23, 42, 0.9); padding: 20px; border-radius: 20px; max-width: 580px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4); transition: all 0.3s ease;
            backdrop-filter: blur(20px); border: 1px solid rgba(148, 163, 184, 0.15);
        }}
        .match-header {{ 
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;
        }}
        .tournament {{ 
            background: linear-gradient(135deg, #38bdf8, #0ea5e9); color: #0f172a; padding: 8px 16px; border-radius: 25px; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3);
            font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;
        }}
        .players {{ 
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;
        }}
        .player {{ text-align: center; flex: 1; }}
        .player-name {{ font-size: 1.25rem; font-weight: 600; margin-bottom: 6px; color: #f1f5f9; }}
        .ranking {{ color: #94a3b8; font-size: 0.9rem; font-weight: 500; }}
        .vs {{ margin: 0 20px; font-size: 1.5rem; color: #38bdf8; font-weight: bold; }}
        .prediction {{ 
            text-align: center; padding: 18px; background: rgba(34, 197, 94, 0.15);
            border-radius: 12px; border-left: 4px solid #22c55e;
            box-shadow: 0 4px 16px rgba(34, 197, 94, 0.1);
        }}
        .winner {{ font-size: 1.15rem; font-weight: 700; color: #22c55e; margin-bottom: 8px; }}
        .confidence {{ font-size: 1.4rem; font-weight: 800; color: #38bdf8; }}
        .filter-btn {{ 
            background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(148, 163, 184, 0.2); color: #e2e8f0; 
            padding: 10px 18px; border-radius: 25px; margin: 0 6px; cursor: pointer;
            font-weight: 500; transition: all 0.3s ease;
        }}
        .filter-btn.active {{ background: linear-gradient(135deg, #38bdf8, #0ea5e9); color: #0f172a; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎾 Tennis Predictions Dashboard</h1>
            <p>Prédictions ML avec Filtres Tournois • ATP/WTA 2025 • MAJ: {timestamp} • FILTRES TOURNOIS ACTIVÉS ✓</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="tournaments">{nb_tournois}</div>
                <div>TOURNOIS</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="total-matches">{len(predictions)}</div>
                <div>MATCHS TOTAUX</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="ml-predictions">{len(predictions)}</div>
                <div>PRÉDICTIONS ML</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">70.0%</div>
                <div>CONFIANCE MOYENNE</div>
            </div>
        </div>
        
        <div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <!-- Filtre par Confiance -->
            <div style="margin-bottom: 15px;">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="margin-right: 15px; font-weight: 600;">🎯 Filtrer par Confiance:</span>
                </div>
                <div>
                    <button class="filter-btn active" data-filter="all" data-type="confidence">Toutes</button>
                    <button class="filter-btn" data-filter="high" data-type="confidence">Haute (>70%)</button>
                    <button class="filter-btn" data-filter="medium" data-type="confidence">Moyenne (50-70%)</button>
                    <button class="filter-btn" data-filter="low" data-type="confidence">Faible (<50%)</button>
                </div>
            </div>
            
            <!-- Filtre par Tournoi -->
            <div>
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="margin-right: 15px; font-weight: 600;">🏆 Filtrer par Tournoi:</span>
                </div>
                <div id="tournament-filters">
                    <button class="filter-btn active" data-filter="all" data-type="tournament">Tous les Tournois</button>
                    <!-- Les boutons de tournois seront ajoutés dynamiquement -->
                </div>
            </div>
        </div>
        
        <div class="matches-grid" id="matches-container"></div>
    </div>

    <script>
        // Données Excel chargées en temps réel avec filtres de tournois
        const matches = {predictions_json};
        let allMatches = matches;
        let currentConfidenceFilter = 'all';
        let currentTournamentFilter = 'all';
        
        console.log('🔥 Données Excel en temps réel:', matches.length, 'matchs');
        if (matches.length > 0) {{
            console.log('🎾 Premier match:', matches[0].Match, '-', matches[0].Tournoi);
        }}
        
        // Générer les boutons de tournois dynamiquement
        function generateTournamentFilters() {{
            console.log('🏆 Génération des filtres de tournois...');
            const tournaments = [...new Set(matches.map(match => match.Tournoi))].sort();
            console.log('🏆 Tournois trouvés:', tournaments);
            
            const tournamentFiltersContainer = document.getElementById('tournament-filters');
            const allButton = tournamentFiltersContainer.querySelector('[data-filter="all"]');
            tournamentFiltersContainer.innerHTML = '';
            tournamentFiltersContainer.appendChild(allButton);
            
            tournaments.forEach(tournament => {{
                const button = document.createElement('button');
                button.className = 'filter-btn';
                button.setAttribute('data-filter', tournament);
                button.setAttribute('data-type', 'tournament');
                button.textContent = tournament;
                tournamentFiltersContainer.appendChild(button);
                console.log('➕ Bouton ajouté:', tournament);
            }});
        }}
        
        function filterMatches(matches, confidenceFilter, tournamentFilter) {{
            let filteredMatches = matches;
            
            // Filtre par confiance
            if (confidenceFilter !== 'all') {{
                filteredMatches = filteredMatches.filter(match => {{
                    const confidence = match['Confiance (%)'];
                    switch(confidenceFilter) {{
                        case 'high': return confidence > 70;
                        case 'medium': return confidence >= 50 && confidence <= 70;
                        case 'low': return confidence < 50;
                        default: return true;
                    }}
                }});
            }}
            
            // Filtre par tournoi
            if (tournamentFilter !== 'all') {{
                filteredMatches = filteredMatches.filter(match => match.Tournoi === tournamentFilter);
            }}
            
            return filteredMatches;
        }}
        
        function displayMatches(matchesToShow) {{
            const container = document.getElementById('matches-container');
            container.innerHTML = '';
            
            matchesToShow.forEach(match => {{
                const matchCard = document.createElement('div');
                matchCard.className = 'match-card';
                
                // Préparer l'affichage du contexte IA
                const aiContext = match.AI_Context;
                let aiInsightHTML = '';
                
                if (aiContext && aiContext.net_adjustment !== 0) {{
                    const advantage = aiContext.advantage;
                    const adjustment = aiContext.net_adjustment;
                    const absAdjustment = Math.abs(adjustment * 100).toFixed(1);
                    const color = adjustment > 0 ? '#22c55e' : adjustment < 0 ? '#ef4444' : '#94a3b8';
                    const icon = adjustment > 0 ? '📈' : adjustment < 0 ? '📉' : '➡️';
                    
                    // Récupérer les facteurs clés
                    const p1Context = aiContext.player1_context || {{}};
                    const p2Context = aiContext.player2_context || {{}};
                    const p1Factors = p1Context.key_factors || [];
                    const p2Factors = p2Context.key_factors || [];
                    
                    aiInsightHTML = `
                        <div style="margin-top: 12px; padding: 10px; background: rgba(56, 189, 248, 0.1); border-radius: 8px; border-left: 3px solid ${{color}};">
                            <div style="font-size: 0.85rem; font-weight: 600; color: ${{color}}; margin-bottom: 6px;">
                                ${{icon}} Analyse IA Contextuelle
                            </div>
                            <div style="font-size: 0.8rem; color: #cbd5e1; margin-bottom: 4px;">
                                Avantage psychologique: <strong style="color: ${{color}};">${{advantage}}</strong> (+${{absAdjustment}}%)
                            </div>
                            ${{p1Factors.length > 0 ? `
                                <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">
                                    🎾 ${{match["Joueur 1"]}}: ${{p1Factors.slice(0, 2).join(', ')}}
                                </div>
                            ` : ''}}
                            ${{p2Factors.length > 0 ? `
                                <div style="font-size: 0.75rem; color: #94a3b8;">
                                    🎾 ${{match["Joueur 2"]}}: ${{p2Factors.slice(0, 2).join(', ')}}
                                </div>
                            ` : ''}}
                        </div>
                    `;
                }}
                
                matchCard.innerHTML = `
                    <div class="match-header">
                        <div class="tournament">${{match.Tournoi}}</div>
                        <div style="color: #b0bec5;">${{match.Date}} - ${{match.Heure}}</div>
                    </div>
                    
                    <div style="text-align: center; padding: 12px 0; background: rgba(56, 189, 248, 0.1); border-radius: 8px; margin-bottom: 15px;">
                        <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px;">Head to Head</div>
                        <div style="font-size: 1.3rem; font-weight: 700; color: #38bdf8;">
                            ${{match["H2H J1"] || "0-0"}}
                        </div>
                    </div>
                    
                    <div class="players">
                        <div class="player">
                            <div class="player-name">${{match["Joueur 1"]}}</div>
                            <div class="ranking">Classement: ${{match["Classement J1"]}}</div>
                            <div class="ranking">Cote: ${{match["Cote J1"]}}</div>
                        </div>
                        <div class="vs">VS</div>
                        <div class="player">
                            <div class="player-name">${{match["Joueur 2"]}}</div>
                            <div class="ranking">Classement: ${{match["Classement J2"]}}</div>
                            <div class="ranking">Cote: ${{match["Cote J2"]}}</div>
                        </div>
                    </div>
                    
                    <div class="prediction">
                        <div class="winner">🏆 Favori: ${{match["Gagnant Prédit"]}}</div>
                        <div class="confidence">${{match["Confiance (%)"]}}%</div>
                        <div style="margin-top: 10px;">
                            <a href="${{match["Lien Tennis Explorer"] || '#'}}" target="_blank" 
                               style="color: #4fc3f7; text-decoration: none; font-size: 0.9rem;">
                                🔗 Tennis Explorer
                            </a>
                        </div>
                    </div>
                    
                    ${{aiInsightHTML}}
                `;
                
                container.appendChild(matchCard);
            }});
        }}
        
        // Gestionnaire d'événements pour les filtres
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('🔧 Initialisation des filtres avec tournois...');
            
            // Générer les filtres de tournois
            generateTournamentFilters();
            
            // Attacher les listeners après génération
            setTimeout(() => {{
                const filterButtons = document.querySelectorAll('.filter-btn');
                console.log('🎯 Boutons de filtre trouvés:', filterButtons.length);
                
                filterButtons.forEach(button => {{
                    button.addEventListener('click', function() {{
                        const filterType = this.dataset.type;
                        const filterValue = this.dataset.filter;
                        console.log('🔄 Filtre cliqué:', filterType, '-', filterValue);
                        
                        if (filterType === 'confidence') {{
                            document.querySelectorAll('[data-type="confidence"]').forEach(btn => btn.classList.remove('active'));
                            this.classList.add('active');
                            currentConfidenceFilter = filterValue;
                        }} else if (filterType === 'tournament') {{
                            document.querySelectorAll('[data-type="tournament"]').forEach(btn => btn.classList.remove('active'));
                            this.classList.add('active');
                            currentTournamentFilter = filterValue;
                        }}
                        
                        // Appliquer les filtres combinés
                        const filteredMatches = filterMatches(allMatches, currentConfidenceFilter, currentTournamentFilter);
                        displayMatches(filteredMatches);
                        console.log('✅ Filtres appliqués:', currentConfidenceFilter, '+', currentTournamentFilter, '=', filteredMatches.length, 'matchs');
                        
                        // Mettre à jour le compteur
                        document.getElementById('total-matches').textContent = filteredMatches.length;
                    }});
                }});
            }}, 100);
        }});
        
        // Afficher tous les matchs par défaut
        displayMatches(matches);
        console.log('✅ Dashboard avec filtres de tournois affiché avec', matches.length, 'matchs');
    </script>
</body>
</html>"""
    
        return html_content
    
    except Exception as e:
        print(f"Erreur dans dashboard(): {e}")
        return f"<h1>Erreur: {e}</h1><p>Vérifiez que le fichier Excel existe et est accessible.</p>"

@app.route('/dashboard_old')
def dashboard_old():
    return '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎾 Tennis Predictions Dashboard</title>
    <style>
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        .stat-card {
            background: white;
            padding: 15px 10px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            min-width: 0;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        .stat-number {
            font-size: 2.2rem;
            font-weight: 800;
            color: #3b82f6;
            margin-bottom: 5px;
        }
        .stat-card div:last-child {
            color: #6b7280;
            font-weight: 500;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .matches-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 20px;
        }
        .match-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
            position: relative;
            overflow: hidden;
            min-width: 0;
            box-sizing: border-box;
            max-width: 480px;
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
            margin-bottom: 30px;
        }
        
        .tournament-title {
            color: #3b82f6;
            margin-bottom: 15px;
            font-size: 1.5rem;
            font-weight: 600;
        }

        .filter-section {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }

        .filter-section h3 {
            margin: 0 0 15px 0;
            color: #1f2937;
            font-size: 1.2rem;
        }

        .filter-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .filter-btn {
            padding: 8px 16px;
            border: 2px solid #e5e7eb;
            background: white;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
            color: #6b7280;
        }

        .filter-btn:hover {
            border-color: #3b82f6;
            color: #3b82f6;
        }

        .filter-btn.active {
            background: #3b82f6;
            border-color: #3b82f6;
            color: white;
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
            <p>Prédictions ML en temps réel • Tournois ATP/WTA 2025</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="tournaments">4</div>
                <div>Tournois</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="total-matches">13</div>
                <div>Matchs Totaux</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="ml-predictions">13</div>
                <div>Prédictions ML</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="avg-confidence">58.0%</div>
                <div>Confiance Moyenne</div>
            </div>
        </div>

        <!-- Filtres par niveau de confiance -->
        <div class="filter-section">
            <h3>🎯 Filtrer par Confiance</h3>
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="all">Toutes</button>
                <button class="filter-btn" data-filter="high">Haute (>70%)</button>
                <button class="filter-btn" data-filter="medium">Moyenne (50-70%)</button>
                <button class="filter-btn" data-filter="low">Faible (<50%)</button>
            </div>
        </div>

        <div id="matches-container">
            <!-- Les tournois seront générés dynamiquement -->
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

        // Variables globales
        let allMatches = [];
        let currentFilter = 'all';

        // Fonctions de filtrage
        function filterMatches(matches, filter) {
            if (filter === 'all') return matches;
            
            return matches.filter(match => {
                const confidence = match['Confiance (%)'];
                switch(filter) {
                    case 'high': return confidence > 70;
                    case 'medium': return confidence >= 50 && confidence <= 70;
                    case 'low': return confidence < 50;
                    default: return true;
                }
            });
        }

        function displayMatches(matches) {
            // Grouper les matchs par tournoi
            const tournamentGroups = {};
            matches.forEach(match => {
                const tournament = match.Tournoi;
                if (!tournamentGroups[tournament]) {
                    tournamentGroups[tournament] = [];
                }
                tournamentGroups[tournament].push(match);
            });
            
            // Vider le conteneur principal
            const matchesContainer = document.getElementById('matches-container');
            matchesContainer.innerHTML = '';
            
            // Créer une section pour chaque tournoi
            Object.keys(tournamentGroups).forEach(tournament => {
                const tournamentMatches = tournamentGroups[tournament];
                
                // Déterminer l'emoji du tournoi
                let emoji = '🏆';
                if (tournament.includes('US Open')) emoji = '🇺🇸';
                else if (tournament.includes('Guadalajara')) emoji = '🇲🇽';
                else if (tournament.includes('Sao Paulo')) emoji = '🇧🇷';
                
                const tournamentSection = document.createElement('div');
                tournamentSection.className = 'tournament-section';
                tournamentSection.innerHTML = `
                    <h2 class="tournament-title">${emoji} ${tournament}</h2>
                    <div class="matches-grid">
                        ${tournamentMatches.map(match => createMatchCard(match)).join('')}
                    </div>
                `;
                
                matchesContainer.appendChild(tournamentSection);
            });
        }

        function updateStats(matches) {
            document.getElementById('total-matches').textContent = allMatches.length;
            document.getElementById('ml-predictions').textContent = allMatches.length;
            
            const avgConfidence = allMatches.reduce((sum, m) => sum + m['Confiance (%)'], 0) / allMatches.length;
            document.getElementById('avg-confidence').textContent = avgConfidence.toFixed(1) + '%';
            
            const tournamentGroups = {};
            matches.forEach(match => {
                if (!tournamentGroups[match.Tournoi]) {
                    tournamentGroups[match.Tournoi] = true;
                }
            });
            document.getElementById('tournaments').textContent = Object.keys(tournamentGroups).length;
        }

        // Gestionnaire d'événements pour les filtres
        document.addEventListener('DOMContentLoaded', function() {
            const filterButtons = document.querySelectorAll('.filter-btn');
            filterButtons.forEach(button => {
                button.addEventListener('click', function() {
                    // Retirer la classe active de tous les boutons
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    // Ajouter la classe active au bouton cliqué
                    this.classList.add('active');
                    
                    // Appliquer le filtre
                    currentFilter = this.dataset.filter;
                    const filteredMatches = filterMatches(allMatches, currentFilter);
                    displayMatches(filteredMatches);
                    updateStats(filteredMatches);
                });
            });
        });

        // Charger les données DIRECTEMENT depuis le système de prédiction
        console.log('🔥 Chargement DIRECT des données Excel...');
        
        // Utiliser les données déjà chargées par le système Python
        const matches = {{ predictions_json | safe }};
        
        console.log('✅ Données Excel chargées:', matches.length, 'matchs');
        if (matches.length > 0) {
            console.log('🎾 Premier match:', matches[0].Match, '-', matches[0].Tournoi);
        }
        
        // Stocker tous les matchs
        allMatches = matches;
        
        // Afficher tous les matchs par défaut
        displayMatches(allMatches);
        updateStats(allMatches);
        
        console.log('✅ Interface mise à jour avec les vraies données Excel');
    </script>
</body>
</html>
    '''

@app.route('/api/matches')
def get_matches():
    """Retourne FORCÉMENT les prédictions Excel - 16 matchs"""
    try:
        # Import direct et création système frais
        import importlib
        import sys
        
        # Forcer le rechargement du module
        if 'ultimate_prediction_system' in sys.modules:
            importlib.reload(sys.modules['ultimate_prediction_system'])
        
        from ultimate_prediction_system import UltimateTennisPredictionSystem
        
        # Nouveau système à chaque appel
        system = UltimateTennisPredictionSystem()
        predictions = system.process_all_matches()
        
        print(f"🔥 API FORCÉE: {len(predictions)} prédictions Excel chargées")
        if predictions:
            print(f"🎾 Premier match: {predictions[0]['Match']} - {predictions[0]['Tournoi']}")
        
        # TOUJOURS retourner les prédictions Excel (pas de fallback)
        return jsonify(predictions)
            
    except Exception as e:
        print(f"❌ Erreur API Excel: {e}")
        import traceback
        traceback.print_exc()
        # En cas d'erreur, retourner une liste vide plutôt que les anciennes données
        return jsonify([])

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'OK',
        'matches': len(SAMPLE_MATCHES),
        'ml_active': True,
        'system': 'SimpleML Dashboard'
    })

@app.route('/api/excel-matches')
def get_excel_matches():
    """Route dédiée pour forcer les données Excel uniquement"""
    try:
        from ultimate_prediction_system import UltimateTennisPredictionSystem
        system = UltimateTennisPredictionSystem()
        predictions = system.process_all_matches()
        
        print(f"🔥 EXCEL API: {len(predictions)} matchs depuis Excel")
        if predictions:
            print(f"🎾 Match 1: {predictions[0]['Match']} - {predictions[0]['Tournoi']}")
            print(f"🎾 Match 2: {predictions[1]['Match']} - {predictions[1]['Tournoi']}")
        
        return jsonify(predictions)
    except Exception as e:
        print(f"❌ Erreur Excel API: {e}")
        return jsonify([])

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

@app.route('/stats.html')
def stats_page():
    """Servir la page des statistiques"""
    try:
        with open('stats.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Page stats.html non trouvée", 404

@app.route('/excel-direct')
def excel_direct():
    """Dashboard Excel direct sans redirection"""
    # Charger les prédictions Excel directement
    predictions = load_predictions()
    
    # Convertir les types numpy en types Python pour la sérialisation JSON
    def convert_numpy_types(obj):
        if hasattr(obj, 'item'):  # numpy scalars
            return obj.item()
        elif isinstance(obj, dict):
            return {k: convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(v) for v in obj]
        return obj
    
    predictions_clean = convert_numpy_types(predictions)
    predictions_json = json.dumps(predictions_clean, ensure_ascii=False, indent=2)
    
    # Créer le HTML avec les données intégrées
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎾 Tennis Predictions Dashboard - Excel Data</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            color: white; min-height: 100vh; margin: 0;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 30px 20px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; color: #4fc3f7; }}
        .stats {{ 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; margin-bottom: 30px;
        }}
        .stat-card {{ 
            background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; text-align: center; backdrop-filter: blur(10px);
        }}
        .stat-number {{ font-size: 2rem; font-weight: bold; color: #4fc3f7; }}
        .matches-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; max-width: 1200px; margin: 0 auto; }}
        .match-card {{ 
            background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 15px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); max-width: 480px;
        }}
        .match-header {{ 
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;
        }}
        .tournament {{ 
            background: linear-gradient(135deg, #38bdf8, #0ea5e9); color: #0f172a; padding: 8px 16px; border-radius: 25px; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3); font-weight: bold; font-size: 0.9rem;
        }}
        .players {{ 
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;
        }}
        .player {{ text-align: center; flex: 1; }}
        .player-name {{ font-size: 1.25rem; font-weight: 600; margin-bottom: 6px; color: #f1f5f9; }}
        .ranking {{ color: #94a3b8; font-size: 0.9rem; font-weight: 500; }}
        .vs {{ margin: 0 20px; font-size: 1.5rem; color: #38bdf8; font-weight: bold; }}
        .prediction {{ 
            text-align: center; padding: 18px; background: rgba(34, 197, 94, 0.15);
            border-radius: 12px; border-left: 4px solid #22c55e;
            box-shadow: 0 4px 16px rgba(34, 197, 94, 0.1);
        }}
        .winner {{ font-size: 1.15rem; font-weight: 700; color: #22c55e; margin-bottom: 8px; }}
        .confidence {{ font-size: 1.4rem; font-weight: 800; color: #38bdf8; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎾 Tennis Predictions Dashboard</h1>
            <p>Prédictions ML en temps réel • Données Excel • {len(predictions)} matchs</p>
        </div>
        
        <div class="stats">
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            color: #4fc3f7;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            backdrop-filter: blur(10px);
        }}
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #4fc3f7;
        }}
        .matches-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            max-width: 1000px;
            margin: 0 auto;
        }}
        .match-card {{
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 480px;
        }}
        .match-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .tournament {{
            background: #4fc3f7;
            color: #1e3c72;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
        }}
        .players {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .player {{
            text-align: center;
            flex: 1;
        }}
        .player-name {{
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .ranking {{
            color: #b0bec5;
            font-size: 0.9rem;
        }}
        .vs {{
            margin: 0 20px;
            font-size: 1.5rem;
            color: #4fc3f7;
            font-weight: bold;
        }}
        .prediction {{
            text-align: center;
            padding: 15px;
            background: rgba(76, 175, 80, 0.2);
            border-radius: 10px;
            border-left: 4px solid #4caf50;
        }}
        .winner {{
            font-size: 1.1rem;
            font-weight: bold;
            color: #4caf50;
            margin-bottom: 5px;
        }}
        .confidence {{
            font-size: 1.3rem;
            font-weight: bold;
            color: #4fc3f7;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎾 Tennis Predictions Dashboard</h1>
            <p>Prédictions ML en temps réel • Données Excel • {len(predictions)} matchs</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="tournaments">{nb_tournois}</div>
                <div>Tournois</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(predictions)}</div>
                <div>Matchs Totaux</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(predictions)}</div>
                <div>Prédictions ML</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">85.2%</div>
                <div>Confiance Moyenne</div>
            </div>
        </div>
        
        <div class="matches-grid" id="matches-container">
            <!-- Les matchs seront injectés ici par JavaScript -->
        </div>
    </div>

    <script>
        // Données Excel chargées directement
        const matches = {predictions_json};
        
        console.log('🔥 Données Excel chargées:', matches.length, 'matchs');
        if (matches.length > 0) {{
            console.log('🎾 Premier match:', matches[0].Match, '-', matches[0].Tournoi);
        }}
        
        function displayMatches(matchesToShow) {{
            const container = document.getElementById('matches-container');
            container.innerHTML = '';
            
            matchesToShow.forEach(match => {{
                const matchCard = document.createElement('div');
                matchCard.className = 'match-card';
                
                matchCard.innerHTML = `
                    <div class="match-header">
                        <div class="tournament">${{match.Tournoi}}</div>
                        <div style="color: #b0bec5;">${{match.Date}} - ${{match.Heure}}</div>
                    </div>
                    
                    <div class="players">
                        <div class="player">
                            <div class="player-name">${{match["Joueur 1"]}}</div>
                            <div class="ranking">Classement: ${{match["Classement J1"]}}</div>
                            <div class="ranking">Cote: ${{match["Cote J1"]}}</div>
                        </div>
                        <div class="vs">VS</div>
                        <div class="player">
                            <div class="player-name">${{match["Joueur 2"]}}</div>
                            <div class="ranking">Classement: ${{match["Classement J2"]}}</div>
                            <div class="ranking">Cote: ${{match["Cote J2"]}}</div>
                        </div>
                    </div>
                    
                    <div class="prediction">
                        <div class="winner">🏆 Gagnant prédit: ${{match["Gagnant Prédit"]}}</div>
                        <div class="confidence">${{match["Confiance (%)"]}}% de confiance</div>
                    </div>
                `;
                
                container.appendChild(matchCard);
            }});
        }}
        
        // Afficher tous les matchs
        displayMatches(matches);
        
        console.log('✅ Dashboard Excel affiché avec', matches.length, 'matchs');
    </script>
</body>
</html>
    """
    
    return html_content

@app.route('/index.html')
def index_page():
    """Servir la page index"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Page index.html non trouvée", 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    print("=== DASHBOARD TENNIS FONCTIONNEL ===")
    
    # Charger les vraies prédictions au démarrage et vider le cache
    cached_predictions = None
    real_predictions = load_predictions()
    if real_predictions:
        cached_predictions = real_predictions
        match_count = len(real_predictions)
    else:
        match_count = len(SAMPLE_MATCHES)
    print(f"Matchs charges: {match_count}")
    print(f"Application disponible sur le port: {port}")
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5003))
    app.run(debug=True, host='0.0.0.0', port=port)
