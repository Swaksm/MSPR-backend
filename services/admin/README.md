# 📊 JARMY - Admin Service

Le service **Admin** est le module de supervision de la plateforme. Il permet aux administrateurs de piloter les données, de surveiller la qualité et de visualiser les analytics business.

## 🚀 Fonctionnalités
- Dashboard de **Qualité de Donnée** (Score sur 100).
- Gestion CRUD (Utilisateurs, Aliments, Exercices).
- Déclenchement manuel du pipeline ETL.
- Export complet de la base de données au format JSON.
- Visualisation des Jobs ETL passés.

## 🛠️ Endpoints Principaux

### Gestion des données (CRUD)
| Méthode | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/users` | Liste paginée des utilisateurs. |
| `PUT` | `/users/{id}` | Mise à jour forcée d'un profil. |
| `DELETE` | `/users/{id}` | Suppression définitive d'un compte. |
| `GET` | `/foods` | Liste complète du catalogue alimentaire. |

### Qualité & Système
| Méthode | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/data-quality` | Rapport d'anomalies et score qualité. |
| `POST` | `/etl/run` | Lancer une synchronisation ETL (Datasets). |
| `GET` | `/export` | Télécharger un dump JSON de la base. |
| `PUT` | `/data/correct` | Corriger une valeur précise en base. |

### Analytics
| Méthode | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/analytics/users` | Répartition par sexe et historique inscriptions. |
| `GET` | `/analytics/nutrition` | Tendances de consommation (kcal moyen). |
| `GET` | `/analytics/fitness` | Top exercices pratiqués. |

## 📝 Exemples de Payload

### Correction manuelle
`PUT /data/correct`
```json
{
  "table_name": "utilisateur",
  "id": 12,
  "column_name": "poids_initial_kg",
  "new_value": 82.5
}
```

## 📈 Score de Qualité
Le score est calculé dynamiquement en fonction :
- Du nombre d'utilisateurs sans objectifs caloriques.
- Des poids irréalistes enregistrés.
- Des aliments avec 0 calories dans le catalogue.
