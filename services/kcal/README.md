# Kcal Service (JARMY AI)

Service d'analyse nutritionnelle par Intelligence Artificielle.

## 🚀 Endpoints

#### `POST /analyze`
Analyse un texte en langage naturel pour extraire les données nutritionnelles.

**Authentification :** `Bearer clesecrete`

**Request Body :**
```json
{
  "text": "266g of rice and chicken and for the dessert i ate an ice cream"
}
```

**Success Response (200 OK) :**
```json
{
  "total_kcal": 850.5,
  "message": "Repas analysé avec succès",
  "items": [
    {
      "food": "rice",
      "grams": 266.0,
      "kcal": 345.8
    },
    {
      "food": "chicken",
      "grams": 150.0,
      "kcal": 247.5
    },
    {
      "food": "ice cream",
      "grams": 100.0,
      "kcal": 257.2
    }
  ]
}
```

## 🛠️ Installation & Lancement
```bash
cd services/kcal
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```
