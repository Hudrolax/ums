from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from core.database import get_db
from .model import CourseDB, Course, CourseCreate
from ..students.model import StudentDB, Student
from ..groups.model import GroupDB

router = APIRouter()


@router.get("/{course_id}", response_model=Course)
def get_course_by_id(course_id: int, db: Session = Depends(get_db)) -> Course:
    """Get course by ID endpoint

    Args:
        course_id (int): Course ID
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Returns:
        Course: Course object
    """
    course = db.get(CourseDB, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)) -> Course:
    """Create a new course

    Args:
        course (CourseCreate): New course object
        db (Session, optional): DB session. Defaults to Depends(get_db).

    Returns:
        Course: Created course object
    """
    try:
        existing_course = db.query(CourseDB).filter(
            CourseDB.name == course.name, CourseDB.teacherId == course.teacherId).first()
        if existing_course:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Course with this name and teacher id already exists")

        new_course = CourseDB(**course.dict())
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid payload.")


@router.get("/{course_id}/students", response_model=List[Student])
def get_students_on_course(course_id: int, db: Session = Depends(get_db)) -> List[Student]:
    """Get student by course ID endpoint

    Args:
        course_id (int): Course ID
        db (Session, optional): DB Session. Defaults to Depends(get_db).

    Returns:
        List[Student]: List of students
    """
    course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    student_db_items = db.query(StudentDB).join(GroupDB).filter(GroupDB.courseId == course_id).all()
    if not student_db_items:
        raise HTTPException(status_code=404, detail="No students found for this course")

    students = [Student.from_orm(item) for item in student_db_items]
    return students