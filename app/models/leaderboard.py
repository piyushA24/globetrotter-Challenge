# app/models/leaderboard.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Leaderboard(Base):
    __tablename__ = "leaderboards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    score = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Link to the user model
    user = relationship("User", back_populates="leaderboard")
