"""Public compatibility import for ExamForge document ingestion."""

from app.ingestion.document import DocumentIngestor, ingest_document

__all__ = ["DocumentIngestor", "ingest_document"]
