# 🎾 Tennis Prediction Mobile App

Application mobile React Native pour visualiser et analyser les prédictions de matchs de tennis en temps réel.

## 📱 Fonctionnalités

### 🏠 Dashboard
- **Statistiques globales** : Nombre de tournois, matchs analysés, confiance moyenne
- **Graphiques interactifs** : Répartition par niveau de confiance, top tournois
- **Status de connexion** : Vérification en temps réel de l'API
- **Dernières prédictions** : Aperçu des matchs récents

### 🎯 Prédictions
- **Liste complète** des prédictions avec probabilités et cotes
- **Filtres avancés** : Par niveau de confiance (Haute/Moyenne/Faible)
- **Recherche** : Par nom de joueur ou tournoi
- **Barres de progression** visuelles pour les probabilités
- **Navigation** vers les détails de chaque match

### 🔍 Détails des Matchs
- **Analyse complète** : Probabilités, cotes, favori prédit
- **Graphiques détaillés** : Répartition des probabilités, niveau de confiance
- **Recommandations** basées sur la fiabilité de la prédiction
- **Informations techniques** : Algorithme ML utilisé, données analysées

### ⚙️ Paramètres
- **Configuration API** : URL personnalisable, test de connexion
- **Préférences** : Notifications, actualisation automatique
- **Actions** : Vider le cache, réinitialiser les paramètres
- **Informations** : Version, technologies utilisées

## 🚀 Installation

### Prérequis
- Node.js (v16 ou supérieur)
- npm ou yarn
- Expo CLI
- Votre API Flask tennis en cours d'exécution

### Étapes d'installation

1. **Installer Expo CLI** (si pas déjà fait)
```bash
npm install -g expo-cli
```

2. **Naviguer vers le dossier mobile**
```bash
cd "Aplli mobile"
```

3. **Installer les dépendances**
```bash
npm install
```

4. **Démarrer l'application**
```bash
npm start
# ou
expo start
```

5. **Lancer sur votre appareil**
- **Android** : Scannez le QR code avec l'app Expo Go
- **iOS** : Scannez le QR code avec l'appareil photo
- **Web** : Appuyez sur 'w' dans le terminal

## 🔧 Configuration

### API Backend
1. Assurez-vous que votre API Flask est en cours d'exécution :
```bash
python run_all_scripts.py
```

2. L'API sera accessible sur `http://127.0.0.1:5000`

3. Dans l'app mobile, allez dans **Paramètres** pour configurer l'URL de l'API

### Connexion Réseau
- **Émulateur Android** : Utilisez `http://10.0.2.2:5000`
- **Appareil physique** : Utilisez l'IP de votre ordinateur `http://192.168.x.x:5000`
- **iOS Simulator** : Utilisez `http://127.0.0.1:5000`

## 📊 Intégration avec l'API

L'application se connecte automatiquement à votre API Flask existante :

### Endpoints utilisés
- `GET /api/predictions` - Liste des prédictions
- `GET /api/dashboard` - Statistiques du dashboard  
- `GET /api/match/{tournament}/{match}` - Détails d'un match
- `GET /api/health` - Vérification de la connexion

### Format des données
L'app attend les données au format JSON avec les champs :
```json
{
  "tournament": "US Open ATP",
  "player_a": "Djokovic",
  "player_b": "Nadal", 
  "probability_a": 65.4,
  "probability_b": 34.6,
  "odds_a": 1.53,
  "odds_b": 2.89,
  "confidence": 72.1,
  "favorite": "Djokovic"
}
```

## 🎨 Technologies Utilisées

- **React Native** - Framework mobile cross-platform
- **Expo** - Plateforme de développement
- **React Navigation** - Navigation entre écrans
- **React Native Paper** - Composants Material Design
- **React Native Chart Kit** - Graphiques et visualisations
- **Axios** - Client HTTP pour l'API
- **React Native Animatable** - Animations fluides

## 📱 Captures d'Écran

### Dashboard
- Statistiques en temps réel
- Graphiques de confiance
- Status de connexion

### Prédictions
- Liste filtrée des matchs
- Probabilités visuelles
- Recherche instantanée

### Détails
- Analyse complète du match
- Graphiques détaillés
- Recommandations ML

## 🔄 Synchronisation

L'application se synchronise automatiquement avec votre système de prédiction :

1. **Données en temps réel** depuis `predictions_results.xlsx`
2. **Calculs ML** via les modèles XGBoost/RandomForest
3. **Base de données** SQLite avec 59,636 matchs historiques
4. **APIs REST** pour une intégration fluide

## 🛠️ Développement

### Structure du projet
```
Aplli mobile/
├── App.js                 # Point d'entrée principal
├── src/
│   ├── screens/          # Écrans de l'application
│   │   ├── DashboardScreen.js
│   │   ├── PredictionsScreen.js
│   │   ├── MatchDetailScreen.js
│   │   └── SettingsScreen.js
│   └── services/         # Services API
│       └── ApiService.js
├── package.json          # Dépendances
├── app.json             # Configuration Expo
└── README.md            # Documentation
```

### Commandes utiles
```bash
# Démarrer en mode développement
npm start

# Build pour Android
expo build:android

# Build pour iOS  
expo build:ios

# Publier sur Expo
expo publish
```

## 🚀 Déploiement

### Option 1: Expo Go (Développement)
- Utilisez l'app Expo Go pour tester
- Scannez le QR code généré

### Option 2: Build Standalone
```bash
# Android APK
expo build:android -t apk

# iOS IPA (nécessite compte développeur Apple)
expo build:ios -t archive
```

### Option 3: App Stores
- Suivez la documentation Expo pour publier sur Google Play/App Store

## 🔧 Dépannage

### Problèmes courants

**Connexion API échouée**
- Vérifiez que l'API Flask est en cours d'exécution
- Testez l'URL dans les paramètres de l'app
- Vérifiez les permissions réseau

**Erreur de build**
- Supprimez `node_modules` et réinstallez : `rm -rf node_modules && npm install`
- Videz le cache Expo : `expo r -c`

**Problèmes de performance**
- Activez le mode développement pour plus de logs
- Vérifiez la console pour les erreurs réseau

## 📞 Support

Pour toute question ou problème :
1. Consultez cette documentation
2. Vérifiez les logs de l'API Flask
3. Testez la connexion dans les paramètres de l'app

## 🎯 Prochaines Fonctionnalités

- [ ] Mode hors ligne avec cache local
- [ ] Notifications push pour nouvelles prédictions  
- [ ] Thème sombre
- [ ] Historique des prédictions
- [ ] Statistiques personnalisées
- [ ] Export des données

---

**Version** : 1.0.0  
**Développé par** : Tennis Prediction System  
**Technologie** : React Native + Expo + Machine Learning
