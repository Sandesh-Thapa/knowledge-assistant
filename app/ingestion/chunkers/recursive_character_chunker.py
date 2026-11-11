from app.ingestion.chunkers.document_chunker import DocumentChunker
from app.ingestion.models import DocumentChunk, ParsedDocument

class RecursiveCharacterChunker(DocumentChunker):
    SEPARATORS = [
        "\n\n",  # Paragraph
        "\n",    # Line
        ". ",    # Sentence
        " ",     # Word
        "",      # Character (last resort)
    ]

    def __init__(self, chunk_size: int, overlap: int = 0) -> None:
        if not isinstance(chunk_size, int) or isinstance(chunk_size, bool):
            raise TypeError("chunk_size must be an integer")

        if not isinstance(overlap, int) or isinstance(overlap, bool):
            raise TypeError("overlap must be an integer")
        
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")
        
        if not 0 <= overlap < chunk_size:
            raise ValueError("overlap must be a non-negative integer less than chunk_size")
        
        self.chunk_size = chunk_size
        self.overlap = overlap


    def chunk(self, document: ParsedDocument) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []

        for page in document.pages:
            page_chunks = self._split_text(page.text)

            for text in page_chunks:
                if not text.strip():
                    continue

                chunks.append(
                    DocumentChunk(
                        chunk_index=len(chunks),
                        text=text,
                        metadata={
                            "filename": document.filename,
                            "page_number": page.page_number,
                        },
                    )
                )

        return chunks
    

    def _split_text(self, text: str, separators: list[str] | None = None) -> list[str]:

        if len(text) <= self.chunk_size:
            return [text] if text.strip() else []

        if separators is None:
            separators = self.SEPARATORS.copy()

        separator = self._get_separator(text, separators)

        if separator is None:
            return self._split_by_size(text)

        separator_index = separators.index(separator)
        remaining_separators = separators[separator_index + 1:]

        splits = text.split(separator)

        if separator:
            splits = [
                part + separator
                for part in splits[:-1]
            ] + [splits[-1]]

        return self._merge_splits(splits, remaining_separators)

    
    def _get_separator(self, text: str, separators: list[str]) -> str | None:
        for separator in separators:
            if separator and separator in text:
                return separator

        return None
    
    
    def _split_by_size(self, text: str) -> list[str]:
        step = self.chunk_size - self.overlap
        return [
            text[i:i + self.chunk_size]
            for i in range(0, len(text), step)
        ]
    

    def _merge_splits(self, splits: list[str], remaining_separators: list[str]) -> list[str]:
        chunks: list[str] = []
        current: list[str] = []
        current_length = 0

        for split in splits:

            if len(split) > self.chunk_size:
                if current:
                    chunks.extend(self._merge_current(current))
                    current = []
                    current_length = 0

                chunks.extend(
                    self._split_text(split, remaining_separators)
                )
                continue

            if current_length + len(split) > self.chunk_size:
                chunks.extend(self._merge_current(current))

                while current and current_length > self.overlap:
                    current_length -= len(current.pop(0))

                current_length = sum(len(part) for part in current)

            current.append(split)
            current_length += len(split)

        if current:
            chunks.extend(self._merge_current(current))

        return chunks    

    
    def _merge_current(self, splits: list[str]) -> list[str]:
        text = "".join(splits)
        return [text] if text.strip() else []
