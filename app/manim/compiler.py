from dataclasses import dataclass
from app.core.models import VisualBlueprint

@dataclass
class CompilationResult:
    valid: bool
    source: str
    errors: list[str]

class ManimCompiler:
    """Blueprint -> template -> Manim source. The LLM never owns this interface."""
    def compile(self, blueprint: VisualBlueprint) -> CompilationResult:
        source=("from manim import *\n\nclass ExamForgeScene(Scene):\n"
                "    def construct(self):\n"
                f"        title = Text({blueprint.learning_objective!r})\n"
                "        self.play(Write(title))\n        self.wait(1)\n")
        return CompilationResult(True, source, [])
