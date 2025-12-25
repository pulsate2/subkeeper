from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import json
from ..database import get_db
from ..models import Settings, Subscription, Reminder
from ..schemas import BackupData
from ..auth import verify_token

router = APIRouter()

@router.get("/export")
async def export_data(db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Export all data as JSON"""
    try:
        # Get all settings
        settings_dict = {}
        all_settings = db.query(Settings).all()
        for setting in all_settings:
            if setting.key in ['smtp_conf', 'wechat_conf', 'global_days']:
                settings_dict[setting.key] = json.loads(setting.value)
            else:
                settings_dict[setting.key] = setting.value
        
        # Get all subscriptions
        subscriptions = []
        for sub in db.query(Subscription).all():
            sub_dict = {
                "id": sub.id,
                "name": sub.name,
                "price": sub.price,
                "cycle_val": sub.cycle_val,
                "cycle_unit": sub.cycle_unit,
                "next_date": sub.next_date.isoformat(),
                "notify_mode": sub.notify_mode,
                "cust_days": sub.cust_days,
                "cust_time": sub.cust_time,
                "last_sent": sub.last_sent.isoformat() if sub.last_sent else None,
                "group_name": sub.group_name,
                "is_disabled": sub.is_disabled,
                "remarks": sub.remarks,
                "notify_email": sub.notify_email,
                "notify_wechat": sub.notify_wechat,
                "notify_webhook": sub.notify_webhook,
                "notify_resend": sub.notify_resend
            }
            subscriptions.append(sub_dict)
        
        # Get all reminders
        reminders = []
        for reminder in db.query(Reminder).all():
            reminder_dict = {
                "id": reminder.id,
                "title": reminder.title,
                "content": reminder.content,
                "target_date": reminder.target_date.isoformat(),
                "target_time": reminder.target_time,
                "is_sent": reminder.is_sent,
                "group_name": reminder.group_name,
                "is_disabled": reminder.is_disabled,
                "notify_email": reminder.notify_email,
                "notify_wechat": reminder.notify_wechat,
                "notify_webhook": reminder.notify_webhook,
                "notify_resend": reminder.notify_resend
            }
            reminders.append(reminder_dict)
        
        # Create backup data
        backup = {
            "meta": {
                "version": "1.0",
                "time": datetime.now().isoformat()
            },
            "settings": settings_dict,
            "subscriptions": subscriptions,
            "reminders": reminders
        }
        
        return JSONResponse(content=backup)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/import")
async def import_data(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Import data from JSON backup"""
    try:
        # Read and parse JSON
        content = await file.read()
        backup_data = json.loads(content)
        
        # Clear existing data
        db.query(Settings).delete()
        db.query(Subscription).delete()
        db.query(Reminder).delete()
        db.commit()
        
        # Import settings
        if "settings" in backup_data:
            for key, value in backup_data["settings"].items():
                if isinstance(value, (dict, list)):
                    value_str = json.dumps(value)
                else:
                    value_str = str(value)
                db.add(Settings(key=key, value=value_str))
        
        # Import subscriptions
        if "subscriptions" in backup_data:
            for sub_data in backup_data["subscriptions"]:
                sub_data_copy = sub_data.copy()
                if "id" in sub_data_copy:
                    del sub_data_copy["id"]
                if "next_date" in sub_data_copy:
                    sub_data_copy["next_date"] = datetime.fromisoformat(sub_data_copy["next_date"]).date()
                if "last_sent" in sub_data_copy and sub_data_copy["last_sent"]:
                    sub_data_copy["last_sent"] = datetime.fromisoformat(sub_data_copy["last_sent"])
                db.add(Subscription(**sub_data_copy))
        
        # Import reminders
        if "reminders" in backup_data:
            for reminder_data in backup_data["reminders"]:
                reminder_data_copy = reminder_data.copy()
                if "id" in reminder_data_copy:
                    del reminder_data_copy["id"]
                if "target_date" in reminder_data_copy:
                    reminder_data_copy["target_date"] = datetime.fromisoformat(reminder_data_copy["target_date"]).date()
                if "content" in reminder_data_copy:
                    reminder_data_copy["content"] = reminder_data_copy["content"]
                db.add(Reminder(**reminder_data_copy))
        
        db.commit()
        
        return {"message": "Data imported successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
