# app/routers/leaderboard.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import SessionLocal
from app.models.leaderboard import Leaderboard

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/leaderboard/global", summary="Get global leaderboard")
def get_global_leaderboard(db: Session = Depends(get_db)):
    # Query the Leaderboard table and sort by score in descending order.
    leaderboard_entries = db.query(Leaderboard).order_by(desc(Leaderboard.score)).all()
    results = []
    for entry in leaderboard_entries:
        results.append({
            "user_id": entry.user_id,
            "username": entry.user.username if entry.user else "",
            "score": entry.score,
            "last_updated": entry.last_updated.isoformat()
        })
    return results
