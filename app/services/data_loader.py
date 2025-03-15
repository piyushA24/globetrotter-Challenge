import json
import os
from app.services.opensearch_service import get_opensearch_client, create_index_if_not_exists
from app.core.config import OPENSEARCH_INDEX
from app.core.database import SessionLocal
from app.models.user import User
from sqlalchemy.exc import IntegrityError


def load_destination_data(json_file_path: str):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def insert_data_into_opensearch():
    client = get_opensearch_client()
    create_index_if_not_exists(client)

    # Build the path to your JSON file (data/destination_info.json)
    json_file_path = os.path.join("data", "destination_info.json")
    data = load_destination_data(json_file_path)

    for idx, doc in enumerate(data):
        response = client.index(index=OPENSEARCH_INDEX, id=idx + 1, body=doc)
        print(f"Inserted document {idx + 1}: {response['result']}")


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
    print("Inserting destination data into OpenSearch...")
    insert_data_into_opensearch()

    print("Inserting a dummy user into PostgreSQL...")
    insert_dummy_user()
