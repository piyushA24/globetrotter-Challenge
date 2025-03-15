from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.leaderboard import Leaderboard
from app.models.notification import Notification
from pydantic import BaseModel
import os
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/challenge/{inviter_id}", summary="Get challenge details for an inviter")
def get_challenge_details(inviter_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == inviter_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Inviter not found")

    lb_entry = db.query(Leaderboard).filter(Leaderboard.user_id == inviter_id).first()
    inviter_score = lb_entry.score if lb_entry else 0

    # Use the FRONTEND_URL environment variable if set; otherwise, default to the static UI
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8000/static/index.html")
    share_link = f"{frontend_url}?inviter_id={inviter_id}"

    return {
        "inviter_id": inviter_id,
        "username": user.username,
        "score": inviter_score,
        "share_link": share_link
    }

class ChallengeResult(BaseModel):
    inviter_id: int
    friend_id: int
    friend_score: int


@router.post("/challenge/update", summary="Update challenge result and notify both parties")
def update_challenge_result(result: ChallengeResult, db: Session = Depends(get_db)):
    # Fetch inviter data and score.
    inviter = db.query(User).filter(User.id == result.inviter_id).first()
    if not inviter:
        raise HTTPException(status_code=404, detail="Inviter not found")
    lb_entry = db.query(Leaderboard).filter(Leaderboard.user_id == result.inviter_id).first()
    inviter_score = lb_entry.score if lb_entry else 0

    # Fetch friend data.
    friend = db.query(User).filter(User.id == result.friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    messages = {}
    if result.friend_score > inviter_score:
        # Create notification for inviter.
        message_for_inviter = (
            f"Your friend {friend.username} beat your score! "
            f"Your score: {inviter_score}, Friend's score: {result.friend_score}"
        )
        notif_inviter = Notification(user_id=result.inviter_id, message=message_for_inviter)
        db.add(notif_inviter)

        # Create notification for friend.
        message_for_friend = (
            f"You beat your friend {inviter.username}! "
            f"Your score: {result.friend_score}, Friend's score: {inviter_score}"
        )
        notif_friend = Notification(user_id=result.friend_id, message=message_for_friend)
        db.add(notif_friend)

        db.commit()
        messages["inviter_message"] = message_for_inviter
        messages["friend_message"] = message_for_friend
        return {"message": messages}
    return {"message": "No notification. Friend did not beat your score."}
