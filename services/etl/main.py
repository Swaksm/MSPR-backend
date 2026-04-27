from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from app.routes import router
import logging
from etl_pipeline import run_pipeline

app = FastAPI(
    title="HealthAI ETL Service",
    description="Service API pour déclencher le pipeline ETL HealthAI.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Scheduler Setup
scheduler = BackgroundScheduler()

def scheduled_etl_job():
    logging.info("Démarrage automatique de l'ETL (Job Planifié)")
    try:
        run_pipeline()
    except Exception as e:
        logging.error(f"Erreur lors de l'ETL planifié : {e}")

@app.on_event("startup")
def start_scheduler():
    # Exécution tous les jours à minuit (peut être modifié selon le besoin)
    scheduler.add_job(scheduled_etl_job, "cron", hour=0, minute=0)
    scheduler.start()
    logging.info("APScheduler démarré.")

@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown()
    logging.info("APScheduler arrêté.")
