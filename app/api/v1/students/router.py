from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .model import StudentDB, Student, StudentCreate
from core.database import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.get("/{student_id}", response_model=Student)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)) -> Student:
    """Get student by ID endpoint

    Args:
        student_id (int): Student ID in datebase
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Returns:
        Student: student object
    """
    student = db.get(StudentDB, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)) -> Student:
    """Create a new student endpoint

    Args:
        student (StudentCreate): new student object
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Returns:
        Student: New created student object
    """
    try:
        existing_student = db.query(StudentDB).filter(
            StudentDB.email == student.email).first()
        if existing_student:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Student with this email already exists")

        new_student = StudentDB(**student.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid groupid.")


@router.put("/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)) -> Student:
    """Update a student endpoint

    Args:
        student_id (int): Student ID
        student (StudentCreate): Student object for updating
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Returns:
        Student: updated student object
    """
    db_student = db.get(StudentDB, student_id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    existing_student = db.query(StudentDB).filter(
        StudentDB.email == student.email).first()
    if existing_student:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Student with this email already exists")

    for key, value in student.dict().items():
        setattr(db_student, key, value)

    try:
        db.commit()
        db.refresh(db_student)
        return db_student
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data.")


@router.delete("/{student_id}", response_model=Student)
def delete_student(student_id: int, db: Session = Depends(get_db)) -> Student:
    """Delete a student endpoint

    Args:
        student_id (int): student ID
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Returns:
        Student: Deleted student object
    """
    student = db.get(StudentDB, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    db.delete(student)
    db.commit()
    return student
