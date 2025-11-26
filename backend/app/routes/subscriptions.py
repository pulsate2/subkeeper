from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Subscription
from ..schemas import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse

router = APIRouter()

@router.get("/", response_model=List[SubscriptionResponse])
async def get_subscriptions(db: Session = Depends(get_db)):
    """Get all subscriptions"""
    return db.query(Subscription).all()

@router.get("/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Get a specific subscription"""
    sub = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub

@router.post("/", response_model=SubscriptionResponse)
async def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    """Create a new subscription"""
    db_sub = Subscription(**subscription.dict())
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

@router.put("/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(subscription_id: int, subscription: SubscriptionUpdate, db: Session = Depends(get_db)):
    """Update a subscription"""
    db_sub = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    update_data = subscription.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sub, field, value)
    
    db.commit()
    db.refresh(db_sub)
    return db_sub

@router.delete("/{subscription_id}")
async def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Delete a subscription"""
    db_sub = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(db_sub)
    db.commit()
    return {"message": "Subscription deleted successfully"}
