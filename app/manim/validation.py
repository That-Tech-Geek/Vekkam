from dataclasses import dataclass
from app.core.models import VisualBlueprint

@dataclass
class ValidationReport:
    code_valid: bool
    render_valid: bool
    pedagogical_valid: bool
    errors: list[str]

def validate_blueprint(blueprint: VisualBlueprint) -> ValidationReport:
    errors=[]
    if not blueprint.learning_objective.strip(): errors.append("Missing learning objective.")
    if not blueprint.animations: errors.append("Blueprint contains no animation actions.")
    return ValidationReport(not errors, False, not errors, errors)
