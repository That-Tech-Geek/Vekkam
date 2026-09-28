from __future__ import annotations

import ast
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from app.ingestion.document import ingest_document
from app.llm.client import LLMClient, load_config

_ALLOWED_CLASS_PATTERN = re.compile(r"class\s+ExamForgeScene\s*\(\s*Scene\s*\)")


@dataclass(frozen=True)
class VideoResult:
    source_path: Path
    output_path: Path
    scene_path: Path
    document_id: str
    provider: str
    model: str


def _extract_code(response: str) -> str:
    match = re.search(r"```(?:python)?\s*(.*?)```", response, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else response.strip()


def _validate_source(source: str) -> None:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise RuntimeError(f"LLM returned invalid Python: {exc}") from exc

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            raise RuntimeError("Generated source may only import from manim.")
        if isinstance(node, ast.ImportFrom) and node.module != "manim":
            raise RuntimeError("Generated source may only import from manim.")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {
            "eval", "exec", "open", "compile", "__import__", "input"
        }:
            raise RuntimeError(f"Generated source uses forbidden function: {node.func.id}")
        if isinstance(node, ast.Name) and node.id in {
            "os", "sys", "subprocess", "pathlib", "socket", "requests"
        }:
            raise RuntimeError(f"Generated source uses forbidden module/name: {node.id}")

    if not _ALLOWED_CLASS_PATTERN.search(source):
        raise RuntimeError("Generated Manim source must define an ExamForgeScene(Scene) class.")

    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    if not any(node.name == "ExamForgeScene" for node in classes):
        raise RuntimeError("Generated source does not contain ExamForgeScene.")


def _prompt(title: str, text: str) -> str:
    return f"""Create a concise educational Manim Community Edition video from the document below.

Document title: {title}

Requirements:
- Return ONLY complete Python source code.
- Import from manim with: from manim import *
- Define exactly one main scene named ExamForgeScene(Scene).
- Teach the most important concepts in a clear sequence using Text, MathTex, axes, shapes, arrows, and simple animations where useful.
- Prefer deterministic, readable Manim primitives over external assets.
- Keep rendering practical: target roughly 30-90 seconds and avoid expensive simulations.
- Do not use network access, file I/O, subprocesses, eval, exec, or arbitrary imports.
- Escape text safely and use MathTex only for valid LaTeX.
- The scene must run with standard Manim Community Edition.

DOCUMENT:
{text[:30000]}
"""


def generate_video(
    source_path: str | Path,
    output_path: str | Path | None = None,
) -> VideoResult:
    source = Path(source_path).expanduser().resolve()
    if not source.exists() or not source.is_file():
        raise FileNotFoundError(f"Input file not found: {source}")
    if source.suffix.lower() not in {".pdf", ".docx"}:
        raise ValueError("Input must be a .pdf or .docx file.")

    config = load_config()
    if config is None:
        raise RuntimeError(
            "No LLM linked. Run examforge llm connect-api or "
            "examforge llm connect-ollama first."
        )

    document = ingest_document(source)
    if not document.pages:
        raise RuntimeError("No readable content was extracted from the document.")

    text = "\n\n".join(page.text for page in document.pages if page.text.strip())
    if not text.strip():
        raise RuntimeError("The document contains no extractable text.")

    response = LLMClient(config).chat(_prompt(document.title, text))
    manim_source = _extract_code(response)
    _validate_source(manim_source)

    target = Path(output_path).expanduser() if output_path else source.with_suffix(".mp4")
    target = target.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)

    scene_dir = target.parent / ".examforge" / source.stem
    scene_dir.mkdir(parents=True, exist_ok=True)
    scene_path = scene_dir / "scene.py"
    scene_path.write_text(manim_source + "\n", encoding="utf-8")

    command = [
        sys.executable, "-m", "manim", "-q", "m", str(scene_path), "ExamForgeScene",
        "--media_dir", str(scene_dir / "media"), "-o", target.name,
    ]
    try:
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Manim is not installed. Install the generation extra: "
            "python -m pip install -e '.[generation]'"
        ) from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "unknown Manim error").strip()
        raise RuntimeError(f"Manim render failed: {detail}") from exc

    rendered = scene_dir / "media" / "videos" / "scene" / "720p30" / target.name
    if rendered.exists() and rendered != target:
        target.write_bytes(rendered.read_bytes())
    elif not target.exists():
        candidates = list((scene_dir / "media").rglob(target.name))
        if candidates:
            target.write_bytes(candidates[0].read_bytes())

    if not target.exists():
        raise RuntimeError(
            "Manim completed without producing the expected video output. "
            f"stdout: {completed.stdout[-1000:]}"
        )

    return VideoResult(
        source_path=source,
        output_path=target,
        scene_path=scene_path,
        document_id=document.document_id,
        provider=config.provider,
        model=config.model,
    )
