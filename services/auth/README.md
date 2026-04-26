# Auth Service

Service de gestion des utilisateurs et d'authentification.

## 🚀 Endpoints

### 🔐 Authentification

#### `POST /login`
Authentifie un utilisateur et retourne ses informations de profil.

**Request Body :**
```json
{
  "email": "jean.dupont@example.com",
  "password": "secret123"
}
```

**Success Response (200 OK) :**
```json
{
  "success": true,
  "message": "Authentification réussie.",
  "user_id": 1,
  "email": "jean.dupont@example.com",
  "prenom": "Jean",
  "nom": "Dupont"
}
```

---

### 👤 Gestion Utilisateurs

#### `GET /users`
Liste tous les utilisateurs enregistrés.

**Success Response (200 OK) :**
```json
[
  {
    "id": 1,
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean.dupont@example.com",
    "sexe": "homme",
    "abonnement": "freemium",
    "date_inscription": "2026-04-25T23:10:35",
    "actif": true,
    "date_naissance": "1990-01-01",
    "poids_initial_kg": 75.5,
    "taille_cm": 180,
    "kcal_objectif": 2200
  }
]
```

#### `GET /users/{user_id}`
Récupère les détails d'un utilisateur spécifique.

**Success Response (200 OK) :**
*(Identique à un objet de la liste ci-dessus)*

#### `POST /users`
Crée un nouveau compte utilisateur.

**Request Body :**
```json
{
  "nom": "Martin",
  "prenom": "Sophie",
  "email": "sophie.martin@example.com",
  "password": "password123",
  "date_naissance": "1995-06-15",
  "sexe": "femme",
  "poids_initial_kg": 62.0,
  "taille_cm": 165,
  "abonnement": "freemium",
  "kcal_objectif": 1800
}
```

**Success Response (201 Created) :**
```json
{
  "id": 2,
  "nom": "Martin",
  "prenom": "Sophie",
  "email": "sophie.martin@example.com",
  "sexe": "femme",
  "abonnement": "freemium",
  "date_inscription": "2026-04-26T12:00:00",
  "actif": true,
  "date_naissance": "1995-06-15",
  "poids_initial_kg": 62.0,
  "taille_cm": 165,
  "kcal_objectif": 1800
}
```

#### `PUT /users/{user_id}/goal`
Met à jour l'objectif calorique quotidien.

**Request Body :**
```json
{
  "kcal_objectif": 2500
}
```

**Success Response (200 OK) :**
```json
{
  "status": "updated",
  "kcal_objectif": 2500
}
```

#### `DELETE /users/{user_id}`
Supprime un utilisateur et toutes ses données associées (repas, etc.).

**Success Response (200 OK) :**
```json
{
  "status": "deleted",
  "user_id": 1
}
```

## 🛠️ Installation & Lancement
```bash
cd services/auth
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8004 --reload
```
