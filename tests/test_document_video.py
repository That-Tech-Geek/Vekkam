from pathlib import Path

import pytest

from app.ingestion.document import ingest_document
from app.video.pipeline import _extract_code, _validate_source


def test_extract_code_block():
    source = "```python\nfrom manim import *\nclass ExamForgeScene(Scene):\n    pass\n```"
    assert _extract_code(source).startswith("from manim import *")


def test_validate_source_accepts_scene():
    _validate_source("from manim import *\nclass ExamForgeScene(Scene):\n    def construct(self):\n        pass\n")


def test_validate_source_rejects_invalid_python():
    with pytest.raises(RuntimeError, match="invalid Python"):
        _validate_source("class ExamForgeScene(Scene):\n    def construct(")


def test_validate_source_rejects_wrong_scene_name():
    with pytest.raises(RuntimeError, match="ExamForgeScene"):
        _validate_source("from manim import *\nclass OtherScene(Scene):\n    pass\n")


def test_ingest_document_rejects_unknown_suffix(tmp_path: Path):
    source = tmp_path / "notes.txt"
    source.write_text("hello", encoding="utf-8")
    with pytest.raises(ValueError, match="\\.pdf or \\.docx"):
        ingest_document(source)
