from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.notification import Notification
from app.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/notifications", summary="Get notifications for current user")
def get_notifications(current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.user_id == current_user).order_by(Notification.created_at.desc()).all()
    return notifications

@router.post("/notifications/{notification_id}/read", summary="Mark a notification as read and delete it")
def mark_notification_as_read(notification_id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == current_user).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted"}
