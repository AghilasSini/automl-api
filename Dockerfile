# ======================================
# Dockerfile pour API Credit Scoring
# ======================================

# Étape 1 : Image de base Python slim (légère)
FROM python:3.9-slim

# Étape 2 : Définir le mainteneur
LABEL maintainer="aghilas.sini@univ-lemans.fr"
LABEL description="API Credit Scoring - TD DevOps"

# Étape 3 : Définir le répertoire de travail
WORKDIR /app

# Étape 4 : Copier uniquement requirements.txt d'abord (optimisation du cache)
COPY requirements.txt .

# Étape 5 : Installer les dépendances Python
# --no-cache-dir évite de garder le cache pip (réduit la taille)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Étape 6 : Copier tout le code de l'application
COPY . .

# Étape 7 : Créer un utilisateur non-root (sécurité)
RUN useradd -m -u 1000 apiuser && \
    chown -R apiuser:apiuser /app

# Étape 8 : Passer à l'utilisateur non-root
USER apiuser

# Étape 9 : Exposer le port 8000
EXPOSE 8000

# Étape 10 : Healthcheck Docker
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Étape 11 : Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

