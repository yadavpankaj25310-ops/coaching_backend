from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
