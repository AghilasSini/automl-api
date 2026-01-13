credit_scoringimport os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]:%(message)s:')

project_name = "credit_scoring"  # Nom du projet / package principal

# Liste des fichiers à créer
list_of_files = [
    f"{project_name}-api/app/main.py",          # Application FastAPI
    f"{project_name}-api/app/models.py",        # Schémas Pydantic
    f"{project_name}-api/app/predictor.py",     # Logique ML
    f"{project_name}-api/app/config.py",        # Configuration
    f"{project_name}-api/models/credit_scoring_model.pkl",  # Modèle ML
    f"{project_name}-api/tests/test_api.py",   # Tests pytest
    f"{project_name}-api/Dockerfile",
    f"{project_name}-api/docker-compose.yml",
    f"{project_name}-api/requirements.txt",
    f"{project_name}-api/openapi.yaml",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    if not filepath.exists() or os.path.getsize(filepath) == 0:
        with open(filepath, "w") as f:
            # On peut ajouter des templates de code minimal pour les fichiers Python
            if filename.endswith(".py"):
                if filename == "main.py":
                    f.write(
                        "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'message': 'Hello World'}\n"
                    )
                elif filename == "models.py":
                    f.write("from pydantic import BaseModel\n\n# Exemple de schéma Pydantic\n")
                elif filename == "predictor.py":
                    f.write("# Logique ML / fonctions de prédiction\n")
                elif filename == "config.py":
                    f.write("import os\n\n# Configuration de l'application\n")
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

