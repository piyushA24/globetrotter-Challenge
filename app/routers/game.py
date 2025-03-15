import uuid, random, time
from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.models.destination import Destination
from app.dependencies import get_current_user
from app.services.leaderboard_service import update_user_leaderboard

router = APIRouter()

# In-memory session store (for hackathon/demo purposes)
sessions = {}

class GameSession:
    def __init__(self, questions):
        self.session_id = str(uuid.uuid4())
        self.questions = questions  # Each question now includes dynamic options
        self.current_index = 0
        self.score = 0
        self.answers = []  # Record user responses

def get_random_destinations(num: int = 10, db: Session = None):
    if db is None:
        db = SessionLocal()
    # Randomly order destinations and limit the number
    destinations = db.query(Destination).order_by(func.random()).limit(num).all()
    dest_list = []
    for dest in destinations:
        dest_list.append({
            "destination_id": dest.id,
            "city": dest.city,
            "country": dest.country,
            "clues": dest.clues,
            "fun_fact": dest.fun_fact,
            "trivia": dest.trivia,
            "options": []  # to be set later
        })
    return dest_list

def get_wrong_options(correct_id: int, db: Session = None, num_options: int = 3):
    if db is None:
        db = SessionLocal()
    # Query three random cities excluding the correct destination
    wrong_options = (
        db.query(Destination.city)
        .filter(Destination.id != correct_id)
        .order_by(func.random())
        .limit(num_options)
        .all()
    )
    # wrong_options is a list of tuples, so extract the city from each tuple
    return [row.city for row in wrong_options]

@router.post("/game/session/start", summary="Start a new game session (10 questions)")
def start_game_session(current_user: int = Depends(get_current_user)):
    db = SessionLocal()
    try:
        questions = get_random_destinations(10, db=db)
        if len(questions) < 10:
            raise HTTPException(status_code=500, detail="Not enough questions available")
        for q in questions:
            correct = q["city"]
            wrong_options = get_wrong_options(q["destination_id"], db=db, num_options=3)
            options = [correct] + wrong_options
            random.shuffle(options)
            q["options"] = options
        session = GameSession(questions)
        sessions[session.session_id] = session
        return {
            "session_id": session.session_id,
            "question": session.questions[0]
        }
    finally:
        db.close()

@router.get("/game/session/{session_id}/question", summary="Get current question in session")
def get_current_question(session_id: str, current_user: int = Depends(get_current_user)):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.current_index >= len(session.questions):
        raise HTTPException(status_code=400, detail="Session completed")
    return {"question": session.questions[session.current_index]}

class SessionAnswer(BaseModel):
    destination_id: int  # Must match the question's destination_id
    selected_option: str  # The chosen option from the provided list
    hint_used: bool = False

@router.post("/game/session/{session_id}/submit", summary="Submit answer for current session question")
def submit_session_answer(session_id: str, answer: SessionAnswer, current_user: int = Depends(get_current_user)):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.current_index >= len(session.questions):
        raise HTTPException(status_code=400, detail="Session already completed")

    current_question = session.questions[session.current_index]
    if int(current_question.get("destination_id")) != answer.destination_id:
        raise HTTPException(
            status_code=400,
            detail="This question has already been answered or an invalid submission was made."
        )

    correct_city = current_question.get("city", "").strip().lower()
    selected_option = answer.selected_option.strip().lower()

    is_correct = (selected_option == correct_city)
    points = 10 if is_correct and not answer.hint_used else 5 if is_correct and answer.hint_used else 0

    session.score += points
    session.answers.append({
        "question": current_question,
        "selected_option": answer.selected_option,
        "correct": is_correct,
        "points": points
    })

    fun_fact = current_question.get("fun_fact", [""])[0]
    if is_correct:
        feedback_text = f"🎉 Correct Answer, \nFun Fact: {fun_fact}"
    else:
        correct_answer = current_question.get("city", "Unknown")
        feedback_text = f"😢 Incorrect Answer, \nCorrect Answer: {correct_answer}, \nFun Fact: {fun_fact}"

    feedback = {
        "correct": is_correct,
        "feedback_text": feedback_text,
        "points_awarded": points,
        "current_score": session.score
    }

    session.current_index += 1
    if session.current_index < len(session.questions):
        feedback["next_question"] = session.questions[session.current_index]
    else:
        feedback["message"] = "Game session completed"
        update_user_leaderboard(current_user, session.score)
        feedback["final_score"] = session.score

    return feedback
