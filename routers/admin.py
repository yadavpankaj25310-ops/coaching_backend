from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.deps import get_current_admin
import os
from database import get_db
from models.student import Student
from core.deps import get_current_admin
from models.uploaded_file import UploadedFile

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def admin_dashboard(admin = Depends(get_current_admin)):
    return {
        "message": "Welcome Admin",
        "admin": admin["sub"]
    }

@router.delete("/admin/delete/{filename}")
def admin_delete_note(
    filename: str,
    admin = Depends(get_current_admin)
):
    file_path = f"uploads/notes/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)
    return {"message": "File deleted by admin"}

@router.delete("/delete-file/{filename}")
def admin_delete_file(
    filename: str,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    file = db.query(UploadedFile).filter_by(filename=filename).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(f"uploads/notes/{filename}")
    db.delete(file)
    db.commit()

    return {"message": "File deleted by admin"}

@router.get("/files")
def all_uploaded_files(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    files = (
        db.query(UploadedFile)
        .order_by(UploadedFile.uploaded_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return files
