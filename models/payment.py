from sqlalchemy import Column, Integer, ForeignKey, Float, Date, String
from sqlalchemy.orm import relationship
from database import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    amount = Column(Float)
    payment_date = Column(Date)
    method = Column(String)

    student = relationship("Student")
    course = relationship("Course")
