import fitz

from app.ingestion.exceptions import PDFParsingError
from app.ingestion.models import (
    DocumentMetadata,
    DocumentPage,
    ParsedDocument,
    RawDocument,
)
from app.ingestion.parsers.document_parser import DocumentParser


class PDFParser(DocumentParser):
    def parse(self, document: RawDocument) -> ParsedDocument:
        try:
            with fitz.open(document.path) as pdf:
                metadata = self._extract_metadata(pdf)
                pages = self._extract_pages(pdf)

                return ParsedDocument(
                    filename=document.filename,
                    metadata=metadata,
                    pages=pages,
                )
        except Exception as exc:
            raise PDFParsingError(
                f"Failed to parse PDF '{document.filename}'"
            ) from exc

    def _extract_metadata(self, pdf: fitz.Document) -> DocumentMetadata:
        return DocumentMetadata(
            page_count=pdf.page_count,
            title=pdf.metadata.get("title") or "",
            author=pdf.metadata.get("author") or "",
        )

    def _extract_pages(self, pdf: fitz.Document) -> list[DocumentPage]:
        pages: list[DocumentPage] = []

        for page in pdf:
            text = page.get_text()
            if text.strip():
                pages.append(DocumentPage(page_number=page.number + 1, text=text))

        return pages