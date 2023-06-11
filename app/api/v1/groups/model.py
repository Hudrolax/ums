from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class GroupDB(Base):
    """The DB model for a group."""
    __tablename__ = "Groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    departmentId = Column(Integer, ForeignKey("Departments.id"))
    courseId = Column(Integer, ForeignKey("Courses.id"))

    students = relationship("StudentDB", backref="group", cascade="all,delete")