from app.core.models import GraphIR, Reconstructability, VisualObject

def interpret_graph(visual_id: str, x_label: str, y_label: str,
                    objects: list[tuple[str, str, str]]) -> GraphIR:
    parsed=[VisualObject(id=f"{visual_id}_{label.lower()}", type=kind, label=label, direction=direction)
            for label, kind, direction in objects]
    return GraphIR(visual_id=visual_id,
                   axes={"x":{"label":x_label,"scale":"unknown"},"y":{"label":y_label,"scale":"unknown"}},
                   objects=parsed, reconstructability=Reconstructability.reconstructable,
                   confidence=0.9 if parsed else 0.5)
