# ExamForge Architecture

The Technical Implementation Plan v2 is the source of truth.

## Core rule

**The canonical learning representation, not Neo4j, the LLM, or the video, is the source of truth.**

The models in `app/core/models.py` implement that contract.

## Flow

1. Inputs: textbook PDFs, slides, graphs/diagrams and past papers.
2. Multimodal extraction: PyMuPDF/OCR/OpenCV/vision adapters preserve coordinates and provenance.
3. Canonical Learning IR: pages, concepts, graph IR, equation IR and table IR.
4. Knowledge: the same IR populates Neo4j and Qdrant through ports.
5. Visual blueprint: concept + evidence + prerequisites + visual IR becomes a declarative blueprint.
6. Manim compiler: blueprints select templates; generation is isolated from the LLM; validation precedes acceptance.
7. Narration/sync: narration derives from the same blueprint.
8. Assessment: questions, rescue and mastery operate on concept IDs.
9. Exam intelligence: PYQs attach to concepts and retain provenance.

## Production adapters

PyMuPDF, pymupdf4llm, Tesseract, OpenCV, a vision model, Neo4j, Qdrant, Manim, Kokoro/Piper, WhisperX, FFmpeg, FSRS and LangGraph/Celery/RQ belong behind adapter boundaries.

## Validation

Manim acceptance has three layers: code validity, visual/render validity and pedagogical validity. Graph extraction carries reconstructability and confidence, with original-figure fallback when reconstruction is not safe.
