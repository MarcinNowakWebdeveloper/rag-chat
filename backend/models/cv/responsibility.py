from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.core.sql_store import Base
from backend.models.cv.responsibility_technology import responsibility_technology
from backend.models.cv.technology import Technology


class Responsibility(Base):
    __tablename__ = "responsibility"
    __table_args__ = {"schema": "cv"}

    id = Column(Integer, primary_key=True)
    original_text = Column(Text)
    responsibilities = Column(JSONB)
    technical_skills: Mapped[list[str]] = mapped_column(JSONB)
    soft_skills_and_approach: Mapped[list[str]] = mapped_column(JSONB)
    achievements = Column(JSONB)
    keywords = Column(JSONB)
    areas = Column(JSONB)
    domains = Column(JSONB)
    concepts = Column(JSONB)
    semantic_summary = Column(Text)

    project_id = Column(Integer, ForeignKey("cv.project.id"))

    project = relationship("Project", back_populates="responsibilities")

    technologies = relationship(
        "Technology",
        secondary=responsibility_technology,
        back_populates="responsibilities",
    )

    def add_technology(self, technology: Technology):
        if technology in self.technologies:
            return
        self.technologies.append(technology)
