# ExamForge

Vekkam is now **ExamForge**: a multimodal exam-preparation engine built around a canonical Learning IR.

The canonical Learning IR is the source of truth. Storage engines, retrieval, LLMs, Manim, narration, quizzes, and mastery state are adapters around that representation.

## Pipeline

```
SOURCE MATERIAL -> MULTIMODAL EXTRACTION -> CANONICAL LEARNING IR
-> KNOWLEDGE GRAPH + VECTOR RETRIEVAL -> VISUAL BLUEPRINT
-> MANIM COMPILER + VALIDATION -> NARRATION + SYNC -> VIDEO
-> ACTIVE RECALL + FSRS -> EXAM INTELLIGENCE
```

## Layout
- `app/core/` canonical domain models and stable IDs
- `app/ingestion/` document/OCR/image extraction
- `app/visual/` graph, table and equation understanding
- `app/knowledge/` graph and vector-store ports
- `app/blueprints/` declarative teaching blueprints
- `app/manim/` scene compilation and validation
- `app/audio/` narration and synchronization
- `app/assessment/` recall, rescue and mastery
- `app/api/` FastAPI surface
- `tests/` contracts
- `docs/` architecture and roadmap

## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Optional integrations are isolated behind adapters: PyMuPDF/OCR/OpenCV, Neo4j, Qdrant, Manim, Kokoro/Piper and WhisperX.
