I'll fetch the repository information for you.Here is the information about the repository https://github.com/AghilasSini/automl-api:

**Repository Name:** automl-api

**Author:** Aghilas SINI

**Description:** API comme cadre aplicatif du DevOps (API as DevOps application framework)

**Purpose:** This is a REST API for automatic credit scoring evaluation based on an AutoML model.

**Main Features:**
- Real-time credit application evaluation
- REST API conforming to OpenAPI 3.0 standards
- Input data validation using Pydantic
- Robust error handling
- Docker containerization
- Unit and integration tests
- Interactive documentation with Swagger UI

**Architecture:**
The project contains several key directories:
- app/ - FastAPI application with main.py, models.py, predictor.py, and config.py
- models/ - Contains the credit scoring machine learning model
- tests/ - pytest test files
- data/ - Data directory
- docs/ - Documentation
- postman/ - Postman collection
- .github/workflows/ - GitHub Actions CI/CD workflows

**Key Files:**
- Dockerfile and docker-compose.yml for containerization
- requirements.txt for Python dependencies
- openapi.yaml for API specification
- api_egs.py and api_curl_egs.sh for usage examples

**Installation:**
The repository provides multiple ways to run the API:
1. Local installation with Python virtual environment
2. Docker build and run
3. Docker Compose deployment

**Technology Stack:**
- FastAPI for the REST API framework
- Pydantic for data validation
- Docker for containerization
- pytest for testing
- Machine learning model for credit scoring predictions

**API Endpoints:**
The API evaluates credit applications and returns a decision (APPROVED/REJECTED) with an approval probability.

**Documentation:**
- Swagger UI available at http://localhost:8000/docs
- ReDoc at http://localhost:8000/redoc
- OpenAPI JSON at http://localhost:8000/openapi.json

**Stats:**
- 1 star
- 0 forks
- Languages: Python 94.7%, Dockerfile 4.3%, Shell 1.0%

**License:** CeCILL 2.1

**Contact:** aghilas.sini@univ-lemans.fr, Universite du Mans - Master 1 IA
