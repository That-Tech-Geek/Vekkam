from pathlib import Path
from app.core.models import LearningDocument

class DocumentIngestor:
    """Boundary for PyMuPDF/OCR/OpenCV-backed document ingestion."""
    def ingest(self, path: Path) -> LearningDocument:
        raise NotImplementedError("Install document extras and provide a concrete adapter.")
