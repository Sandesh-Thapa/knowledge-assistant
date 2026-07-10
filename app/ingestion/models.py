from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class RawDocument:
    path: Path
    filename: str
    extension: str
    category: str


@dataclass
class ParsedDocument:
    text: str
    metadata: dict[str, any] = field(default_factory=dict)
    filename: str


@dataclass
class DocumentChunk:
    chunk_index: int
    text: str
    metadata: dict[str, any] = field(default_factory=dict)