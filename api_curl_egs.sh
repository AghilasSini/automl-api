# Health check
curl http://localhost:8000/health

# Prédiction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "income": 3200,
    "credit_amount": 15000,
    "duration": 48
  }'

# Model info
curl http://localhost:8000/model/info
