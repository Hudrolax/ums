from sqlalchemy import Column, Integer, ForeignKey
from core.database import Base

class ClassroomDB(Base):
    """The DB model for a classroom."""
    __tablename__ = "Classrooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    buildingId = Column(Integer, ForeignKey("Buildings.id"))