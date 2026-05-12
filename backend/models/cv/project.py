from sqlalchemy import Column, Integer, String, ForeignKey
from backend.core.sql_store import Base
from sqlalchemy.orm import relationship


class Project(Base):
    __tablename__ = "project"
    __table_args__ = {"schema": "cv"}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    experience_id = Column(Integer, ForeignKey("cv.experience.id"))

    experience = relationship("Experience", back_populates="projects")

    responsibilities = relationship("Responsibility", back_populates="project")
