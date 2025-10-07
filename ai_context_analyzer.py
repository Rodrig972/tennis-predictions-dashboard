"""
Module d'analyse contextuelle IA pour enrichir les prédictions tennis
Analyse l'état psychologique des joueurs via recherche web et IA
"""

import os
import json
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Optional
import time

class AIContextAnalyzer:
    """Analyse le contexte des joueurs via IA pour affiner les prédictions"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 3600  # Cache de 1 heure
        
        # Configuration API (utiliser des variables d'environnement)
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.serper_api_key = os.getenv('SERPER_API_KEY', '')  # Pour recherche Google
        
    def analyze_player_context(self, player_name: str, tournament: str = "") -> Dict:
        """
        Analyse le contexte d'un joueur via IA
        
        Args:
            player_name: Nom du joueur
            tournament: Nom du tournoi (optionnel)
            
        Returns:
            Dict avec insights psychologiques et ajustement de probabilité
        """
        # Vérifier le cache
        cache_key = f"{player_name}_{tournament}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data
        
        # Rechercher des informations récentes
        recent_news = self._search_player_news(player_name, tournament)
        
        # Analyser avec IA
        analysis = self._ai_analyze_context(player_name, recent_news, tournament)
        
        # Mettre en cache
        self.cache[cache_key] = (analysis, time.time())
        
        return analysis
    
    def _search_player_news(self, player_name: str, tournament: str = "") -> List[Dict]:
        """Recherche des actualités récentes sur le joueur"""
        
        if not self.serper_api_key:
            # Mode fallback sans API
            return self._fallback_news_search(player_name, tournament)
        
        try:
            # Construire la requête de recherche
            query = f"{player_name} tennis"
            if tournament:
                query += f" {tournament}"
            query += " news blessure entraineur forme"
            
            # Recherche via Serper API (alternative à Google Search API)
            url = "https://google.serper.dev/search"
            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
            }
            payload = {
                'q': query,
                'num': 5,
                'gl': 'fr',
                'hl': 'fr'
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                news = []
                
                # Extraire les résultats
                for item in data.get('organic', [])[:5]:
                    news.append({
                        'title': item.get('title', ''),
                        'snippet': item.get('snippet', ''),
                        'link': item.get('link', ''),
                        'date': item.get('date', '')
                    })
                
                return news
            else:
                return self._fallback_news_search(player_name, tournament)
                
        except Exception as e:
            print(f"Erreur recherche news pour {player_name}: {e}")
            return self._fallback_news_search(player_name, tournament)
    
    def _fallback_news_search(self, player_name: str, tournament: str = "") -> List[Dict]:
        """Recherche fallback sans API (simulation)"""
        # Base de données locale de contextes courants (à mettre à jour manuellement)
        player_contexts = {
            'sinner': {
                'forme': 'excellente',
                'contexte': 'En grande forme, vainqueur récent de plusieurs tournois',
                'mental': 'confiant',
                'facteurs': ['Série de victoires', 'Confiance élevée']
            },
            'alcaraz': {
                'forme': 'bonne',
                'contexte': 'Retour de blessure récente au bras',
                'mental': 'déterminé',
                'facteurs': ['Retour de blessure', 'Motivation élevée']
            },
            'djokovic': {
                'forme': 'stable',
                'contexte': 'Expérience et régularité',
                'mental': 'solide',
                'facteurs': ['Expérience', 'Mental d\'acier']
            },
            'sabalenka': {
                'forme': 'excellente',
                'contexte': 'Dominante sur dur',
                'mental': 'agressif',
                'facteurs': ['Puissance', 'Confiance']
            }
        }
        
        # Chercher le joueur dans la base
        player_lower = player_name.lower()
        for key, context in player_contexts.items():
            if key in player_lower:
                return [{
                    'title': f'{player_name} - Contexte actuel',
                    'snippet': context['contexte'],
                    'source': 'local_database',
                    'factors': context['facteurs']
                }]
        
        # Contexte par défaut
        return [{
            'title': f'{player_name} - Informations limitées',
            'snippet': 'Aucune information contextuelle récente disponible',
            'source': 'default',
            'factors': []
        }]
    
    def _ai_analyze_context(self, player_name: str, news: List[Dict], tournament: str = "") -> Dict:
        """Analyse les news avec IA pour extraire des insights psychologiques"""
        
        if not self.openai_api_key or not news:
            return self._fallback_analysis(player_name, news)
        
        try:
            # Préparer le contexte pour l'IA
            news_text = "\n".join([
                f"- {item.get('title', '')}: {item.get('snippet', '')}"
                for item in news[:5]
            ])
            
            # Prompt pour l'analyse
            prompt = f"""Analyse le contexte psychologique du joueur de tennis {player_name} pour le tournoi {tournament}.

Informations récentes:
{news_text}

Analyse les facteurs suivants et donne un score d'impact (-10 à +10):
1. État physique (blessures, fatigue, forme)
2. État mental (confiance, motivation, pression)
3. Contexte personnel (changement d'entraîneur, vie privée)
4. Momentum récent (résultats, série)

Réponds au format JSON:
{{
    "physical_state": {{"score": X, "description": "..."}},
    "mental_state": {{"score": X, "description": "..."}},
    "personal_context": {{"score": X, "description": "..."}},
    "momentum": {{"score": X, "description": "..."}},
    "overall_adjustment": X.XX,
    "key_factors": ["facteur1", "facteur2"],
    "summary": "Résumé en une phrase"
}}

Le score overall_adjustment doit être entre -0.15 et +0.15 (ajustement de probabilité)."""

            # Appel API OpenAI
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': 'gpt-4o-mini',  # Modèle économique
                'messages': [
                    {'role': 'system', 'content': 'Tu es un expert en analyse psychologique des joueurs de tennis professionnels.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3,
                'max_tokens': 500
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Parser le JSON
                # Nettoyer le contenu (enlever les balises markdown si présentes)
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.startswith('```'):
                    content = content[3:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()
                
                analysis = json.loads(content)
                analysis['source'] = 'openai_gpt4'
                analysis['timestamp'] = datetime.now().isoformat()
                
                return analysis
            else:
                return self._fallback_analysis(player_name, news)
                
        except Exception as e:
            print(f"Erreur analyse IA pour {player_name}: {e}")
            return self._fallback_analysis(player_name, news)
    
    def _fallback_analysis(self, player_name: str, news: List[Dict]) -> Dict:
        """Analyse fallback basée sur des heuristiques"""
        
        # Analyser les mots-clés dans les news
        keywords_positive = ['victoire', 'forme', 'confiance', 'excellent', 'dominateur', 'série']
        keywords_negative = ['blessure', 'défaite', 'fatigue', 'doute', 'abandon', 'problème']
        keywords_neutral = ['entraîneur', 'changement', 'préparation']
        
        positive_count = 0
        negative_count = 0
        key_factors = []
        
        for item in news:
            text = (item.get('snippet', '') + ' ' + item.get('title', '')).lower()
            
            for keyword in keywords_positive:
                if keyword in text:
                    positive_count += 1
                    if keyword not in [f.lower() for f in key_factors]:
                        key_factors.append(keyword.capitalize())
            
            for keyword in keywords_negative:
                if keyword in text:
                    negative_count += 1
                    if keyword not in [f.lower() for f in key_factors]:
                        key_factors.append(keyword.capitalize())
        
        # Calculer l'ajustement
        net_score = positive_count - negative_count
        adjustment = max(-0.10, min(0.10, net_score * 0.02))
        
        # Déterminer la description
        if adjustment > 0.05:
            summary = f"{player_name} semble en excellente forme psychologique"
        elif adjustment > 0:
            summary = f"{player_name} montre des signes positifs"
        elif adjustment < -0.05:
            summary = f"{player_name} pourrait être affecté négativement"
        elif adjustment < 0:
            summary = f"{player_name} présente quelques préoccupations"
        else:
            summary = f"{player_name} - état psychologique neutre"
        
        return {
            'physical_state': {'score': 0, 'description': 'Information limitée'},
            'mental_state': {'score': int(adjustment * 50), 'description': summary},
            'personal_context': {'score': 0, 'description': 'Information limitée'},
            'momentum': {'score': net_score, 'description': f'{positive_count} facteurs positifs, {negative_count} négatifs'},
            'overall_adjustment': round(adjustment, 3),
            'key_factors': key_factors[:3] if key_factors else ['Aucun facteur identifié'],
            'summary': summary,
            'source': 'heuristic_fallback',
            'timestamp': datetime.now().isoformat()
        }
    
    def compare_players_context(self, player1_name: str, player2_name: str, tournament: str = "") -> Dict:
        """Compare le contexte de deux joueurs et calcule l'ajustement net"""
        
        # Analyser les deux joueurs
        context1 = self.analyze_player_context(player1_name, tournament)
        context2 = self.analyze_player_context(player2_name, tournament)
        
        # Calculer l'ajustement net (positif = avantage joueur 1)
        adj1 = context1.get('overall_adjustment', 0)
        adj2 = context2.get('overall_adjustment', 0)
        net_adjustment = adj1 - adj2
        
        # Limiter l'ajustement total
        net_adjustment = max(-0.15, min(0.15, net_adjustment))
        
        return {
            'player1_context': context1,
            'player2_context': context2,
            'net_adjustment': round(net_adjustment, 3),
            'advantage': player1_name if net_adjustment > 0.02 else player2_name if net_adjustment < -0.02 else 'Neutre',
            'confidence_boost': abs(net_adjustment) * 100,  # Boost de confiance en %
            'analysis_timestamp': datetime.now().isoformat()
        }


def test_analyzer():
    """Test du système d'analyse contextuelle"""
    analyzer = AIContextAnalyzer()
    
    # Test avec deux joueurs
    player1 = "Jannik Sinner"
    player2 = "Carlos Alcaraz"
    tournament = "ATP Finals"
    
    print(f"[ANALYSE] Contexte: {player1} vs {player2}")
    print(f"[TOURNOI] {tournament}\n")
    
    comparison = analyzer.compare_players_context(player1, player2, tournament)
    
    print(f"[RESULTATS]")
    print(f"  Ajustement net: {comparison['net_adjustment']:+.3f}")
    print(f"  Avantage: {comparison['advantage']}")
    print(f"  Boost de confiance: {comparison['confidence_boost']:.1f}%\n")
    
    print(f"[JOUEUR 1] {player1}:")
    p1_ctx = comparison['player1_context']
    print(f"  Resume: {p1_ctx['summary']}")
    print(f"  Facteurs cles: {', '.join(p1_ctx['key_factors'])}")
    print(f"  Ajustement: {p1_ctx['overall_adjustment']:+.3f}\n")
    
    print(f"[JOUEUR 2] {player2}:")
    p2_ctx = comparison['player2_context']
    print(f"  Resume: {p2_ctx['summary']}")
    print(f"  Facteurs cles: {', '.join(p2_ctx['key_factors'])}")
    print(f"  Ajustement: {p2_ctx['overall_adjustment']:+.3f}\n")
    
    print(f"[SOURCE] {p1_ctx.get('source', 'unknown')}")


if __name__ == "__main__":
    test_analyzer()
