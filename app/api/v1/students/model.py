from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from pydantic import BaseModel, EmailStr

class StudentDB(Base):
    """The DB model for a student."""
    __tablename__ = "Students"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    groupId = Column(Integer, ForeignKey("Groups.id"))

    grades = relationship("GradeDB", backref="student", cascade="all,delete")

class Student(BaseModel):
    """The Pydantic model for a student."""
    id: int
    firstName: str
    lastName: str
    email: EmailStr
    groupId: int

    class Config:
        orm_mode = True

class StudentCreate(BaseModel):
    """The Pydantic model for creating a student."""
    firstName: str
    lastName: str
    email: EmailStr
    groupId: int