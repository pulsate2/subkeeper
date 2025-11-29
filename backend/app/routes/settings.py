from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from typing import Dict
from ..database import get_db
from ..models import Settings
from ..auth import verify_token
from ..notifier import Notifier

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
    
    # Get Resend config
    resend = db.query(Settings).filter(Settings.key == "resend_conf").first()
    settings_dict["resend_conf"] = json.loads(resend.value) if resend else None
    
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
        
        # Update Resend config
        if "resend_conf" in settings:
            resend = db.query(Settings).filter(Settings.key == "resend_conf").first()
            if resend:
                resend.value = json.dumps(settings["resend_conf"])
            else:
                db.add(Settings(key="resend_conf", value=json.dumps(settings["resend_conf"])))
        
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

@router.post("/test/{notification_type}")
async def test_notification(
    notification_type: str, 
    config: Dict = None,
    db: Session = Depends(get_db), 
    current_user: str = Depends(verify_token)
):
    """Test notification configuration with provided config"""
    try:
        test_title = "测试通知"
        test_content = "这是一条测试通知，用于验证您的通知配置是否正确。"
        
        result = {"success": False, "message": ""}
        
        if notification_type == "smtp":
            if config and config.get('host'):
                # Create temporary notifier with provided config
                temp_notifier = Notifier(db)
                temp_notifier.smtp_config = config
                success = temp_notifier.send_email(test_title, test_content)
                if success:
                    result = {"success": True, "message": "SMTP 邮件测试成功"}
                else:
                    result = {"success": False, "message": "SMTP 邮件测试失败，请检查配置"}
            else:
                result = {"success": False, "message": "SMTP 配置不完整"}
                
        elif notification_type == "wechat":
            if config and config.get('corpid'):
                temp_notifier = Notifier(db)
                temp_notifier.wechat_config = config
                success = temp_notifier.send_wechat(test_title, test_content)
                if success:
                    result = {"success": True, "message": "企业微信测试成功"}
                else:
                    result = {"success": False, "message": "企业微信测试失败，请检查配置"}
            else:
                result = {"success": False, "message": "企业微信配置不完整"}
                
        elif notification_type == "webhook":
            if config and config.get('webhook_key'):
                temp_notifier = Notifier(db)
                temp_notifier.webhook_config = config
                temp_notifier.send_webhook_notification(test_title, test_content)
                result = {"success": True, "message": "企业微信 Webhook 测试成功"}
            else:
                result = {"success": False, "message": "Webhook 配置不完整"}
                
        elif notification_type == "resend":
            if config and config.get('api_key'):
                temp_notifier = Notifier(db)
                temp_notifier.resend_config = config
                success = temp_notifier.send_resend(test_title, test_content)
                if success:
                    result = {"success": True, "message": "Resend 邮件测试成功"}
                else:
                    result = {"success": False, "message": "Resend 邮件测试失败，请检查配置"}
            else:
                result = {"success": False, "message": "Resend 配置不完整"}
        else:
            raise HTTPException(status_code=400, detail="Invalid notification type")
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))