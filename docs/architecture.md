# ExamForge Architecture

The Technical Implementation Plan v2 is the source of truth.

## Core rule

**The canonical learning representation, not Neo4j, the LLM, or the video, is the source of truth.**

The models in `app/core/models.py` implement that contract.

## Flow

1. Inputs: textbook PDFs, DOCX files, slides, graphs/diagrams and past papers.
2. Multimodal extraction: PyMuPDF/DOCX/OCR/OpenCV/vision adapters preserve coordinates and provenance where available.
3. Canonical Learning IR: pages, concepts, graph IR, equation IR and table IR.
4. Knowledge: the same IR populates Neo4j and Qdrant through ports.
5. Visual blueprint: concept + evidence + prerequisites + visual IR becomes a declarative blueprint.
6. Manim compiler: blueprints select templates; generation is isolated from the LLM; validation precedes acceptance.
7. Document-to-video path: `examforge video --file <path>` extracts PDF/DOCX text, sends the learning material to the configured LLM for scene generation, validates the generated Python, then renders `ExamForgeScene` with Manim.
8. Narration/sync: narration derives from the same blueprint.
9. Assessment: questions, rescue and mastery operate on concept IDs.
10. Exam intelligence: PYQs attach to concepts and retain provenance.

## Production adapters

PyMuPDF, python-docx, pymupdf4llm, Tesseract, OpenCV, a vision model, Neo4j, Qdrant, Manim, Kokoro/Piper, WhisperX, FFmpeg, FSRS and LangGraph/Celery/RQ belong behind adapter boundaries.

## Validation

Manim acceptance has three layers: code validity, visual/render validity and pedagogical validity. The document-to-video path performs syntax and import/security validation before handing generated source to Manim. Graph extraction carries reconstructability and confidence, with original-figure fallback when reconstruction is not safe.
