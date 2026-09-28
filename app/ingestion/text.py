from app.core.ids import stable_id
from app.core.models import Concept, LearningDocument, PageIR, SourceRegion

def ingest_text(document_id: str, text: str) -> LearningDocument:
    page_id = stable_id("page", document_id, "1")
    concept_id = stable_id("concept", document_id, text[:160])
    concept = Concept(concept_id=concept_id, name="Imported concept", description=text[:1000],
                      evidence=[SourceRegion(page_id=page_id, extracted_text=text[:4000])])
    return LearningDocument(document_id=document_id, title=document_id,
                            pages=[PageIR(page_id=page_id, page_number=1, text=text)],
                            concepts=[concept])
