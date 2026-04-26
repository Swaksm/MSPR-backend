# Meal Service

Service de gestion des repas et du catalogue alimentaire pour HealthAI.

## 🚀 Endpoints

### 🍎 Catalogue Alimentaire
- `GET /aliments` : Liste les aliments (filtre `?query=...` disponible).
- `POST /aliments` : Ajoute un nouvel aliment au catalogue.

### 🍽️ Gestion des Repas
- `GET /users/{user_id}/meals` : Liste tous les repas d'un utilisateur.
- `POST /users/{user_id}/meals` : Ajoute un repas (avec plusieurs lignes d'aliments).
- `GET /meals/{meal_id}` : Récupère le détail d'un repas.
- `DELETE /meals/{meal_id}` : Supprime un repas.

## 🛠️ Installation & Lancement

```bash
cd services/meal
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

## 📝 Exemples d'appels

### Ajouter un repas
```bash
curl -X POST http://localhost:8003/users/1/meals \
     -H "Content-Type: application/json" \
     -d '{
       "type_repas": "dejeuner",
       "date_repas": "2026-04-08",
       "notes": "Salade de poulet",
       "items": [
         { "aliment_nom": "poulet", "quantite_g": 150, "calories_100g": 165 },
         { "aliment_id": 42, "quantite_g": 100 }
       ]
     }'
```

### Rechercher un aliment
```bash
curl -X GET "http://localhost:8003/aliments?query=riz"
```
