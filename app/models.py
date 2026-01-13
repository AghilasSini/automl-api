"""
Schémas Pydantic pour la validation des données
"""
from pydantic import BaseModel, Field, field_validator
from typing import Literal


class CreditRequest(BaseModel):
    """Schéma de la requête de crédit"""
    age: int = Field(..., ge=18, le=100, description="Âge du demandeur")
    income: float = Field(..., gt=0, description="Revenu mensuel en euros")
    credit_amount: float = Field(..., gt=0, description="Montant du crédit demandé")
    duration: int = Field(..., ge=6, le=120, description="Durée du crédit en mois")

    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if v < 18:
            raise ValueError("L'âge doit être supérieur ou égal à 18 ans")
        if v > 100:
            raise ValueError("L'âge doit être inférieur à 100 ans")
        return v

    @field_validator('duration')
    @classmethod
    def validate_duration(cls, v):
        if v < 6:
            raise ValueError("La durée minimale est de 6 mois")
        if v > 120:
            raise ValueError("La durée maximale est de 120 mois")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "age": 35,
                "income": 3200.0,
                "credit_amount": 15000.0,
                "duration": 48
            }
        }


class CreditResponse(BaseModel):
    """Schéma de la réponse de crédit"""
    decision: Literal["APPROVED", "REJECTED"] = Field(
        ..., 
        description="Décision sur la demande de crédit"
    )
    probability: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Probabilité d'approbation (0 à 1)"
    )
    model_version: str = Field(..., description="Version du modèle utilisé")

    class Config:
        json_schema_extra = {
            "example": {
                "decision": "APPROVED",
                "probability": 0.82,
                "model_version": "credit_scoring_model_v1"
            }
        }


class ModelInfo(BaseModel):
    """Informations sur le modèle"""
    model_name: str
    algorithm: str
    version: str
    features: list[str]
    threshold: float = Field(description="Seuil de décision")

    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "Credit Scoring AutoML",
                "algorithm": "AutoML (FLAML)",
                "version": "1.0",
                "features": ["age", "income", "credit_amount", "duration"],
                "threshold": 0.5
            }
        }


class HealthResponse(BaseModel):
    """Réponse du health check"""
    status: str
    model_loaded: bool
    model_version: str
    timestamp: str
