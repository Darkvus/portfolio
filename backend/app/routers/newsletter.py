import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Subscriber
from ..schemas import SubscribeRequest, SubscribeOut, SubscriberOut
from ..auth import get_current_admin

router = APIRouter(prefix="/newsletter", tags=["newsletter"])

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@router.post("/subscribe", response_model=SubscribeOut, status_code=201)
def subscribe(data: SubscribeRequest, db: Session = Depends(get_db)):
    if not EMAIL_RE.match(data.email):
        raise HTTPException(status_code=422, detail="Invalid email address")
    exists = db.query(Subscriber).filter(Subscriber.email == data.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="Already subscribed")
    db.add(Subscriber(email=data.email))
    db.commit()
    return SubscribeOut(message="Subscribed successfully")


@router.get("/subscribers", response_model=List[SubscriberOut])
def list_subscribers(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    return db.query(Subscriber).order_by(Subscriber.created_at.desc()).all()


@router.delete("/subscribers/{subscriber_id}", status_code=204)
def delete_subscriber(
    subscriber_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    sub = db.query(Subscriber).filter(Subscriber.id == subscriber_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    db.delete(sub)
    db.commit()
