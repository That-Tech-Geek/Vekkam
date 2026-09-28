from app.core.ids import stable_id
from app.core.models import Concept, SceneAction, VisualBlueprint

def build_blueprint(concept: Concept) -> VisualBlueprint:
    scene_type="graph_plot" if concept.visuals else "comparison"
    return VisualBlueprint(
        blueprint_id=stable_id("blueprint", concept.concept_id),
        concept_id=concept.concept_id,
        scene_type=scene_type,
        learning_objective=f"Understand {concept.name}",
        objects=[{"concept_id":concept.concept_id,"name":concept.name}],
        animations=[SceneAction(start=0,end=2,action="introduce_concept")],
        narration_cues=[{"at":0,"text":concept.description[:500]}],
        checkpoint={"type":"active_recall","concept_id":concept.concept_id},
    )
