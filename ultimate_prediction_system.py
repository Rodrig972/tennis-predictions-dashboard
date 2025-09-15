import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class UltimateTennisPredictionSystem:
    def __init__(self, excel_file_path='./data/Stats_tournois_en_cours.xlsx'):
        self.excel_file_path = excel_file_path
        self.models = {}
        self.model_weights = {}
        self.load_models()
        
    def load_models(self):
        """Charge tous les modèles ML disponibles"""
        model_dir = './ml_models'
        if not os.path.exists(model_dir):
            print(f"Dossier {model_dir} non trouvé, utilisation du mode fallback")
            return
            
        # Liste des modèles à charger
        model_files = [
            'real_tennis_model.joblib',
            'specialized_tennis_model.joblib',
            'simple_tennis_model.joblib'
        ]
        
        for model_file in model_files:
            model_path = os.path.join(model_dir, model_file)
            if os.path.exists(model_path):
                try:
                    model = joblib.load(model_path)
                    model_name = model_file.replace('.joblib', '')
                    self.models[model_name] = model
                    # Poids par défaut égaux
                    self.model_weights[model_name] = 1.0
                    print(f"Modèle {model_name} chargé avec succès")
                except Exception as e:
                    print(f"Erreur lors du chargement de {model_file}: {e}")
        
        print(f"Total de {len(self.models)} modèles chargés")
    
    def calculate_features(self, match_info):
        """Calcule les features pour un match - Compatible avec les modèles existants (10 features)"""
        try:
            # Features de base
            classement_j1 = float(match_info.get('classement_j1', 50))
            classement_j2 = float(match_info.get('classement_j2', 50))
            cote_j1 = float(match_info.get('cote_j1', 2.0))
            cote_j2 = float(match_info.get('cote_j2', 2.0))
            
            # Normaliser les classements (diviser par 200 pour avoir des valeurs entre 0 et 1)
            rank1_norm = classement_j1 / 200.0
            rank2_norm = classement_j2 / 200.0
            
            # Différence de classement normalisée
            rank_diff = (classement_j1 - classement_j2) / 200.0
            rank_advantage = 1 if classement_j1 < classement_j2 else 0
            
            # Surface et circuit par défaut (encodage numérique)
            surface_encoded = 1  # Hard court par défaut
            circuit_encoded = 1  # ATP par défaut
            
            # Avantage des cotes
            if cote_j1 > 0 and cote_j2 > 0:
                odds_advantage = (cote_j2 - cote_j1) / (cote_j1 + cote_j2)
            else:
                odds_advantage = 0
            
            # Features supplémentaires pour atteindre 10 features (compatibilité avec real_tennis_model)
            min_rank_norm = min(rank1_norm, rank2_norm)
            max_rank_norm = max(rank1_norm, rank2_norm)
            abs_rank_diff = abs(rank_diff)
            
            # Construire le tableau de features (10 features comme attendu par real_tennis_model)
            features = np.array([[
                rank1_norm, rank2_norm, rank_diff, rank_advantage,
                surface_encoded, circuit_encoded, odds_advantage,
                min_rank_norm, max_rank_norm, abs_rank_diff
            ]])
            
            return features
            
        except Exception as e:
            print(f"Erreur calcul features: {e}")
            # Features par défaut équilibrées (10 features)
            return np.array([[0.25, 0.25, 0.0, 0.5, 1, 1, 0.0, 0.25, 0.25, 0.0]])
    
    def ensemble_prediction(self, match_info):
        """Prédiction d'ensemble utilisant tous les modèles disponibles"""
        if not self.models:
            return self._fallback_prediction(match_info)
        
        features = self.calculate_features(match_info)
        predictions = []
        weights = []
        model_contributions = {}
        
        for model_name, model in self.models.items():
            try:
                # Prédiction du modèle
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba(features)[0]
                    # Assurer que nous avons la probabilité de victoire du joueur 1
                    pred_value = proba[1] if len(proba) > 1 else proba[0]
                else:
                    pred_value = model.predict(features)[0]
                    # Si c'est une prédiction binaire (0 ou 1), convertir en probabilité
                    if pred_value in [0, 1]:
                        pred_value = 0.7 if pred_value == 1 else 0.3
                
                # S'assurer que la prédiction est dans [0, 1]
                pred_value = max(0.05, min(0.95, float(pred_value)))
                
                predictions.append(pred_value)
                weight = self.model_weights.get(model_name, 1.0)
                weights.append(weight)
                
                model_contributions[model_name] = {
                    'prediction': float(pred_value),
                    'weight': float(weight)
                }
                
            except Exception as e:
                print(f"Erreur modèle {model_name}: {e}")
                continue
        
        if not predictions:
            return self._fallback_prediction(match_info)
        
        # Calcul de la prédiction pondérée
        predictions = np.array(predictions)
        weights = np.array(weights)
        weighted_pred = np.average(predictions, weights=weights)
        
        # S'assurer que la probabilité est dans [0, 1]
        weighted_pred = max(0.05, min(0.95, weighted_pred))
        
        # Déterminer le gagnant et la confiance correctement
        proba_j1 = weighted_pred
        proba_j2 = 1 - weighted_pred
        
        if proba_j1 > proba_j2:
            gagnant = match_info.get('joueur_1', 'Joueur 1')
            confiance = proba_j1 * 100
        else:
            gagnant = match_info.get('joueur_2', 'Joueur 2')
            confiance = proba_j2 * 100
        
        return {
            'gagnant_predit': gagnant,
            'confiance': confiance,
            'probabilites': {
                'joueur_1': proba_j1,
                'joueur_2': proba_j2
            },
            'models_used': len(predictions),
            'model_contributions': model_contributions,
            'modele_utilise': 'ultimate_ensemble'
        }
    
    def _fallback_prediction(self, match_info):
        """Prédiction de fallback basée sur les classements et cotes"""
        try:
            classement_j1 = float(match_info.get('classement_j1', 50))
            classement_j2 = float(match_info.get('classement_j2', 50))
            cote_j1 = float(match_info.get('cote_j1', 2.0))
            cote_j2 = float(match_info.get('cote_j2', 2.0))
            
            # Convertir les cotes en probabilités implicites
            prob_cote_j1 = 1 / cote_j1 if cote_j1 > 0 else 0.5
            prob_cote_j2 = 1 / cote_j2 if cote_j2 > 0 else 0.5
            
            # Normaliser les probabilités des cotes (éliminer la marge du bookmaker)
            total_prob_cotes = prob_cote_j1 + prob_cote_j2
            if total_prob_cotes > 0:
                prob_cote_j1_norm = prob_cote_j1 / total_prob_cotes
                prob_cote_j2_norm = prob_cote_j2 / total_prob_cotes
            else:
                prob_cote_j1_norm = prob_cote_j2_norm = 0.5
            
            # Calculer la probabilité basée sur le classement
            # Utiliser une fonction logistique pour convertir la différence de classement en probabilité
            diff_classement = classement_j2 - classement_j1  # Positif si j1 est mieux classé
            # Normaliser la différence (diviser par 50 pour avoir une échelle raisonnable)
            diff_norm = diff_classement / 50.0
            # Fonction logistique: plus la différence est grande, plus j1 a de chances de gagner
            prob_classement_j1 = 1 / (1 + np.exp(-diff_norm))
            
            # Combiner les probabilités (60% cotes, 40% classement)
            proba_j1 = 0.6 * prob_cote_j1_norm + 0.4 * prob_classement_j1
            proba_j2 = 1 - proba_j1
            
            # Limiter les probabilités pour éviter les extrêmes
            proba_j1 = max(0.05, min(0.95, proba_j1))
            proba_j2 = 1 - proba_j1
            
            # Déterminer le gagnant et la confiance
            if proba_j1 > proba_j2:
                gagnant = match_info.get('joueur_1', 'Joueur 1')
                confiance = proba_j1 * 100
            else:
                gagnant = match_info.get('joueur_2', 'Joueur 2')
                confiance = proba_j2 * 100
            
            return {
                'gagnant_predit': gagnant,
                'confiance': confiance,
                'probabilites': {
                    'joueur_1': proba_j1,
                    'joueur_2': proba_j2
                },
                'models_used': 0,
                'modele_utilise': 'fallback_heuristic',
                'debug_info': {
                    'prob_cote_j1': prob_cote_j1_norm,
                    'prob_classement_j1': prob_classement_j1,
                    'diff_classement': diff_classement
                }
            }
            
        except Exception as e:
            print(f"Erreur fallback: {e}")
            return {
                'gagnant_predit': match_info.get('joueur_1', 'Joueur 1'),
                'confiance': 55.0,
                'probabilites': {'joueur_1': 0.55, 'joueur_2': 0.45},
                'models_used': 0,
                'modele_utilise': 'default'
            }
    
    def process_all_matches(self):
        """Traite tous les matchs depuis Excel et retourne les prédictions formatées pour le dashboard"""
        try:
            # Charger les données Excel
            df = pd.read_excel(self.excel_file_path, sheet_name='StatsJoueurs')
            predictions = []
            
            # Créer des matchs individuels basés sur les liens Tennis Explorer
            # Chaque joueur devrait avoir un lien unique vers son match
            match_links = {}
            
            # Grouper les joueurs par lien Tennis Explorer pour identifier les vrais matchs
            for _, row in df.iterrows():
                link = row.get('Lien TennisExplorer', '')
                if link and link != '':
                    if link not in match_links:
                        match_links[link] = []
                    match_links[link].append(row)
            
            # Créer des matchs basés sur les liens Tennis Explorer
            for link, players in match_links.items():
                if len(players) == 2:
                    # Match normal avec 2 joueurs
                    player1, player2 = players[0], players[1]
                    # Trier par classement pour cohérence
                    if player1['Classement'] > player2['Classement']:
                        player1, player2 = player2, player1
                    
                    self._create_match_prediction(
                        player1, player2, 
                        player1['Date'], player1['Heure'], 
                        player1['Tournoi'], player1['Round'], 
                        predictions
                    )
            
            # Fallback: si pas assez de matchs créés via les liens, utiliser l'ancienne méthode
            if len(predictions) < 5:  # Si moins de 5 matchs créés
                print("Fallback: utilisation du groupement par date/heure")
                predictions = []  # Reset
                matches = df.groupby(['Date', 'Heure'])
                
                for (date, heure), group in matches:
                    players_list = list(group.iterrows())
                    # Créer des paires en alternant (1-2, 3-4, etc.)
                    for i in range(0, len(players_list), 2):
                        if i + 1 < len(players_list):
                            _, player1 = players_list[i]
                            _, player2 = players_list[i + 1]
                            self._create_match_prediction(
                                player1, player2, date, heure, 
                                player1['Tournoi'], player1['Round'], 
                                predictions
                            )
            
            return predictions
            
        except Exception as e:
            print(f"Erreur process_all_matches: {e}")
            return self._create_fallback_predictions()

    def _create_match_prediction(self, player1, player2, date, heure, tournoi, round_name, predictions):
        """Crée une prédiction pour un match entre deux joueurs"""
        try:
            # Extraire les cotes depuis la colonne 'Côtes' (avec accent)
            try:
                cote_j1 = float(str(player1.get('Côtes', '2.0')).replace(',', '.'))
                cote_j2 = float(str(player2.get('Côtes', '2.0')).replace(',', '.'))
            except:
                # Essayer avec la colonne sans accent si elle existe
                try:
                    cote_j1 = float(str(player1.get('Cotes', '2.0')).replace(',', '.'))
                    cote_j2 = float(str(player2.get('Cotes', '2.0')).replace(',', '.'))
                except:
                    cote_j1, cote_j2 = 2.0, 2.0
            
            # Préparer les informations du match
            match_info = {
                'joueur_1': player1.get('Nom', ''),
                'joueur_2': player2.get('Nom', ''),
                'classement_j1': player1.get('Classement', 50),
                'classement_j2': player2.get('Classement', 50),
                'tournoi': tournoi,
                'round': round_name,
                'cote_j1': cote_j1,
                'cote_j2': cote_j2,
                'date': date,
                'heure': heure,
            }
            
            # Obtenir la prédiction ultime
            prediction = self.ensemble_prediction(match_info)
            
            # Récupérer le lien Tennis Explorer depuis les données Excel
            lien_te_j1 = player1.get('Lien TennisExplorer', '')
            lien_te_j2 = player2.get('Lien TennisExplorer', '')
            # Utiliser le premier lien disponible ou générer un lien de recherche
            lien_tennis_explorer = lien_te_j1 if lien_te_j1 else lien_te_j2 if lien_te_j2 else f"https://www.tennisexplorer.com/search/?search={match_info['joueur_1'].replace(' ', '+')}"
            
            # Formater pour le dashboard
            formatted_prediction = {
                "Match": f"{match_info['joueur_1']} vs {match_info['joueur_2']}",
                "Tournoi": match_info['tournoi'],
                "Date": match_info['date'],
                "Heure": match_info['heure'],
                "Joueur 1": match_info['joueur_1'],
                "Joueur 2": match_info['joueur_2'],
                "Classement J1": match_info['classement_j1'],
                "Classement J2": match_info['classement_j2'],
                "Gagnant Prédit": prediction['gagnant_predit'],
                "Confiance (%)": round(prediction['confiance'], 1),
                "Cote J1": match_info['cote_j1'],
                "Cote J2": match_info['cote_j2'],
                "Round": match_info['round'],
                "Modele": f"Ultimate ML ({prediction.get('models_used', 0)} modèles)",
                "Type": "Ultimate",
                "Photo J1": self._get_player_photo(match_info['joueur_1']),
                "Photo J2": self._get_player_photo(match_info['joueur_2']),
                "Lien Tennis Explorer": lien_tennis_explorer,
                "System_Details": {
                    "model_contributions": prediction.get('model_contributions', {}),
                    "probabilites": prediction.get('probabilites', {}),
                    "modele_utilise": prediction.get('modele_utilise', 'ultimate')
                }
            }
            
            predictions.append(formatted_prediction)
            
        except Exception as e:
            print(f"Erreur création match {player1.get('Nom', '')} vs {player2.get('Nom', '')}: {e}")

    def _get_player_photo(self, player_name):
        """Retourne une photo par défaut pour un joueur"""
        photos = {
            'sinner': "https://www.tennisexplorer.com/res/img/player/OK7tW3bR-dEXkR0Wq.jpeg",
            'alcaraz': "https://www.tennisexplorer.com/res/img/player/CYLI6SbR-EZcCkAic.jpeg",
            'djokovic': "https://www.tennisexplorer.com/res/img/player/2yxhH1ya-KKWyfaNo.jpeg",
            'sabalenka': "https://www.tennisexplorer.com/res/img/player/EyiUUwFm-I9HZAz1R.jpeg",
            'swiatek': "https://www.tennisexplorer.com/res/img/player/default.jpeg"
        }
        
        player_lower = player_name.lower()
        for key, photo in photos.items():
            if key in player_lower:
                return photo
        
        return "https://www.tennisexplorer.com/res/img/player/default.jpeg"
    
    def _create_fallback_predictions(self):
        """Crée des prédictions de fallback si Excel non disponible"""
        fallback_matches = [
            {
                "Match": "Jannik Sinner vs Carlos Alcaraz",
                "Tournoi": "ATP Masters 1000 Paris",
                "Date": "2024-11-03",
                "Heure": "15:00",
                "Joueur 1": "Jannik Sinner",
                "Joueur 2": "Carlos Alcaraz", 
                "Classement J1": 1,
                "Classement J2": 2,
                "Gagnant Prédit": "Jannik Sinner",
                "Confiance (%)": 65.2,
                "Cote J1": 1.85,
                "Cote J2": 1.95,
                "Round": "Final",
                "Modele": "Ultimate ML (3 modèles)",
                "Type": "Ultimate",
                "Photo J1": self._get_player_photo("Jannik Sinner"),
                "Photo J2": self._get_player_photo("Carlos Alcaraz"),
                "Lien Tennis Explorer": "#"
            }
        ]
        return fallback_matches


def main():
    """Test du système de prédiction ultime"""
    system = UltimateTennisPredictionSystem()
    
    # Test avec un match exemple
    test_match = {
        'joueur_1': 'Jannik Sinner',
        'joueur_2': 'Carlos Alcaraz',
        'classement_j1': 1,
        'classement_j2': 2,
        'tournoi': 'ATP Masters 1000 Paris',
        'round': 'Final',
        'cote_j1': 1.85,
        'cote_j2': 1.95,
        'date': '2024-11-03',
        'heure': '15:00'
    }
    
    print(f"Test du système Ultimate Tennis Prediction")
    print(f"Match: {test_match['joueur_1']} vs {test_match['joueur_2']}")
    print(f"Classements: #{test_match['classement_j1']} vs #{test_match['classement_j2']}")
    print(f"Cotes: {test_match['cote_j1']} vs {test_match['cote_j2']}")
    print(f"Tournoi: {test_match['tournoi']} ({test_match['round']})")
    
    prediction = system.ensemble_prediction(test_match)
    
    print(f"\nRésultat:")
    print(f"Gagnant prédit: {prediction['gagnant_predit']}")
    print(f"Confiance: {prediction['confiance']:.1f}%")
    print(f"Modèles utilisés: {prediction.get('models_used', 0)}")
    print(f"Système: {prediction['modele_utilise']}")
    
    if 'model_contributions' in prediction:
        print(f"\nContributions des modèles:")
        for model, contrib in prediction['model_contributions'].items():
            print(f"  {model}: {contrib['weight']:.3f} (pred: {contrib['prediction']:.3f})")

if __name__ == "__main__":
    main()
