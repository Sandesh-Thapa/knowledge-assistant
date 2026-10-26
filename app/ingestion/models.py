from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict, Any

@dataclass
class RawDocument:
    path: Path
    filename: str
    extension: str
    category: str


class DocumentMetadata(TypedDict):
    page_count: int
    title: str
    author: str


@dataclass
class DocumentPage:
    page_number: int
    text: str


@dataclass
class ParsedDocument:
    filename: str
    metadata: DocumentMetadata
    pages: list[DocumentPage]

    @property
    def text(self) -> str:
        return "\n\n".join(page.text for page in self.pages)


class ChunkMetadata(TypedDict):
    filename: str
    page_number: int


@dataclass
class DocumentChunk:
    chunk_index: int
    text: str
    metadata: ChunkMetadata