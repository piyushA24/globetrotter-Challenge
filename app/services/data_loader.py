import json
import os
from app.core.database import SessionLocal, engine, Base
from app.models.destination import Destination
from app.models.user import User
from sqlalchemy.exc import IntegrityError

def load_destination_data(json_file_path: str):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def insert_data_into_postgres():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Build the path to your JSON file using a relative path.
        # Adjust the relative path based on your project structure.
        json_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data", "destination_info.json"
        )
        data = load_destination_data(json_file_path)
        print(data[0:10])
        for idx, doc in enumerate(data):
            destination = Destination(
                city=doc.get("city"),
                country=doc.get("country"),
                clues=doc.get("clues"),
                fun_fact=doc.get("fun_fact"),
                trivia=doc.get("trivia"),
                options=doc.get("options")
            )
            db.add(destination)
        db.commit()
        print("Inserted destination data into PostgreSQL for destination.")
    except Exception as e:
        db.rollback()
        print("Error inserting destination data:", e)
    finally:
        db.close()

def insert_dummy_user():
    db = SessionLocal()
    # Create a dummy user for testing PostgreSQL insertion.
    dummy_user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="fakehashedpassword"
    )
    try:
        db.add(dummy_user)
        db.commit()
        db.refresh(dummy_user)
        print("Inserted dummy user:", dummy_user.username)
    except IntegrityError:
        db.rollback()
        print("Dummy user already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    print("Inserting destination data into PostgreSQL...")
    insert_data_into_postgres()
    insert_dummy_user()
    # Optionally, insert a dummy user:
    # insert_dummy_user()
