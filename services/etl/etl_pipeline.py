"""
=============================================================
 HealthAI Coach — Pipeline ETL
 Ingestion, nettoyage et chargement des datasets Kaggle
 Version : 1.3.0
=============================================================
"""

import os
import sys
import logging
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# =============================================================
# CONFIGURATION
# =============================================================

DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     os.getenv("DB_PORT",     "5432"),
    "dbname":   os.getenv("DB_NAME",     "healthai"),
    "user":     os.getenv("DB_USER",     "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}

DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# =============================================================
# LOGGER
# =============================================================

class StringHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_content = ""
    def emit(self, record):
        self.log_content += self.format(record) + "\n"

log_capture = StringHandler()

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("healthai_etl")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S")
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    
    log_capture.setFormatter(fmt)
    logger.addHandler(log_capture)
    return logger

logger = setup_logger()

# =============================================================
# CONNEXION BASE DE DONNÉES
# =============================================================

def get_engine():
    url = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    return create_engine(url, echo=False, pool_pre_ping=True)

# =============================================================
# OUTILS ETL
# =============================================================

def charger_fichier(nom_fichier: str, colonnes_attendues: list[str] = None, **kwargs) -> pd.DataFrame | None:
    chemin = DATA_DIR / nom_fichier
    if not chemin.exists():
        logger.warning(f"Fichier introuvable : {chemin}")
        return None

    ext = chemin.suffix.lower()
    try:
        if ext == ".csv": df = pd.read_csv(chemin, **kwargs)
        elif ext == ".json": df = pd.read_json(chemin, **kwargs)
        elif ext in (".xlsx", ".xls"): df = pd.read_excel(chemin, **kwargs)
        else: return None
        
        if colonnes_attendues:
            missing = [c for c in colonnes_attendues if c not in df.columns]
            if missing:
                logger.error(f"Colonnes manquantes dans {nom_fichier} : {missing}")
                return None
        return df.dropna(how='all')
    except Exception as e:
        logger.error(f"Erreur chargement {nom_fichier} : {e}")
        return None

def inserer_en_base(df: pd.DataFrame, table: str, engine):
    if df.empty: return 0
    try:
        df.to_sql(table, engine, if_exists="append", index=False, method="multi")
        return len(df)
    except Exception as e:
        logger.error(f"Erreur insertion {table} : {e}")
        return 0

# =============================================================
# ÉTAPES ETL
# =============================================================

def etl_aliments(engine):
    logger.info("ETL 1 : Aliments — début")
    # Tentative avec le fichier existant
    df = charger_fichier("daily_food_nutrition_dataset.csv")
    
    if df is None:
        logger.warning("Fichier principal absent, tentative avec kaggle_nutrition.csv")
        df = charger_fichier("kaggle_nutrition.csv")

    if df is None:
        logger.error("Aucun fichier d'aliments trouvé.")
        return {"dataset": "aliments", "statut": "erreur"}
    
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM ligne_repas"))
        conn.execute(text("DELETE FROM journal_repas"))
        conn.execute(text("DELETE FROM aliment"))
        conn.commit()

    # Mapping flexible selon le fichier
    if "calories" in df.columns:
        df = df.rename(columns={"name": "nom", "calories": "calories_100g", "protein": "proteines_g", "fat": "lipides_g", "carbohydrate": "glucides_g"})
    elif "Calories" in df.columns:
        df = df.rename(columns={"Food Item": "nom", "Calories": "calories_100g", "Protein": "proteines_g", "Fat": "lipides_g", "Carbohydrates": "glucides_g"})

    df["source_dataset"] = "Kaggle Food Nutrition"
    cols_to_keep = [c for c in ["nom", "calories_100g", "proteines_g", "glucides_g", "lipides_g", "source_dataset"] if c in df.columns]
    
    nb = inserer_en_base(df[cols_to_keep].head(500), "aliment", engine)
    return {"dataset": "aliments", "insérés": nb}

def etl_utilisateurs_metriques(engine):
    logger.info("ETL 2 : Utilisateurs — début")
    df = charger_fichier("gym_members_exercise.csv")
    
    utilisateurs = []
    if df is not None:
        # Transformation simplifiée pour démo
        df = df.head(10)
        for i, row in df.iterrows():
            utilisateurs.append({
                "nom": f"User{i}", "prenom": "Demo", "email": f"u{i}@healthai.demo",
                "mdp_hash": hashlib.sha256("secret".encode()).hexdigest(),
                "sexe": "homme", "poids_initial_kg": 70, "taille_cm": 175, "abonnement": "freemium",
                "date_inscription": datetime.now() - timedelta(days=i*2)
            })

    # USERS DE TEST FIXES (JARMY TEAM)
    test_users = [
        {"nom": "Belatar", "prenom": "Youssef", "email": "youssef@jarmy.pro", "mdp_hash": hashlib.sha256("youssef".encode()).hexdigest(), "sexe": "homme", "poids_initial_kg": 80, "taille_cm": 185, "abonnement": "premium_plus", "date_inscription": datetime.now() - timedelta(days=120)},
        {"nom": "Izac", "prenom": "Matthieu", "email": "matthieu@jarmy.pro", "mdp_hash": hashlib.sha256("matthieu".encode()).hexdigest(), "sexe": "homme", "poids_initial_kg": 78, "taille_cm": 182, "abonnement": "premium", "date_inscription": datetime.now() - timedelta(days=45)},
        {"nom": "Kabouri", "prenom": "Anass", "email": "anass@jarmy.pro", "mdp_hash": hashlib.sha256("anass".encode()).hexdigest(), "sexe": "homme", "poids_initial_kg": 72, "taille_cm": 178, "abonnement": "freemium", "date_inscription": datetime.now() - timedelta(days=15)},
        {"nom": "Admin", "prenom": "Jarmy", "email": "admin@jarmy.pro", "mdp_hash": hashlib.sha256("admin".encode()).hexdigest(), "sexe": "autre", "poids_initial_kg": 70, "taille_cm": 170, "abonnement": "premium_plus", "date_inscription": datetime.now() - timedelta(days=365)},
    ]
    
    df_all = pd.DataFrame(utilisateurs + test_users)
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM utilisateur WHERE email LIKE '%@healthai.demo' OR email LIKE '%@jarmy.pro'"))
        conn.commit()
        
    nb = inserer_en_base(df_all, "utilisateur", engine)
    return {"dataset": "utilisateurs", "insérés": nb}

def etl_exercices(engine):
    logger.info("ETL 3 : Exercices — début")
    df = charger_fichier("exercises.json")
    if df is None: return {"dataset": "exercices", "statut": "erreur"}
    
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM exercice_muscle"))
        conn.execute(text("DELETE FROM exercice"))
        conn.commit()
    
    # Correction mapping : name -> nom, instructions -> description
    df = df.rename(columns={"name": "nom", "instructions": "description"})
    
    # S'assurer que les colonnes existent
    if "description" not in df.columns:
        df["description"] = "Aucune description fournie."
        
    nb = inserer_en_base(df[["nom", "description"]].head(100), "exercice", engine)
    return {"dataset": "exercices", "insérés": nb}

# =============================================================
# ORCHESTRATEUR
# =============================================================

def run_pipeline():
    start = datetime.now()
    log_capture.log_content = "" # Reset capture
    engine = get_engine()
    
    run_log_id = None
    try:
        with engine.connect() as conn:
            res = conn.execute(text("INSERT INTO etl_run_log (start_time, status) VALUES (NOW(), 'RUNNING') RETURNING id"))
            conn.commit()
            run_log_id = result_id = res.scalar()
    except: pass

    rapports = []
    etl_fonctions = [("Aliments", etl_aliments), ("Users", etl_utilisateurs_metriques), ("Exercices", etl_exercices)]
    
    total = 0
    for nom, fn in etl_fonctions:
        try:
            r = fn(engine)
            rapports.append(r)
            total += r.get("insérés", 0)
        except Exception as e:
            logger.error(f"Erreur {nom} : {e}")

    end = datetime.now()
    status = "SUCCESS" if all(r.get("statut") != "erreur" for r in rapports) else "PARTIAL"
    
    if run_log_id:
        try:
            with engine.connect() as conn:
                conn.execute(text("UPDATE etl_run_log SET end_time=NOW(), status=:s, records_processed=:n, logs=:l WHERE id=:id"),
                    {"s": status, "n": total, "l": log_capture.log_content, "id": run_log_id})
                conn.commit()
        except: pass
    
    logger.info(f"Pipeline terminé : {total} records en {(end-start).total_seconds():.1f}s")

if __name__ == "__main__":
    run_pipeline()
