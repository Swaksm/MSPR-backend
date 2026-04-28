# 🛡️ JARMY - Auth Service

Le service **Auth** est responsable de la gestion des utilisateurs, de la sécurité et des profils. Il assure l'authentification classique (email/password) et l'intégration SSO avec Google.

## 🚀 Fonctionnalités
- Inscription et Connexion.
- Intégration **Google OAuth2** (Vérification des ID Tokens).
- Gestion des profils (Objectifs caloriques, Poids, Taille).
- Gestion des abonnements (Freemium, Premium, Premium Plus).
- Statistiques globales pour l'administration.

## 🛠️ Endpoints Principaux

### Authentification
| Méthode | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/login` | Connexion classique. |
| `POST` | `/google-login` | Connexion via Google SSO. |
| `POST` | `/users` | Création de compte. |

### Profil & Paramètres
| Méthode | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/users/{id}` | Récupérer les infos d'un utilisateur. |
| `PUT` | `/users/{id}/goal` | Mettre à jour l'objectif kcal. |
| `PUT` | `/users/{id}/subscription` | Modifier l'abonnement (Admin). |

### Administration & Stats
| Méthode | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/stats/global` | KPI globaux (conversions, totaux). |
| `GET` | `/users` | Liste complète des utilisateurs. |

## 📝 Exemples de Payload

### Login Google
```json
{
  "token": "eyJhbGciOiJSUzI1NiIs..."
}
```

### Création d'utilisateur
```json
{
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean.dupont@example.com",
  "password": "secret_password",
  "sexe": "homme",
  "poids_initial_kg": 75.5,
  "taille_cm": 180
}
```

## ⚙️ Configuration
Le service utilise les variables d'environnement suivantes (définies dans `docker-compose.yml`) :
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- `GOOGLE_CLIENT_ID` (Optionnel pour validation stricte)
