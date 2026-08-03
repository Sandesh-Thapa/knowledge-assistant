from abc import ABC, abstractmethod

from app.ingestion.models import ParsedDocument

class DocumentCleaner(ABC):
    @abstractmethod
    def clean(self, document: ParsedDocument) -> ParsedDocument:
        """Clean the given document and return the cleaned version."""
        pass