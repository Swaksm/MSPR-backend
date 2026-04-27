import json
import httpx
import os
from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from database import fetch_all, fetch_one, execute_write

router = APIRouter()

# Configuration
ETL_SERVICE_URL = os.getenv("ETL_SERVICE_URL", "http://etl:8002")

# --- Modèles ---
class ApproveRequest(BaseModel):
    batch_id: Optional[int] = None
    status: str = "APPROVED"

class CorrectionRequest(BaseModel):
    table_name: str
    id: int
    column_name: str
    new_value: str | int | float | bool

# -------------------------------------------------------------
# CRUD & MANAGEMENT
# -------------------------------------------------------------

@router.get("/users", summary="Lister les utilisateurs (Admin)", tags=["CRUD"])
def admin_get_users():
    return fetch_all("SELECT * FROM utilisateur ORDER BY id DESC")

@router.put("/users/{user_id}", summary="Mettre à jour un utilisateur", tags=["CRUD"])
def admin_update_user(user_id: int, payload: dict):
    valid_cols = ["nom", "prenom", "email", "sexe", "abonnement", "poids_initial_kg", "taille_cm", "actif", "kcal_objectif"]
    updates = []
    params = {"id": user_id}
    for k, v in payload.items():
        if k in valid_cols:
            updates.append(f"{k} = :{k}")
            params[k] = v
    if not updates:
        return {"status": "no changes"}
    query = f"UPDATE utilisateur SET {', '.join(updates)} WHERE id = :id"
    execute_write(query, params)
    return {"status": "updated", "user_id": user_id}

@router.delete("/users/{user_id}", summary="Supprimer un utilisateur", tags=["CRUD"])
def admin_delete_user(user_id: int):
    execute_write("DELETE FROM journal_repas WHERE utilisateur_id = :id", {"id": user_id})
    execute_write("DELETE FROM utilisateur WHERE id = :id", {"id": user_id})
    return {"status": "deleted"}

@router.get("/foods", summary="Lister les aliments", tags=["CRUD"])
def admin_get_foods():
    return fetch_all("SELECT * FROM aliment ORDER BY id DESC LIMIT 500")

@router.get("/exercises", summary="Lister les exercices", tags=["CRUD"])
def admin_get_exercises():
    return fetch_all("SELECT * FROM exercice ORDER BY id DESC LIMIT 500")

# -------------------------------------------------------------
# QUALITÉ DES DONNÉES & ETL
# -------------------------------------------------------------

@router.get("/data-quality", summary="Analyse qualité des données", tags=["Qualité"])
def get_data_quality():
    missing_goals = fetch_all("SELECT id, nom, prenom, email FROM utilisateur WHERE kcal_objectif IS NULL OR kcal_objectif = 0 LIMIT 10")
    invalid_weights = fetch_all("SELECT id, nom, prenom, poids_initial_kg as value FROM utilisateur WHERE poids_initial_kg < 30 OR poids_initial_kg > 200 LIMIT 10")
    zero_cal_foods = fetch_all("SELECT id, nom, calories_100g as value FROM aliment WHERE calories_100g = 0 LIMIT 10")
    etl_logs = fetch_all("SELECT * FROM etl_run_log ORDER BY id DESC LIMIT 10")
    
    return {
        "anomalies": {
            "users_missing_goals": {"count": len(missing_goals), "samples": missing_goals},
            "users_unrealistic_weight": {"count": len(invalid_weights), "samples": invalid_weights},
            "foods_zero_calories": {"count": len(zero_cal_foods), "samples": zero_cal_foods},
        },
        "etl_logs": etl_logs
    }

@router.post("/etl/run", summary="Lancer l'ETL manuellement", tags=["Qualité"])
async def run_etl_manually():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{ETL_SERVICE_URL}/etl/run", 
                headers={"Authorization": "Bearer clesecrete"}
            )
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Service ETL injoignable : {e}")

@router.post("/data/approve", summary="Approuver batch", tags=["Qualité"])
def approve_data(payload: ApproveRequest):
    execute_write("INSERT INTO etl_run_log (start_time, end_time, status, logs) VALUES (NOW(), NOW(), 'APPROVED_MANUAL', 'Validation manuelle via Admin UI')")
    return {"status": "approved", "batch_id": payload.batch_id}

@router.put("/data/correct", summary="Correction manuelle", tags=["Qualité"])
def correct_data(payload: CorrectionRequest):
    allowed_tables = ["utilisateur", "aliment", "exercice"]
    if payload.table_name not in allowed_tables:
        raise HTTPException(400, "Table non autorisée")
    
    # Conversion de type sécurisée
    val = payload.new_value
    if payload.column_name in ["kcal_objectif", "calories_100g", "poids_initial_kg", "taille_cm"]:
        try:
            val = float(val) if "." in str(val) else int(val)
        except:
            raise HTTPException(400, "Valeur numérique invalide")

    query = f"UPDATE {payload.table_name} SET {payload.column_name} = :val WHERE id = :id"
    execute_write(query, {"val": val, "id": payload.id})
    return {"status": "corrected"}

# -------------------------------------------------------------
# EXPORT & ANALYTICS
# -------------------------------------------------------------

@router.get("/export", summary="Export JSON des données", tags=["Système"])
def export_data():
    try:
        users = fetch_all("SELECT id, prenom, nom, email, abonnement FROM utilisateur")
        foods = fetch_all("SELECT id, nom, calories_100g, categorie FROM aliment LIMIT 1000")
        data = {"utilisateurs": users, "aliments": foods, "export_date": datetime.now().isoformat()}
        
        def default_serializer(obj):
            from decimal import Decimal
            if isinstance(obj, (datetime, date)): return obj.isoformat()
            if isinstance(obj, Decimal): return float(obj)
            raise TypeError(f"Type {type(obj)} non serializable")
            
        content = json.dumps(data, default=default_serializer)
        return Response(
            content=content,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=jarmy_export_{date.today()}.json"}
        )
    except Exception as e:
        print(f"EXPORT ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/users", summary="Analytics Utilisateurs", tags=["Analytics"])
def analytics_users():
    repartition_sexe = fetch_all("SELECT sexe, COUNT(*) as count FROM utilisateur GROUP BY sexe")
    inscriptions = fetch_all("SELECT DATE_TRUNC('month', date_inscription) as mois, COUNT(*) as count FROM utilisateur GROUP BY mois ORDER BY mois")
    return {"repartition_sexe": repartition_sexe, "inscriptions_historique": inscriptions}

@router.get("/analytics/nutrition", summary="Analytics Nutrition", tags=["Analytics"])
def analytics_nutrition():
    type_repas = fetch_all("SELECT type_repas, COUNT(*) as count FROM journal_repas GROUP BY type_repas")
    moyenne_cal = fetch_all("""
        SELECT jr.type_repas, AVG(lr.quantite_g / 100.0 * a.calories_100g) as avg_cal
        FROM journal_repas jr
        JOIN ligne_repas lr ON lr.journal_id = jr.id
        JOIN aliment a ON a.id = lr.aliment_id
        GROUP BY jr.type_repas
    """)
    return {"repartition_repas": type_repas, "moyenne_calorique": moyenne_cal}

@router.get("/analytics/fitness", summary="Analytics Fitness", tags=["Analytics"])
def analytics_fitness():
    exercices_populaires = fetch_all("""
        SELECT e.nom, COUNT(*) as count FROM seance_exercice se JOIN exercice e ON e.id = se.exercice_id 
        GROUP BY e.nom ORDER BY count DESC LIMIT 10
    """)
    return {"exercices_populaires": exercices_populaires}
