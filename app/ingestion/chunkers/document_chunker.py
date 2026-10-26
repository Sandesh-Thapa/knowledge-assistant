from abc import ABC, abstractmethod

from app.ingestion.models import DocumentChunk, ParsedDocument


class DocumentChunker(ABC):
    @abstractmethod
    def chunk(self, document: ParsedDocument) -> list[DocumentChunk]:
        """Chunk the given document into smaller parts."""
        pass