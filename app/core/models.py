from __future__ import annotations
from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field

class VisualType(StrEnum):
    text="text"; equation="equation"; graph="graph"; chart="chart"; table="table"
    diagram="diagram"; flowchart="flowchart"; geometric_figure="geometric_figure"
    photograph="photograph"; illustration="illustration"; unknown="unknown"

class Reconstructability(StrEnum):
    reconstructable="RECONSTRUCTABLE"; partial="PARTIALLY_RECONSTRUCTABLE"; none="NON_RECONSTRUCTABLE"

class BoundingBox(BaseModel):
    x: float; y: float; width: float; height: float

class SourceRegion(BaseModel):
    page_id: str; bbox: BoundingBox | None=None
    extracted_text: str | None=None; artifact_path: str | None=None

class VisualObject(BaseModel):
    id: str; type: str; label: str | None=None; direction: str | None=None
    source_region: SourceRegion | None=None

class GraphIR(BaseModel):
    visual_id: str; type: str="graph"; axes: dict[str, object]=Field(default_factory=dict)
    objects: list[VisualObject]=Field(default_factory=list)
    intersections: list[dict[str, object]]=Field(default_factory=list)
    annotations: list[dict[str, object]]=Field(default_factory=list)
    semantic_interpretation: dict[str, str]=Field(default_factory=dict)
    reconstructability: Reconstructability=Reconstructability.partial
    confidence: float=0.0

class EquationIR(BaseModel):
    latex: str; type: str; variables: list[str]=Field(default_factory=list); operation: str | None=None

class TableIR(BaseModel):
    columns: list[str]; rows: list[list[object]]

class VisualArtifact(BaseModel):
    visual_id: str; visual_type: VisualType; source: SourceRegion
    graph: GraphIR | None=None; equation: EquationIR | None=None; table: TableIR | None=None
    confidence: float=0.0

class PageIR(BaseModel):
    page_id: str; page_number: int; text: str=""
    blocks: list[dict[str, object]]=Field(default_factory=list)
    figures: list[str]=Field(default_factory=list); tables: list[str]=Field(default_factory=list)
    equations: list[str]=Field(default_factory=list); visual_regions: list[VisualArtifact]=Field(default_factory=list)

class Concept(BaseModel):
    concept_id: str; name: str; description: str=""
    prerequisites: list[str]=Field(default_factory=list); definitions: list[str]=Field(default_factory=list)
    formulas: list[str]=Field(default_factory=list); examples: list[str]=Field(default_factory=list)
    visuals: list[str]=Field(default_factory=list); evidence: list[SourceRegion]=Field(default_factory=list)

class LearningDocument(BaseModel):
    document_id: str; title: str=""; pages: list[PageIR]=Field(default_factory=list)
    concepts: list[Concept]=Field(default_factory=list); created_at: datetime=Field(default_factory=datetime.utcnow)

class SceneAction(BaseModel):
    start: float=0.0; end: float=0.0; action: str; payload: dict[str, object]=Field(default_factory=dict)

class VisualBlueprint(BaseModel):
    blueprint_id: str; concept_id: str; scene_type: str; learning_objective: str
    objects: list[dict[str, object]]=Field(default_factory=list)
    animations: list[SceneAction]=Field(default_factory=list)
    narration_cues: list[dict[str, object]]=Field(default_factory=list)
    checkpoint: dict[str, object]=Field(default_factory=dict)

class QuestionType(StrEnum):
    recall="RECALL"; conceptual="CONCEPTUAL"; calculation="CALCULATION"; application="APPLICATION"
    transfer="TRANSFER"; error_detection="ERROR_DETECTION"; graph_interpretation="GRAPH_INTERPRETATION"
    diagram_interpretation="DIAGRAM_INTERPRETATION"

class Question(BaseModel):
    question_id: str; concept_id: str; type: QuestionType; prompt: str; answer: str; explanation: str=""

class QuestionRequest(BaseModel):
    concept: Concept; count: int=Field(default=4, ge=1, le=20)

class MasteryState(BaseModel):
    concept_id: str; stability: float=0.0; difficulty: float=0.0; retrievability: float=0.0
    last_review: datetime | None=None; next_review: datetime | None=None
    review_history: list[dict[str, object]]=Field(default_factory=list)
