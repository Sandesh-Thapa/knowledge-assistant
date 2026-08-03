from app.ingestion.models import ParsedDocument
from app.ingestion.cleaners.document_cleaner import DocumentCleaner


class CleanerPipeline(DocumentCleaner):
    def __init__(self, cleaners: list[DocumentCleaner]):
        self.cleaners = cleaners

    def clean(self, document: ParsedDocument) -> ParsedDocument:
        for cleaner in self.cleaners:
            document = cleaner.clean(document)
        return document