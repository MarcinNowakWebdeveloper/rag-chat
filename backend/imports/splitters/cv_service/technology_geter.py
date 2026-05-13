from backend.core.sql_store import get_session_local
from backend.models.cv.technology import Technology
from typing import Dict
from sqlalchemy.orm import Session


class TechnologyGeter:

    technologies: Dict[str, Technology] = {}
    db: Session

    def __init__(self):
        self.db = get_session_local()
        self.set_technologies()

    def get_technology_by_name(self, technology: str) -> Technology:
        if technology in self.technologies:
            return self.technologies[technology]

        technology_object = Technology(name=technology)
        self.db.add(technology_object)
        self.technologies[technology] = technology_object

        return technology_object

    def set_technologies(self):
        technologies = self.db.query(Technology).all()

        for technology in technologies:
            self.technologies[technology.name] = technology
