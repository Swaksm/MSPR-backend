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
    email: EmailStr = Field(..., example="jean.dupont@example.com", description="Adresse email de l'utilisateur")
    password: str = Field(..., min_length=6, example="secret123", description="Mot de passe de l'utilisateur")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "jean.dupont@example.com",
                "password": "secret123"
            }
        }


class LoginResponse(BaseModel):
    success: bool = Field(..., example=True, description="Succès de l'authentification")
    message: str = Field(..., example="Authentification réussie.", description="Message de retour")
    user_id: int | None = Field(None, example=1, description="ID utilisateur si succès")
    email: EmailStr | None = Field(None, example="jean.dupont@example.com", description="Email utilisateur si succès")
    prenom: str | None = Field(None, example="Jean")
    nom: str | None = Field(None, example="Dupont")


class UserCreate(BaseModel):
    nom: str = Field(..., min_length=2, example="Dupont", description="Nom de famille")
    prenom: str = Field(..., min_length=2, example="Jean", description="Prénom")
    email: EmailStr = Field(..., example="jean.dupont@example.com", description="Adresse email")
    password: str = Field(..., min_length=6, example="secret123", description="Mot de passe")
    date_naissance: Optional[date] = Field(None, example="1990-01-01", description="Date de naissance")
    sexe: Optional[str] = Field("non_renseigne", example="homme", description="Sexe")
    poids_initial_kg: Optional[float] = Field(None, gt=0, example=70, description="Poids initial (kg)")
    taille_cm: Optional[int] = Field(None, ge=50, le=300, example=175, description="Taille (cm)")
    abonnement: Optional[str] = Field("freemium", example="freemium", description="Type d'abonnement")
    kcal_objectif: Optional[int] = Field(2000, ge=500, le=10000)


class UserResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    email: EmailStr
    sexe: str
    abonnement: str
    date_inscription: datetime
    actif: bool
    date_naissance: Optional[date] = None
    poids_initial_kg: Optional[float] = None
    taille_cm: Optional[int] = None
    kcal_objectif: int


class GoalUpdateRequest(BaseModel):
    kcal_objectif: int = Field(..., ge=500, le=10000)


class SubscriptionUpdateRequest(BaseModel):
    abonnement: str = Field(..., example="premium")


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
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


@router.get("/users", response_model=list[UserResponse])
def list_users():
    users = fetch_all("SELECT id, nom, prenom, email, sexe, abonnement, date_inscription, actif, date_naissance, poids_initial_kg, taille_cm, kcal_objectif FROM utilisateur ORDER BY id")
    return [UserResponse(**u) for u in users]


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = fetch_one(
        "SELECT id, nom, prenom, email, sexe, abonnement, date_inscription, actif, date_naissance, poids_initial_kg, taille_cm, kcal_objectif FROM utilisateur WHERE id = :user_id",
        {"user_id": user_id},
    )
    if not user:
        raise HTTPException(404, "Utilisateur introuvable")
    return UserResponse(**user)


@router.put("/users/{user_id}/goal")
def update_user_goal(user_id: int, payload: GoalUpdateRequest):
    user = fetch_one("SELECT id FROM utilisateur WHERE id = :user_id", {"user_id": user_id})
    if not user:
        raise HTTPException(404, "Utilisateur introuvable")
    
    execute_write(
        "UPDATE utilisateur SET kcal_objectif = :goal WHERE id = :user_id",
        {"goal": payload.kcal_objectif, "user_id": user_id}
    )
    return {"status": "updated", "kcal_objectif": payload.kcal_objectif}


@router.put("/users/{user_id}/subscription")
def update_user_subscription(user_id: int, payload: SubscriptionUpdateRequest):
    user = fetch_one("SELECT id FROM utilisateur WHERE id = :user_id", {"user_id": user_id})
    if not user:
        raise HTTPException(404, "Utilisateur introuvable")
    
    execute_write(
        "UPDATE utilisateur SET abonnement = CAST(:sub AS type_abonnement) WHERE id = :user_id",
        {"sub": payload.abonnement, "user_id": user_id}
    )
    return {"status": "updated", "abonnement": payload.abonnement}


@router.post("/users", response_model=UserResponse)
def create_user(payload: UserCreate):
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


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = fetch_one("SELECT id FROM utilisateur WHERE id = :user_id", {"user_id": user_id})
    if not user:
        raise HTTPException(404, "Utilisateur introuvable")
    
    # Delete meals first (using cross-service knowledge for now as they share DB)
    execute_write("DELETE FROM journal_repas WHERE utilisateur_id = :user_id", {"user_id": user_id})
    # Delete user
    execute_write("DELETE FROM utilisateur WHERE id = :user_id", {"user_id": user_id})
    
    return {"status": "deleted", "user_id": user_id}
