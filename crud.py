from sqlalchemy.orm import Session
import models, schemas

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_all_students(db: Session):
    return db.query(models.Student).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    if student:
        db.delete(student)
        db.commit()
    return student
def get_student_by_mobile(db: Session, mobile: str):
    return db.query(models.Student).filter(models.Student.mobile == mobile).first()

def update_student(db: Session, student_id: int, student: schemas.StudentCreate):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        return None

    for key, value in student.dict().items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student
