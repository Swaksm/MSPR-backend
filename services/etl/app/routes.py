from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from etl_pipeline import run_pipeline

router = APIRouter()
security = HTTPBearer()

SECRET_TOKEN = "clesecrete"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token.")
    return credentials.credentials

@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "healthai_etl"}

@router.post("/etl/run")
async def run_etl(background_tasks: BackgroundTasks, token: str = Depends(verify_token)):
    background_tasks.add_task(run_pipeline)
    return {
        "status": "started",
        "message": "ETL pipeline has been started in the background. Check logs for progress."
    }
