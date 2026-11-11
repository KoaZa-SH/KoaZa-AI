
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException

from app.core.supabase import get_supabase


app = FastAPI(
    title="KoaZa AI API",
    description="Central API for KoaZa AI Platform",
    version="0.2.0"
)


@app.get("/")
async def root():
    return {
        "application": "KoaZa AI",
        "status": "online",
        "version": "0.2.0"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "koaza-ai-backend",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/health/database")
async def database_health():
    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("profiles")
            .select("id")
            .limit(1)
            .execute()
        )

        return {
            "status": "connected",
            "database": "supabase",
            "table": "profiles",
            "query_successful": response.data is not None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database connection or query failed"
        )
