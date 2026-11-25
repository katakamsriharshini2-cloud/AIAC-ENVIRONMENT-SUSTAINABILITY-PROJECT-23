import os
from pathlib import Path
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from apscheduler.schedulers.background import BackgroundScheduler

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.initial_data import init_db
from app.services.data_collection_service import DataCollectionService

# Import API routes
from app.api.auth_routes import router as auth_router
from app.api.station_routes import router as station_router
from app.api.record_routes import router as record_router
from app.api.live_data_routes import router as live_data_router
from app.api.analytics_routes import router as analytics_router
from app.api.ai_routes import router as ai_router
from app.api.optimization_routes import router as optimization_router
from app.api.iot_routes import router as iot_router
from app.api.portal_routes import router as portal_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Assisted Smart Environmental Monitoring and Sustainability Platform for Warangal, Telangana.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware — allow all local dev origins explicitly
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
    expose_headers=["*"],
    max_age=3600,
)

# Include API Routers
app.include_router(auth_router)
app.include_router(station_router)
app.include_router(record_router)
app.include_router(live_data_router)
app.include_router(analytics_router)
app.include_router(ai_router)
app.include_router(optimization_router)
app.include_router(iot_router)
app.include_router(portal_router)

# Background Scheduler for Environmental Sync
scheduler = BackgroundScheduler()

def scheduled_weather_sync():
    with SessionLocal() as db:
        try:
            DataCollectionService.sync_weather(db, city=settings.DEFAULT_CITY, lat=settings.DEFAULT_LATITUDE, lon=settings.DEFAULT_LONGITUDE)
        except Exception as e:
            print(f"[Scheduler] Weather sync error: {e}")

def scheduled_air_sync():
    with SessionLocal() as db:
        try:
            DataCollectionService.sync_air_quality(db, city=settings.DEFAULT_CITY, state=settings.DEFAULT_STATE)
        except Exception as e:
            print(f"[Scheduler] Air quality sync error: {e}")

@app.on_event("startup")
def on_startup():
    # 1. Create database tables
    Base.metadata.create_all(bind=engine)

    # 2. Seed initial roles, admin, stations, authentic data
    with SessionLocal() as db:
        init_db(db)

    # 3. Start background periodic jobs if explicitly enabled
    if os.getenv("ENABLE_BACKGROUND_SCHEDULER") == "true" and not scheduler.running:
        scheduler.add_job(scheduled_weather_sync, "interval", minutes=15, id="weather_poller")
        scheduler.add_job(scheduled_air_sync, "interval", minutes=15, id="air_poller")
        try:
            scheduler.start()
        except Exception as e:
            print(f"[Scheduler] Could not start APScheduler: {e}")

@app.on_event("shutdown")
def on_shutdown():
    if scheduler.running:
        scheduler.shutdown(wait=False)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "region": f"{settings.DEFAULT_CITY}, {settings.DEFAULT_STATE}, {settings.DEFAULT_COUNTRY}"
    }

# Serve Frontend build if present, or provide API landing
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/", include_in_schema=False)
    async def serve_root():
        index_file = FRONTEND_DIST / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {
            "message": "ECOSPHERE AI Backend Operational",
            "docs": "/docs",
            "frontend_dev_server": "http://localhost:5173"
        }
else:
    @app.get("/", include_in_schema=False)
    async def serve_root():
        return {
            "message": "ECOSPHERE AI Backend Operational",
            "docs": "/docs",
            "frontend_dev_server": "http://localhost:5173"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
