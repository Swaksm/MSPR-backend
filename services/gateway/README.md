# Gateway Service

Proxy centralisant les appels API pour les différents microservices de HealthAI.

## 🚀 Routes Exposées (Port 8000)

Le gateway redirige les appels vers les services internes :

- `/auth/*` ➔ **Auth Service** (Port 8004)
- `/meal/*` ➔ **Meal Service** (Port 8003)
- `/kcal/predict` ➔ **Kcal Service** `/analyze` (Port 8001)

## 🛠️ Installation & Lancement

```bash
cd services/gateway
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📝 Exemples d'appels via le Gateway

### Connexion
`POST http://localhost:8000/auth/login`

### Ajout de repas
`POST http://localhost:8000/meal/users/1/meals`

### Analyse Kcal
`POST http://localhost:8000/kcal/predict`
