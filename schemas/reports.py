from pydantic import BaseModel
from datetime import date

class EnrollmentReport(BaseModel):
    student_name: str
    student_email: str
    course_name: str
    enrollment_date: date

    class Config:
        from_attributes = True

class PaymentReport(BaseModel):
    student_name: str
    course_name: str
    amount: float
    payment_date: date
    method: str

    class Config:
        from_attributes = True
