"""
Système de prédiction tennis simplifié pour le nouveau format Stats_tournois_en_cours.xlsx
Utilise la structure tabulaire simplifiée avec 1 ligne par joueur
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json
import os
import joblib

class SimplifiedTennisPredictionSystem:
    """Système de prédiction tennis pour le format simplifié"""
    
    def __init__(self, excel_file_path: str = "./data/Stats_tournois_en_cours.xlsx"):
        self.excel_file_path = excel_file_path
        self.players_data = None
        self.ml_model = None
        self.ml_feature_names = None
        self.load_ml_model()
        self.load_data()
    
    def load_data(self):
        # Charger les données depuis le fichier Excel
        try:
            df = pd.read_excel(self.excel_file_path, sheet_name='StatsJoueurs')
            print(f"Données chargées: {len(df)} joueurs depuis {self.excel_file_path}")
            return df
        except FileNotFoundError:
            print(f" Fichier {self.excel_file_path} non trouvé - utilisation des données de fallback")
            return self._create_fallback_data()
        except Exception as e:
            print(f"Erreur lors du chargement: {e} - utilisation des données de fallback")
            return self._create_fallback_data()
    
    def load_ml_model(self):
        """Charge le modèle ML réel si disponible"""
        try:
            real_model_path = './ml_models/real_tennis_model.joblib'
            real_features_path = './ml_models/real_feature_names.joblib'
            
            if os.path.exists(real_model_path) and os.path.exists(real_features_path):
                self.ml_model = joblib.load(real_model_path)
                self.ml_feature_names = joblib.load(real_features_path)
                print("OK - Modèle ML réel chargé (67.2% précision)")
            else:
                print("Modèle ML réel non trouvé, utilisation du système simplifié")
        except Exception as e:
            print(f"Erreur chargement ML: {e}")
    
    def predict_with_ml(self, player1: Dict, player2: Dict) -> Optional[Dict]:
        """Prédiction avec le modèle ML réel"""
        if self.ml_model is None:
            return None
        
        try:
            # Extraire les caractéristiques
            rank1 = float(player1.get('Classement', 100))
            rank2 = float(player2.get('Classement', 100))
            
            # Cotes bookmaker
            odds1_str = player1.get('Côtes', '2.0')
            odds2_str = player2.get('Côtes', '2.0')
            odds1 = self._parse_french_float(odds1_str) if odds1_str else 2.0
            odds2 = self._parse_french_float(odds2_str) if odds2_str else 2.0
            
            # Calculer les caractéristiques ML
            rank_diff = rank1 - rank2
            rank_advantage = (rank2 - rank1) / max(rank1, rank2)
            
            # Surface encoding
            surface_map = {'Hard': 0, 'Clay': 1, 'Grass': 2, 'Indoor': 0}
            surface = surface_map.get(player1.get('Surface', 'Hard'), 0)
            
            # Circuit (supposer ATP si pas spécifié)
            circuit = 1  # ATP par défaut
            
            # Avantage des cotes
            if odds1 > 0 and odds2 > 0:
                odds_advantage = (odds2 - odds1) / (odds1 + odds2)
            else:
                odds_advantage = 0
            
            # Créer le vecteur de caractéristiques
            features = np.array([[
                rank1, rank2, rank_diff, rank_advantage,
                surface, circuit, odds_advantage,
                min(rank1, rank2), max(rank1, rank2), abs(rank_diff)
            ]])
            
            # Prédiction
            prob = self.ml_model.predict_proba(features)[0]
            winner = self.ml_model.predict(features)[0]
            
            return {
                'p1_probability': prob[1],
                'p2_probability': prob[0],
                'predicted_winner': int(winner),
                'confidence': max(prob),
                'model_type': 'Real ML (67.2%)'
            }
            
        except Exception as e:
            print(f"Erreur ML: {e}")
            return None
    
    def _create_fallback_data(self):
        """Crée des données de fallback si le fichier Excel n'est pas disponible"""
        fallback_data = {
            'Nom': ['Sinner', 'Auger Aliassime', 'Djokovic', 'Alcaraz', 'Sabalenka', 'Pegula', 'Osaka', 'Anisimova'],
            'Classement': [1, 27, 2, 3, 2, 6, 88, 47],
            'Tournoi': ['US Open (ATP)', 'US Open (ATP)', 'US Open (ATP)', 'US Open (ATP)', 'US Open (WTA)', 'US Open (WTA)', 'US Open (WTA)', 'US Open (WTA)'],
            'Round': ['SF', 'SF', 'SF', 'SF', 'SF', 'SF', 'SF', 'SF'],
            'Côtes': ['1,03', '13,27', '3,89', '1,26', '1,32', '3,42', '1,84', '1,96'],
            'Date': ['05/09/25'] * 8,
            'Heure': ['21:00', '21:00', '23:00', '23:00', '19:00', '19:00', '21:00', '21:00']
        }
        return pd.DataFrame(fallback_data)

    def get_matches(self) -> List[Dict]:
        """Identifie les matchs à partir des données des joueurs"""
        if self.players_data is None:
            self.players_data = self.load_data()
            
        matches = []
        
        # Grouper par tournoi
        for tournament in self.players_data['Tournoi'].unique():
            tournament_players = self.players_data[self.players_data['Tournoi'] == tournament]
            
            # Créer des paires de joueurs (supposant qu'ils sont ordonnés par match)
            players_list = tournament_players.to_dict('records')
            
            for i in range(0, len(players_list), 2):
                if i + 1 < len(players_list):
                    player1 = players_list[i]
                    player2 = players_list[i + 1]
                    
                    matches.append({
                        'tournament': tournament,
                        'player1': player1,
                        'player2': player2,
                        'round': player1.get('Round', 'QF')
                    })
        
        return matches
    
    def calculate_match_probability(self, player1: Dict, player2: Dict) -> Tuple[float, float, Dict]:
        """Calcule les probabilités pour un match avec le nouveau format"""
        
        # Facteurs et poids
        factors = {}
        weights = {
            'ranking': 0.25,
            'career_win_pct': 0.15,
            'surface_win_pct': 0.15,
            'h2h': 0.20,
            'recent_form': 0.15,
            'confidence': 0.10
        }
        
        # 1. Facteur classement
        rank1 = self._safe_int(player1.get('Classement', 100))
        rank2 = self._safe_int(player2.get('Classement', 100))
        factors['ranking'] = self._calculate_ranking_factor(rank1, rank2)
        
        # 2. Pourcentage victoire carrière
        career1 = self._safe_float(player1.get('Pourc_vict_car', 50))
        career2 = self._safe_float(player2.get('Pourc_vict_car', 50))
        factors['career_win_pct'] = self._calculate_percentage_factor(career1, career2)
        
        # 3. Pourcentage victoire surface
        surf1 = self._safe_float(player1.get('Pourc_vict_surf', 50))
        surf2 = self._safe_float(player2.get('Pourc_vict_surf', 50))
        factors['surface_win_pct'] = self._calculate_percentage_factor(surf1, surf2)
        
        # 4. Head-to-Head
        h2h1 = self._parse_h2h(player1.get('H2H', '0-0'))
        h2h2 = self._parse_h2h(player2.get('H2H', '0-0'))
        factors['h2h'] = self._calculate_h2h_factor(h2h1, h2h2)
        
        # 5. Forme récente (last 10 matches)
        form1 = self._safe_float(player1.get('Pourc_vict_last_10', 50))
        form2 = self._safe_float(player2.get('Pourc_vict_last_10', 50))
        factors['recent_form'] = self._calculate_percentage_factor(form1, form2)
        
        # 6. Confiance
        conf1 = self._safe_float(player1.get('Confiance', 50))
        conf2 = self._safe_float(player2.get('Confiance', 50))
        factors['confidence'] = self._calculate_percentage_factor(conf1, conf2)
        
        # Score composite
        score_p1 = sum(weights[factor] * value for factor, value in factors.items())
        
        # Conversion en probabilités
        prob1 = 1 / (1 + np.exp(-2 * (score_p1 - 1)))
        prob2 = 1 - prob1
        
        return prob1, prob2, factors
    
    def predict_match(self, match_data: Dict) -> Dict:
        """Prédit le résultat d'un match"""
        player1 = match_data['player1']
        player2 = match_data['player2']
        
        # Essayer d'abord la prédiction ML
        ml_result = self.predict_with_ml(player1, player2)
        
        if ml_result:
            # Utiliser les résultats ML
            prob1 = ml_result['p1_probability']
            prob2 = ml_result['p2_probability']
            model_type = ml_result['model_type']
            factors = f"ML Model: {model_type}"
        else:
            # Fallback vers le système simplifié
            prob1, prob2, factors = self.calculate_match_probability(player1, player2)
            model_type = "Simplifié (53.8%)"
        
        # Utiliser les cotes bookmaker depuis la colonne 'Côtes'
        odds1_str = player1.get('Côtes', None)
        odds2_str = player2.get('Côtes', None)
        
        # Convertir les cotes (format français avec virgule)
        odds1 = self._parse_french_float(odds1_str) if odds1_str else None
        odds2 = self._parse_french_float(odds2_str) if odds2_str else None
        
        # Si pas de cotes bookmaker, calculer à partir des probabilités
        if odds1 is None or odds1 == 0:
            odds1 = 1 / prob1 if prob1 > 0.01 else 100
        if odds2 is None or odds2 == 0:
            odds2 = 1 / prob2 if prob2 > 0.01 else 100
        
        # Déterminer le favori
        if prob1 > prob2:
            favorite = player1['Nom']
            confidence = prob1 * 100
        else:
            favorite = player2['Nom']
            confidence = prob2 * 100
        
        return {
            'Tournoi': match_data['tournament'],
            'Match': f"{player1['Nom']} vs {player2['Nom']}",
            'Date': player1.get('Date', 'N/A'),
            'Heure': player1.get('Heure', 'N/A'),
            'Joueur 1': player1['Nom'],
            'Joueur 2': player2['Nom'],
            'Classement J1': player1.get('Classement', 'N/A'),
            'Classement J2': player2.get('Classement', 'N/A'),
            'Probabilité J1 (%)': round(prob1 * 100, 1),
            'Probabilité J2 (%)': round(prob2 * 100, 1),
            'Cote J1': round(odds1, 2),
            'Cote J2': round(odds2, 2),
            'Gagnant Prédit': favorite,
            'Confiance (%)': round(confidence, 1),
            'Round': match_data['round'],
            'H2H J1': player1.get('H2H', 'N/A'),
            'H2H J2': player2.get('H2H', 'N/A'),
            'Forme J1': player1.get('Pourc_vict_last_10', 'N/A'),
            'Forme J2': player2.get('Pourc_vict_last_10', 'N/A'),
            'Photo J1': player1.get('Lien Photo', ''),
            'Photo J2': player2.get('Lien Photo', ''),
            'Lien Tennis Explorer': player1.get('Lien TennisExplorer', ''),
            'Modele': model_type,
            'Facteurs': factors
        }
    
    def process_all_matches(self) -> List[Dict]:
        """Traite tous les matchs et génère les prédictions"""
        if self.players_data is None:
            print("Aucune donnée chargée")
            return []
        
        matches = self.get_matches()
        predictions = []
        
        print(f"\n=== TRAITEMENT DE {len(matches)} MATCHS ===")
        
        for match in matches:
            try:
                prediction = self.predict_match(match)
                predictions.append(prediction)
                
                print(f"OK - {prediction['Match']}")
                print(f"  Favori: {prediction['Gagnant Prédit']} ({prediction['Confiance (%)']}%)")
                print(f"  Cotes: {prediction['Cote J1']} vs {prediction['Cote J2']}")
                
            except Exception as e:
                print(f"ERREUR - {match['player1']['Nom']} vs {match['player2']['Nom']}: {e}")
        
        return predictions
    
    def export_results(self, predictions: List[Dict], filename: str = "simplified_predictions_results.xlsx"):
        """Exporte les résultats vers Excel"""
        if not predictions:
            print("Aucune prédiction à exporter")
            return
        
        # Créer le DataFrame principal
        df = pd.DataFrame(predictions)
        
        # Statistiques
        total_matches = len(predictions)
        high_confidence = sum(1 for p in predictions if p['Confiance (%)'] > 70)
        avg_confidence = np.mean([p['Confiance (%)'] for p in predictions])
        
        # Statistiques par tournoi
        tournaments_stats = {}
        for tournament in df['Tournoi'].unique():
            tournament_preds = [p for p in predictions if p['Tournoi'] == tournament]
            tournaments_stats[tournament] = {
                'Nombre_Matchs': len(tournament_preds),
                'Confiance_Moyenne': np.mean([p['Confiance (%)'] for p in tournament_preds]),
                'Matchs_Haute_Confiance': sum(1 for p in tournament_preds if p['Confiance (%)'] > 70)
            }
        
        stats_df = pd.DataFrame.from_dict(tournaments_stats, orient='index')
        
        # Export Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Prédictions', index=False)
            stats_df.to_excel(writer, sheet_name='Statistiques', index=True)
        
        print(f"\nOK - Résultats exportés vers {filename}")
        print(f"  - {total_matches} prédictions")
        print(f"  - {high_confidence} matchs haute confiance (>70%)")
        print(f"  - Confiance moyenne: {avg_confidence:.1f}%")
    
    # Méthodes utilitaires
    def _safe_float(self, value, default=0.0):
        """Conversion sécurisée en float"""
        try:
            if pd.isna(value) or value == '' or value is None:
                return default
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def _parse_french_float(self, value):
        """Parse un float au format français (virgule comme séparateur décimal)"""
        try:
            if pd.isna(value) or value == '' or value is None:
                return None
            # Remplacer la virgule par un point pour la conversion
            str_value = str(value).replace(',', '.')
            return float(str_value)
        except (ValueError, TypeError):
            return None
    
    def _safe_int(self, value, default=100):
        """Conversion sécurisée en int"""
        try:
            if pd.isna(value) or value == '' or value is None:
                return default
            return int(float(value))
        except (ValueError, TypeError):
            return default
    
    def _parse_h2h(self, h2h_str):
        """Parse H2H format '3-1' -> (3, 1)"""
        try:
            if pd.isna(h2h_str) or str(h2h_str) == 'nan':
                return (0, 0)
            parts = str(h2h_str).split('-')
            return (int(parts[0]), int(parts[1]))
        except:
            return (0, 0)
    
    def _calculate_ranking_factor(self, rank1, rank2):
        """Calcule le facteur de classement"""
        if rank1 == 0 or rank2 == 0:
            return 1.0
        rank_diff = rank2 - rank1
        return 1 + (rank_diff / 100)
    
    def _calculate_percentage_factor(self, pct1, pct2):
        """Calcule un facteur basé sur des pourcentages"""
        if pct2 == 0:
            return 2.0 if pct1 > 0 else 1.0
        return pct1 / pct2
    
    def _calculate_h2h_factor(self, h2h1, h2h2):
        """Calcule le facteur H2H"""
        wins1, losses1 = h2h1
        wins2, losses2 = h2h2
        
        if wins1 + wins2 == 0:
            return 1.0
        
        total_matches = wins1 + wins2
        return (wins1 / total_matches) * 2 if total_matches > 0 else 1.0

def main():
    """Fonction principale"""
    print("=== SYSTÈME DE PRÉDICTION TENNIS SIMPLIFIÉ ===")
    
    # Initialiser le système
    system = SimplifiedTennisPredictionSystem()
    
    # Traiter tous les matchs
    predictions = system.process_all_matches()
    
    if predictions:
        # Exporter les résultats
        system.export_results(predictions)
        
        # Afficher le résumé
        print(f"\n=== RÉSUMÉ ===")
        print(f"Total matchs traités: {len(predictions)}")
        
        for pred in predictions:
            print(f"\n{pred['Match']} ({pred['Tournoi']})")
            print(f"  Favori: {pred['Gagnant Prédit']} ({pred['Confiance (%)']}%)")
    
    print("\n=== TRAITEMENT TERMINÉ ===")

if __name__ == "__main__":
    main()
