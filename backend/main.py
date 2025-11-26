from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base
# from scheduler import scheduler_service
# from notifications import NotificationService
from app.routes import settings, subscriptions, reminders, backup

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and start scheduler
    from app.scheduler import scheduler
    Base.metadata.create_all(bind=engine)
    scheduler.start()
    yield
    # Shutdown: Stop scheduler
    scheduler.shutdown()

app = FastAPI(title="SubKeeper", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(settings.router, prefix="/api/settings", tags=["settings"])
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])
app.include_router(backup.router, prefix="/api", tags=["backup"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
