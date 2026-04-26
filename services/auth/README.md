# Auth Service

Service d'authentification et de gestion des profils utilisateurs pour HealthAI.

## 🚀 Endpoints

### 🔐 Authentification
- `POST /login` : Authentifie un utilisateur.
  - Body : `{ "email": "...", "password": "..." }`
  - Retourne : `{ "success": true, "user_id": 1, ... }`

### 👤 Gestion Utilisateurs
- `GET /users` : Liste tous les utilisateurs.
- `GET /users/{user_id}` : Récupère les détails d'un utilisateur.
- `POST /users` : Crée un nouvel utilisateur.
- `PUT /users/{user_id}/goal` : Met à jour l'objectif calorique.
- `DELETE /users/{user_id}` : Supprime un utilisateur et ses données liées.

## 🛠️ Installation & Lancement

```bash
cd services/auth
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8004 --reload
```

## 📝 Exemples d'appels

### Connexion
```bash
curl -X POST http://localhost:8004/login \
     -H "Content-Type: application/json" \
     -d '{"email": "jean.dupont@example.com", "password": "secret123"}'
```

### Création d'utilisateur
```bash
curl -X POST http://localhost:8004/users \
     -H "Content-Type: application/json" \
     -d '{
       "nom": "Dupont",
       "prenom": "Jean",
       "email": "jean.dupont@example.com",
       "password": "secret123",
       "sexe": "homme",
       "kcal_objectif": 2500
     }'
```
