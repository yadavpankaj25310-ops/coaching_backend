from pydantic import BaseModel
from datetime import date

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date

class EnrollmentResponse(EnrollmentCreate):
    id: int
    class Config:
        from_attributes = True  # Pydantic v2
