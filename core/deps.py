# core/deps.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict

from database import get_db
from models.student import Student
from auth import verify_token  # tumhara JWT verify function

# ----------------------------
# Current user function
# ----------------------------
def get_current_user(token: str = Depends(verify_token), db: Session = Depends(get_db)) -> Student:
    """
    Token se current user retrieve karo.
    verify_token function dict return kare jisme 'id' key ho.
    """
    try:
        user_id = token["id"]  # JWT decode se user id aayega
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    user = db.query(Student).filter(Student.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

# ----------------------------
# Role-based dependencies
# ----------------------------
def admin_required(current_user: Student = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def staff_required(current_user: Student = Depends(get_current_user)):
    if current_user.role not in ["staff", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff access required"
        )
    return current_user

def teacher_required(current_user: Student = Depends(get_current_user)):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher access required"
        )
    return current_user

def student_required(current_user: Student = Depends(get_current_user)):
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student access required"
        )
    return current_user

# ----------------------------
# Current Student
# ----------------------------
def get_current_student(
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
) -> Student:
    email: str | None = token_data.get("sub")

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    student = db.query(Student).filter(Student.email == email).first()

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Student not found",
        )

    return student


# ----------------------------
# Current Admin (simple version)
# ----------------------------
def get_current_admin(
    token_data: dict = Depends(verify_token),
):
    role = token_data.get("role")

    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return token_data