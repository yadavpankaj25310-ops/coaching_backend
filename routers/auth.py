from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.student import Student
from schemas.auth import LoginRequest, Token, RegisterSchema
from passlib.context import CryptContext
from core.security import create_access_token
from auth import verify_token, create_access_token
from pydantic import BaseModel
from core.security import get_password_hash
from models.student import Student

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "sub": user.email,
        "role": "student"
    })

@router.post("/refresh")
def refresh_access_token(token_data: dict = Depends(verify_token)):
    if token_data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({
        "sub": token_data["sub"],
        "role": token_data.get("role", "student")
    })

    return {"access_token": new_access_token}
    refresh_token = create_refresh_token({
        "sub": user.email
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/auth/login")
def login(data: dict):
    return {
        "message": "Login success",
        "email": data["email"]
    }

@router.post("/register")
def register_admin(user: RegisterSchema, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    print(user.dict())
    new_user = Student(
        name=user.name,
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "email": user.email}


