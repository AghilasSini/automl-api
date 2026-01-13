"""
Application FastAPI pour le Credit Scoring
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from app.models import (
    CreditRequest, 
    CreditResponse, 
    ModelInfo, 
    HealthResponse
)
from app.predictor import predictor
from app.config import API_CONFIG

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title=API_CONFIG["title"],
    description=API_CONFIG["description"],
    version=API_CONFIG["version"],
    contact=API_CONFIG["contact"],
)


@app.on_event("startup")
async def startup_event():
    """Événement exécuté au démarrage de l'API"""
    logger.info("🚀 Démarrage de l'API Credit Scoring")
    if predictor.is_loaded():
        logger.info("✅ Modèle ML chargé avec succès")
    else:
        logger.error("❌ Échec du chargement du modèle")


@app.on_event("shutdown")
async def shutdown_event():
    """Événement exécuté à l'arrêt de l'API"""
    logger.info("🛑 Arrêt de l'API Credit Scoring")


@app.get("/", include_in_schema=False)
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "API Credit Scoring - Bienvenue",
        "documentation": "/docs",
        "openapi": "/openapi.json",
        "health": "/health"
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Vérifier l'état de l'API",
    description="Endpoint de santé pour vérifier que l'API fonctionne correctement",
    tags=["Health"]
)
async def health_check():
    """
    Vérifie l'état de santé de l'API et du modèle ML
    
    Returns:
        HealthResponse: Statut de l'API et du modèle
    """
    model_loaded = predictor.is_loaded()
    
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        model_version=predictor.model_config["version"],
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@app.post(
    "/predict",
    response_model=CreditResponse,
    status_code=status.HTTP_200_OK,
    summary="Évaluer une demande de crédit",
    description="Analyse une demande de crédit et retourne une décision APPROVED ou REJECTED",
    tags=["Prediction"],
    responses={
        200: {
            "description": "Décision de crédit retournée avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "decision": "APPROVED",
                        "probability": 0.82,
                        "model_version": "credit_scoring_model_v1"
                    }
                }
            }
        },
        400: {
            "description": "Requête invalide - données manquantes ou incorrectes"
        },
        500: {
            "description": "Erreur interne du serveur lors de la prédiction"
        }
    }
)
async def predict_credit(request: CreditRequest):
    """
    Évalue une demande de crédit et retourne une décision
    
    Args:
        request: Données de la demande de crédit
        
    Returns:
        CreditResponse: Décision (APPROVED/REJECTED) et probabilité
        
    Raises:
        HTTPException: En cas d'erreur lors de la prédiction
    """
    try:
        # Vérifier que le modèle est chargé
        if not predictor.is_loaded():
            logger.error("❌ Tentative de prédiction avec modèle non chargé")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Le modèle n'est pas disponible"
            )
        
        # Log de la requête
        logger.info(f"📥 Nouvelle demande de crédit : {request.model_dump()}")
        
        # Faire la prédiction
        decision, probability = predictor.predict(
            age=request.age,
            income=request.income,
            credit_amount=request.credit_amount,
            duration=request.duration
        )
        
        # Créer la réponse
        response = CreditResponse(
            decision=decision,
            probability=round(probability, 4),
            model_version=f"credit_scoring_model_v{predictor.model_config['version']}"
        )
        
        logger.info(f"📤 Réponse : {response.model_dump()}")
        
        return response
        
    except HTTPException:
        # Re-lever les HTTPException sans modification
        raise
        
    except ValueError as e:
        # Erreur de validation
        logger.error(f"❌ Erreur de validation : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Données invalides : {str(e)}"
        )
        
    except Exception as e:
        # Erreur inattendue
        logger.error(f"❌ Erreur lors de la prédiction : {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la prédiction : {str(e)}"
        )


@app.get(
    "/model/info",
    response_model=ModelInfo,
    summary="Informations sur le modèle AutoML",
    description="Retourne les métadonnées du modèle de credit scoring",
    tags=["Model"]
)
async def get_model_info():
    """
    Récupère les informations sur le modèle déployé
    
    Returns:
        ModelInfo: Métadonnées du modèle (nom, algorithme, version, features)
    """
    try:
        info = predictor.get_model_info()
        return ModelInfo(**info)
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des infos : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Impossible de récupérer les informations du modèle"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Gestionnaire global des exceptions non gérées"""
    logger.error(f"❌ Exception non gérée : {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Une erreur interne s'est produite",
            "type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
