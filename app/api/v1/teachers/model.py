from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel, EmailStr
from core.database import Base


class TeacherDB(Base):
    """The DB model for a teacher."""
    __tablename__ = "Teachers"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String)
    facultyId = Column(Integer, ForeignKey("Faculties.id"))


class Teacher(BaseModel):
    """The Pydantic model for a teacher."""
    id: int
    firstName: str
    lastName: str
    email: EmailStr 
    facultyId: int

    class Config:
        orm_mode = True