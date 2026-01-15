from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.base import BaseHTTPMiddleware
from database import Base, engine, get_db
from models.student import Student
from auth import verify_password, create_access_token
from fastapi.staticfiles import StaticFiles
from routers.student import router as student_router
from routers.course import router as course_router
from routers.enrollment import router as enrollment_router
from routers.payment import router as payment_router
from routers.auth import router as auth_router
from routers.admin import router as admin_router
from routers.staff import router as staff_router
from routers.reports import router as reports_router
from models.uploaded_file import UploadedFile
from fastapi.responses import JSONResponse
from core.exceptions import AppException

Base.metadata.create_all(bind=engine, checkfirst=True)


app = FastAPI()

# ---------- ROUTERS ----------
app.include_router(student_router)
app.include_router(course_router)
app.include_router(enrollment_router)
app.include_router(payment_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(staff_router)
app.include_router(reports_router)

# ---------- LOGIN API ----------
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(Student).filter(Student.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({
    "sub": user.email,
    "role": user.role
})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.headers.get("content-length"):
            if int(request.headers["content-length"]) > 1_000_000:  # 1MB
                raise HTTPException(status_code=413, detail="File too large")
        return await call_next(request)

app.add_middleware(LimitUploadSizeMiddleware)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None
        }
    )
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}
