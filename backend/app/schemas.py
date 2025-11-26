from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class SubscriptionBase(BaseModel):
    name: str
    price: float
    cycle_val: int
    cycle_unit: str  # 'day', 'week', 'month', or 'year'
    next_date: date
    notify_mode: str = 'global'  # 'global' or 'custom'
    cust_days: Optional[str] = None
    cust_time: Optional[str] = None
    group_name: str = 'default'

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
    group_name: str = 'default'

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