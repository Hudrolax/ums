from sqlalchemy import Column, Integer, Date, Time, ForeignKey
from core.database import Base

class ScheduleDB(Base):
    """The DB model for a schedule."""
    __tablename__ = "Schedules"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    time = Column(Time)
    courseId = Column(Integer, ForeignKey("Courses.id"))
    classroomId = Column(Integer, ForeignKey("Classrooms.id"))