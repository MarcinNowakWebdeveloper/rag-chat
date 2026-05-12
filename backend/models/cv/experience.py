from sqlalchemy import Column, Integer, String
from backend.core.sql_store import Base
from sqlalchemy.orm import relationship


class Experience(Base):
    __tablename__ = "experience"
    __table_args__ = {"schema": "cv"}

    id = Column(Integer, primary_key=True)
    company = Column(String)
    role = Column(String)
    dates = Column(String)

    projects = relationship("Project", back_populates="experience")
