from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import Optional
import os

app = FastAPI(
    title="Activity Logs Service",
    description="Service de journalisation des activites utilisateur (MongoDB)",
    version="1.0.0"
)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
MONGO_DB = os.getenv("MONGO_DB", "healthai_logs")

client: Optional[AsyncIOMotorClient] = None
db = None


@app.on_event("startup")
async def startup_db():
    global client, db
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[MONGO_DB]
    await db.activity_logs.create_index("user_id")
    await db.activity_logs.create_index("action")
    await db.activity_logs.create_index("timestamp")


@app.on_event("shutdown")
async def shutdown_db():
    global client
    if client:
        client.close()


class ActivityLogCreate(BaseModel):
    user_id: int = Field(..., description="ID de l'utilisateur")
    action: str = Field(..., description="Type d'action (login, add_meal, search_food, update_profile, etc.)")
    detail: Optional[dict] = Field(default=None, description="Details supplementaires au format libre")


class ActivityLogResponse(BaseModel):
    id: str
    user_id: int
    action: str
    detail: Optional[dict]
    timestamp: str


@app.get("/health")
async def health_check():
    try:
        await client.admin.command("ping")
        return {"status": "ok", "database": "mongodb", "service": "activity-logs"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"MongoDB unreachable: {str(e)}")


@app.post("/logs", response_model=ActivityLogResponse, status_code=201)
async def create_log(log: ActivityLogCreate):
    document = {
        "user_id": log.user_id,
        "action": log.action,
        "detail": log.detail,
        "timestamp": datetime.utcnow()
    }
    result = await db.activity_logs.insert_one(document)
    document["_id"] = result.inserted_id
    return _format_log(document)


@app.get("/logs")
async def get_logs(user_id: Optional[int] = None, action: Optional[str] = None, limit: int = 50):
    query = {}
    if user_id is not None:
        query["user_id"] = user_id
    if action is not None:
        query["action"] = action

    cursor = db.activity_logs.find(query).sort("timestamp", -1).limit(limit)
    logs = []
    async for doc in cursor:
        logs.append(_format_log(doc))
    return logs


@app.get("/logs/stats")
async def get_stats(user_id: Optional[int] = None):
    match_stage = {}
    if user_id is not None:
        match_stage = {"$match": {"user_id": user_id}}

    pipeline = [
        {"$group": {"_id": "$action", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    if match_stage:
        pipeline.insert(0, match_stage)

    cursor = db.activity_logs.aggregate(pipeline)
    stats = []
    async for doc in cursor:
        stats.append({"action": doc["_id"], "count": doc["count"]})
    return stats


def _format_log(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "user_id": doc["user_id"],
        "action": doc["action"],
        "detail": doc.get("detail"),
        "timestamp": doc["timestamp"].isoformat() if isinstance(doc["timestamp"], datetime) else str(doc["timestamp"])
    }
