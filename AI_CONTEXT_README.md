# 🤖 Système d'Analyse Contextuelle IA

## Vue d'ensemble

Le système d'analyse contextuelle IA enrichit les prédictions tennis en analysant l'état psychologique des joueurs via des informations contextuelles récentes (blessures, changements d'entraîneur, vie privée, forme récente, etc.).

## Fonctionnalités

### 1. **Recherche d'Informations**
- Recherche automatique d'actualités récentes sur les joueurs
- Sources: Google News, bases de données locales
- Mots-clés: blessure, forme, entraîneur, victoire, défaite, etc.

### 2. **Analyse IA (GPT-4)**
- Analyse psychologique des joueurs basée sur les actualités
- Évaluation de 4 dimensions:
  - **État physique** (blessures, fatigue, forme)
  - **État mental** (confiance, motivation, pression)
  - **Contexte personnel** (changement d'entraîneur, vie privée)
  - **Momentum** (résultats récents, série)

### 3. **Ajustement des Prédictions**
- Calcul d'un ajustement de probabilité (-15% à +15%)
- Application automatique dans le système de prédiction
- Affichage des insights dans le dashboard

## Configuration

### Option 1: Avec API (Recommandé)

1. **Créer un fichier `.env`** à la racine du projet:
```bash
cp .env.example .env
```

2. **Configurer les clés API**:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
SERPER_API_KEY=xxxxxxxxxxxxx
```

3. **Obtenir les clés**:
   - **OpenAI**: https://platform.openai.com/api-keys
   - **Serper** (recherche Google): https://serper.dev/

### Option 2: Mode Fallback (Sans API)

Le système fonctionne automatiquement en mode fallback si les clés API ne sont pas configurées:
- Utilise une base de données locale de contextes
- Analyse heuristique basée sur des mots-clés
- Ajustements limités mais fonctionnels

## Utilisation

### Dans le Code

```python
from ultimate_prediction_system import UltimateTennisPredictionSystem

# Avec analyse IA activée (par défaut)
system = UltimateTennisPredictionSystem(enable_ai_context=True)

# Sans analyse IA
system = UltimateTennisPredictionSystem(enable_ai_context=False)

# Traiter les matchs
predictions = system.process_all_matches()
```

### Test du Module IA

```bash
python ai_context_analyzer.py
```

## Structure des Données

### Contexte IA Retourné

```json
{
  "player1_context": {
    "physical_state": {"score": 5, "description": "En bonne forme"},
    "mental_state": {"score": 8, "description": "Très confiant"},
    "personal_context": {"score": 0, "description": "Stable"},
    "momentum": {"score": 7, "description": "Série de victoires"},
    "overall_adjustment": 0.08,
    "key_factors": ["Série de victoires", "Confiance élevée"],
    "summary": "Joueur en excellente forme psychologique"
  },
  "player2_context": { ... },
  "net_adjustment": 0.05,
  "advantage": "Joueur 1",
  "confidence_boost": 5.0
}
```

### Affichage Dashboard

Les insights IA sont affichés dans chaque carte de match:
- 📈 **Avantage positif** (vert) - Joueur 1 favorisé
- 📉 **Avantage négatif** (rouge) - Joueur 2 favorisé
- ➡️ **Neutre** (gris) - Pas d'avantage significatif

## Exemples de Facteurs Analysés

### Facteurs Positifs
- ✅ Série de victoires récentes
- ✅ Retour en forme après blessure
- ✅ Nouveau partenariat avec entraîneur réputé
- ✅ Confiance élevée (déclarations)
- ✅ Bon historique sur la surface

### Facteurs Négatifs
- ❌ Blessure récente ou retour de blessure
- ❌ Série de défaites
- ❌ Changement d'entraîneur récent
- ❌ Problèmes personnels médiatisés
- ❌ Fatigue (calendrier chargé)

### Facteurs Neutres
- ⚪ Préparation standard
- ⚪ Pas d'actualités récentes
- ⚪ Informations limitées

## Limites et Considérations

### Limites du Système
1. **Dépendance aux actualités**: Qualité variable selon la médiatisation
2. **Langue**: Optimisé pour le français et l'anglais
3. **Coût API**: Utilisation de GPT-4 (environ $0.01 par analyse)
4. **Cache**: 1 heure de cache pour éviter les appels répétés

### Bonnes Pratiques
- ✅ Utiliser le mode fallback pour les tests
- ✅ Configurer les API pour la production
- ✅ Vérifier les logs pour détecter les erreurs
- ✅ Mettre à jour la base locale régulièrement

## Coûts Estimés

### Avec API OpenAI
- **GPT-4o-mini**: ~$0.15 / 1M tokens input, ~$0.60 / 1M tokens output
- **Coût par match**: ~$0.005 - $0.01
- **100 matchs/jour**: ~$0.50 - $1.00/jour

### Avec Mode Fallback
- **Gratuit** - Aucun coût API
- Précision réduite mais fonctionnel

## Dépendances

```bash
pip install requests python-dotenv
```

## Support

Pour toute question ou problème:
1. Vérifier les logs du serveur Flask
2. Tester le module isolément: `python ai_context_analyzer.py`
3. Vérifier la configuration `.env`
4. Consulter la documentation OpenAI/Serper

## Roadmap

### Améliorations Futures
- [ ] Support de plus de sources d'actualités
- [ ] Analyse de sentiment avancée
- [ ] Historique des analyses
- [ ] Dashboard d'administration IA
- [ ] Modèles ML personnalisés pour l'analyse contextuelle
- [ ] Intégration réseaux sociaux (Twitter/X)
