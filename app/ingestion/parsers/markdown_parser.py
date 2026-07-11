from app.ingestion.parsers.document_parser import DocumentParser
from app.ingestion.models import ParsedDocument, RawDocument


class MarkdownParser(DocumentParser):
    def parse(self, document: RawDocument) -> ParsedDocument:...