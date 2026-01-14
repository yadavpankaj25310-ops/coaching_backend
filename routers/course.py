from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.course import Course
from schemas.course import CourseCreate, CourseUpdate, CourseOut
from core.deps import get_current_admin, get_current_student

router = APIRouter(prefix="/courses", tags=["Courses"])


# ➕ Create Course (ADMIN)
@router.post("/", response_model=CourseOut)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


# 📄 Get All Courses (STUDENT + ADMIN)
@router.get("/", response_model=list[CourseOut])
def get_courses(
    db: Session = Depends(get_db),
    user = Depends(get_current_student)
):
    return db.query(Course).all()


# ✏ Update Course (ADMIN)
@router.put("/{course_id}", response_model=CourseOut)
def update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db_course.title = course.title
    db_course.description = course.description
    db_course.fee = course.fee

    db.commit()
    db.refresh(db_course)
    return db_course


# ❌ Delete Course (ADMIN)
@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(db_course)
    db.commit()
    return {"message": "Course deleted successfully"}
