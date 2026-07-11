from app.ingestion.models import RawDocument
from app.ingestion.parsers.document_parser import DocumentParser


class PDFParser(DocumentParser):
    def parse(self, document: RawDocument):...