from abc import ABC, abstractmethod
from app.ingestion.models import RawDocument, ParsedDocument


class DocumentParser(ABC):
    @abstractmethod
    def parse(self, document: RawDocument) -> ParsedDocument:...