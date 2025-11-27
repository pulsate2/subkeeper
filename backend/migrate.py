#!/usr/bin/env python3
"""
Database migration script for SubKeeper
This script automatically adds missing columns to the database tables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from sqlalchemy import text

def run_migrations():
    """Run all pending migrations"""
    print("Starting database migrations...")
    
    with engine.connect() as conn:
        # Migration for subscriptions table
        print("Checking subscriptions table...")
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
        
        conn.commit()
    
    print("Database migrations completed successfully!")

if __name__ == "__main__":
    try:
        run_migrations()
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)