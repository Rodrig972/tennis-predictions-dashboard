"""Test rapide pour vérifier les nouvelles probabilités"""

from ultimate_prediction_system import UltimateTennisPredictionSystem

# Test avec un match équilibré
system = UltimateTennisPredictionSystem(enable_ai_context=False)

match_equilibre = {
    'joueur_1': 'Joueur A',
    'joueur_2': 'Joueur B',
    'classement_j1': 50,
    'classement_j2': 52,
    'cote_j1': 1.90,
    'cote_j2': 1.95,
    'tournoi': 'Test',
    'round': 'R1'
}

print("=" * 60)
print("TEST RAPIDE - VERIFICATION DES PROBABILITES")
print("=" * 60)

print("\n[MATCH EQUILIBRE]")
print(f"Joueur A (#50, cote 1.90) vs Joueur B (#52, cote 1.95)")

pred = system.ensemble_prediction(match_equilibre)

print(f"\nResultat:")
print(f"  Gagnant: {pred['gagnant_predit']}")
print(f"  Confiance: {pred['confiance']:.1f}%")
print(f"  Proba J1: {pred['probabilites']['joueur_1']*100:.1f}%")
print(f"  Proba J2: {pred['probabilites']['joueur_2']*100:.1f}%")

if pred['confiance'] >= 60:
    print(f"\n[OK] SUCCES: Probabilite >= 60% ({pred['confiance']:.1f}%)")
else:
    print(f"\n[ERREUR] ECHEC: Probabilite < 60% ({pred['confiance']:.1f}%)")

# Test avec favori clair
match_clair = {
    'joueur_1': 'Top Player',
    'joueur_2': 'Outsider',
    'classement_j1': 5,
    'classement_j2': 150,
    'cote_j1': 1.15,
    'cote_j2': 6.00,
    'tournoi': 'Test',
    'round': 'R1'
}

print("\n" + "=" * 60)
print("[FAVORI CLAIR]")
print(f"Top Player (#5, cote 1.15) vs Outsider (#150, cote 6.00)")

pred2 = system.ensemble_prediction(match_clair)

print(f"\nResultat:")
print(f"  Gagnant: {pred2['gagnant_predit']}")
print(f"  Confiance: {pred2['confiance']:.1f}%")

if pred2['confiance'] >= 80:
    print(f"\n[EXCELLENT] Probabilite >= 80% ({pred2['confiance']:.1f}%)")
elif pred2['confiance'] >= 70:
    print(f"\n[BON] Probabilite >= 70% ({pred2['confiance']:.1f}%)")
else:
    print(f"\n[MOYEN] Probabilite < 70% ({pred2['confiance']:.1f}%)")

print("\n" + "=" * 60)
print("CONCLUSION")
print("=" * 60)

if pred['confiance'] >= 60 and pred2['confiance'] >= 75:
    print("\n[OK] Les optimisations sont ACTIVES et fonctionnent correctement!")
    print("   - Match equilibre: >= 60%")
    print("   - Favori clair: >= 75%")
else:
    print("\n[ERREUR] Les optimisations ne semblent PAS actives")
    print("   Verifiez que ultimate_prediction_system.py a bien ete modifie")

print()
