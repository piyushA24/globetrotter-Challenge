# # tests/test_api.py
# import pytest
# import uuid
# from fastapi.testclient import TestClient
# from sqlalchemy import text
#
# from app.core.database import SessionLocal
# from app.main import app
# import json
#
# client = TestClient(app)
#
#
# # --- Fixture: Clear in-memory sessions between tests ---
# @pytest.fixture(autouse=True)
# def clear_sessions():
#     from app.routers import game
#     game.sessions.clear()
#
#
# # --- Fixture: Clear the users table in PostgreSQL before each test ---
# @pytest.fixture(autouse=True)
# def clear_users():
#     db = SessionLocal()
#     # Wrap the SQL statement with text() to avoid the ArgumentError.
#     db.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
#     db.commit()
#     db.close()
#
#
# # --- Fake OpenSearch Client Fixture for Testing ---
# @pytest.fixture(autouse=True)
# def fake_opensearch(monkeypatch):
#     from app.services import opensearch_service
#
#     class FakeOpenSearchClient:
#         def search(self, index, body):
#             # For random destination query, always return one predictable document.
#             return {
#                 "hits": {
#                     "hits": [
#                         {
#                             "_id": "1",
#                             "_source": {
#                                 "city": "Paris",
#                                 "country": "France",
#                                 "clues": ["This city is home to a famous tower.", "Known as the City of Love."],
#                                 "fun_fact": ["The Eiffel Tower was meant to be temporary."],
#                                 "trivia": ["Originally called Lutetia."],
#                                 "destination_id": "1"
#                             }
#                         }
#                     ]
#                 }
#             }
#
#         def get(self, index, id):
#             if str(id) == "1":
#                 return {
#                     "_source": {
#                         "city": "Paris",
#                         "country": "France",
#                         "clues": ["This city is home to a famous tower.", "Known as the City of Love."],
#                         "fun_fact": ["The Eiffel Tower was meant to be temporary."],
#                         "trivia": ["Originally called Lutetia."],
#                         "destination_id": "1"
#                     }
#                 }
#             raise Exception("Not found")
#
#         def index(self, index, id, body):
#             return {"result": "created"}
#
#         # Simulate index existence check
#         class Indices:
#             def exists(self, index):
#                 return True
#
#             def create(self, index, body):
#                 return {"acknowledged": True}
#
#         @property
#         def indices(self):
#             return FakeOpenSearchClient.Indices()
#
#     monkeypatch.setattr(opensearch_service, "get_opensearch_client", lambda: FakeOpenSearchClient())
#
#
# # --- Root Endpoint Test ---
# def test_read_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Welcome to Globetrotter Challenge!"}
#
#
# # --- User Registration Tests ---
# def test_register_user_success():
#     unique_email = f"user1_{uuid.uuid4()}@example.com"
#     unique_username = f"user1_{uuid.uuid4()}"
#     payload = {
#         "email": unique_email,
#         "username": unique_username,
#         "password": "securepassword"
#     }
#     response = client.post("/auth/register", json=payload)
#     assert response.status_code == 200
#     data = response.json()
#     assert "user_id" in data
#     assert data["username"] == unique_username
#
#
# def test_register_user_duplicate_email():
#     # First register a user with a fixed email
#     payload = {
#         "email": "duplicate@example.com",
#         "username": f"uniqueuser_{uuid.uuid4()}",
#         "password": "password123"
#     }
#     response = client.post("/auth/register", json=payload)
#     assert response.status_code == 200
#
#     # Attempt to register with the same email but a different username
#     payload2 = {
#         "email": "duplicate@example.com",
#         "username": f"anotheruser_{uuid.uuid4()}",
#         "password": "password456"
#     }
#     response = client.post("/auth/register", json=payload2)
#     assert response.status_code == 400
#     data = response.json()
#     assert data["detail"] == "Email already exists"
#
#
# def test_register_user_duplicate_username():
#     # First register a user with a fixed username
#     fixed_username = f"duplicateuser_{uuid.uuid4()}"
#     payload = {
#         "email": f"uniqueemail_{uuid.uuid4()}@example.com",
#         "username": fixed_username,
#         "password": "password123"
#     }
#     response = client.post("/auth/register", json=payload)
#     assert response.status_code == 200
#
#     # Attempt to register with the same username but a different email
#     payload2 = {
#         "email": f"anotheremail_{uuid.uuid4()}@example.com",
#         "username": fixed_username,
#         "password": "password456"
#     }
#     response = client.post("/auth/register", json=payload2)
#     assert response.status_code == 400
#     data = response.json()
#     assert data["detail"] == "Username already exists"
#
#
# # --- Game Session Flow Tests ---
# # def test_game_session_flow():
# #     # 1. Start a new game session
# #     response = client.post("/game/session/start")
# #     assert response.status_code == 200
# #     session_data = response.json()
# #     session_id = session_data.get("session_id")
# #     first_question = session_data.get("question")
# #     assert session_id is not None
# #     assert first_question is not None
# #     first_destination_id = first_question.get("destination_id")
# #
# #     # 2. Get current question using session_id
# #     response = client.get(f"/game/session/{session_id}/question")
# #     assert response.status_code == 200
# #     current_question = response.json().get("question")
# #     print(current_question)
# #     assert current_question.get("destination_id") == first_destination_id
# #
# #     # 3. Submit an answer for the first question
# #     answer_payload = {
# #         "destination_id": first_destination_id,  # Must match current question's id
# #         "user_answer": current_question["city"],
# #         "hint_used": False
# #     }
# #     response = client.post(f"/game/session/{session_id}/submit", json=answer_payload)
# #     assert response.status_code == 200
# #     feedback = response.json()
# #     # Expect correct answer since "Paris" is correct.
# #     assert feedback["correct"] is True
# #     assert feedback["points_awarded"] == 10  # Full points for correct answer without hint
# #     # Now current question index should have advanced
# #     if "next_question" in feedback:
# #         next_question = feedback["next_question"]
# #         assert next_question is not None
# #
# #     # 4. Attempt duplicate submission for the same question
# #     duplicate_response = client.post(f"/game/session/{session_id}/submit", json=answer_payload)
# #     assert duplicate_response.status_code == 400
# #     duplicate_data = duplicate_response.json()
# #     assert "already been answered" in duplicate_data["detail"]
# #
# #     # 5. Simulate answering remaining questions to complete session
# #     for _ in range(9):  # Already answered 1 question, so answer remaining 9
# #         res = client.get(f"/game/session/{session_id}/question")
# #         # If session is completed, break out of loop
# #         if res.status_code != 200:
# #             break
# #         current = res.json()["question"]
# #         payload = {
# #             "destination_id": current.get("destination_id"),
# #             "user_answer": "Paris",  # Fake answer, always correct based on our fake data
# #             "hint_used": False
# #         }
# #         _ = client.post(f"/game/session/{session_id}/submit", json=payload)
# #         # Not asserting on each iteration
# #
# #     # After 10 submissions, session should be completed
# #     final_response = client.get(f"/game/session/{session_id}/question")
# #     assert final_response.status_code == 400
#
#
# def test_option_based_game_flow():
#     # Start a new session
#     response = client.post("/game/session/start")
#     assert response.status_code == 200
#     session_data = response.json()
#     session_id = session_data["session_id"]
#     question = session_data["question"]
#     assert "options" in question
#     assert isinstance(question["options"], list)
#     # Assume the correct answer is in the options
#     correct_option = question["city"]
#     assert correct_option in question["options"]
#
#     # Submit the correct answer
#     payload = {
#         "destination_id": question["destination_id"],
#         "selected_option": correct_option,
#         "hint_used": False
#     }
#     response = client.post(f"/game/session/{session_id}/submit", json=payload)
#     assert response.status_code == 200
#     feedback = response.json()
#     assert feedback["correct"] is True
#     # The next question should also have options
#     if "next_question" in feedback:
#         next_question = feedback["next_question"]
#         assert "options" in next_question
#
#
# # --- Challenge Endpoints Tests ---
# def test_challenge_endpoints():
#     # First, register a new user so we have a valid inviter
#     unique_email = f"challenge_{uuid.uuid4()}@example.com"
#     unique_username = f"challenge_{uuid.uuid4()}"
#     reg_payload = {
#         "email": unique_email,
#         "username": unique_username,
#         "password": "password123"
#     }
#     reg_response = client.post("/auth/register", json=reg_payload)
#     assert reg_response.status_code == 200
#     user_data = reg_response.json()
#     inviter_id = user_data["user_id"]
#
#     # Now, get challenge details for the newly registered user
#     response = client.get(f"/challenge/{inviter_id}")
#     assert response.status_code == 200
#     challenge_details = response.json()
#     assert "share_link" in challenge_details
#     # Our dummy score is always 50 for challenge endpoints
#     assert challenge_details["score"] == 50
#
#     # Test updating challenge result when friend's score beats inviter's score
#     payload = {
#         "inviter_id": inviter_id,
#         "friend_score": 60
#     }
#     response = client.post("/challenge/update", json=payload)
#     assert response.status_code == 200
#     update_result = response.json()
#     assert "beat" in update_result["message"]
#
#     # Test updating challenge result when friend's score does not beat inviter's score
#     payload["friend_score"] = 40
#     response = client.post("/challenge/update", json=payload)
#     assert response.status_code == 200
#     update_result = response.json()
#     assert "did not beat" in update_result["message"] or "No notification" in update_result["message"]
#
#
# def test_global_leaderboard():
#     # First, register a new user and simulate a leaderboard update.
#     unique_email = f"leader_{uuid.uuid4()}@example.com"
#     unique_username = f"leader_{uuid.uuid4()}"
#     reg_payload = {
#         "email": unique_email,
#         "username": unique_username,
#         "password": "password123"
#     }
#     reg_response = client.post("/auth/register", json=reg_payload)
#     assert reg_response.status_code == 200
#     user_data = reg_response.json()
#     user_id = user_data["user_id"]
#
#     # Simulate updating the user's leaderboard score
#     from app.services import leaderboard_service
#     leaderboard_service.update_user_leaderboard(user_id, 80)
#
#     # Get the global leaderboard
#     response = client.get("/leaderboard/global")
#     assert response.status_code == 200
#     leaderboard_data = response.json()
#     # Check that our user appears in the leaderboard
#     matching = [entry for entry in leaderboard_data if entry["user_id"] == user_id]
#     assert len(matching) == 1
#     assert matching[0]["score"] == 80
