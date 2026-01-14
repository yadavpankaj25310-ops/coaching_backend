from pydantic import BaseModel
from datetime import date

class PaymentCreate(BaseModel):
    student_id: int
    course_id: int
    amount: float
    payment_date: date
    method: str

class PaymentResponse(PaymentCreate):
    id: int
    class Config:
        from_attributes = True
