from sqlalchemy import Table, Column, Integer, ForeignKey
from backend.core.sql_store import Base

responsibility_technology = Table(
    "responsibility_technology",
    Base.metadata,
    Column(
        "responsibility_id",
        Integer,
        ForeignKey("cv.responsibility.id"),
        primary_key=True,
    ),
    Column("technology_id", Integer, ForeignKey("cv.technology.id"), primary_key=True),
    schema="cv",
)
