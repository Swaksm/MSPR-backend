# MSPR-backend

Backend de l'application MSPR pour l'analyse nutritionnelle des repas avec architecture microservices.

## 🚀 Démarrage rapide

### Lancement avec Docker Compose

```bash
# Cloner le repository
git clone https://github.com/Swaksm/MSPR-backend.git
cd MSPR-backend

# Lancer les services
docker-compose up --build
```

Les services seront disponibles sur :
- **Gateway API** : http://localhost:8000
- **Service Kcal** : http://localhost:8001 (interne)
- **Documentation API** : http://localhost:8000/docs

### Arrêt des services

```bash
docker-compose down
```

## 📡 Exemples d'appels API

### Analyse d'un repas

Envoyez une requête POST au gateway pour analyser un repas :

```bash
curl -X POST "http://localhost:8000/kcal/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "266g de riz et poulet et pour le dessert j'\''ai mangé une glace et 50g de pomme"
     }'
```

**Exemple de réponse :**
```json
{
  "total_calories": 450.5,
  "items": [
    {
      "food": "riz",
      "quantity": 266,
      "unit": "g",
      "calories": 350.0
    },
    {
      "food": "poulet",
      "quantity": 100,
      "unit": "g",
      "calories": 165.0
    },
    {
      "food": "glace",
      "quantity": 1,
      "unit": "portion",
      "calories": 150.0
    },
    {
      "food": "pomme",
      "quantity": 50,
      "unit": "g",
      "calories": 25.5
    }
  ]
}
```

### Test avec Python

```python
import requests

url = "http://localhost:8000/kcal/predict"
data = {
    "text": "un steak de 200g avec des frites et une salade"
}

response = requests.post(url, json=data)
print(response.json())
```

## Description

Ce projet fournit une API REST développée avec FastAPI pour analyser les repas décrits en texte libre et calculer leur apport calorique. Il utilise un module d'intelligence artificielle basé sur spaCy pour extraire les aliments et leurs quantités du texte.

## Architecture

- **Gateway** : Service de routage FastAPI (port 8000)
- **Kcal** : Service d'analyse nutritionnelle (port 8001)

## Fonctionnalités

- Analyse de texte libre décrivant un repas
- Extraction automatique des aliments et quantités
- Calcul des calories totales
- Correction des fautes d'orthographe et synonymes
- API RESTful avec documentation interactive
- Authentification par Bearer Token
- Support CORS pour les applications frontend

## Installation locale (sans Docker)

### Prérequis

- Python 3.11+
- pip

### Étapes d'installation

1. Cloner le repository :
```bash
git clone https://github.com/Swaksm/MSPR-backend.git
cd MSPR-backend
```

2. Installer les dépendances :
```bash
pip install -r services/kcal/requirements.txt
```

3. Entraîner le modèle NLP (si nécessaire) :
```bash
cd services/kcal/ia-kcal
python nlp/train_ner.py
```

## Utilisation locale

### Démarrage du serveur

```bash
cd services/kcal
python -m uvicorn main:app --reload
```

L'API sera disponible sur http://localhost:8000/docs
```

Le serveur sera accessible sur `http://localhost:8000`

### Documentation API

Une fois le serveur démarré, accédez à la documentation interactive :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

## Authentification

L'endpoint `/analyze` est protégé par un Bearer Token à passer dans le header `Authorization` :

```
Authorization: Bearer clesecrete
```

## API Endpoints

### GET /

Retourne le statut du service. *(public)*

**Réponse :**
```json
{
  "status": "ok",
  "service": "JARMY API"
}
```

### POST /analyze

Analyse un repas décrit en texte libre. *(authentification requise)*

**Headers :**
```
Authorization: Bearer clesecrete
Content-Type: application/json
```

**Corps de la requête :**
```json
{
  "text": "266g of rice and chicken and for the dessert i ate an ice cream and 50g of apple"
}
```

**Réponse :**
```json
{
  "total_kcal": 450.5,
  "message": "Meal analyzed successfully",
  "items": [
    { "food": "rice",      "grams": 266.0, "kcal": 350.0 },
    { "food": "chicken",   "grams": 100.0, "kcal": 165.0 },
    { "food": "ice cream", "grams": 100.0, "kcal": 200.0 },
    { "food": "apple",     "grams": 50.0,  "kcal": 25.5  }
  ]
}
```

## Structure du projet

```
MSPR-backend/
├── main.py                 # Point d'entrée FastAPI
├── requirements.txt        # Dépendances Python
├── README.md               # Ce fichier
└── ia-kcal/               # Module IA d'analyse nutritionnelle
    ├── analyze.py         # Orchestration de l'analyse
    ├── app.py             # Interface CLI
    ├── data/              # Données nutritionnelles
    │   ├── kaggle_nutrition.csv
    │   ├── nutrition_data.py
    │   └── training_sentences.json
    └── nlp/               # Traitement du langage naturel
        ├── parser.py      # Parsing avec spaCy
        ├── train_ner.py   # Entraînement du modèle
        └── food_ner_model/ # Modèle spaCy entraîné
```

## Développement

### Tests

Pour exécuter les tests du module IA :
```bash
cd ia-kcal
python app.py
```

### Entraînement du modèle

Pour réentraîner le modèle NER :
```bash
cd ia-kcal/nlp
python train_ner.py
```

## Technologies utilisées

- **FastAPI** : Framework web pour l'API
- **spaCy** : Bibliothèque de traitement du langage naturel
- **Pydantic** : Validation des données
- **Uvicorn** : Serveur ASGI

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -am 'Ajout de nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## Licence

Ce projet est développé dans le cadre de la formation Concepteur Développeur d'Applications (RNCP36581 Bloc E6.1).

## Docker

### 1. Build de l'image Docker

À la racine du projet :

```powershell
cd C:\Users\swaks\Desktop\Laboratoire\MSPR-backend
docker build -t jarmy-api .
```

- `-t jarmy-api` : nom de l'image
- `.` : chemin du contexte (répertoire courant)

### 2. Lancer le conteneur

```powershell
docker run -d -p 8000:8000 --name jarmy-api jarmy-api
```

- `-d` : mode détaché (background)
- `-p 8000:8000` : mappe le port du conteneur sur le port local
- `--name jarmy-api` : nom du conteneur

### 3. Vérifier l'API

```powershell
curl http://localhost:8000/
```

Réponse attendue :

```json
{"status":"ok","service":"JARMY API"}
```

Swagger : http://localhost:8000/docs

### 4. Arrêter et supprimer le conteneur

```powershell
docker stop jarmy-api
docker rm jarmy-api
```

### 5. Remise à zéro (si conteneur existant)

```powershell
docker rm -f jarmy-api 2>$null
docker run -d -p 8000:8000 --name jarmy-api jarmy-api
```

> Note : si le projet a d'importants fichiers de données (ex: `ia-kcal/data/kaggle_nutrition.csv`), assurez-vous de ne pas les exclure de `.dockerignore`.
