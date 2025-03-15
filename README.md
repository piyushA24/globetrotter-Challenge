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
git clone <your-repo-url>
cd <your-repo-folder>
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
- **API Docs:** Open [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation:** Open [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Frontend UI:** Open `FRONTEND_URL` (configured in `.env` or `docker-compose.yml`)

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
/app
├── main.py        # FastAPI app entry point
├── models.py      # Database models
├── routes.py      # API endpoints
├── requirements.txt  # Dependencies
├── entrypoint.sh  # Script to initialize DB and start server
├── Dockerfile     # Docker configuration
└── docker-compose.yml  # Docker Compose setup
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

