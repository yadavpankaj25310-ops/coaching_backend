from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models.student import Student
from schemas.auth import LoginRequest, Token, RegisterSchema
from core.security import create_access_token, get_password_hash

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# ================= REGISTER =================

@router.post("/register")
def register(user: RegisterSchema, db: Session = Depends(get_db)):
    existing_user = db.query(Student).filter(Student.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)

    new_user = Student(
        name=user.name,
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_password   # ⚠️ column ka naam password hona chahiye
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "email": user.email}


# ================= LOGIN =================

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Student).filter(Student.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "sub": user.email,
        "role": "student"
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email
    }



