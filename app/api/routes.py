from fastapi import APIRouter

from app.assessment.quiz import generate_questions
from app.blueprints.engine import build_blueprint
from app.core.models import Concept, LearningDocument, QuestionRequest
from app.ingestion.text import ingest_text

router = APIRouter(prefix="/v1")


@router.post("/ingest/text", response_model=LearningDocument)
def ingest(payload: dict[str, str]) -> LearningDocument:
    return ingest_text(payload.get("document_id", "document"), payload.get("text", ""))


@router.post("/blueprints")
def blueprint(concept: Concept) -> dict:
    return build_blueprint(concept).model_dump(mode="json")


@router.post("/questions")
def questions(request: QuestionRequest) -> list[dict]:
    return [q.model_dump(mode="json") for q in generate_questions(request.concept, request.count)]


@router.get("/architecture")
def architecture() -> dict[str, object]:
    return {"source_of_truth": "canonical_learning_ir", "stages": [
        "multimodal_extraction", "canonical_learning_ir", "knowledge_graph",
        "vector_retrieval", "visual_blueprint", "manim_validation",
        "narration_sync", "active_recall", "mastery", "exam_intelligence"
    ]}
