from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import shutil

from database import get_db
from models.student import Student
from models.uploaded_file import UploadedFile
from schemas.student import StudentCreate, StudentUpdate, StudentOut
from schemas.file import UploadedFileOut
from core.security import get_password_hash
from core.deps import get_current_student, get_current_admin

router = APIRouter(prefix="/students", tags=["Students"])

UPLOAD_DIR = "uploads/notes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ================= CREATE STUDENT (ADMIN) =================

@router.post("/", response_model=StudentOut)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_student = Student(
        name=student.name,
        email=student.email,
        phone=student.phone,
        hashed_password=get_password_hash(student.password)
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# ================= LIST STUDENTS (ADMIN + PAGINATION) =================

@router.get("/", response_model=List[StudentOut])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(Student).offset(skip).limit(limit).all()


# ================= SEARCH STUDENTS =================

@router.get("/search", response_model=List[StudentOut])
def search_students(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return (
        db.query(Student)
        .filter(
            (Student.name.ilike(f"%{q}%")) |
            (Student.email.ilike(f"%{q}%"))
        )
        .all()
    )


# ================= UPDATE STUDENT =================

@router.put("/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db_student.name = student.name
    db_student.email = student.email
    db_student.phone = student.phone

    db.commit()
    db.refresh(db_student)
    return db_student


# ================= DELETE STUDENT =================

@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}


# ================= STUDENT PROFILE =================

@router.get("/me", response_model=StudentOut)
def my_profile(
    student=Depends(get_current_student)
):
    return student


# ================= FILE UPLOAD =================

@router.post("/upload-note")
def upload_note(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    student=Depends(get_current_student)
):
    allowed_types = ["application/pdf", "image/jpeg", "image/png"]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG, PNG files are allowed"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_file = UploadedFile(
        filename=file.filename,
        owner_email=student.email
    )
    db.add(db_file)
    db.commit()

    return {"message": "File uploaded successfully"}


# ================= FILE DOWNLOAD =================

@router.get("/download/{filename}")
def download_file(
    filename: str,
    db: Session = Depends(get_db),
    student=Depends(get_current_student)
):
    file = db.query(UploadedFile).filter_by(filename=filename).first()

    if not file or file.owner_email != student.email:
        raise HTTPException(status_code=403, detail="Access denied")

    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=filename)


# ================= MY FILES LIST =================

@router.get("/my-files", response_model=List[UploadedFileOut])
def my_uploaded_files(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db),
    student=Depends(get_current_student)
):
    return (
        db.query(UploadedFile)
        .filter(UploadedFile.owner_email == student.email)
        .offset(skip)
        .limit(limit)
        .all()
    )
