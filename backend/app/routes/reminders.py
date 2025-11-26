from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Reminder
from ..schemas import ReminderCreate, ReminderUpdate, ReminderResponse
from ..auth import verify_token

router = APIRouter()

@router.get("/", response_model=List[ReminderResponse])
async def get_reminders(db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Get all reminders"""
    return db.query(Reminder).all()


@router.get("/groups", response_model=List[str])
async def get_reminder_groups(db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Get all unique reminder groups"""
    groups = db.query(Reminder.group_name).distinct().all()
    return [group[0] for group in groups if group[0] is not None]

@router.get("/{reminder_id}", response_model=ReminderResponse)
async def get_reminder(reminder_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Get a specific reminder"""
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder

@router.post("/", response_model=ReminderResponse)
async def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Create a new reminder"""
    db_reminder = Reminder(**reminder.dict())
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.put("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(reminder_id: int, reminder: ReminderUpdate, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Update a reminder"""
    db_reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    update_data = reminder.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reminder, field, value)
    
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.delete("/{reminder_id}")
async def delete_reminder(reminder_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Delete a reminder"""
    db_reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    db.delete(db_reminder)
    db.commit()
    return {"message": "Reminder deleted successfully"}
