#!/usr/bin/env python3
"""
Test script to verify disable/enable functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from app.models import Subscription, Reminder
from datetime import date, datetime, timedelta

def test_disable_functionality():
    """Test that disabled items are properly filtered out"""
    db = SessionLocal()
    
    try:
        # Create test subscription
        test_sub = Subscription(
            name="Test Subscription",
            price=10.0,
            cycle_val=1,
            cycle_unit="month",
            next_date=date.today(),
            is_disabled=True  # Disabled
        )
        db.add(test_sub)
        
        # Create test reminder
        test_reminder = Reminder(
            title="Test Reminder",
            target_date=date.today(),
            target_time="23:59",
            is_disabled=True  # Disabled
        )
        db.add(test_reminder)
        
        # Create enabled items
        enabled_sub = Subscription(
            name="Enabled Subscription",
            price=20.0,
            cycle_val=1,
            cycle_unit="month",
            next_date=date.today(),
            is_disabled=False  # Enabled
        )
        db.add(enabled_sub)
        
        enabled_reminder = Reminder(
            title="Enabled Reminder",
            target_date=date.today(),
            target_time="23:59",
            is_disabled=False  # Enabled
        )
        db.add(enabled_reminder)
        
        db.commit()
        
        # Test queries
        all_subs = db.query(Subscription).all()
        enabled_subs = db.query(Subscription).filter(Subscription.is_disabled == False).all()
        disabled_subs = db.query(Subscription).filter(Subscription.is_disabled == True).all()
        
        all_reminders = db.query(Reminder).all()
        enabled_reminders = db.query(Reminder).filter(Reminder.is_disabled == False).all()
        disabled_reminders = db.query(Reminder).filter(Reminder.is_disabled == True).all()
        
        print(f"Total subscriptions: {len(all_subs)}")
        print(f"Enabled subscriptions: {len(enabled_subs)}")
        print(f"Disabled subscriptions: {len(disabled_subs)}")
        
        print(f"Total reminders: {len(all_reminders)}")
        print(f"Enabled reminders: {len(enabled_reminders)}")
        print(f"Disabled reminders: {len(disabled_reminders)}")
        
        # Test enabling/disabling
        test_sub.is_disabled = False
        test_reminder.is_disabled = False
        db.commit()
        
        enabled_subs_after = db.query(Subscription).filter(Subscription.is_disabled == False).all()
        enabled_reminders_after = db.query(Reminder).filter(Reminder.is_disabled == False).all()
        
        print(f"After enabling:")
        print(f"Enabled subscriptions: {len(enabled_subs_after)}")
        print(f"Enabled reminders: {len(enabled_reminders_after)}")
        
        # Clean up test data
        db.delete(test_sub)
        db.delete(test_reminder)
        db.delete(enabled_sub)
        db.delete(enabled_reminder)
        db.commit()
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_disable_functionality()