from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    owner_email = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
