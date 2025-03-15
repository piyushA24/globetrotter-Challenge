# import os
# import json
# from app.core.database import SessionLocal, engine, Base
# from app.models.destination import Destination  # Adjust based on your actual model
#
# # Create tables if they don't exist
# Base.metadata.create_all(bind=engine)
#
#
# def load_data():
#     session = SessionLocal()
#     try:
#         # Optional: Check if data already exists
#         if session.query(Destination).first():
#             print("Data already seeded.")
#             return
#
#         json_file_path = os.path.join("/app/data", "destination_info.json")
#         with open(json_file_path, "r") as f:
#             destinations = json.load(f)
#
#         for dest in destinations:
#             # Adjust field mapping as needed
#             new_dest = Destination(**dest)
#             session.add(new_dest)
#         session.commit()
#         print("Data seeded successfully.")
#     except Exception as e:
#         print("Error seeding data:", e)
#     finally:
#         session.close()
#
#
# if __name__ == "__main__":
#     load_data()
