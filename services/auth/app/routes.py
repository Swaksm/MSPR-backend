from datetime import date, datetime
from hashlib import sha256
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, HTTPException

from database import fetch_one, fetch_all, execute_write

router = APIRouter()


def hash_password(raw_password: str) -> str:
    return sha256(raw_password.encode("utf-8")).hexdigest()


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="premium@gmail.com", description="L'adresse email de l'utilisateur")
    password: str = Field(..., min_length=6, example="premium@gmail.com", description="Le mot de passe de l'utilisateur")

class LoginResponse(BaseModel):
    success: bool = Field(..., description="Indique si l'authentification a réussi")
    message: str = Field(..., description="Message d'information sur le résultat")
    user_id: int | None = Field(None, description="ID unique de l'utilisateur")
    email: EmailStr | None = Field(None, description="Email de l'utilisateur connecté")
    prenom: str | None = Field(None, description="Prénom de l'utilisateur")
    nom: str | None = Field(None, description="Nom de famille de l'utilisateur")

class UserCreate(BaseModel):
    nom: str = Field(..., min_length=2, description="Nom de famille")
    prenom: str = Field(..., min_length=2, description="Prénom")
    email: EmailStr = Field(..., description="Adresse email unique")
    password: str = Field(..., min_length=6, description="Mot de passe (sera haché)")
    date_naissance: Optional[date] = Field(None, description="Date de naissance (YYYY-MM-DD)")
    sexe: Optional[str] = Field("non_renseigne", description="Sexe (homme, femme, autre, non_renseigne)")
    poids_initial_kg: Optional[float] = Field(None, gt=0, description="Poids au moment de l'inscription")
    taille_cm: Optional[int] = Field(None, ge=50, le=300, description="Taille en centimètres")
    abonnement: Optional[str] = Field("freemium", description="Type d'abonnement (freemium, premium, premium_plus)")
    kcal_objectif: Optional[int] = Field(2000, description="Objectif calorique quotidien")

class UserResponse(BaseModel):
    id: int = Field(..., description="Identifiant unique")
    nom: str = Field(..., description="Nom de famille")
    prenom: str = Field(..., description="Prénom")
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    sexe: str = Field(..., description="Sexe enregistré")
    abonnement: str = Field(..., description="Statut de l'abonnement actuel")
    date_inscription: datetime = Field(..., description="Date et heure de création du compte")
    actif: bool = Field(..., description="Statut du compte (actif ou non)")
    date_naissance: Optional[date] = None
    poids_initial_kg: Optional[float] = None
    taille_cm: Optional[int] = None
    kcal_objectif: int = Field(..., description="Objectif calorique personnalisé")

class GoalUpdateRequest(BaseModel):
    kcal_objectif: int = Field(..., ge=500, le=10000, description="Nouvel objectif en kcal")

class SubscriptionUpdateRequest(BaseModel):
    abonnement: str = Field(..., description="Nouveau statut (freemium, premium, premium_plus)")

@router.post("/login", response_model=LoginResponse, summary="Authentification utilisateur", description="Vérifie les identifiants et retourne les informations de l'utilisateur.")
def login(payload: LoginRequest):
    # ... (code existant)
    user = fetch_one(
        "SELECT id, email, mdp_hash, actif, prenom, nom FROM utilisateur WHERE email = :email",
        {"email": payload.email},
    )
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")

    if not user["actif"]:
        raise HTTPException(status_code=403, detail="Utilisateur inactif.")

    if user["mdp_hash"] != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")

    return LoginResponse(
        success=True,
        message="Authentification réussie.",
        user_id=user["id"],
        email=user["email"],
        prenom=user["prenom"],
        nom=user["nom"],
    )


@router.get("/users", response_model=list[UserResponse], summary="Liste des utilisateurs", tags=["Gestion Utilisateurs"])
def list_users():
    """Retourne la liste complète de tous les utilisateurs enregistrés."""
    users = fetch_all("SELECT id, nom, prenom, email, sexe, abonnement, date_inscription, actif, date_naissance, poids_initial_kg, taille_cm, kcal_objectif FROM utilisateur ORDER BY id")
    return [UserResponse(**u) for u in users]


@router.get("/users/{user_id}", response_model=UserResponse, summary="Détails d'un utilisateur", tags=["Gestion Utilisateurs"])
def get_user(user_id: int):
    """Récupère les informations détaillées d'un utilisateur spécifique par son ID."""
    user = fetch_one(
        "SELECT id, nom, prenom, email, sexe, abonnement, date_inscription, actif, date_naissance, poids_initial_kg, taille_cm, kcal_objectif FROM utilisateur WHERE id = :user_id",
        {"user_id": user_id},
    )
    if not user:
        raise HTTPException(404, "Utilisateur introuvable")
    return UserResponse(**user)


@router.put("/users/{user_id}/goal", summary="Mise à jour de l'objectif", tags=["Profil & Objectifs"])
def update_user_goal(user_id: int, payload: GoalUpdateRequest):
    """Met à jour l'objectif calorique quotidien d'un utilisateur."""
    user = fetch_one("SELECT id FROM utilisateur WHERE id = :user_id", {"user_id": user_id})
    if not user:
        raise HTTPException(404, "Utilisateur introuvable")
    
    execute_write(
        "UPDATE utilisateur SET kcal_objectif = :goal WHERE id = :user_id",
        {"goal": payload.kcal_objectif, "user_id": user_id}
    )
    return {"status": "updated", "kcal_objectif": payload.kcal_objectif}


@router.put("/users/{user_id}/subscription", summary="Mise à jour de l'abonnement", tags=["Administration"])
def update_user_subscription(user_id: int, payload: SubscriptionUpdateRequest):
    """Change le type d'abonnement d'un utilisateur (admin seulement)."""
    user = fetch_one("SELECT id FROM utilisateur WHERE id = :user_id", {"user_id": user_id})
    if not user:
        raise HTTPException(404, "Utilisateur introuvable")
    
    execute_write(
        "UPDATE utilisateur SET abonnement = CAST(:sub AS type_abonnement) WHERE id = :user_id",
        {"sub": payload.abonnement, "user_id": user_id}
    )
    return {"status": "updated", "abonnement": payload.abonnement}


@router.get("/stats/global", summary="KPIs Business", tags=["Administration"])
def get_global_stats():
    """Retourne les statistiques globales de la plateforme (conversions, utilisateurs, etc.)."""
    stats = fetch_one("SELECT * FROM vue_kpis_business")
    # Fetch recent meals count for more data
    meals_count = fetch_one("SELECT COUNT(*) FROM journal_repas")
    aliments_count = fetch_one("SELECT COUNT(*) FROM aliment")
    
    if stats:
        stats = dict(stats)
        stats["total_repas"] = meals_count["count"] if meals_count else 0
        stats["total_aliments"] = aliments_count["count"] if aliments_count else 0
        return stats
    return {"error": "Stats non disponibles"}


@router.get("/stats/users/{user_id}/activity", summary="Statistiques d'activité utilisateur", tags=["Administration"])
def get_user_activity_stats(user_id: int):
    """Récupère les statistiques sportives d'un utilisateur spécifique (séances, durée)."""
    activity = fetch_one("SELECT * FROM vue_stats_activite WHERE utilisateur_id = :user_id", {"user_id": user_id})
    return activity if activity else {"nb_seances": 0, "total_minutes": 0}


@router.post("/users", response_model=UserResponse, summary="Création de compte", tags=["Gestion Utilisateurs"])
def create_user(payload: UserCreate):
    """Enregistre un nouvel utilisateur dans la base de données."""
    existing = fetch_one("SELECT id FROM utilisateur WHERE email = :email", {"email": payload.email})
    if existing:
        raise HTTPException(400, "Email déjà utilisé")

    params = payload.model_dump(exclude={"password"})
    params["mdp_hash"] = hash_password(payload.password)
    result = execute_write(
        "INSERT INTO utilisateur (nom, prenom, email, mdp_hash, date_naissance, sexe, poids_initial_kg, taille_cm, abonnement, kcal_objectif)"
        " VALUES (:nom, :prenom, :email, :mdp_hash, :date_naissance, :sexe, :poids_initial_kg, :taille_cm, :abonnement, :kcal_objectif)"
        " RETURNING id, nom, prenom, email, sexe, abonnement, date_inscription, actif, date_naissance, poids_initial_kg, taille_cm, kcal_objectif",
        params,
    )
    row = result.mappings().first()
    return UserResponse(**dict(row))


@router.delete("/users/{user_id}", summary="Suppression de compte", tags=["Gestion Utilisateurs"])
def delete_user(user_id: int):
    """Supprime définitivement un utilisateur et ses données associées."""
    user = fetch_one("SELECT id FROM utilisateur WHERE id = :user_id", {"user_id": user_id})
    if not user:
        raise HTTPException(404, "Utilisateur introuvable")
    
    # Delete meals first (using cross-service knowledge for now as they share DB)
    execute_write("DELETE FROM journal_repas WHERE utilisateur_id = :user_id", {"user_id": user_id})
    # Delete user
    execute_write("DELETE FROM utilisateur WHERE id = :user_id", {"user_id": user_id})
    
    return {"status": "deleted", "user_id": user_id}
