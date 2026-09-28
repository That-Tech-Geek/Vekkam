from app.core.ids import stable_id
from app.core.models import Concept, Question, QuestionType

def generate_questions(concept: Concept, count: int=4) -> list[Question]:
    templates=[
      (QuestionType.recall,f"What is {concept.name}?",concept.description or "State the definition precisely."),
      (QuestionType.conceptual,f"Explain the central idea behind {concept.name}.",concept.description or "Explain it in your own words."),
      (QuestionType.application,f"Give one concrete application of {concept.name}.",concept.examples[0] if concept.examples else "Provide a valid application."),
      (QuestionType.error_detection,f"What is a common mistake when using {concept.name}?","Identify the incorrect assumption and explain why it fails."),
    ]
    return [Question(question_id=stable_id("question",concept.concept_id,str(i)),
                     concept_id=concept.concept_id,type=k,prompt=p,answer=a)
            for i,(k,p,a) in enumerate(templates[:count])]
