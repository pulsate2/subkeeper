import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = os.getenv("DB_PATH", "/app/data/subkeeper.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_migrations():
    """Run database migrations to update schema"""
    with engine.connect() as conn:
        # Force add notification columns to subscriptions table
        print("Adding notification columns to subscriptions table...")
        result = conn.execute(text("PRAGMA table_info(subscriptions)"))
        columns = [row[1] for row in result]
        
        if 'is_disabled' not in columns:
            print("Adding is_disabled column to subscriptions table...")
            conn.execute(text('ALTER TABLE subscriptions ADD COLUMN is_disabled BOOLEAN DEFAULT FALSE'))
        else:
            print("is_disabled column already exists in subscriptions table")
        
        # Migration for reminders table
        print("Checking reminders table...")
        result = conn.execute(text("PRAGMA table_info(reminders)"))
        columns = [row[1] for row in result]
        
        if 'is_disabled' not in columns:
            print("Adding is_disabled column to reminders table...")
            conn.execute(text('ALTER TABLE reminders ADD COLUMN is_disabled BOOLEAN DEFAULT FALSE'))
        else:
            print("is_disabled column already exists in reminders table")
        
        try:
            conn.execute(text('ALTER TABLE subscriptions ADD COLUMN notify_email BOOLEAN DEFAULT TRUE'))
            print("Added notify_email column to subscriptions table")
        except Exception:
            print("notify_email column already exists in subscriptions table")
        
        try:
            conn.execute(text('ALTER TABLE subscriptions ADD COLUMN notify_wechat BOOLEAN DEFAULT TRUE'))
            print("Added notify_wechat column to subscriptions table")
        except Exception:
            print("notify_wechat column already exists in subscriptions table")
        
        try:
            conn.execute(text('ALTER TABLE subscriptions ADD COLUMN notify_webhook BOOLEAN DEFAULT TRUE'))
            print("Added notify_webhook column to subscriptions table")
        except Exception:
            print("notify_webhook column already exists in subscriptions table")
        
        try:
            conn.execute(text('ALTER TABLE subscriptions ADD COLUMN notify_resend BOOLEAN DEFAULT TRUE'))
            print("Added notify_resend column to subscriptions table")
        except Exception:
            print("notify_resend column already exists in subscriptions table")
        
        # Force add notification columns to reminders table
        print("Adding notification columns to reminders table...")
        try:
            conn.execute(text('ALTER TABLE reminders ADD COLUMN notify_email BOOLEAN DEFAULT TRUE'))
            print("Added notify_email column to reminders table")
        except Exception:
            print("notify_email column already exists in reminders table")
        
        try:
            conn.execute(text('ALTER TABLE reminders ADD COLUMN notify_wechat BOOLEAN DEFAULT TRUE'))
            print("Added notify_wechat column to reminders table")
        except Exception:
            print("notify_wechat column already exists in reminders table")
        
        try:
            conn.execute(text('ALTER TABLE reminders ADD COLUMN notify_webhook BOOLEAN DEFAULT TRUE'))
            print("Added notify_webhook column to reminders table")
        except Exception:
            print("notify_webhook column already exists in reminders table")
        
        try:
            conn.execute(text('ALTER TABLE reminders ADD COLUMN notify_resend BOOLEAN DEFAULT TRUE'))
            print("Added notify_resend column to reminders table")
        except Exception:
            print("notify_resend column already exists in reminders table")
        
        conn.commit()
        print("Database migrations completed successfully!")
