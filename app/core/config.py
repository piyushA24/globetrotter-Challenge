# app/core/config.py
import os
from dotenv import load_dotenv
from urllib.parse import quote


load_dotenv()  # Load environment variables from a .env file if available

# PostgreSQL settings
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Piyush@123")
POSTGRES_DB = os.getenv("POSTGRES_DB", "globetrotter")  # Replace with your actual DB name
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# URL encode the password
POSTGRES_PASSWORD_ENCODED = quote(POSTGRES_PASSWORD)

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD_ENCODED}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
print("here")
print(SQLALCHEMY_DATABASE_URL)
# OpenSearch settings
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = os.getenv("OPENSEARCH_PORT", "9201")
OPENSEARCH_USER = os.getenv("OPENSEARCH_USER", "admin")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD", "Piyush@123")
OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX", "destinations")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000/static/index.html")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")  # Replace with a strong secret in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30