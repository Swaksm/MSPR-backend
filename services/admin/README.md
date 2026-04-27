# Admin Service (Management & Analytics)

Ce microservice gère les fonctions avancées de JARMY : administration des utilisateurs, contrôle qualité des données, exécution du pipeline ETL et fourniture de métriques analytiques.

## 🚀 Fonctionnalités
*   **CRUD Admin :** Gestion complète des utilisateurs, aliments et exercices.
*   **Contrôle Qualité :** Détection et correction interactive des anomalies (objectifs manquants, poids invalides).
*   **Orchestration ETL :** Déclenchement manuel ou planifié (via `apscheduler`) du pipeline de données.
*   **Analytics :** Endpoints dédiés pour les graphiques (démographie, nutrition, fitness).
*   **Export :** Génération de dumps JSON complets de la base de données.

## 🛠️ Installation
Le service utilise FastAPI et communique avec la base PostgreSQL partagée.
```bash
cd services/admin
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8006
```

## 📡 Endpoints Principaux

### Gestion
*   `GET /users` : Liste complète des utilisateurs avec métriques.
*   `PUT /users/{id}` : Mise à jour administrative d'un compte.
*   `DELETE /users/{id}` : Suppression sécurisée (cascade).

### Qualité & ETL
*   `GET /data-quality` : Analyse des anomalies et historique des jobs.
*   `POST /etl/run` : Lance un nouveau run du pipeline de données.
*   `PUT /data/correct` : Corrige une valeur spécifique dans une table (Correction interactive).
*   `GET /export` : Télécharge un export JSON.

### Analytics
*   `GET /analytics/users` : Inscriptions dans le temps et répartition par genre.
*   `GET /analytics/nutrition` : Volume de repas et moyennes caloriques.
*   `GET /analytics/fitness` : Exercices les plus populaires.

## 🗄️ Base de données
Utilise les vues SQL définies dans le schéma global :
*   `vue_kpis_business`
*   `vue_stats_activite`
*   `etl_run_log` (pour l'historique)
