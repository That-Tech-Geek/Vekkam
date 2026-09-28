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
from app.llm.client import LLMClient, LLMConfig, config_path, load_config, save_config
from app.video.pipeline import generate_video


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


def _video(args: argparse.Namespace) -> None:
    result = generate_video(args.file, args.output)
    _emit(
        {
            "source": str(result.source_path),
            "output": str(result.output_path),
            "scene": str(result.scene_path),
            "document_id": result.document_id,
            "provider": result.provider,
            "model": result.model,
        }
    )


def _llm_connect_api(args: argparse.Namespace) -> None:
    config = LLMConfig(provider="api", endpoint=args.endpoint, model=args.model, api_key_env=args.api_key_env)
    path = save_config(config)
    _emit({"provider": config.provider, "endpoint": config.endpoint, "model": config.model, "api_key_env": config.api_key_env, "config_path": str(path)})


def _llm_connect_ollama(args: argparse.Namespace) -> None:
    config = LLMConfig(provider="ollama", endpoint=args.endpoint, model=args.model)
    path = save_config(config)
    _emit({"provider": config.provider, "endpoint": config.endpoint, "model": config.model, "config_path": str(path)})


def _llm_status(_: argparse.Namespace) -> None:
    config = load_config()
    if config is None:
        _emit({"connected": False, "config_path": str(config_path())})
        return
    _emit({
        "connected": True,
        "provider": config.provider,
        "endpoint": config.endpoint,
        "model": config.model,
        "api_key_env": config.api_key_env,
        "api_key_configured": bool(config.api_key),
        "config_path": str(config_path()),
    })


def _llm_chat(args: argparse.Namespace) -> None:
    config = load_config()
    if config is None:
        raise SystemExit("No LLM linked. Run examforge llm connect-api or examforge llm connect-ollama.")
    response = LLMClient(config).chat(args.prompt, args.system)
    _emit({"provider": config.provider, "model": config.model, "response": response})


def _llm_parser(sub: argparse._SubParsersAction) -> None:
    llm = sub.add_parser("llm", help="Link ExamForge to an LLM provider.")
    llm_sub = llm.add_subparsers(dest="llm_command", required=True)

    api = llm_sub.add_parser("connect-api", help="Link an OpenAI-compatible LLM API.")
    api.add_argument("--endpoint", default="https://api.openai.com/v1")
    api.add_argument("--model", required=True)
    api.add_argument("--api-key-env", default="OPENAI_API_KEY", help="Environment variable containing the API key.")
    api.set_defaults(handler=_llm_connect_api)

    ollama = llm_sub.add_parser("connect-ollama", help="Link a local Ollama server.")
    ollama.add_argument("--endpoint", default="http://localhost:11434")
    ollama.add_argument("--model", required=True, help="Installed Ollama model, e.g. llama3.2:3b.")
    ollama.set_defaults(handler=_llm_connect_ollama)

    status = llm_sub.add_parser("status", help="Show the active LLM connection.")
    status.set_defaults(handler=_llm_status)

    chat = llm_sub.add_parser("chat", help="Send one prompt through the active LLM.")
    chat.add_argument("prompt")
    chat.add_argument("--system")
    chat.set_defaults(handler=_llm_chat)


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

    video = sub.add_parser("video", help="Convert a PDF or DOCX document into a rendered Manim video.")
    video.add_argument("--file", required=True, help="Path to a .pdf or .docx document.")
    video.add_argument("--output", help="Output .mp4 path; defaults to the input filename with .mp4.")
    video.set_defaults(handler=_video)

    review = sub.add_parser("review", help="Schedule a mastery review from a JSON state.")
    review.add_argument("--state", help="Path to a MasteryState JSON file.")
    review.add_argument("--recalled", action="store_true", help="Mark the review as successfully recalled.")
    review.set_defaults(handler=_review)

    _llm_parser(sub)

    architecture = sub.add_parser("architecture", help="Print the ExamForge pipeline.")
    architecture.set_defaults(
        handler=lambda _: _emit(
            {
                "source_of_truth": "canonical_learning_ir",
                "stages": ["multimodal_extraction", "canonical_learning_ir", "knowledge_graph", "vector_retrieval", "visual_blueprint", "manim_validation", "narration_sync", "active_recall", "mastery", "exam_intelligence", "llm_integration"],
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
