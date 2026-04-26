# Kcal Service (JARMY API)

Service d'analyse nutritionnelle automatique basé sur l'IA pour HealthAI.

## 🚀 Endpoints

- `POST /analyze` : Analyse un texte descriptif pour en extraire les aliments, les quantités et les calories.
  - **Auth Required** : Bearer Token (`clesecrete`)
  - Body : `{ "text": "200g of chicken and 100g of rice" }`
  - Retourne : `{ "total_kcal": 450, "items": [...] }`

## 🛠️ Installation & Lancement

```bash
cd services/kcal
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## 📝 Exemple d'appel

```bash
curl -X POST http://localhost:8001/analyze \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer clesecrete" \
     -d '{"text": "266g of rice and chicken and for the dessert i ate an ice cream"}'
```
