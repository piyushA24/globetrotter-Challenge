# app/models/destination.py
from sqlalchemy import Column, Integer, String, JSON
from app.core.database import Base

class Destination(Base):
    __tablename__ = "destinations"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, unique=True, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)
    clues = Column(JSON, nullable=False)      # Store as JSON if your PostgreSQL supports it
    fun_fact = Column(JSON, nullable=False)
    trivia = Column(JSON)
    options = Column(JSON)
