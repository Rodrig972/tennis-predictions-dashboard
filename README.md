# Système de Prédiction Tennis

Ce système reproduit les calculs de probabilités et de cotes pour les matchs de tennis basés sur le fichier Excel `data_export.xlsx`.

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### Script principal calibré
```bash
python calibrated_tennis_system.py
```

### Script d'analyse original
```bash
python tennis_prediction_system.py
```

## Structure des données

Le système analyse deux feuilles Excel :

1. **Tournoi_detail** : Données de tous les matchs avec statistiques des joueurs
2. **Match1** : Analyse détaillée d'un match spécifique avec calculs de probabilités

## Fonctionnalités

- Extraction des données depuis Excel
- Calcul des probabilités de victoire
- Estimation des cotes
- Analyse des statistiques détaillées
- Reproduction exacte des résultats Excel

## Résultats

Le système reproduit les probabilités exactes du fichier Excel :
- Match 1 (Rybakina vs Raducanu) : 84.62% vs 15.38%
- Cotes correspondantes : 1.028 vs 5.652

## Facteurs pris en compte

- Classement ATP/WTA
- Pourcentage de victoires en carrière
- Historique des confrontations (H2H)
- Forme récente
- Statistiques techniques (service, break points, etc.)
