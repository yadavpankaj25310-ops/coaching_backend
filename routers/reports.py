from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from core.deps import admin_required
from models.student import Student
from models.enrollment import Enrollment
from models.course import Course
from models.payment import Payment
from schemas.reports import EnrollmentReport, PaymentReport

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# 📝 Enrollment Report
@router.get("/enrollments", response_model=list[EnrollmentReport])
def enrollment_report(admin = Depends(admin_required), db: Session = Depends(get_db)):
    results = (
        db.query(Student.name.label("student_name"),
                 Student.email.label("student_email"),
                 Course.name.label("course_name"),
                 Enrollment.enrollment_date)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .join(Course, Enrollment.course_id == Course.id)
        .all()
    )
    return results

# 💰 Payment Report
@router.get("/payments", response_model=list[PaymentReport])
def payment_report(admin = Depends(admin_required), db: Session = Depends(get_db)):
    results = (
        db.query(Student.name.label("student_name"),
                 Course.name.label("course_name"),
                 Payment.amount,
                 Payment.payment_date,
                 Payment.method)
        .join(Payment, Payment.student_id == Student.id)
        .join(Course, Payment.course_id == Course.id)
        .all()
    )
    return results
