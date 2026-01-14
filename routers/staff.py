from fastapi import APIRouter, Depends
from core.deps import staff_required, teacher_required

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/staff-info")
def staff_dashboard(staff = Depends(staff_required)):
    return {"msg": "Staff can see limited info"}

@router.get("/teacher-info")
def teacher_dashboard(teacher = Depends(teacher_required)):
    return {"msg": "Teacher can see assigned students"}
