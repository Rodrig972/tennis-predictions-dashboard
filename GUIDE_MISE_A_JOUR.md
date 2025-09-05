# 📋 Guide de Mise à Jour des Données Tennis

## 🔄 Ordre d'Exécution des Scripts

### 1️⃣ **Scraper Tennis Explorer** (Collecte des données)
```bash
python scraper_tennis_explorer.py
```
- **Objectif** : Extraction des données depuis Tennis Explorer
- **Sortie** : `data/Result_data_export.xlsx`
- **Durée** : 5-10 minutes
- **Prérequis** : Firefox + geckodriver installés

### 2️⃣ **Transform Stats** (Transformation des données)
```bash
python transform_stats.py
```
- **Objectif** : Nettoyage et transformation des données brutes
- **Entrée** : `data/Result_data_export.xlsx`
- **Sortie** : `data/Stats_tournois_en_cours.xlsx`
- **Durée** : 1-2 minutes

### 3️⃣ **Entraînement ML** (Optionnel - améliorer les modèles)
```bash
python simple_ml_trainer.py
```
- **Objectif** : Entraîner les modèles ML avec nouvelles données
- **Sortie** : `ml_models/simple_tennis_model.joblib`
- **Durée** : 30 secondes

### 4️⃣ **Génération Prédictions** (Calcul des prédictions)
```bash
python simplified_prediction_system.py
```
- **Objectif** : Générer les prédictions avec ML Engine
- **Entrée** : `data/Stats_tournois_en_cours.xlsx`
- **Sortie** : Prédictions en mémoire + fichiers Excel
- **Durée** : 10-20 secondes

### 5️⃣ **Lancement Dashboard** (Interface utilisateur)
```bash
python working_dashboard.py
```
- **Objectif** : Démarrer l'interface web avec données à jour
- **URL** : http://127.0.0.1:5001
- **Durée** : Permanent (serveur web)

## 🚀 Script d'Automatisation Complète

### Option A : Pipeline Automatique
```bash
python automated_data_pipeline.py
```
Exécute automatiquement les étapes 1-4 dans l'ordre.

### Option B : Pipeline Rapide (sans scraping)
```bash
python quick_pipeline.py
```
Exécute seulement les étapes 3-5 (si données déjà à jour).

## 📁 Fichiers de Données Importants

| Fichier | Description | Mise à jour |
|---------|-------------|-------------|
| `data/Result_data_export.xlsx` | Données brutes scrapées | Étape 1 |
| `data/Stats_tournois_en_cours.xlsx` | Données transformées | Étape 2 |
| `ml_models/simple_tennis_model.joblib` | Modèle ML entraîné | Étape 3 |
| `predictions_results.xlsx` | Prédictions exportées | Étape 4 |

## ⚠️ Points d'Attention

### Prérequis Techniques
- **Python 3.8+** avec packages : pandas, scikit-learn, flask, selenium
- **Firefox** + geckodriver pour le scraping
- **Connexion Internet** pour Tennis Explorer

### Gestion d'Erreurs
- Si **Étape 1 échoue** : Vérifier Firefox/geckodriver ou utiliser données existantes
- Si **Étape 2 échoue** : Vérifier format du fichier Excel d'entrée
- Si **Étape 3 échoue** : Modèles ML non critiques, peut être ignoré
- Si **Étape 4 échoue** : Vérifier colonnes dans Stats_tournois_en_cours.xlsx

### Fréquence de Mise à Jour
- **Quotidienne** : Étapes 1-2-4-5 (nouvelles données + prédictions)
- **Hebdomadaire** : Étape 3 (réentraînement ML)
- **En continu** : Étape 5 (dashboard toujours actif)

## 🎯 Commandes Rapides

### Mise à jour complète (recommandée)
```bash
# 1. Collecter nouvelles données
python scraper_tennis_explorer.py

# 2. Transformer les données
python transform_stats.py

# 3. Générer prédictions
python simplified_prediction_system.py

# 4. Lancer dashboard
python working_dashboard.py
```

### Mise à jour rapide (données existantes)
```bash
# 1. Générer prédictions avec données actuelles
python simplified_prediction_system.py

# 2. Lancer dashboard
python working_dashboard.py
```

### Vérification du système
```bash
# Tester l'API
curl http://127.0.0.1:5001/api/health

# Voir les prédictions
curl http://127.0.0.1:5001/api/matches
```
