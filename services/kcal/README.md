# 🧠 JARMY - Kcal IA Service

Le service **Kcal** est le moteur d'intelligence artificielle de JARMY. Il utilise le traitement du langage naturel (NLP) pour transformer une simple phrase en données structurées (aliments, poids, calories).

## 🚀 Fonctionnalités
- Extraction d'entités nommées (NER) avec **SpaCy**.
- Détection automatique des quantités et unités (g, ml, kg, oz, etc.).
- Calcul instantané des calories basées sur une base de données embarquée.
- Reconnaissance des synonymes et corrections orthographiques légères.

## 🛠️ Endpoints Principaux

| Méthode | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check et statut du service. |
| `POST` | `/analyze` | Analyser un texte et retourner les kcal. |

## 📝 Exemples de Requêtes

### Analyser un repas
`POST /analyze`
```json
{
  "text": "J'ai mangé 200g de poulet, du riz blanc et une pomme"
}
```

**Réponse (exemple) :**
```json
{
  "total_kcal": 542.0,
  "message": "Ce repas contient environ 542 kcal.",
  "items": [
    { "food": "roast chicken", "grams": 200.0, "kcal": 330.0 },
    { "food": "rice", "grams": 180.0, "kcal": 158.0 },
    { "food": "apple", "grams": 150.0, "kcal": 54.0 }
  ]
}
```

## 🏗️ Architecture IA
Le dossier `ia-kcal` contient le moteur :
- `nlp/` : Modèles SpaCy entraînés et scripts d'entraînement.
- `data/` : Dictionnaires nutritionnels de référence.
- `analyze.py` : Logique de haut niveau pour l'agrégation des résultats.

## 🔒 Sécurité
L'accès à l'API requiert un Bearer Token : `clesecrete` (configurable dans `main.py`).
