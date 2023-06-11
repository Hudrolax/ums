from sqlalchemy import Column, Integer, Text, ForeignKey
from core.database import Base

class CourseProgramDB(Base):
    """The DB model for a course program"""
    __tablename__ = "CoursePrograms"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    courseId = Column(Integer, ForeignKey("Courses.id"))