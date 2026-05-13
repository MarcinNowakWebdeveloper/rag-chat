from backend.imports.splitters.base_splitter import BaseSplitter
from backend.imports.splitters.cv_service.data_normalizer import DataNormalizer
from backend.imports.splitters.cv_service.technology_geter import TechnologyGeter
from backend.core.sql_store import get_session_local
from backend.models.cv.experience import Experience
from backend.models.cv.person_data import PersonData
from backend.models.cv.project import Project
from backend.models.cv.responsibility import Responsibility
from backend.models.cv.technology import Technology
from langchain_core.documents import Document

import json


class CVSplitter(BaseSplitter):

    technologyGeter: TechnologyGeter

    def __init__(self):
        self.technologyGeter = TechnologyGeter()

    @classmethod
    def get_name(cls):
        return "cv"

    @classmethod
    def get_support_prompt(cls):
        return "Does the text concern professional experience or CV data?"

    def split_documents(self, document: Document) -> list[Document]:
        #         data = DataNormalizer().data_normalization(document)
        #         print('set_person_data')
        #         self.set_person_data(data)
        #         print('set_experience_data')
        #         self.set_experience_data(data)
        print("get_chunks_to_embedding")
        return self.get_chunks_to_embedding()

    def set_person_data(self, data):
        db = get_session_local()

        person_data = PersonData(
            full_name=data["full_name"],
            location=data["location"],
            email=data["email"],
            phone=data["phone"],
            linked_in=data["linked_in"],
            git_hub=data["git_hub"],
            education=json.dumps(data["education"]),
            languages=json.dumps(data["languages"]),
            additional_skills=json.dumps(data["additional_skills"]),
        )

        db.add(person_data)
        db.commit()

    def set_experience_data(self, data):
        db = get_session_local()
        for experience in data["experience"]:
            experience_object = self.generate_experience(experience)

            project_count = 0
            for project in experience["projects"]:
                project_count = project_count + 1
                project_object = self.generate_project(project, project_count)
                experience_object.projects.append(project_object)

                for responsibility in project["responsibilities"]:
                    try:
                        responsibility_object = self.generate_responsibility(
                            responsibility
                        )
                        project_object.responsibilities.append(responsibility_object)
                        for technology in responsibility.get("technologies", []):
                            technology_object = (
                                self.technologyGeter.get_technology_by_name(technology)
                            )
                            responsibility_object.add_technology(technology_object)

                    except AttributeError as e:
                        print("responsibility:")
                        print(responsibility)
                        raise e

            db.add(experience_object)
            db.commit()

    def get_chunks_to_embedding(self):
        db = get_session_local()
        responsibilities = db.query(Responsibility).all()
        chunks: list[Document] = []

        for responsibility in responsibilities:
            for technical_skill in responsibility.technical_skills:
                chunks.append(
                    Document(
                        page_content=technical_skill,
                        metadata={
                            "responsibility_id": responsibility.id,
                            "collection": "technical_skills",
                        },
                    )
                )

        for soft_skill_and_approach in responsibility.soft_skills_and_approach:
            chunks.append(
                Document(
                    page_content=soft_skill_and_approach,
                    metadata={
                        "responsibility_id": responsibility.id,
                        "collection": "soft_skills_and_approach",
                    },
                )
            )

        return chunks

    def generate_experience(self, experience) -> Experience:
        return Experience(
            company=experience["company"],
            role=experience["role"],
            dates=experience["dates"],
        )

    def generate_project(self, project, project_count) -> Project:
        return Project(
            name=project["name/type"] or str(project_count),
        )

    def generate_responsibility(self, responsibility) -> Responsibility:
        return Responsibility(
            original_text=responsibility.get("original_text", ""),
            responsibilities=responsibility.get("responsibilities", []),
            technical_skills=responsibility.get("technical_skills", []),
            soft_skills_and_approach=responsibility.get("soft_skills_and_approach", []),
            achievements=responsibility.get("achievements", []),
            keywords=responsibility.get("keywords", []),
            areas=responsibility.get("areas", []),
            domains=responsibility.get("domains", []),
            concepts=responsibility.get("concepts", []),
            semantic_summary=responsibility.get("semantic_summary"),
        )
