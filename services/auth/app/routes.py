from hashlib import sha256
from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, HTTPException

from database import fetch_one

router = APIRouter()


def hash_password(raw_password: str) -> str:
    return sha256(raw_password.encode("utf-8")).hexdigest()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginResponse(BaseModel):
    success: bool
    message: str
    user_id: int | None = None
    email: EmailStr | None = None


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    user = fetch_one(
        "SELECT id, email, mdp_hash, actif FROM utilisateur WHERE email = :email",
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
    )
