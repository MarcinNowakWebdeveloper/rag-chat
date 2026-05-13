from backend.core.llm import get_llm
from langchain_core.documents import Document
from typing import Any

# TMP
from pathlib import Path


import json

llm = get_llm()


class DataNormalizer:

    def data_normalization(self, document: Document) -> list[Document]:
        #         prompt = self.normalization_prompt(document.page_content)
        #         data = self.get_normalized_data(prompt)
        #         self.get_normalized_responsibilities_data(data)

        # TMP
        data = self.get_test_data()

        return data

    def get_normalized_data(self, prompt: str, repeat=1) -> dict[str, Any]:
        data = llm.invoke(prompt)
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            if repeat == 6:
                raise ValueError(f"Response is not json: {data}")
            print(f"repeat: {repeat}")

            return self.get_normalized_data(prompt, repeat + 1)

        return data

    def get_normalized_responsibilities_data(self, data):
        for experience in data["experience"]:
            for project in experience["projects"]:
                for i, responsibility in enumerate(project["responsibilities"]):
                    responsibility_data = self.get_normalized_responsibility_data(
                        responsibility
                    )
                    responsibility_data["original_text"] = responsibility
                    project["responsibilities"][i] = responsibility_data

    def get_normalized_responsibility_data(
        self, responsibilities: list
    ) -> dict[str, Any]:
        prompt = self.responsibilities_normalization_prompt(responsibilities)
        return self.get_normalized_data(prompt)

    def normalization_prompt(self, text: str) -> str:
        return f"""
    You are a strict information extraction system.
    Extract structured data from the CV text.

    Return ONLY valid JSON.
    Do NOT include explanations, comments, or extra text.

    If a field is missing, use empty string "" or empty array [].

    Schema:

    {{
      "full_name": "",
      "location": "",
      "email": "",
      "phone": "",
      "linked_in": "",
      "git_hub": "",
      "experience": [
        {{
          "company": "",
          "role": "",
          "dates": "",
          "projects": [
            {{
                "name/type": ""
                "responsibilities": []
            }}
          ],
        }}
      ],
      "additional_skills": [],
      "education": [],
      "languages": []
    }}

    CV TEXT:
    "{text}"

    RULES (HARD REQUIREMENTS):
    - Output MUST be valid JSON.
    - Output MUST be parseable by Python json.loads().
    - Output MUST contain ONLY JSON.
    - DO NOT output any text before or after JSON.
    - DO NOT include explanations, headings, or comments.
    - DO NOT wrap output in markdown.
    - If you output anything other than raw JSON, the response is invalid.
    - If data is unknown, use empty arrays or empty strings.
    - do not hallucinate data
    - if unknown, return empty values.
    - Extract ALL responsibilities mentioned in the text for each role.
    - Do NOT summarize or merge items.
    - Do NOT limit the number of items.
    - Split into atomic bullet points (one responsibility per item).
    - Preserve original meaning, but normalize wording if needed.
    - Include implicit responsibilities if clearly described in the text.
    """

    def responsibilities_normalization_prompt(self, responsibilities: list) -> str:
        text = "\n".join(f"- {item}" for item in responsibilities)
        return f"""
You are an expert system for semantic experience extraction and ATS optimization.

Your task is to transform raw professional experience notes into structured JSON objects optimized for:
- semantic search
- vector embeddings
- ATS CV generation
- job offer matching

Return ONLY valid JSON.
Do NOT include explanations, markdown, comments, or extra text.

The output MUST be parseable using Python json.loads().

INPUT FORMAT:
The input contains multiple experience entries separated by "-".

GOALS:
1. Normalize messy/non-formal experience descriptions.
2. Extract technologies and responsibilities.
3. Infer semantic meaning useful for recruitment matching.
4. Generate metadata for semantic retrieval.
5. Reply in THE SAME language as the input text.

RULES:

GENERAL:
- Do not hallucinate companies or technologies.
- Infer concepts only if strongly implied.
- Keep wording concise and normalized.
- Remove duplicates.
- Preserve technical meaning.

RESPONSIBILITIES:
- Extract ALL responsibilities mentioned in the text.
- Do NOT summarize.
- Do NOT limit the number of items.
- Split compound sentences into atomic responsibilities.
- One responsibility per array item.
- Include implied responsibilities if clearly described.

TECHNOLOGIES:
- Extract explicitly mentioned technologies.
- Infer technologies only if obvious from context.
- Normalize names:
  - "js" -> "JavaScript"
  - "ts" -> "TypeScript"
  - etc.
- Remove duplicates.
- List of strings without keys


TECHNICAL_SKILLS:
- Isolate clearly listed technical skills.
- DO NOT summarize.
- DO NOT limit the number of items.
- Include implied technical skills if they are clearly described.
- Remove duplicates.
- List strings without keys

Examples:
- Advanced PHP knowledge
- Knowledge of PHP frameworks such as Symfony
- Writing SOLID-compliant code
- Knowledge of version control systems
- Knowledge of database management systems
- Understanding of OOP
- Knowledge of design patterns
- Creating optimized code
- Analysis and optimization of application performance
- Integration with external APIs
- Web service management
- Knowledge of web application security
- Development of e-commerce platforms
- Implementation of backend technologies

SOFT_SKILLS_AND_APPROACH:
- Isolate clearly listed soft skills and approach.
- DO NOT summarize.
- DO NOT limit the number of items.
- Include implied soft skills and approach if they are clearly described.
- Remove duplicates.
- List strings without keys

Examples:
- Continuous learning
- Staying current with technologies
- Communicativeness
- Openness to collaboration
- Effective teamwork
- Building positive relationships
- Proactivity
- Problem-solving
- Responsibility
- Reliability
- Commitment to quality
- AI-powered mindset
- Openness to testing AI tools
- Collaboration with developers, testers, the Product Owner, and the Scrum Master


KEYWORDS:
- Generate ATS-friendly keywords.
- Use short phrases only.
- Include:
  - technical skills
  - architecture concepts
  - business/domain terms
  - methodologies
- Keywords may be inferred.

AREAS:
Generate high-level engineering areas, such as:
- backend
- frontend
- devops
- cloud
- ecommerce
- integrations
- mobile
- architecture
- data engineering
- security
- performance
- ai
- automation

DOMAINS:
Generate business/product domains, such as:
- ecommerce
- fintech
- healthcare
- logistics
- education
- retail
- marketing
- SaaS

CONCEPTS:
Generate semantic engineering concepts useful for semantic matching.

Examples:
- scalable integrations
- asynchronous processing
- event-driven architecture
- microservices
- high-volume systems
- payment processing
- product synchronization
- distributed systems
- CI/CD automation
- API integrations

SEMANTIC SUMMARY:
Generate ONE concise sentence optimized for vector embeddings.
The sentence should:
- summarize the engineering/business value
- contain semantic meaning
- describe the type of systems/work involved
- NOT be a copy of the original text

GOOD EXAMPLE:
"Built scalable ecommerce integrations with asynchronous product synchronization and custom business logic."

OUTPUT SCHEMA:

{{
  "technologies": [],
  "responsibilities": [],
  "technical_skills": [],
  "soft_skills_and_approach": [],
  "achievements": [],
  "keywords": [],
  "areas": [],
  "domains": [],
  "concepts": [],
  "semantic_summary": ""
}}

INPUT:
{text}
"""

    def get_test_data(self):
        BASE_DIR = Path(__file__).resolve().parent
        json_path = BASE_DIR.parent / "a.json"
        with open(json_path, "r", encoding="utf-8") as file:
            return json.load(file)
