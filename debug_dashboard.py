"""
Dashboard de debug minimal pour identifier le problème
"""

from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Debug Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: white; }
        .match { background: #333; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .error { color: red; padding: 20px; background: #400; border-radius: 8px; }
        .success { color: green; padding: 20px; background: #040; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>🎾 Debug Dashboard</h1>
    <div id="status">Chargement...</div>
    <div id="matches"></div>
    
    <script>
        console.log('Script démarré');
        
        fetch('/api/matches')
            .then(response => {
                console.log('Réponse reçue:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Données reçues:', data);
                
                document.getElementById('status').innerHTML = 
                    '<div class="success">✅ Données chargées: ' + data.length + ' matchs</div>';
                
                let html = '';
                data.forEach(match => {
                    html += `
                        <div class="match">
                            <h3>${match.Match}</h3>
                            <p>Favori: ${match['Gagnant Prédit']} (${match['Confiance (%)']}%)</p>
                            <p>Modèle: ${match.Modele || 'Non défini'}</p>
                        </div>
                    `;
                });
                
                document.getElementById('matches').innerHTML = html;
            })
            .catch(error => {
                console.error('Erreur:', error);
                document.getElementById('status').innerHTML = 
                    '<div class="error">❌ Erreur: ' + error.message + '</div>';
            });
    </script>
</body>
</html>
    '''

@app.route('/api/matches')
def get_matches():
    try:
        from simplified_prediction_system import SimplifiedTennisPredictionSystem
        
        system = SimplifiedTennisPredictionSystem()
        predictions = system.process_all_matches()
        
        print(f"DEBUG: {len(predictions)} prédictions générées")
        for p in predictions:
            print(f"  - {p.get('Match', 'N/A')}: {p.get('Modele', 'N/A')}")
        
        return jsonify(predictions)
        
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        return jsonify([{
            "Match": "Test Match",
            "Gagnant Prédit": "Test Player",
            "Confiance (%)": 50,
            "Modele": "Test Model",
            "error": str(e)
        }])

if __name__ == '__main__':
    print("=== DEBUG DASHBOARD ===")
    print("URL: http://127.0.0.1:5002")
    app.run(debug=True, host='0.0.0.0', port=5002)
