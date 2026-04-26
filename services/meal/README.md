# Meal Service

Service de gestion des repas et du catalogue alimentaire.

## 🚀 Endpoints

### 🍎 Catalogue Alimentaire

#### `GET /aliments`
Liste les aliments du catalogue. Filtrable par nom.

**Query Params :** `?query=riz` (optionnel)

**Success Response (200 OK) :**
```json
[
  {
    "id": 1,
    "nom": "Riz blanc",
    "calories_100g": 130.0,
    "categorie": "Féculents",
    "source_dataset": "manual",
    "created_at": "2026-04-26T10:00:00"
  }
]
```

#### `POST /aliments`
Ajoute un nouvel aliment au catalogue mondial.

**Request Body :**
```json
{
  "nom": "Banane",
  "calories_100g": 89,
  "categorie": "Fruits",
  "proteines_g": 1.1,
  "glucides_g": 22.8,
  "lipides_g": 0.3
}
```

**Success Response (201 Created) :**
```json
{
  "id": 10,
  "nom": "Banane",
  "calories_100g": 89.0,
  "categorie": "Fruits",
  "source_dataset": "manual",
  "created_at": "2026-04-26T12:00:00"
}
```

---

### 🍽️ Gestion des Repas

#### `POST /users/{user_id}/meals`
Enregistre un nouveau repas pour un utilisateur.

**Request Body :**
```json
{
  "type_repas": "dejeuner",
  "date_repas": "2026-04-26",
  "notes": "Déjeuner équilibré",
  "items": [
    {
      "aliment_id": 1,
      "quantite_g": 150
    },
    {
      "aliment_nom": "Poulet grillé",
      "quantite_g": 100,
      "calories_100g": 165,
      "categorie": "Viandes"
    }
  ]
}
```

**Success Response (201 Created) :**
```json
{
  "id": 5,
  "utilisateur_id": 1,
  "date_repas": "2026-04-26",
  "type_repas": "dejeuner",
  "notes": "Déjeuner équilibré",
  "created_at": "2026-04-26T12:30:00",
  "total_calories": 360.0,
  "items": [
    {
      "id": 12,
      "aliment_id": 1,
      "aliment_nom": "Riz blanc",
      "quantite_g": 150.0,
      "calories_calculees": 195.0,
      "calories_100g": 130.0,
      "categorie": "Féculents",
      "source_dataset": "manual"
    },
    {
      "id": 13,
      "aliment_id": 15,
      "aliment_nom": "Poulet grillé",
      "quantite_g": 100.0,
      "calories_calculees": 165.0,
      "calories_100g": 165.0,
      "categorie": "Viandes",
      "source_dataset": "manual"
    }
  ]
}
```

#### `GET /users/{user_id}/meals`
Récupère l'historique complet des repas d'un utilisateur.

**Success Response (200 OK) :**
```json
[
  {
    "id": 5,
    "utilisateur_id": 1,
    "date_repas": "2026-04-26",
    "type_repas": "dejeuner",
    "total_calories": 360.0,
    "items": [...]
  }
]
```

#### `GET /meals/{meal_id}`
Détails d'un repas spécifique.

**Success Response (200 OK) :**
*(Identique au format de retour du POST meal)*

#### `DELETE /meals/{meal_id}`
Supprime un repas de l'historique.

**Success Response (200 OK) :**
```json
{
  "status": "deleted",
  "meal_id": 5
}
```

## 🛠️ Installation & Lancement
```bash
cd services/meal
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```
