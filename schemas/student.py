from pydantic import BaseModel, EmailStr

class StudentBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class StudentCreate(StudentBase):
    password: str

class StudentUpdate(StudentBase):
    name: str
    email: EmailStr


class StudentOut(StudentBase):
    id: int

    class Config:
        from_attributes = True
class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True
