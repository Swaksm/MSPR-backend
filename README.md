# HealthAI Backend - Microservices

Backend de l'application HealthAI pour l'analyse nutritionnelle et le suivi sportif, basé sur une architecture microservices FastAPI.

---

## 🏗️ Architecture des Services

Le projet est découpé en plusieurs services spécialisés :

| Service | Port | Description |
| :--- | :--- | :--- |
| **[Gateway](./services/gateway)** | 8000 | Proxy unique pour le frontend. |
| **[Auth](./services/auth)** | 8004 | Gestion des utilisateurs et authentification. |
| **[Meal](./services/meal)** | 8003 | Gestion du catalogue alimentaire et des repas. |
| **[Kcal](./services/kcal)** | 8001 | IA d'analyse nutritionnelle (Natural Language). |
| **[ETL](./services/etl)** | 8002 | Pipeline d'importation de données. |

---

## 🚀 Démarrage Rapide

Le moyen le plus simple de lancer tout l'écosystème est d'utiliser Docker Compose.

```bash
docker-compose up --build
```

### Accès aux documentations (Swagger)
Chaque service expose sa propre documentation interactive :
- **Auth** : [http://localhost:8004/docs](http://localhost:8004/docs)
- **Meal** : [http://localhost:8003/docs](http://localhost:8003/docs)
- **Kcal** : [http://localhost:8001/docs](http://localhost:8001/docs)
- **Gateway** : [http://localhost:8000/docs](http://localhost:8000/docs) (routes proxifiées uniquement)

---

## 🔗 Flux de Données Principal

1. **Authentification** : Le frontend appelle le Gateway `/auth/login`.
2. **Saisie de Repas** :
   - L'utilisateur envoie une phrase au Gateway `/kcal/predict`.
   - L'IA retourne une liste d'aliments et calories.
   - Le frontend valide et enregistre via le Gateway `/meal/users/{id}/meals`.
3. **Administration** : Les données sont stockées dans PostgreSQL et visualisables via **Adminer** sur [http://localhost:8080](http://localhost:8080).

---

## 🛠️ Base de données (PostgreSQL)

- **Serveur** : `db` (localhost:5432)
- **Base** : `healthai`
- **Utilisateur/MDP** : `postgres` / `postgres`

---

## 🏷️ Licence
Projet MSPR - Formation Concepteur Développeur d'Applications.
