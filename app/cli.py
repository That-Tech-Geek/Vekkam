from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from app.assessment.mastery import schedule_review
from app.assessment.quiz import generate_questions
from app.blueprints.engine import build_blueprint
from app.core.models import Concept, MasteryState
from app.ingestion.text import ingest_text


def _emit(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, default=str))


def _read_text(path: str | None, inline: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    if inline is not None:
        return inline
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("Provide --text, --file, or pipe text on stdin.")


def _concept(args: argparse.Namespace) -> Concept:
    document = ingest_text(args.document_id, _read_text(args.file, args.text))
    if not document.concepts:
        raise SystemExit("No concepts were produced.")
    return document.concepts[0]


def _review(args: argparse.Namespace) -> None:
    if not args.state:
        state = MasteryState(concept_id="concept")
    else:
        state = MasteryState.model_validate_json(Path(args.state).read_text(encoding="utf-8"))
    _emit(schedule_review(state, args.recalled).model_dump(mode="json"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="examforge",
        description="ExamForge CLI: multimodal exam-preparation engine over canonical Learning IR.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest-text", help="Convert text into canonical Learning IR.")
    ingest.add_argument("--document-id", default="document")
    ingest.add_argument("--text")
    ingest.add_argument("--file", help="UTF-8 text file; omit to read stdin.")
    ingest.set_defaults(
        handler=lambda a: _emit(
            ingest_text(a.document_id, _read_text(a.file, a.text)).model_dump(mode="json")
        )
    )

    blueprint = sub.add_parser("blueprint", help="Build a visual teaching blueprint from text.")
    blueprint.add_argument("--document-id", default="document")
    blueprint.add_argument("--text")
    blueprint.add_argument("--file")
    blueprint.set_defaults(handler=lambda a: _emit(build_blueprint(_concept(a)).model_dump(mode="json")))

    questions = sub.add_parser("questions", help="Generate deterministic active-recall questions.")
    questions.add_argument("--document-id", default="document")
    questions.add_argument("--text")
    questions.add_argument("--file")
    questions.add_argument("--count", type=int, default=4)
    questions.set_defaults(
        handler=lambda a: _emit(
            [q.model_dump(mode="json") for q in generate_questions(_concept(a), a.count)]
        )
    )

    review = sub.add_parser("review", help="Schedule a mastery review from a JSON state.")
    review.add_argument("--state", help="Path to a MasteryState JSON file.")
    review.add_argument("--recalled", action="store_true", help="Mark the review as successfully recalled.")
    review.set_defaults(handler=_review)

    architecture = sub.add_parser("architecture", help="Print the ExamForge pipeline.")
    architecture.set_defaults(
        handler=lambda _: _emit(
            {
                "source_of_truth": "canonical_learning_ir",
                "stages": [
                    "multimodal_extraction",
                    "canonical_learning_ir",
                    "knowledge_graph",
                    "vector_retrieval",
                    "visual_blueprint",
                    "manim_validation",
                    "narration_sync",
                    "active_recall",
                    "mastery",
                    "exam_intelligence",
                ],
            }
        )
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.handler(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
