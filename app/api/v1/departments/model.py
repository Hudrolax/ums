from sqlalchemy import Column, Integer, String, ForeignKey
from core.database import Base

class DepartmentDB(Base):
    """The DB model for a department."""
    __tablename__ = "Departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    facultyId = Column(Integer, ForeignKey("Faculties.id"))