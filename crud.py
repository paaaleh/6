from sqlalchemy.orm import Session
from models import Student
from sqlalchemy import func

def insert_student(db: Session, student_data: dict):
    student = Student(**student_data)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def get_all_students(db: Session):
    return db.query(Student).all()

def get_students_by_faculty(db: Session, faculty: str):
    return db.query(Student).filter(Student.faculty == faculty).all()

def get_unique_courses(db: Session):
    return db.query(Student.course).distinct().all()

def get_average_grade_by_faculty(db: Session):
    return db.query(Student.faculty, func.avg(Student.grade)).group_by(Student.faculty).all()

def get_students_with_low_grade(db: Session, course: str, threshold: int = 30):
    return db.query(Student).filter(Student.course == course, Student.grade < threshold).all()

def update_student(db: Session, student_id: int, updates: dict):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None
    for key, value in updates.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None
    db.delete(student)
    db.commit()
    return student

from database import SessionLocal
from models import Student

async def delete_students_by_ids(ids: list[int]):
    db = SessionLocal()
    try:
        for student_id in ids:
            student = db.query(Student).filter(Student.id == student_id).first()
            if student:
                db.delete(student)
        db.commit()
    finally:
        db.close()

async def get_all_students():
    db = SessionLocal()
    try:
        return db.query(Student).all()
    finally:
        db.close()