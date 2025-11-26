from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base, run_migrations
# from scheduler import scheduler_service
# from notifications import NotificationService
from app.routes import settings, subscriptions, reminders, backup, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and run migrations
    from app.scheduler import scheduler
    # Create all tables, including any new columns
    Base.metadata.create_all(bind=engine)
    # Run migrations to update existing tables with new columns
    run_migrations()
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

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])
app.include_router(backup.router, prefix="/api", tags=["backup"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
