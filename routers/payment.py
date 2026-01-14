from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db  # ✅ correct import
from models.payment import Payment
from schemas.payment import PaymentCreate, PaymentResponse

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

# ➕ Create Payment
@router.post("/", response_model=PaymentResponse)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    payment = Payment(**data.model_dump())  # ✅ Pydantic v2
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

# 📄 Get All Payments
@router.get("/", response_model=list[PaymentResponse])
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()
