from sqlalchemy import Column, Integer
from core.database import Base

class SemesterDB(Base):
    """The DB model for a semester"""
    __tablename__ = "Semesters"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    semester = Column(Integer)