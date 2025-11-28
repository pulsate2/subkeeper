import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Subscription
from ..schemas import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from ..auth import verify_token

router = APIRouter()

@router.get("/", response_model=List[SubscriptionResponse])
async def get_subscriptions(db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Get all subscriptions"""
    return db.query(Subscription).all()


@router.get("/groups", response_model=List[str])
async def get_subscription_groups(db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Get all unique subscription groups"""
    groups = db.query(Subscription.group_name).distinct().all()
    return [group[0] for group in groups if group[0] is not None]

@router.get("/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(subscription_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Get a specific subscription"""
    sub = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub

def process_cust_days(cust_days):
    """Process and convert cust_days to proper JSON string format"""
    if cust_days is None:
        return None
    
    if isinstance(cust_days, list):
        # If it's already a list, convert to JSON string
        return json.dumps(cust_days)
    elif isinstance(cust_days, str):
        # If it's a string, try to parse as JSON first
        try:
            parsed = json.loads(cust_days)
            if isinstance(parsed, list):
                return cust_days  # Already proper JSON
            else:
                # If parsed JSON is not a list, handle as comma-separated string
                if ',' in cust_days:
                    days_str = cust_days.split(',')
                    days_list = [int(day.strip()) for day in days_str if day.strip().lstrip('-').isdigit()]
                    return json.dumps(days_list)
                else:
                    return json.dumps([])  # Return empty array if not valid
        except json.JSONDecodeError:
            # If not valid JSON, handle as comma-separated string
            if ',' in cust_days:
                days_str = cust_days.split(',')
                days_list = [int(day.strip()) for day in days_str if day.strip().lstrip('-').isdigit()]
                return json.dumps(days_list)
            elif cust_days.strip().lstrip('-').isdigit():
                return json.dumps([int(cust_days.strip())])
            else:
                return json.dumps([])  # Return empty array if not valid
    else:
        return json.dumps([])  # Return empty array if not valid type

@router.post("/", response_model=SubscriptionResponse)
async def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Create a new subscription"""
    # Process cust_days to ensure proper JSON format
    subscription_dict = subscription.dict()
    subscription_dict['cust_days'] = process_cust_days(subscription_dict.get('cust_days'))
    
    db_sub = Subscription(**subscription_dict)
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

@router.put("/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(subscription_id: int, subscription: SubscriptionUpdate, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Update a subscription"""
    db_sub = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    update_data = subscription.dict(exclude_unset=True)
    
    # Process cust_days to ensure proper JSON format
    if 'cust_days' in update_data:
        update_data['cust_days'] = process_cust_days(update_data['cust_days'])
    
    for field, value in update_data.items():
        setattr(db_sub, field, value)
    
    db.commit()
    db.refresh(db_sub)
    return db_sub

@router.delete("/{subscription_id}")
async def delete_subscription(subscription_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Delete a subscription"""
    db_sub = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(db_sub)
    db.commit()
    return {"message": "Subscription deleted successfully"}

@router.post("/{subscription_id}/renew")
async def renew_subscription(subscription_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    """Manually trigger next billing cycle for a subscription"""
    db_sub = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Calculate next date based on cycle
    from datetime import timedelta
    from dateutil.relativedelta import relativedelta
    
    if db_sub.cycle_unit == 'day':
        db_sub.next_date = db_sub.next_date + timedelta(days=db_sub.cycle_val)
    elif db_sub.cycle_unit == 'week':
        db_sub.next_date = db_sub.next_date + timedelta(weeks=db_sub.cycle_val)
    elif db_sub.cycle_unit == 'month':
        db_sub.next_date = db_sub.next_date + relativedelta(months=db_sub.cycle_val)
    elif db_sub.cycle_unit == 'year':
        db_sub.next_date = db_sub.next_date + relativedelta(years=db_sub.cycle_val)
    
    # Reset last_sent to allow notifications for the new cycle
    db_sub.last_sent = None
    
    db.commit()
    db.refresh(db_sub)
    return db_sub
