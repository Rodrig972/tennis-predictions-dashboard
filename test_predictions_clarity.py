"""
Test de clarté des prédictions - Vérification des probabilités
"""

from ultimate_prediction_system import UltimateTennisPredictionSystem

def test_predictions_clarity():
    """Teste la clarté des prédictions sur tous les matchs Excel"""
    
    print("=" * 70)
    print("TEST DE CLARTE DES PREDICTIONS")
    print("=" * 70)
    
    system = UltimateTennisPredictionSystem(enable_ai_context=True)
    predictions = system.process_all_matches()
    
    # Analyser la distribution des probabilités
    ranges = {
        '50-60%': 0,
        '60-70%': 0,
        '70-80%': 0,
        '80-90%': 0,
        '90-100%': 0
    }
    
    very_clear = []  # > 75%
    clear = []       # 65-75%
    moderate = []    # 60-65%
    unclear = []     # < 60%
    
    print(f"\n[ANALYSE] {len(predictions)} matchs traites\n")
    print("-" * 70)
    print(f"{'Match':<40} {'Favori':<20} {'Confiance':>10}")
    print("-" * 70)
    
    for pred in predictions:
        confiance = pred['Confiance (%)']
        match = pred['Match']
        favori = pred['Gagnant Prédit']
        
        # Afficher
        print(f"{match[:40]:<40} {favori[:20]:<20} {confiance:>9.1f}%")
        
        # Catégoriser
        if confiance >= 90:
            ranges['90-100%'] += 1
        elif confiance >= 80:
            ranges['80-90%'] += 1
        elif confiance >= 70:
            ranges['70-80%'] += 1
        elif confiance >= 60:
            ranges['60-70%'] += 1
        else:
            ranges['50-60%'] += 1
        
        # Clarté
        if confiance >= 75:
            very_clear.append((match, confiance))
        elif confiance >= 65:
            clear.append((match, confiance))
        elif confiance >= 60:
            moderate.append((match, confiance))
        else:
            unclear.append((match, confiance))
    
    # Statistiques
    print("\n" + "=" * 70)
    print("DISTRIBUTION DES PROBABILITES")
    print("=" * 70)
    
    for range_name, count in ranges.items():
        percentage = (count / len(predictions) * 100) if predictions else 0
        bar = "#" * int(percentage / 2)
        print(f"{range_name:>10} : {count:>3} matchs ({percentage:>5.1f}%) {bar}")
    
    print("\n" + "=" * 70)
    print("CLARTE DES PREDICTIONS")
    print("=" * 70)
    
    print(f"\n[TRES CLAIRE] >= 75% : {len(very_clear)} matchs")
    if very_clear:
        for match, conf in very_clear[:5]:
            print(f"  - {match[:50]}: {conf:.1f}%")
    
    print(f"\n[CLAIRE] 65-75% : {len(clear)} matchs")
    if clear:
        for match, conf in clear[:5]:
            print(f"  - {match[:50]}: {conf:.1f}%")
    
    print(f"\n[MODEREE] 60-65% : {len(moderate)} matchs")
    if moderate:
        for match, conf in moderate[:5]:
            print(f"  - {match[:50]}: {conf:.1f}%")
    
    print(f"\n[PEU CLAIRE] < 60% : {len(unclear)} matchs")
    if unclear:
        for match, conf in unclear:
            print(f"  - {match[:50]}: {conf:.1f}%")
    
    # Recommandations
    print("\n" + "=" * 70)
    print("RECOMMANDATIONS")
    print("=" * 70)
    
    total_clear = len(very_clear) + len(clear)
    clarity_rate = (total_clear / len(predictions) * 100) if predictions else 0
    
    print(f"\nTaux de clarte (>= 65%) : {clarity_rate:.1f}%")
    
    if clarity_rate >= 80:
        print("[EXCELLENT] Les predictions sont tres claires et exploitables!")
    elif clarity_rate >= 60:
        print("[BON] La majorite des predictions sont claires.")
    elif clarity_rate >= 40:
        print("[MOYEN] Environ la moitie des predictions sont claires.")
    else:
        print("[FAIBLE] Beaucoup de predictions restent proches de 50%.")
    
    # Moyenne de confiance
    avg_confidence = sum(p['Confiance (%)'] for p in predictions) / len(predictions) if predictions else 0
    print(f"\nConfiance moyenne : {avg_confidence:.1f}%")
    
    if avg_confidence >= 70:
        print("[EXCELLENT] Confiance moyenne tres elevee!")
    elif avg_confidence >= 65:
        print("[BON] Confiance moyenne satisfaisante.")
    else:
        print("[A AMELIORER] Confiance moyenne encore faible.")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_predictions_clarity()
