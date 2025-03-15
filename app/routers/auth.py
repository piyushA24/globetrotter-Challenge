from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database import SessionLocal
from app.models.user import User
from datetime import datetime, timedelta
import jwt
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()
security = HTTPBearer()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def fake_hash_password(password: str):
    return "fakehashed" + password


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


@router.post("/auth/register", summary="Register a new user")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    try:
        new_user = User(
            email=user.email,
            username=user.username,
            hashed_password=fake_hash_password(user.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "User registered successfully", "user_id": new_user.id, "username": new_user.username}


# ------------------ LOGIN ENDPOINT ------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str = None  # Optional field for username


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    # Compare the stored hashed password with the hash of the provided password.
    if user.hashed_password != fake_hash_password(password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/auth/login", response_model=Token, summary="User login and receive JWT token")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"user_id": user.id, "username": user.username}
    access_token = create_access_token(data=token_data, expires_delta=access_token_expires)

    print("Login successful")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }
