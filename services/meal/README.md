# 🍽️ JARMY - Meal Service

Le service **Meal** gère l'inventaire des aliments et le journal alimentaire des utilisateurs. C'est ici que sont stockées toutes les informations nutritionnelles et l'historique des repas.

## 🚀 Fonctionnalités
- Catalogue nutritionnel complet (Calories, Protéines, Glucides, Lipides).
- Recherche d'aliments par mot-clé.
- Enregistrement de repas multi-lignes.
- Historique des repas par utilisateur.

## 🛠️ Endpoints Principaux

### Catalogue Alimentaire
| Méthode | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/aliments` | Rechercher des aliments (query params). |
| `POST` | `/aliments` | Ajouter un nouvel aliment au catalogue. |

### Journal Alimentaire
| Méthode | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/users/{id}/meals` | Historique complet des repas d'un utilisateur. |
| `POST` | `/users/{id}/meals` | Enregistrer un nouveau repas (plusieurs items). |
| `GET` | `/meals/{id}` | Détails d'un repas spécifique. |
| `DELETE` | `/meals/{id}` | Supprimer un repas. |

## 📝 Exemples de Payload

### Enregistrer un repas (Petit-déjeuner)
```json
{
  "type_repas": "petit_dejeuner",
  "date_repas": "2026-04-28",
  "notes": "Très bon petit-déjeuner",
  "items": [
    {
      "aliment_id": 42,
      "quantite_g": 200
    },
    {
      "aliment_nom": "Banane",
      "quantite_g": 120,
      "calories_100g": 89,
      "categorie": "Fruits"
    }
  ]
}
```

## 🧠 Intelligence de Résolution
Le service possède une logique de résolution d'aliments :
1. Si un `aliment_id` est fourni, il l'utilise.
2. Sinon, il cherche par `aliment_nom` dans la base.
3. Si rien n'est trouvé, il crée automatiquement un nouvel aliment avec les infos fournies.
