from sqlalchemy import Column, Integer, Text, ForeignKey
from core.database import Base

class StudyPlanDB(Base):
    """The DB model for a study plan"""
    __tablename__ = "StudyPlans"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    semesterId = Column(Integer, ForeignKey("Semesters.id"))
    courseId = Column(Integer, ForeignKey("Courses.id"))
    groupId = Column(Integer, ForeignKey("Groups.id"))