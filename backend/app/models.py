from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, Text
from sqlalchemy.dialects.sqlite import JSON
from .database import Base

class Settings(Base):
    __tablename__ = "settings"
    
    key = Column(String, primary_key=True, index=True)
    value = Column(Text, nullable=False)

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    cycle_val = Column(Integer, nullable=False)
    cycle_unit = Column(String, nullable=False)  # 'month' or 'year'
    next_date = Column(Date, nullable=False)
    notify_mode = Column(String, default='global')  # 'global' or 'custom'
    cust_days = Column(Text, nullable=True)  # JSON string for custom days
    cust_time = Column(String, nullable=True)  # HH:MM format for custom time
    last_sent = Column(DateTime, nullable=True)

class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)  # 添加内容字段
    target_date = Column(Date, nullable=False)
    target_time = Column(String, nullable=False)  # HH:MM format
    is_sent = Column(Boolean, default=False)
