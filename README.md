# GlobeTrotter Challenge - Backend Setup

## Tech Stack
- **Backend:** FastAPI (Python 3.10)
- **Database:** PostgreSQL
- **Frontend:** HTML (basic UI, mainly backend-focused)
- **Containerization:** Docker & Docker Compose

## The Globetrotter Challenge – The Ultimate Travel Guessing Game!
🧩 I built Globetrotter, a full-stack web app where users get cryptic clues about a famous place and must guess which destination it refers to. Once they guess, they unlock fun facts, trivia, and surprises about the destination!

### 🔹 Features and Implementation
#### 1️⃣ Dataset & AI Integration
- I started with a basic dataset and expanded it using AI tools (e.g., ChatGPT, OpenAI API, Web Scraping, etc.).
- The final dataset contains **102 unique destinations**, each with clues, fun facts, and trivia.

**Example Dataset Entry:**
```json
{
  "city": "Sydney",
  "country": "Australia",
  "clues": [
    "This city is known for its iconic opera house and harbor bridge.",
    "Famous for its sunny beaches and vibrant cultural scene."
  ],
  "fun_fact": [
    "Sydney Opera House is a UNESCO World Heritage site.",
    "The harbor bridge is affectionately known as 'The Coathanger'."
  ],
  "trivia": [
    "Home to world-class beaches like Bondi and Manly.",
    "Hosts the annual Sydney New Year's Eve fireworks spectacular."
  ]
}
```

#### 2️⃣ Core Game Functionality
✅ Displays 1–2 random clues from a randomly selected destination.
✅ Allows users to select from multiple possible answers.
✅ Provides immediate funky feedback:
   - 🎉 **Correct Answer:** Triggers a confetti animation and reveals a fun fact.
   - 😢 **Incorrect Answer:** Shows a sad-face animation and still reveals a fun fact.
✅ Includes a ‘Play Again’ or ‘Next’ button to load a new random destination.
✅ Users can answer **up to 10 questions** per session.
✅ All dataset queries and responses are handled on the backend, preventing users from accessing answers via browser source code.

#### 3️⃣ “Challenge a Friend” Feature
✅ Users enter a unique username, which registers them in the system.
✅ Clicking ‘Challenge a Friend’ opens a **share popup with a dynamic image & invite link** for WhatsApp.
✅ The invitee can see the inviter’s score before playing.
✅ If the invited friend beats the inviter’s score, a notification is sent saying:
   - **"You beat [friend's username] with a score of [new high score]!"**
✅ A **Leaderboard** updates automatically on the home page after every completed game, displaying the top players.

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
│   ├── routers/            # API endpoints
│   ├── services/           # Business logic
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
### 📄 Documentation
For a detailed project overview and system design, refer to the full documentation here:
[Globetrotter Challenge Documentation](https://docs.google.com/document/d/1pElZbP8s9p1WI0abB_eVI5zz5f8o31t6d6K7fD_SjMQ/edit?tab=t.0#heading=h.o6hawjs956a)

## Deployment
This application is deployed using **Railway**, which automatically manages environment variables and database connectivity.

I used **Railway** to deploy the application live, making it accessible at the following links:
- **Live Game UI:** [https://globetrotter-challenge-production-37b8.up.railway.app/static/index.html#](https://globetrotter-challenge-production-37b8.up.railway.app/static/index.html#)
- **Live API Docs:** [https://globetrotter-challenge-production-37b8.up.railway.app/docs](https://globetrotter-challenge-production-37b8.up.railway.app/docs)

---
This project is primarily focused on backend integration, ensuring a robust API and database setup. The frontend is minimal, designed mainly for testing API interactions.

