# Activity Logs Service (MongoDB)

Microservice de journalisation des activites utilisateur pour la plateforme JARMY.

## Pourquoi MongoDB ?

Le projet JARMY utilise PostgreSQL pour les donnees relationnelles (utilisateurs, repas, aliments). Le service Activity Logs introduit **MongoDB** pour une raison technique precise : les logs d'activite ont une **structure variable** (schema flexible) et un **volume eleve** en ecriture.

| Critere               | PostgreSQL (existant)         | MongoDB (ce service)             |
|------------------------|-------------------------------|----------------------------------|
| Schema                 | Fixe, migrations requises     | Flexible, pas de migrations      |
| Type de donnee         | Relationnelle (FK, JOINs)     | Document JSON imbrique           |
| Cas d'usage            | Utilisateurs, repas, aliments | Logs, evenements, audit trail    |
| Volume d'ecriture      | Modere                        | Eleve (chaque action = 1 log)    |
| Requetes principales   | JOINs complexes               | Filtrage + Aggregation pipeline  |

## Endpoints

| Methode | Route         | Description                                |
|---------|---------------|--------------------------------------------|
| GET     | /health       | Verification de la connexion MongoDB       |
| POST    | /logs         | Creer un log d'activite                    |
| GET     | /logs         | Lister les logs (filtres: user_id, action) |
| GET     | /logs/stats   | Statistiques d'actions par type            |

## Exemple de document MongoDB

```json
{
  "_id": "ObjectId(...)",
  "user_id": 42,
  "action": "add_meal",
  "detail": {
    "meal_name": "Dejeuner",
    "calories": 650,
    "items": ["poulet", "riz", "salade"]
  },
  "timestamp": "2026-04-29T14:30:00Z"
}
```

Le champ `detail` est un objet JSON libre : chaque type d'action peut stocker des informations differentes sans modifier le schema. C'est exactement le type de flexibilite que MongoDB apporte par rapport a PostgreSQL.

## Technologies

- **FastAPI** : coherent avec le reste du projet JARMY
- **Motor** : driver MongoDB asynchrone pour Python
- **MongoDB 7** : base de donnees NoSQL orientee documents

## Lancement

Le service demarre automatiquement via Docker Compose avec le reste du projet.

Port : **8005**
