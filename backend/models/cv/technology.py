from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.core.sql_store import Base
from backend.models.cv.responsibility_technology import responsibility_technology


class Technology(Base):
    __tablename__ = "technology"
    __table_args__ = {"schema": "cv"}
    __truncate__ = False

    id = Column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column()

    responsibilities = relationship(
        "Responsibility",
        secondary=responsibility_technology,
        back_populates="technologies",
    )
