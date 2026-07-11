from app.ingestion.parsers.document_parser import DocumentParser
from app.ingestion.parsers.docx_parser import DOCXParser
from app.ingestion.parsers.markdown_parser import MarkdownParser
from app.ingestion.parsers.pdf_parser import PDFParser


class ParserNotFoundError(Exception):...


class ParserFactory:
    def __init__(self):
        self.parsers = {
            ".pdf": PDFParser(),
            ".docx": DOCXParser(),
            ".md": MarkdownParser(),
        }

    def get_parser(self, extension: str) -> DocumentParser:
        parser_class = self.parsers.get(extension.lower())
        if not parser_class:
            raise ParserNotFoundError(f"No parser registered for extension: {extension}")
        return parser_class