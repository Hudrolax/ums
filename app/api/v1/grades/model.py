from sqlalchemy import Column, Integer, ForeignKey
from core.database import Base
from pydantic import BaseModel


class GradeDB(Base):
    """The DB model for a grade"""
    __tablename__ = "Grades"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Integer)
    studentId = Column(Integer, ForeignKey("Students.id"))
    courseId = Column(Integer, ForeignKey("Courses.id"))


class Grade(BaseModel):
    """The Pydantic model for a grade."""
    id: int
    grade: int
    studentId: int
    courseId: int

    class Config:
        orm_mode = True


class GradeCreate(BaseModel):
    """The Pydantic model for creating a grade."""
    grade: int
    studentId: int
    courseId: int
