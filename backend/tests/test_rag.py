from backend.rag.router import answer_question
from backend.constants.answer_style import AnswerStyle

style = AnswerStyle["FORMAL"]

question = "How do I start a docker container?"

response = answer_question(question, style)

print("\n=== ANSWER ===\n")
print(response)
