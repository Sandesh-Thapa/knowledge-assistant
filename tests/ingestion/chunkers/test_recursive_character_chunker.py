import pytest

from app.ingestion.chunkers.recursive_character_chunker import RecursiveCharacterChunker
from app.ingestion.models import DocumentPage, ParsedDocument


@pytest.fixture
def document():
    return ParsedDocument(
        filename="handbook.pdf",
        metadata={
            "page_count": 1,
            "title": "Employee Handbook",
            "author": "HR",
        },
        pages=[
            DocumentPage(
                page_number=1,
                text="Hello world.\n\nHow are you?\n\nI am learning Python.",
            )
        ],
    )


def test_returns_single_chunk_when_text_fits():
    chunker = RecursiveCharacterChunker(chunk_size=100)

    document = ParsedDocument(
        filename="test.pdf",
        metadata={"page_count": 1, "title": "", "author": ""},
        pages=[DocumentPage(page_number=1, text="Hello world.")],
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 1
    assert chunks[0].text == "Hello world."


def test_preserves_paragraph_boundaries_when_possible():
    chunker = RecursiveCharacterChunker(chunk_size=30)

    document = ParsedDocument(
        filename="test.pdf",
        metadata={"page_count": 1, "title": "", "author": ""},
        pages=[
            DocumentPage(
                page_number=1,
                text="First paragraph.\n\nSecond paragraph.",
            )
        ],
    )

    chunks = chunker.chunk(document)

    assert [chunk.text for chunk in chunks] == [
        "First paragraph.\n\n",
        "Second paragraph.",
    ]


def test_preserves_page_metadata():
    chunker = RecursiveCharacterChunker(chunk_size=10)

    document = ParsedDocument(
        filename="handbook.pdf",
        metadata={"page_count": 1, "title": "", "author": ""},
        pages=[
            DocumentPage(page_number=3, text="ABCDEFGHIJKLMNO"),
        ],
    )

    chunks = chunker.chunk(document)

    assert all(
        chunk.metadata["filename"] == "handbook.pdf"
        and chunk.metadata["page_number"] == 3
        for chunk in chunks
    )


def test_chunk_indices_are_sequential():
    chunker = RecursiveCharacterChunker(chunk_size=5)

    document = ParsedDocument(
        filename="test.pdf",
        metadata={"page_count": 1, "title": "", "author": ""},
        pages=[
            DocumentPage(page_number=1, text="ABCDEFGHIJKLMNO"),
        ],
    )

    chunks = chunker.chunk(document)

    assert [chunk.chunk_index for chunk in chunks] == list(range(len(chunks)))


def test_does_not_modify_original_document(document):
    chunker = RecursiveCharacterChunker(chunk_size=15)
    original_text = document.pages[0].text

    chunker.chunk(document)

    assert document.pages[0].text == original_text


def test_rejects_invalid_chunk_size():
    with pytest.raises(ValueError):
        RecursiveCharacterChunker(chunk_size=0)


def test_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        RecursiveCharacterChunker(chunk_size=10, overlap=10)


def test_preserves_trailing_paragraph_whitespace():
    chunker = RecursiveCharacterChunker(chunk_size=20)

    text = "First paragraph.\n\nSecond paragraph."

    chunks = chunker._split_text(text)

    assert chunks == [
        "First paragraph.\n\n",
        "Second paragraph.",
    ]


def test_preserves_whitespace_between_merged_splits():
    chunker = RecursiveCharacterChunker(chunk_size=30)

    text = "Hello world. This is Python."

    chunks = chunker._split_text(text)

    assert "".join(chunks) == text


def test_preserves_whitespace_across_multiple_paragraphs():
    chunker = RecursiveCharacterChunker(chunk_size=25)

    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."

    chunks = chunker._split_text(text)

    assert "".join(chunks) == text
    assert all(len(chunk) <= 25 for chunk in chunks)


def test_preserves_whitespace_with_overlap():
    chunker = RecursiveCharacterChunker(
        chunk_size=15,
        overlap=3,
    )

    text = "Hello world. This is a test."

    chunks = chunker._split_text(text)

    assert all(len(chunk) <= 15 for chunk in chunks)
    assert all(chunk.strip() for chunk in chunks)
