# ⚡ JARMY - Gateway Service

La **Gateway** est le point de contact unique entre le Frontend (Next.js) et la constellation de microservices JARMY. Elle simplifie la communication en centralisant les URLs et en gérant les problématiques transversales.

## 🚀 Fonctionnalités
- **Routage Intelligent** : Redirige les requêtes vers le bon microservice en fonction du préfixe d'URL.
- **Abstraction** : Le frontend ne connaît qu'une seule URL (Port 8000).
- **CORS Centralisé** : Autorise les requêtes provenant de n'importe quelle origine (configuré pour le développement).
- **Proxy d'Analyse IA** : Simplifie l'accès au service Kcal.

## 🛠️ Routage (Mapping)

| Préfixe | Service Cible | Description |
| :--- | :--- | :--- |
| `/auth/*` | `http://auth:8004/*` | Authentification & Profils. |
| `/meal/*` | `http://meal:8003/*` | Repas & Aliments. |
| `/admin/*` | `http://admin:8006/*` | Administration & Stats. |
| `/kcal/predict` | `http://kcal:8001/analyze` | Analyse NLP. |

## ⚙️ Configuration
La Gateway utilise les variables d'environnement pour localiser les services internes dans le réseau Docker :
- `AUTH_SERVICE_URL`
- `MEAL_SERVICE_URL`
- `KCAL_SERVICE_URL`
- `ADMIN_SERVICE_URL`

## 📝 Exemple d'Utilisation Frontend
Au lieu d'appeler plusieurs serveurs, le frontend utilise une base commune :
`GET http://localhost:8000/auth/users/1` -> Proxy vers Auth Service.
`POST http://localhost:8000/meal/aliments` -> Proxy vers Meal Service.
