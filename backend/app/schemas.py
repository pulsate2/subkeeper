from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class SettingsBase(BaseModel):
    smtp_conf: Optional[dict] = None
    wechat_conf: Optional[dict] = None
    global_days: List[int] = [3, 1, 0]
    global_time: str = "09:00"

class SubscriptionBase(BaseModel):
    name: str
    price: float
    cycle_val: int
    cycle_unit: str  # 'month' or 'year'
    next_date: date
    notify_mode: str = 'global'  # 'global' or 'custom'
    cust_days: Optional[str] = None
    cust_time: Optional[str] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    pass

class SubscriptionResponse(SubscriptionBase):
    id: int
    last_sent: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ReminderBase(BaseModel):
    title: str
    content: Optional[str] = None  # 添加内容字段
    target_date: date
    target_time: str  # HH:MM format

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(ReminderBase):
    pass

class ReminderResponse(ReminderBase):
    id: int
    is_sent: bool
    
    class Config:
        from_attributes = True

class BackupData(BaseModel):
    meta: dict
    settings: dict
    subscriptions: List[dict]
    reminders: List[dict]