from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from pydantic import BaseModel


class CourseDB(Base):
    """The DB model for a course."""
    __tablename__ = "Courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    teacherId = Column(Integer, ForeignKey("Teachers.id"))

    grades = relationship("GradeDB", backref="course", cascade="all,delete")
    groups = relationship("GroupDB", backref="course", cascade="all,delete")


class Course(BaseModel):
    """The Pydantic model for a course."""
    id: int
    name: str
    teacherId: int

    class Config:
        orm_mode = True


class CourseCreate(BaseModel):
    """The Pydantic model for creating a course."""
    name: str
    teacherId: int
