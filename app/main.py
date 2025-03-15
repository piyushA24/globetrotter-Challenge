from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routers import game, auth, challenge, leaderboard, notifications
from PIL import Image, ImageDraw, ImageFont
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import io
from fastapi.openapi.models import APIKey

app = FastAPI(
    title="Globetrotter Challenge API",
    docs_url="/docs",  # Swagger UI available at /docs
    redoc_url="/redoc",  # Redoc available at /redoc
    openapi_url="/openapi.json"
)
app.openapi_schema = {
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    },
    "security": [{"BearerAuth": []}]
}

# Mount your static files on /static (or another subpath)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Allow all origins for development (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(game.router)
app.include_router(auth.router)
app.include_router(challenge.router)
app.include_router(leaderboard.router)
app.include_router(notifications.router)


@app.get("/", response_class=RedirectResponse)
def root():
    return "/static/index.html"


@app.get("/dynamic-image/{username}/{score}")
def dynamic_image(username: str, score: int):
    # Create a new RGB image with a background color
    img = Image.new('RGB', (500, 200), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Compose dynamic creative text with a line break
    text = (f"Invited by {username} (Score: {score})\n"
            "Come and play the Globetrotter Challenge with me!\n"
            "Can you beat my score?")

    # Calculate text bounding box and derive width and height
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center the text on the image
    x = (500 - text_width) / 2
    y = (200 - text_height) / 2
    d.multiline_text((x, y), text, fill=(255, 255, 0), font=font, align="center")

    # Save image to an in-memory bytes buffer
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()
    return Response(content=byte_im, media_type="image/png")
