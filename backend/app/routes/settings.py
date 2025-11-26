from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from typing import Dict
from ..database import get_db
from ..models import Settings
from ..auth import verify_token

router = APIRouter()

@router.get("/")
async def get_settings(db: Session = Depends(get_db), current_user: str = Depends(verify_token)) -> Dict:
    """Get all settings"""
    settings_dict = {}
    
    # Get SMTP config
    smtp = db.query(Settings).filter(Settings.key == "smtp_conf").first()
    settings_dict["smtp_conf"] = json.loads(smtp.value) if smtp else None
    
    # Get WeChat config
    wechat = db.query(Settings).filter(Settings.key == "wechat_conf").first()
    settings_dict["wechat_conf"] = json.loads(wechat.value) if wechat else None
    
    # Get Webhook config
    webhook = db.query(Settings).filter(Settings.key == "webhook_conf").first()
    settings_dict["webhook_conf"] = json.loads(webhook.value) if webhook and webhook.value else {"webhook_key": ""}
    
    # Get global days
    global_days = db.query(Settings).filter(Settings.key == "global_days").first()
    settings_dict["global_days"] = json.loads(global_days.value) if global_days else [3, 1, 0]
    
    # Get global time
    global_time = db.query(Settings).filter(Settings.key == "global_time").first()
    settings_dict["global_time"] = global_time.value if global_time else "09:00"
    
    return settings_dict

@router.put("/")
async def update_settings(settings: Dict, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Update settings"""
    try:
        # Update SMTP config
        if "smtp_conf" in settings:
            smtp = db.query(Settings).filter(Settings.key == "smtp_conf").first()
            if smtp:
                smtp.value = json.dumps(settings["smtp_conf"])
            else:
                db.add(Settings(key="smtp_conf", value=json.dumps(settings["smtp_conf"])))
        
        # Update WeChat config
        if "wechat_conf" in settings:
            wechat = db.query(Settings).filter(Settings.key == "wechat_conf").first()
            if wechat:
                wechat.value = json.dumps(settings["wechat_conf"])
            else:
                db.add(Settings(key="wechat_conf", value=json.dumps(settings["wechat_conf"])))
        
        # Update Webhook config
        if "webhook_conf" in settings:
            webhook = db.query(Settings).filter(Settings.key == "webhook_conf").first()
            if webhook:
                webhook.value = json.dumps(settings["webhook_conf"])
            else:
                db.add(Settings(key="webhook_conf", value=json.dumps(settings["webhook_conf"])))
        
        # Update global days
        if "global_days" in settings:
            global_days = db.query(Settings).filter(Settings.key == "global_days").first()
            if global_days:
                global_days.value = json.dumps(settings["global_days"])
            else:
                db.add(Settings(key="global_days", value=json.dumps(settings["global_days"])))
        
        # Update global time
        if "global_time" in settings:
            global_time = db.query(Settings).filter(Settings.key == "global_time").first()
            if global_time:
                global_time.value = settings["global_time"]
            else:
                db.add(Settings(key="global_time", value=settings["global_time"]))
        
        db.commit()
        return {"message": "Settings updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))