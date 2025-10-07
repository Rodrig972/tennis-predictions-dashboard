"""
Test d'intégration du système IA dans les prédictions
"""

from ultimate_prediction_system import UltimateTennisPredictionSystem
import json

def test_prediction_with_ai():
    """Test des prédictions avec analyse IA"""
    
    print("=" * 60)
    print("TEST D'INTEGRATION IA - SYSTEME DE PREDICTION TENNIS")
    print("=" * 60)
    
    # Test 1: Système avec IA activée
    print("\n[TEST 1] Systeme avec IA activee")
    print("-" * 60)
    system_with_ai = UltimateTennisPredictionSystem(enable_ai_context=True)
    
    # Test avec un match exemple
    test_match = {
        'joueur_1': 'Jannik Sinner',
        'joueur_2': 'Carlos Alcaraz',
        'classement_j1': 1,
        'classement_j2': 2,
        'tournoi': 'ATP Finals',
        'round': 'Final',
        'cote_j1': 1.85,
        'cote_j2': 1.95,
        'date': '2024-11-03',
        'heure': '15:00'
    }
    
    print(f"\nMatch test: {test_match['joueur_1']} vs {test_match['joueur_2']}")
    print(f"Classements: #{test_match['classement_j1']} vs #{test_match['classement_j2']}")
    print(f"Cotes: {test_match['cote_j1']} vs {test_match['cote_j2']}")
    
    prediction = system_with_ai.ensemble_prediction(test_match)
    
    print(f"\n[RESULTAT]")
    print(f"  Gagnant predit: {prediction['gagnant_predit']}")
    print(f"  Confiance: {prediction['confiance']:.1f}%")
    print(f"  Modeles utilises: {prediction.get('models_used', 0)}")
    
    # Vérifier le contexte IA
    if 'ai_context' in prediction and prediction['ai_context']:
        ai_ctx = prediction['ai_context']
        print(f"\n[CONTEXTE IA]")
        print(f"  Ajustement net: {ai_ctx.get('net_adjustment', 0):+.3f}")
        print(f"  Avantage: {ai_ctx.get('advantage', 'N/A')}")
        print(f"  Boost confiance: {ai_ctx.get('confidence_boost', 0):.1f}%")
        
        # Détails joueur 1
        p1_ctx = ai_ctx.get('player1_context', {})
        if p1_ctx:
            print(f"\n  Joueur 1 ({test_match['joueur_1']}):")
            print(f"    Resume: {p1_ctx.get('summary', 'N/A')}")
            print(f"    Facteurs: {', '.join(p1_ctx.get('key_factors', []))}")
            print(f"    Ajustement: {p1_ctx.get('overall_adjustment', 0):+.3f}")
        
        # Détails joueur 2
        p2_ctx = ai_ctx.get('player2_context', {})
        if p2_ctx:
            print(f"\n  Joueur 2 ({test_match['joueur_2']}):")
            print(f"    Resume: {p2_ctx.get('summary', 'N/A')}")
            print(f"    Facteurs: {', '.join(p2_ctx.get('key_factors', []))}")
            print(f"    Ajustement: {p2_ctx.get('overall_adjustment', 0):+.3f}")
    else:
        print(f"\n[CONTEXTE IA] Non disponible (mode fallback)")
    
    # Test 2: Système sans IA
    print("\n" + "=" * 60)
    print("[TEST 2] Systeme SANS IA (comparaison)")
    print("-" * 60)
    system_without_ai = UltimateTennisPredictionSystem(enable_ai_context=False)
    
    prediction_no_ai = system_without_ai.ensemble_prediction(test_match)
    
    print(f"\n[RESULTAT SANS IA]")
    print(f"  Gagnant predit: {prediction_no_ai['gagnant_predit']}")
    print(f"  Confiance: {prediction_no_ai['confiance']:.1f}%")
    print(f"  Modeles utilises: {prediction_no_ai.get('models_used', 0)}")
    
    # Comparaison
    print("\n" + "=" * 60)
    print("[COMPARAISON]")
    print("-" * 60)
    diff_confiance = prediction['confiance'] - prediction_no_ai['confiance']
    print(f"  Difference de confiance: {diff_confiance:+.1f}%")
    print(f"  Impact IA: {'Significatif' if abs(diff_confiance) > 2 else 'Minime'}")
    
    # Test 3: Traitement de tous les matchs Excel
    print("\n" + "=" * 60)
    print("[TEST 3] Traitement des matchs Excel avec IA")
    print("-" * 60)
    
    try:
        predictions = system_with_ai.process_all_matches()
        print(f"\n[SUCCES] {len(predictions)} matchs traites")
        
        # Compter combien ont un contexte IA
        with_ai = sum(1 for p in predictions if p.get('AI_Context'))
        print(f"  Matchs avec analyse IA: {with_ai}/{len(predictions)}")
        
        # Afficher quelques exemples
        if predictions:
            print(f"\n[EXEMPLES]")
            for i, pred in enumerate(predictions[:3]):
                print(f"\n  Match {i+1}: {pred['Match']}")
                print(f"    Tournoi: {pred['Tournoi']}")
                print(f"    Prediction: {pred['Gagnant Prédit']} ({pred['Confiance (%)']}%)")
                if pred.get('AI_Context'):
                    ai = pred['AI_Context']
                    print(f"    IA Avantage: {ai.get('advantage', 'N/A')} ({ai.get('net_adjustment', 0):+.3f})")
    except Exception as e:
        print(f"\n[ERREUR] Impossible de charger les matchs Excel: {e}")
    
    print("\n" + "=" * 60)
    print("TEST TERMINE")
    print("=" * 60)

if __name__ == "__main__":
    test_prediction_with_ai()
