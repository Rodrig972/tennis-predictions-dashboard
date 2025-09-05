import subprocess
import sys
import os
import time
from datetime import datetime

def run_script(script_name):
    """
    Exécute un script Python et vérifie son succès.
    Retourne True si le script s'est exécuté avec succès, False sinon.
    """
    print(f"\n{'='*50}")
    print(f"Exécution de {script_name}")
    print(f"{'='*50}")
    
    try:
        # Vérifier si le script existe
        if not os.path.exists(script_name):
            print(f"ERREUR: Le script {script_name} n'existe pas!")
            return False
            
        print(f"Chemin complet du script: {os.path.abspath(script_name)}")
        print(f"Contenu du dossier courant: {os.listdir('.')}")
        
        # Exécuter le script
        print(f"Démarrage de l'exécution de {script_name}...")
        process = subprocess.Popen(
            [sys.executable, script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Lire la sortie en temps réel
        if process.stdout is not None:
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
        else:
            # Si stdout n'est pas disponible, attendre simplement la fin du processus
            process.wait()
            
        # Obtenir le code de retour
        return_code = process.returncode
        
        # En cas d'erreur, afficher également stderr
        if return_code != 0 and process.stderr is not None:
            error_output = process.stderr.read()
            if error_output:
                print(f"Erreur détaillée: {error_output}")
        
        if return_code == 0:
            print(f"{script_name} terminé avec succès")
            return True
        else:
            print(f"Erreur lors de l'exécution de {script_name}")
            return False
            
    except Exception as e:
        print(f"Erreur lors de l'exécution de {script_name}: {str(e)}")
        return False

def main():
    # Liste des scripts à exécuter dans l'ordre
    scripts = [
        'maj_joueurs_atp_wta.py',
        'update_players_list.py',
        'scraper_tennis_explorer.py',
        'transform_stats.py',
        'simplified_prediction_system.py',
        'simple_ml_trainer.py',
        'working_dashboard.py'
        
        
        
        
        
        
        
        
        
        

    
        
    ]
    
    print(f"\nDébut de l'exécution des scripts - {datetime.now()}")
    #Corriger le répertoire courant
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Chemin courant: {os.getcwd()}")
    print(f"{'='*50}\n")
    
    # Vérifier que tous les scripts existent
    missing_scripts = [script for script in scripts if not os.path.exists(script)]
    if missing_scripts:
        print("ERREUR: Les scripts suivants sont manquants:")
        for script in missing_scripts:
            print(f"- {script}")
        print("\nContenu du dossier courant:")
        print(os.listdir('.'))
        return
    
    # Exécuter chaque script dans l'ordre
    for i, script in enumerate(scripts, 1):
        print(f"\nExécution du script {i}/{len(scripts)}: {script}")
        if not run_script(script):
            print(f"\nArrêt de l'exécution suite à une erreur dans {script}")
            return
        print(f"\nAttente de 2 secondes avant le prochain script...")
        time.sleep(2)
    
    print(f"\nTous les scripts ont été exécutés avec succès!")
    print(f"Fin de l'exécution - {datetime.now()}")

if __name__ == "__main__":
    main() 