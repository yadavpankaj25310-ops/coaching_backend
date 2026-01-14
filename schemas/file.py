from pydantic import BaseModel
from datetime import datetime

class UploadedFileOut(BaseModel):
    id: int
    filename: str
    owner_email: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
