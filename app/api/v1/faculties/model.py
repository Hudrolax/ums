from sqlalchemy import Column, Integer, String
from core.database import Base

class FacultyDB(Base):
    """The DB model for a Faculty"""
    __tablename__ = "Faculties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)