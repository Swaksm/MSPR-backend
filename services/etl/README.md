# 🔄 JARMY - ETL Service

Le service **ETL** (Extract, Transform, Load) est le moteur de données de JARMY. Il est chargé d'alimenter la base de données avec des datasets externes de haute qualité et de maintenir la cohérence du référentiel.

## 🚀 Fonctionnalités
- Importation de datasets **Kaggle** (Nutrition, Gym, Fitness Tracker).
- Nettoyage et transformation des données (normalisation des unités).
- Déduplication des entrées.
- Planification automatique (APScheduler).
- Journalisation détaillée des exécutions (`etl_run_log`).

## 🛠️ Endpoints Principaux

| Méthode | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Statut du service. |
| `POST` | `/etl/run` | Déclencher manuellement le pipeline (Background Task). |

## 🏗️ Pipeline de Données
Le pipeline s'exécute en 4 étapes :
1. **Extraction** : Lecture des fichiers CSV dans `data/`.
2. **Transformation** : Filtrage des colonnes inutiles, conversion des types, calculs nutritionnels.
3. **Chargement** : Insertion massive (Bulk Insert) dans PostgreSQL.
4. **Log** : Enregistrement du statut (`SUCCESS` ou `ERROR`) et du nombre de lignes traitées.

## ⚙️ Schedulers
Par défaut, l'ETL est configuré pour se lancer tous les jours à minuit (`cron: hour=0, minute=0`). Cette configuration est modifiable dans `main.py`.

## 🔒 Sécurité
Comme le service Kcal, les opérations critiques requièrent un Bearer Token : `clesecrete`.
