import requests

# Prédiction
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "age": 35,
        "income": 3200,
        "credit_amount": 15000,
        "duration": 48
    }
)

result = response.json()
print(f"Décision: {result['decision']}")
print(f"Probabilité: {result['probability']}")
