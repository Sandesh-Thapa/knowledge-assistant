from app.ingestion.chunkers.document_chunker import DocumentChunker
from app.ingestion.models import DocumentChunk, ParsedDocument


class FixedCharacterChunker(DocumentChunker):
    def __init__(self, chunk_size: int):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        self.chunk_size = chunk_size

    def chunk(self, document: ParsedDocument) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []
        chunk_index = 0

        for page in document.pages:
            for start in range(0, len(page.text), self.chunk_size):
                chunk_text = page.text[start:start + self.chunk_size]

                # Skip empty chunks.
                if not chunk_text:
                    continue

                chunks.append(
                    DocumentChunk(
                        chunk_index=chunk_index,
                        text=chunk_text,
                        metadata={
                            "filename": document.filename,
                            "page_number": page.page_number,
                        },
                    )
                )

                chunk_index += 1

        return chunks