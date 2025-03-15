from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext  # ✅ Secure password hashing

from app.core.database import SessionLocal
from app.models.user import User
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ✅ Secure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Hash passwords properly
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ Verify passwords properly
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ User Registration Schema
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

@router.post("/auth/register", summary="Register a new user")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # ✅ Check if email exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    # ✅ Check if username exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    try:
        new_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hash_password(user.password)  # ✅ Securely hash password
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
    username: str  # ✅ Make username required

# ✅ Authenticate user with hashed password
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# ✅ Create JWT token with expiration
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/auth/login", response_model=Token, summary="User login and receive JWT token")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = create_access_token(data={"user_id": user.id, "username": user.username})

    return {"access_token": access_token, "token_type": "bearer", "username": user.username}
