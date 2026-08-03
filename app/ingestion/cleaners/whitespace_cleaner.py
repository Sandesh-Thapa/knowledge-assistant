from app.ingestion.cleaners.document_cleaner import DocumentCleaner
from app.ingestion.models import ParsedDocument, DocumentPage


class WhitespaceCleaner(DocumentCleaner):
    def clean(self, document: ParsedDocument) -> ParsedDocument:
        cleaned_pages = [
            DocumentPage(
                page_number=page.page_number,
                text=self._clean_text(page.text)
            )
            for page in document.pages
        ]

        return ParsedDocument(
            filename=document.filename,
            metadata=document.metadata,
            pages=cleaned_pages
        )
    

    def _clean_text(self, text: str) -> str:
        return text.strip()