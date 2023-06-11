from sqlalchemy import Column, Integer, String
from core.database import Base

class BuildingDB(Base):
    """The DB model for a building"""
    __tablename__ = "Buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)