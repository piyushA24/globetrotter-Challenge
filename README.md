# GlobeTrotter Challenge - Backend Setup

## Tech Stack
- **Backend:** FastAPI (Python 3.10)
- **Database:** PostgreSQL
- **Frontend:** HTML (basic UI, mainly backend-focused)
- **Containerization:** Docker & Docker Compose

## Prerequisites
Ensure you have the following installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/piyushA24/globetrotter-Challenge.git
cd globetrotter-Challenge
```

### 2. Create a `.env` file (Optional)
If needed, create a `.env` file to override environment variables.

### 3. Build and Run the Containers
```sh
docker-compose up --build
```
This command will:
- Build the FastAPI backend from the Dockerfile.
- Start the PostgreSQL database service.
- Expose the FastAPI app on port `8000`.

### 4. Access the Application
- **API Docs (Local):** Open [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation (Local):** Open [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Frontend UI (Local):** Open `FRONTEND_URL` (configured in `.env` or `docker-compose.yml`)
- **Live Game UI:** [https://globetrotter-challenge-production-37b8.up.railway.app/static/index.html#](https://globetrotter-challenge-production-37b8.up.railway.app/static/index.html#)
- **Live API Docs:** [https://globetrotter-challenge-production-37b8.up.railway.app/docs](https://globetrotter-challenge-production-37b8.up.railway.app/docs)

## Database Configuration
The PostgreSQL database is configured with:
- **User:** `postgres`
- **Password:** `VgPJpyArnNArMLxnxcTyFDXJVshVzIbM`
- **Database Name:** `railway`
- **Host:** `postgres.railway.internal`
- **Port:** `5432`

### ⚠️ Important Note
If running locally, replace the database host (`POSTGRES_HOST`) from `postgres.railway.internal` to `localhost` in all relevant configuration files (`docker-compose.yml`, environment variables, etc.). The current setup is for deployment and uses a public URL.

## Project Structure
```
/globetrotter-Challenge
├── Dockerfile              # Docker setup
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── entrypoint.sh           # Script to initialize DB and start server
├── data/                   # Data-related files
│   ├── destination_info.json
├── static/                 # Static frontend files
│   ├── index.html
├── app/                    # Backend application
│   ├── __init__.py
│   ├── main.py             # FastAPI app entry point
│   ├── dependencies.py     # Dependency injections
│   ├── seed.py             # Database seeding script
│   ├── core/               # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py       # Application config settings
│   │   ├── database.py     # Database connection
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   ├── destination.py
│   │   ├── leaderboard.py
│   │   ├── notifications.py
│   │   ├── user.py
│   ├── routers/            # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── challenge.py
│   │   ├── game.py
│   │   ├── leaderboard.py
│   │   ├── notifications.py
│   ├── services/           # Business logic
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── leaderboard_service.py
```

## Development
### Running Locally without Docker
If you prefer running without Docker, set up a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Deployment
This application is deployed using **Railway**, which automatically manages environment variables and database connectivity.

---
This project is primarily focused on backend integration, ensuring a robust API and database setup. The frontend is minimal, designed mainly for testing API interactions.
