from sqlalchemy import Column, Integer, String, Text
from backend.core.sql_store import Base


class PersonData(Base):
    __tablename__ = "person_data"
    __table_args__ = {"schema": "cv"}

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    location = Column(String)
    email = Column(String)
    phone = Column(String)
    linked_in = Column(String)
    git_hub = Column(String)
    education = Column(Text)
    languages = Column(Text)
    additional_skills = Column(Text)
