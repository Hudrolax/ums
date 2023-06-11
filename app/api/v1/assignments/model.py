from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from core.database import Base

class AssignmentDB(Base):
    """The DB model for an assignment."""
    __tablename__ = "Assignments"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    dateAssigned = Column(Date)
    dueDate = Column(Date)
    courseId = Column(Integer, ForeignKey("Courses.id"))