import pandas as pd
from sqlalchemy.orm import Session
from models import Student

def load_students_from_csv(file_path: str, db: Session):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        student = Student(
            last_name=row["Фамилия"],
            first_name=row["Имя"],
            faculty=row["Факультет"],
            course=row["Курс"],
            grade=int(row["Оценка"])
        )
        db.add(student)
    db.commit()
