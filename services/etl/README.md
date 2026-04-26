# ETL Service

Service de pipeline ETL (Extract, Transform, Load) pour le chargement des données.

## 🚀 Endpoints

#### `POST /etl/run`
Déclenche le pipeline de traitement des données en arrière-plan.

**Success Response (202 Accepted) :**
```json
{
  "status": "started",
  "message": "ETL pipeline has been started in the background. Check logs for progress."
}
```

#### `GET /health`
Vérifie la santé du service.

**Success Response (200 OK) :**
```json
{
  "status": "ok",
  "service": "healthai_etl"
}
```

## 🛠️ Installation & Lancement
```bash
cd services/etl
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```
