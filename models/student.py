from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="student")
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete")