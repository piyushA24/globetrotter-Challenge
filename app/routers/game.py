import uuid, random
from fastapi import APIRouter, HTTPException, Path, Depends
from pydantic import BaseModel
from app.services.opensearch_service import get_opensearch_client
from app.core.config import OPENSEARCH_INDEX
from app.dependencies import get_current_user
from app.services.leaderboard_service import update_user_leaderboard
import time
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


def get_random_destinations(num: int = 10):
    client = get_opensearch_client()
    query = {
        "query": {
            "function_score": {
                "query": {"match_all": {}},
                "random_score": {}
            }
        },
        "size": num
    }
    response = client.search(index=OPENSEARCH_INDEX, body=query)
    hits = response.get("hits", {}).get("hits", [])
    destinations = []
    for hit in hits:
        doc = hit["_source"]
        doc["destination_id"] = hit["_id"]
        destinations.append(doc)
    return destinations


def get_wrong_options(correct_id: str, num_options: int = 3):
    client = get_opensearch_client()
    seed = int(time.time() * 1000)  # More granular seed
    query = {
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "must_not": [
                            {"term": {"_id": correct_id}}
                        ]
                    }
                },
                "random_score": {"seed": seed}
            }
        },
        "size": num_options
    }
    response = client.search(index=OPENSEARCH_INDEX, body=query)
    hits = response.get("hits", {}).get("hits", [])
    wrong_options = [hit["_source"]["city"] for hit in hits]
    return wrong_options


@router.post("/game/session/start", summary="Start a new game session (10 questions)")
def start_game_session(current_user: int = Depends(get_current_user)):
    questions = get_random_destinations(10)
    if len(questions) < 10:
        raise HTTPException(status_code=500, detail="Not enough questions available")
    for q in questions:
        correct = q["city"]
        wrong_options = get_wrong_options(q["destination_id"], 3)
        options = [correct] + wrong_options
        random.shuffle(options)
        q["options"] = options
    session = GameSession(questions)
    sessions[session.session_id] = session
    print(session.session_id,)
    print(session.questions[0])
    return {
        "session_id": session.session_id,
        "question": session.questions[0]
    }


@router.get("/game/session/{session_id}/question", summary="Get current question in session")
def get_current_question(session_id: str = Path(...), current_user: int = Depends(get_current_user)):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.current_index >= len(session.questions):
        raise HTTPException(status_code=400, detail="Session completed")
    print(session.questions[session.current_index])

    return {"question": session.questions[session.current_index]}


class SessionAnswer(BaseModel):
    destination_id: str  # Must match the question's destination_id
    selected_option: str  # The chosen option from the provided list
    hint_used: bool = False


# @router.post("/game/session/{session_id}/submit", summary="Submit answer for current session question")
# def submit_session_answer(session_id: str, answer: SessionAnswer, current_user: int = Depends(get_current_user)):
#     session = sessions.get(session_id)
#     if not session:
#         raise HTTPException(status_code=404, detail="Session not found")
#     if session.current_index >= len(session.questions):
#         raise HTTPException(status_code=400, detail="Session already completed")
#
#     current_question = session.questions[session.current_index]
#     if str(current_question.get("destination_id")) != str(answer.destination_id):
#         raise HTTPException(
#             status_code=400,
#             detail="This question has already been answered or an invalid submission was made."
#         )
#
#     correct_city = current_question.get("city", "").strip().lower()
#     selected_option = answer.selected_option.strip().lower()
#
#     is_correct = (selected_option == correct_city)
#     points = 10 if is_correct and not answer.hint_used else 5 if is_correct and answer.hint_used else 0
#
#     session.score += points
#     session.answers.append({
#         "question": current_question,
#         "selected_option": answer.selected_option,
#         "correct": is_correct,
#         "points": points
#     })
#
#     feedback = {
#         "correct": is_correct,
#         "fun_fact": current_question.get("fun_fact", [""])[0],
#         "points_awarded": points,
#         "current_score": session.score
#     }
#
#     session.current_index += 1
#     if session.current_index < len(session.questions):
#         feedback["next_question"] = session.questions[session.current_index]
#     else:
#         feedback["message"] = "Game session completed"
#         # Update leaderboard with final score for the current user.
#         update_user_leaderboard(current_user, session.score)
#         feedback["final_score"] = session.score
#
#     return feedback
@router.post("/game/session/{session_id}/submit", summary="Submit answer for current session question")
def submit_session_answer(session_id: str, answer: SessionAnswer, current_user: int = Depends(get_current_user)):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.current_index >= len(session.questions):
        raise HTTPException(status_code=400, detail="Session already completed")

    current_question = session.questions[session.current_index]
    if str(current_question.get("destination_id")) != str(answer.destination_id):
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

    # Get the fun fact; fallback to empty string if not available
    fun_fact = current_question.get("fun_fact", [""])[0]

    # Build feedback text with emojis and correct answer (if needed)
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
        print("===========")
        print(current_user,session.score)
        update_user_leaderboard(current_user, session.score)
        feedback["final_score"] = session.score

    print(feedback)

    return feedback
