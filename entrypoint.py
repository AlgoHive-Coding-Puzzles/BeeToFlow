import os
import sys

def main():
    # Récupérer l'argument des dossiers cibles
    target_dirs = sys.argv[1]
    
    # Convertir en liste
    directories = target_dirs.split(',')
    
    print("📂 Liste des dossiers à traiter :")
    for directory in directories:
        directory = directory.strip()
        if os.path.isdir(directory):
            print(f"✅ {directory}")
        else:
            print(f"⚠️ Le dossier '{directory}' n'existe pas.")

if __name__ == "__main__":
    main()
