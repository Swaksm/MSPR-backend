# ETL Service

Service de pipeline ETL (Extract, Transform, Load) pour charger et traiter les données nutritionnelles et sportives de HealthAI.

## 🚀 Endpoints

- `POST /etl/run` : Déclenche l'exécution du pipeline ETL en arrière-plan.
- `GET /health` : Vérifie l'état du service.

## 🛠️ Installation & Lancement

### Docker (Recommandé)
```bash
docker-compose up etl
```

### Manuel
```bash
cd services/etl
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

## 📊 Pipeline ETL
Le pipeline traite les sources suivantes :
- **CSV Kaggle** : Aliments, Exercices, Profils utilisateurs.
- **Base de données** : Nettoyage et insertion dans PostgreSQL `healthai`.

## 📂 Structure
- `data/` : Contient les fichiers sources (CSV, JSON).
- `etl_pipeline.py` : Logique principale du traitement de données.
- `healthai_schema.sql` : Schéma de la base de données.
