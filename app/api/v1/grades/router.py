from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from core.database import get_db
from .model import GradeDB, Grade, GradeCreate

router = APIRouter()

@router.post("/", response_model=Grade)
def create_grade(grade: GradeCreate, db: Session = Depends(get_db)) -> Grade:
    """Create a new grade

    Args:
        grade (GradeCreate): new grade object
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Returns:
        Grade: created grade
    """
    try:
        existing_grade = db.query(GradeDB).filter(
            GradeDB.studentId == grade.studentId, GradeDB.courseId == grade.courseId).first()
        if existing_grade:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Grade with this student id and course id already exists")

        new_grade = GradeDB(**grade.dict())
        db.add(new_grade)
        db.commit()
        db.refresh(new_grade)
        return new_grade
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid payload.")


@router.put("/{grade_id}", response_model=Grade)
def update_grade(grade_id: int, grade: GradeCreate, db: Session = Depends(get_db)) -> Grade:
    """Update a grade endpoint

    Args:
        grade_id (int): grade id in DB
        grade (GradeCreate): a new grade object
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Returns:
        Grade: updated grade
    """
    db_grade = db.get(GradeDB, grade_id)
    if not db_grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")

    for key, value in grade.dict().items():
        setattr(db_grade, key, value)

    try:
        db.commit()
        db.refresh(db_grade)
        return db_grade
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data.")