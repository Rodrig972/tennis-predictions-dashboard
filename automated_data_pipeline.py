"""
Script d'automatisation complète du pipeline de données tennis
Ordre d'exécution: scraper -> transform -> prediction -> app
"""

import subprocess
import sys
import time
import os
from datetime import datetime

class TennisDataPipeline:
    def __init__(self):
        self.scripts_order = [
            {
                'name': 'Scraper Tennis Explorer',
                'file': 'scraper_tennis_explorer.py',
                'description': 'Extraction des données depuis Tennis Explorer',
                'output_file': 'data/Result_data_export.xlsx'
            },
            {
                'name': 'Transform Stats',
                'file': 'transform_stats.py', 
                'description': 'Transformation et nettoyage des données',
                'output_file': 'data/Stats_tournois_en_cours.xlsx'
            },
            {
                'name': 'Simplified Prediction System',
                'file': 'simplified_prediction_system.py',
                'description': 'Génération des prédictions ML',
                'output_file': None  # Pas de fichier de sortie spécifique
            },
            {
                'name': 'Flask App',
                'file': 'simple_app_updated.py',
                'description': 'Lancement de l\'application web',
                'output_file': None
            }
        ]
        
    def log_message(self, message, level="INFO"):
        """Affiche un message avec timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def check_file_exists(self, filepath):
        """Vérifie si un fichier existe"""
        if filepath and os.path.exists(filepath):
            size = os.path.getsize(filepath)
            self.log_message(f"✅ Fichier trouvé: {filepath} ({size} bytes)")
            return True
        elif filepath:
            self.log_message(f"❌ Fichier manquant: {filepath}", "WARNING")
            return False
        return True
        
    def run_script(self, script_info, timeout=600):
        """Exécute un script Python avec gestion d'erreurs"""
        script_name = script_info['name']
        script_file = script_info['file']
        
        self.log_message(f"🚀 Démarrage: {script_name}")
        self.log_message(f"📄 Fichier: {script_file}")
        self.log_message(f"📝 Description: {script_info['description']}")
        
        try:
            # Vérifier que le fichier script existe
            if not os.path.exists(script_file):
                self.log_message(f"❌ Script non trouvé: {script_file}", "ERROR")
                return False
                
            # Exécuter le script
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, script_file],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.getcwd()
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                self.log_message(f"✅ {script_name} terminé avec succès ({execution_time:.1f}s)")
                
                # Afficher la sortie si elle existe
                if result.stdout.strip():
                    self.log_message("📤 Sortie du script:")
                    for line in result.stdout.strip().split('\n')[-5:]:  # 5 dernières lignes
                        print(f"    {line}")
                
                # Vérifier le fichier de sortie si spécifié
                if script_info['output_file']:
                    time.sleep(2)  # Attendre que le fichier soit écrit
                    return self.check_file_exists(script_info['output_file'])
                
                return True
                
            else:
                self.log_message(f"❌ {script_name} a échoué (code: {result.returncode})", "ERROR")
                if result.stderr:
                    self.log_message("📥 Erreurs:")
                    for line in result.stderr.strip().split('\n')[-3:]:  # 3 dernières lignes d'erreur
                        print(f"    {line}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_message(f"⏰ {script_name} a dépassé le timeout ({timeout}s)", "ERROR")
            return False
        except Exception as e:
            self.log_message(f"💥 Erreur lors de l'exécution de {script_name}: {str(e)}", "ERROR")
            return False
    
    def run_pipeline(self, start_from=0, stop_before_app=False):
        """
        Exécute le pipeline complet
        
        Args:
            start_from (int): Index du script à partir duquel commencer (0=scraper, 1=transform, etc.)
            stop_before_app (bool): S'arrêter avant le lancement de l'app Flask
        """
        self.log_message("🎯 DÉMARRAGE DU PIPELINE DE DONNÉES TENNIS")
        self.log_message("=" * 60)
        
        # Déterminer les scripts à exécuter
        scripts_to_run = self.scripts_order[start_from:]
        if stop_before_app:
            scripts_to_run = [s for s in scripts_to_run if s['file'] != 'simple_app_updated.py']
        
        total_scripts = len(scripts_to_run)
        successful_scripts = 0
        
        for i, script_info in enumerate(scripts_to_run, 1):
            self.log_message(f"📊 Étape {i}/{total_scripts}")
            self.log_message("-" * 40)
            
            success = self.run_script(script_info)
            
            if success:
                successful_scripts += 1
                self.log_message(f"✅ Étape {i} réussie\n")
            else:
                self.log_message(f"❌ Étape {i} échouée", "ERROR")
                
                # Demander si on continue malgré l'erreur
                user_input = input("Continuer malgré l'erreur? (o/N): ").lower()
                if user_input not in ['o', 'oui', 'y', 'yes']:
                    self.log_message("🛑 Pipeline interrompu par l'utilisateur", "WARNING")
                    break
                else:
                    self.log_message("⚠️ Continuation malgré l'erreur", "WARNING")
        
        # Résumé final
        self.log_message("=" * 60)
        self.log_message("📋 RÉSUMÉ DU PIPELINE")
        self.log_message(f"✅ Scripts réussis: {successful_scripts}/{total_scripts}")
        
        if successful_scripts == total_scripts:
            self.log_message("🎉 Pipeline terminé avec succès!")
            
            if not stop_before_app and any(s['file'] == 'simple_app_updated.py' for s in scripts_to_run):
                self.log_message("🌐 Application web démarrée sur http://127.0.0.1:5000")
        else:
            self.log_message("⚠️ Pipeline terminé avec des erreurs", "WARNING")
        
        return successful_scripts == total_scripts

def main():
    """Fonction principale avec options de lancement"""
    pipeline = TennisDataPipeline()
    
    print("🎾 PIPELINE D'AUTOMATISATION TENNIS")
    print("=" * 50)
    print("Options disponibles:")
    print("1. Pipeline complet (scraper → transform → prediction → app)")
    print("2. À partir de transform (transform → prediction → app)")
    print("3. À partir de prediction (prediction → app)")
    print("4. Pipeline sans app (scraper → transform → prediction)")
    print("5. Seulement l'app")
    print()
    
    try:
        choice = input("Choisissez une option (1-5): ").strip()
        
        if choice == "1":
            pipeline.run_pipeline(start_from=0)
        elif choice == "2":
            pipeline.run_pipeline(start_from=1)
        elif choice == "3":
            pipeline.run_pipeline(start_from=2)
        elif choice == "4":
            pipeline.run_pipeline(start_from=0, stop_before_app=True)
        elif choice == "5":
            pipeline.run_pipeline(start_from=3)
        else:
            print("❌ Option invalide")
            return
            
    except KeyboardInterrupt:
        print("\n🛑 Pipeline interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {str(e)}")

if __name__ == "__main__":
    main()
