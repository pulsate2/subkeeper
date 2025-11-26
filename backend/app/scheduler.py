from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import json
from .database import SessionLocal
from .models import Settings, Subscription, Reminder
from .notifier import Notifier

scheduler = BackgroundScheduler()

def notification_job():
    """Check and send notifications every minute"""
    db = SessionLocal()
    try:
        now = datetime.now()
        today = now.date()
        current_time = now.strftime("%H:%M")
        
        # Get global settings
        global_days_setting = db.query(Settings).filter(Settings.key == "global_days").first()
        global_time_setting = db.query(Settings).filter(Settings.key == "global_time").first()
        
        global_days = json.loads(global_days_setting.value) if global_days_setting else [3, 1, 0]
        global_time = global_time_setting.value if global_time_setting else "09:00"
        
        notifier = Notifier(db)
        
        # Process subscriptions
        subscriptions = db.query(Subscription).all()
        
        for sub in subscriptions:
            # Determine notification settings
            if sub.notify_mode == 'global':
                notify_days = global_days
                notify_time = global_time
            else:
                notify_days = json.loads(sub.cust_days) if sub.cust_days else []
                notify_time = sub.cust_time or "09:00"
            
            # Calculate days until next payment
            days_until = (sub.next_date - today).days
            
            # Check if should notify
            should_notify = (
                days_until in notify_days and
                current_time >= notify_time and
                (not sub.last_sent or sub.last_sent.date() != today)
            )
            
            if should_notify:
                title = f"订阅提醒: {sub.name}"
                content = f"服务: {sub.name}\n金额: ¥{sub.price}\n扣款日期: {sub.next_date}\n还有 {days_until} 天"
                notifier.send_notification(title, content)
                
                sub.last_sent = now
                db.commit()
        
        # Process reminders
        reminders = db.query(Reminder).filter(Reminder.is_sent == False).all()
        for reminder in reminders:
            should_notify = (
                reminder.target_date == today and
                current_time >= reminder.target_time
            )
            
            if should_notify:
                title = f"待办提醒: {reminder.title}"
                # 构建内容，包含标题、内容和时间
                reminder_content = f"提醒事项: {reminder.title}\n"
                if reminder.content:
                    reminder_content += f"内容: {reminder.content}\n"
                reminder_content += f"时间: {reminder.target_date} {reminder.target_time}"
                notifier.send_notification(title, reminder_content)
                
                reminder.is_sent = True
                db.commit()
                
    except Exception as e:
        print(f"Notification job error: {e}")
    finally:
        db.close()

def renewal_job():
    """Auto-renew subscriptions past due date"""
    db = SessionLocal()
    try:
        today = date.today()
        subscriptions = db.query(Subscription).filter(Subscription.next_date < today).all()
        
        for sub in subscriptions:
            # Calculate next date based on cycle
            if sub.cycle_unit == 'day':
                sub.next_date = sub.next_date + timedelta(days=sub.cycle_val)
            elif sub.cycle_unit == 'week':
                sub.next_date = sub.next_date + timedelta(weeks=sub.cycle_val)
            elif sub.cycle_unit == 'month':
                sub.next_date = sub.next_date + relativedelta(months=sub.cycle_val)
            elif sub.cycle_unit == 'year':
                sub.next_date = sub.next_date + relativedelta(years=sub.cycle_val)
            
            # Keep adding cycles until next_date is in the future
            while sub.next_date < today:
                if sub.cycle_unit == 'day':
                    sub.next_date = sub.next_date + timedelta(days=sub.cycle_val)
                elif sub.cycle_unit == 'week':
                    sub.next_date = sub.next_date + timedelta(weeks=sub.cycle_val)
                elif sub.cycle_unit == 'month':
                    sub.next_date = sub.next_date + relativedelta(months=sub.cycle_val)
                elif sub.cycle_unit == 'year':
                    sub.next_date = sub.next_date + relativedelta(years=sub.cycle_val)
        
        db.commit()
    except Exception as e:
        print(f"Renewal job error: {e}")
    finally:
        db.close()

# Add jobs to scheduler
scheduler.add_job(notification_job, CronTrigger.from_crontab('* * * * *'))  # Every minute
scheduler.add_job(renewal_job, CronTrigger.from_crontab('1 0 * * *'))  # Daily at 00:01
