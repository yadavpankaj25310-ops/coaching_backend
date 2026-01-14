from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import os
import shutil
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.student import Student
from schemas.student import StudentCreate, StudentUpdate, StudentOut
from auth import get_password_hash
from core.deps import get_current_student, get_current_admin
from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from core.exceptions import AppException
from models.uploaded_file import UploadedFile
from schemas.file import UploadedFileOut
router = APIRouter(prefix="/students", tags=["Students"])
# ➕ Create Student (ADMIN ONLY)
@router.post("/", response_model=StudentOut)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    db_student = db.query(Student).filter(Student.email == student.email).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_student = Student(
        name=student.name,
        email=student.email,
        password=get_password_hash(student.password)
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/search")
def search_students(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    return (
        db.query(Student)
        .filter(
            (Student.name.ilike(f"%{q}%")) |
            (Student.email.ilike(f"%{q}%"))
        )
        .all()
    )

@router.get("/", response_model=List[dict])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    students = (
        db.query(Student)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return students

# 📄 Get All Students (ADMIN ONLY)
@router.get("/", response_model=list[StudentOut])
def get_students(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    return db.query(Student).all()


# ✏ Update Student (ADMIN ONLY)
@router.put("/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise AppException("File not found", 404)
    
    db_student.name = student.name
    db_student.email = student.email
    db.commit()
    db.refresh(db_student)
    return db_student


# ❌ Delete Student (ADMIN ONLY)
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}

# 👤 My Profile (STUDENT)
@router.get("/me", response_model=StudentOut)
def my_profile(
    current_student = Depends(get_current_student)
):
    return current_student

UPLOAD_DIR = "uploads/notes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-note")
def upload_note(
    file: UploadFile = File(...),
    student = Depends(get_current_student)
):
    # allowed types
    allowed_types = ["application/pdf", "image/jpeg", "image/png"]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG, PNG files are allowed"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }

@router.get("/download/{filename}")
def download_note(
    filename: str,
    student = Depends(get_current_student)
):
    file_path = f"uploads/notes/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )

@router.delete("/delete/{filename}")
def delete_note(
    filename: str,
    student = Depends(get_current_student)
):
    file_path = f"uploads/notes/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)

    return {"message": "File deleted successfully"}

@router.post("/upload-note")
def upload_note(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    student = Depends(get_current_student)
):
    file_path = f"uploads/notes/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_file = UploadedFile(
        filename=file.filename,
        owner_email=student.email
    )
    db.add(db_file)
    db.commit()

    return {"message": "File uploaded successfully"}

@router.get("/download/{filename}")
def download_file(
    filename: str,
    db: Session = Depends(get_db),
    student = Depends(get_current_student)
):
    file = db.query(UploadedFile).filter_by(filename=filename).first()

    if not file or file.owner_email != student.email:
        raise HTTPException(status_code=403, detail="Access denied")

    file_path = f"uploads/notes/{filename}"
    return FileResponse(file_path)

@router.get("/my-files",response_model=list[UploadedFileOut])


def my_uploaded_files(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db),
    student = Depends(get_current_student)
):
    files = (
        db.query(UploadedFile)
        .filter(UploadedFile.owner_email == student.email)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": len(files),
        "files": files
    }
