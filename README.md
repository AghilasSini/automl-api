
# API Credit Scoring - TD3 DevOps

API REST pour l'évaluation automatique de demandes de crédit, basée sur un modèle AutoML.

##  Description

Cette API permet d'évaluer des demandes de crédit en temps réel en utilisant un modèle de machine learning. Elle retourne une décision (APPROVED/REJECTED) accompagnée d'une probabilité d'approbation.

##  Fonctionnalités

- Évaluation de demandes de crédit en temps réel
- API REST conforme aux standards OpenAPI 3.0
- Validation des données entrantes (Pydantic)
- Gestion d'erreurs robuste
- Conteneurisation Docker
- Tests unitaires et d'intégration
- Documentation interactive (Swagger UI)

##  Architecture
````bash
automl-api/
├── app/
│   ├── main.py          # Application FastAPI
│   ├── models.py        # Schémas Pydantic
│   ├── predictor.py     # Logique ML
│   └── config.py        # Configuration
├── models/
│   └── credit_scoring_model.pkl
├── tests/
│   └── test_api.py      # Tests pytest
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── openapi.yaml         # Spécification API
```

## Installation

# Cloner le dépôt
git clone https://github.com/AghilasSini/automl-api.git
cd automl-api

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt

# Générer le modèle (première fois)
python models/train_model.py



## Utilisation
### Lancement local
```bash
	# Démarrer l'API
	uvicorn app.main:app --reload
```


### Lancement avec Docker

Vous devez installer docker (ou  [docker-desktop](https://docs.docker.com/desktop/setup/install/linux/ubuntu/)). 


```bash
	# Construire l'image
	docker build -t credit-scoring-api .

	# Lancer le conteneur
	docker run -p 8000:8000 credit-scoring-api

	# OU utiliser docker-compose
	docker-compose up
```

### Accéder à la documentation
Une fois l'API lancée :

Swagger UI : http://localhost:8000/docs
ReDoc : http://localhost:8000/redoc
OpenAPI JSON : http://localhost:8000/openapi.json





### Tests
Exécuter les tests unitaires
```bash

# Lancer tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=app --cov-report=html

```



## Docker deuxième approche

```bash
# Build
docker build -t credit-scoring-api:v1.0 .

# Run
docker run -d -p 8000:8000 --name credit-api credit-scoring-api:v1.0

# Logs
docker logs credit-api

# Stop
docker stop credit-api

# Remove
docker rm credit-api
```


## Configuration

Modifier `app/config.py` pour ajuster :

- Chemin du modèle
- Seuil de décision
- Paramètres de l'API

## Bonnes pratiques appliquées
	**API-first design** : Spécification OpenAPI avant implémentation  
	**Validation des données** : Schémas Pydantic stricts  
 	**Gestion d'erreurs** : Codes HTTP appropriés et messages clairs  
	**Logging** : Traçabilité des requêtes  
   	**Tests** : Couverture unitaire et d'intégration  
	**Conteneurisation** : Docker multi-stage optimisé  
	**Documentation** : README, docstrings, Swagger  
	**Sécurité** : Utilisateur non-root dans Docker  

## Contribution

Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

CeCILL 2.1 - Voir [LICENSE](https://cecill.info/licences/Licence_CeCILL_V2.1-en.html)

## Auteur

**Aghilas SINI**  
aghilas.sini@univ-lemans.fr  
Université du Mans - Master 1 IA

## Support

En cas de problème :

1. Consulter la documentation Swagger : http://localhost:8000/docs
2. Vérifier les logs : `docker logs credit-api`
3. Ouvrir une issue sur GitHub


