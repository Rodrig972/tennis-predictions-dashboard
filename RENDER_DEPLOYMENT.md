# Déploiement sur Render

## Configuration Automatique

Le site se déploie automatiquement sur Render à chaque push sur la branche `master`.

**URL** : https://tennis-predictions-dashboard.onrender.com/

## Fichiers de Configuration

### `render.yaml`
Configure le service web sur Render :
- Type : Web Service
- Environnement : Python 3.11
- Commande de build : `pip install -r requirements.txt`
- Commande de démarrage : `gunicorn working_dashboard:app`

### `requirements.txt`
Liste toutes les dépendances Python nécessaires.

## Variables d'Environnement

### Obligatoires
- `PORT` : Automatiquement défini par Render

### Optionnelles (pour l'IA)
- `OPENAI_API_KEY` : Clé API OpenAI pour l'analyse contextuelle
- `SERPER_API_KEY` : Clé API Serper pour la recherche Google

**Note** : Le système fonctionne en mode fallback sans ces clés.

## Fichiers de Données

⚠️ **Important** : Les fichiers suivants sont exclus du dépôt Git mais nécessaires sur Render :

### Fichiers Excel
- `data/Stats_tournois_en_cours.xlsx` - Données des matchs en cours

### Modèles ML
- `ml_models/real_tennis_model.joblib`
- `ml_models/simple_tennis_model.joblib`

### Solutions

#### Option 1 : Upload Manuel sur Render
1. Aller sur le dashboard Render
2. Accéder à l'onglet "Shell"
3. Uploader les fichiers manuellement

#### Option 2 : Utiliser un Service de Stockage
1. Héberger les fichiers sur AWS S3, Google Cloud Storage, etc.
2. Télécharger les fichiers au démarrage de l'application

#### Option 3 : Inclure dans le Dépôt (Temporaire)
```bash
# Retirer temporairement du .gitignore
git add -f data/Stats_tournois_en_cours.xlsx
git add -f ml_models/*.joblib
git commit -m "temp: Add data files for Render"
git push origin master
```

## Forcer un Redéploiement

### Méthode 1 : Via le Dashboard Render
1. Aller sur https://dashboard.render.com/
2. Sélectionner le service "tennis-predictions-dashboard"
3. Cliquer sur "Manual Deploy" → "Deploy latest commit"

### Méthode 2 : Via Git
```bash
# Faire un commit vide pour forcer le redéploiement
git commit --allow-empty -m "trigger: Force Render redeploy"
git push origin master
```

### Méthode 3 : Via l'API Render
```bash
curl -X POST https://api.render.com/deploy/srv-YOUR_SERVICE_ID?key=YOUR_DEPLOY_HOOK_KEY
```

## Vérification du Déploiement

### Logs
```bash
# Via le dashboard Render
Dashboard → Service → Logs
```

### Santé du Service
```bash
curl https://tennis-predictions-dashboard.onrender.com/
```

## Résolution des Problèmes

### Le site ne se met pas à jour
1. Vérifier que le push Git a réussi
2. Vérifier les logs de build sur Render
3. Forcer un redéploiement manuel

### Erreur "Module not found"
1. Vérifier que toutes les dépendances sont dans `requirements.txt`
2. Vérifier la version de Python (3.11)

### Erreur "File not found" (Excel/Models)
1. Vérifier que les fichiers de données sont présents
2. Utiliser une des solutions ci-dessus pour les ajouter

### Le site est lent au démarrage
- Normal : Render met en veille les services gratuits après 15 min d'inactivité
- Le premier accès peut prendre 30-60 secondes

## Mise à Jour du Site

### Workflow Standard
```bash
# 1. Faire vos modifications localement
# 2. Tester localement
python working_dashboard.py

# 3. Commiter et pousser
git add .
git commit -m "feat: Vos modifications"
git push origin master

# 4. Render se redéploie automatiquement (2-3 minutes)
```

## Monitoring

### Métriques Disponibles
- Temps de réponse
- Utilisation CPU/RAM
- Nombre de requêtes
- Erreurs

### Alertes
Configurer des alertes sur le dashboard Render pour :
- Service down
- Erreurs 500
- Utilisation excessive de ressources

## Limites du Plan Gratuit

- 750 heures/mois
- Mise en veille après 15 min d'inactivité
- Redémarrage automatique à la première requête
- 512 MB RAM
- Pas de domaine personnalisé

## Upgrade vers un Plan Payant

Pour de meilleures performances :
- Pas de mise en veille
- Plus de RAM/CPU
- Domaine personnalisé
- Support prioritaire

**Prix** : À partir de $7/mois

## Support

- Documentation Render : https://render.com/docs
- Support : support@render.com
- GitHub Issues : https://github.com/Rodrig972/tennis-predictions-dashboard/issues
