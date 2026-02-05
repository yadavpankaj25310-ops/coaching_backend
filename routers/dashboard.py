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

@router.get("/charts")
def dashboard_charts(current_user = Depends(get_current_user)):
    return {
        "revenue": [
            {"month": "Jan", "amount": 20000},
            {"month": "Feb", "amount": 35000},
            {"month": "Mar", "amount": 48000},
            {"month": "Apr", "amount": 60000},
            {"month": "May", "amount": 72000},
            {"month": "Jun", "amount": 85000},
        ],
        "students": [
            {"month": "Jan", "students": 20},
            {"month": "Feb", "students": 35},
            {"month": "Mar", "students": 55},
            {"month": "Apr", "students": 70},
            {"month": "May", "students": 95},
            {"month": "Jun", "students": 120},
        ],
        "fees": [
            {"name": "Paid", "value": 75},
            {"name": "Pending", "value": 25},
        ]
    }

