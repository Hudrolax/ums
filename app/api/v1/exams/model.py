from sqlalchemy import Column, Integer, Date, Time, ForeignKey
from core.database import Base

class ExamDB(Base):
    """The DB model for an exam."""
    __tablename__ = "Exams"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    time = Column(Time)
    courseId = Column(Integer, ForeignKey("Courses.id"))
    classroomId = Column(Integer, ForeignKey("Classrooms.id"))