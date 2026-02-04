from pydantic import BaseModel, EmailStr
from typing import Optional

class StudentBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None

class StudentCreate(StudentBase):
    password: str

class StudentUpdate(StudentBase):
    name: str
    email: EmailStr


class StudentOut(StudentBase):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True
class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True
