"""
Logique de chargement et prédiction du modèle ML
"""
import joblib
import numpy as np
from pathlib import Path
import logging
from typing import Optional

from app.config import MODEL_PATH, MODEL_CONFIG

logger = logging.getLogger(__name__)


class CreditScoringPredictor:
    """Classe pour gérer le modèle de credit scoring"""
    
    def __init__(self, model_path: Path = MODEL_PATH):
        """
        Initialise le prédicteur
        
        Args:
            model_path: Chemin vers le modèle sérialisé
        """
        self.model_path = model_path
        self.model: Optional[object] = None
        self.model_config = MODEL_CONFIG
        self._load_model()
    
    def _load_model(self) -> None:
        """Charge le modèle depuis le fichier"""
        try:
            if not self.model_path.exists():
                raise FileNotFoundError(f"Modèle introuvable : {self.model_path}")
            
            self.model = joblib.load(self.model_path)
            logger.info(f"✅ Modèle chargé avec succès depuis {self.model_path}")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement du modèle : {str(e)}")
            raise
    
    def is_loaded(self) -> bool:
        """Vérifie si le modèle est chargé"""
        return self.model is not None
    
    def predict(self, age: int, income: float, credit_amount: float, 
                duration: int) -> tuple[str, float]:
        """
        Fait une prédiction sur une demande de crédit
        
        Args:
            age: Âge du demandeur
            income: Revenu mensuel
            credit_amount: Montant du crédit demandé
            duration: Durée du crédit en mois
            
        Returns:
            tuple: (décision, probabilité)
                - décision: "APPROVED" ou "REJECTED"
                - probabilité: float entre 0 et 1
        """
        if not self.is_loaded():
            raise RuntimeError("Le modèle n'est pas chargé")
        
        try:
            # Préparer les features dans l'ordre attendu
            features = np.array([[age, income, credit_amount, duration]])
            
            logger.info(f"🔍 Prédiction pour : age={age}, income={income}, "
                       f"credit={credit_amount}, duration={duration}")
            
            # Obtenir la probabilité de la classe positive (approbation)
            probability = self.model.predict_proba(features)[0, 1]
            
            # Décision basée sur le seuil
            threshold = self.model_config["threshold"]
            decision = "APPROVED" if probability >= threshold else "REJECTED"
            
            logger.info(f"✅ Décision: {decision} (probabilité: {probability:.2f})")
            
            return decision, float(probability)
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la prédiction : {str(e)}")
            raise
    
    def get_model_info(self) -> dict:
        """Retourne les informations sur le modèle"""
        return {
            "model_name": self.model_config["name"],
            "algorithm": self.model_config["algorithm"],
            "version": self.model_config["version"],
            "features": self.model_config["features"],
            "threshold": self.model_config["threshold"]
        }


# Instance globale du prédicteur (singleton)
predictor = CreditScoringPredictor()
