from sqlalchemy import Column, Integer, String
from database import Base

class CoachingStudent(Base):
    __tablename__ = "coaching_students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    course = Column(String, nullable=True)
