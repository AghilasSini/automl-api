"""
Configuration de l'application API Credit Scoring
"""
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "credit_scoring_model.pkl"

# Configuration du modèle
MODEL_CONFIG = {
    "name": "Credit Scoring AutoML",
    "algorithm": "AutoML (FLAML)",
    "version": "1.0",
    "features": ["age", "income", "credit_amount", "duration"],
    "threshold": 0.5,  # Seuil de décision pour APPROVED/REJECTED
}

# Configuration API
API_CONFIG = {
    "title": "API Credit Scoring",
    "description": "API de credit scoring basée sur un modèle AutoML",
    "version": "1.0.0",
    "contact": {
        "email": "aghilas.sini@univ-lemans.fr"
    },
}
