from fastapi import APIRouter, Depends
from core.security import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def dashboard(current_user = Depends(get_current_user)):
    return {
        "message": "Welcome to Dashboard",
        "user": current_user
    }

@router.get("/stats")
def dashboard_stats(current_user = Depends(get_current_user)):
    return {
        "total_students": 245,
        "total_revenue": 485000,
        "pending_fees": 72000,
        "today_admissions": 5
    }

