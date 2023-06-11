from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .model import TeacherDB, Teacher
from core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[Teacher])
def get_teachers(limit: int = 500, db: Session = Depends(get_db)) -> List[Teacher]:
    """Get teachers list endpoint

    Args:
        limit (int, optional): Limit of teachers. Defaults to 500.
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Returns:
        List[Teacher]: List of teacher objects
    """
    teachers = db.query(TeacherDB).limit(limit).all()
    return [Teacher.from_orm(teacher) for teacher in teachers]