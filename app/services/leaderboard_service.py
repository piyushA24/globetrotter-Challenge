# app/services/leaderboard_service.py
from app.core.database import SessionLocal
from app.models.leaderboard import Leaderboard

def update_user_leaderboard(user_id: int, new_score: int):
    db = SessionLocal()
    try:
        entry = db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()
        if entry:
            # For simplicity, assume new_score replaces old score.
            # Alternatively, you might accumulate scores or use a more complex algorithm.
            entry.score = new_score
        else:
            entry = Leaderboard(user_id=user_id, score=new_score)
            db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()
