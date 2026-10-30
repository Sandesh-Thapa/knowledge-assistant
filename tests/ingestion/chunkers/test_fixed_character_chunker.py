import pytest

from app.ingestion.chunkers.fixed_character_chunker import FixedCharacterChunker
from app.ingestion.models import DocumentPage, ParsedDocument


@pytest.fixture
def document() -> ParsedDocument:
    return ParsedDocument(
        filename="handbook.pdf",
        metadata={
            "page_count": 2,
            "title": "Employee Handbook",
            "author": "HR",
        },
        pages=[
            DocumentPage(page_number=1, text="ABCDEFGHIJ"),
            DocumentPage(page_number=3, text="KLMNO"),
        ],
    )


def test_rejects_zero_chunk_size():
    with pytest.raises(ValueError):
        FixedCharacterChunker(chunk_size=0)


def test_rejects_negative_chunk_size():
    with pytest.raises(ValueError):
        FixedCharacterChunker(chunk_size=-10)


def test_splits_text_into_fixed_size_chunks():
    chunker = FixedCharacterChunker(chunk_size=4)

    document = ParsedDocument(
        filename="test.pdf",
        metadata={"page_count": 1, "title": "", "author": ""},
        pages=[DocumentPage(page_number=1, text="ABCDEFGHI")],
    )

    chunks = chunker.chunk(document)

    assert [chunk.text for chunk in chunks] == [
        "ABCD",
        "EFGH",
        "I",
    ]


def test_preserves_filename_and_original_page_number(document):
    chunker = FixedCharacterChunker(chunk_size=4)

    chunks = chunker.chunk(document)

    assert chunks[0].metadata == {
        "filename": "handbook.pdf",
        "page_number": 1,
    }
    assert chunks[3].metadata == {
        "filename": "handbook.pdf",
        "page_number": 3,
    }


def test_chunk_indices_are_sequential_across_pages(document):
    chunker = FixedCharacterChunker(chunk_size=4)

    chunks = chunker.chunk(document)

    assert [chunk.chunk_index for chunk in chunks] == [0, 1, 2, 3, 4]


def test_text_shorter_than_chunk_size_produces_one_chunk():
    chunker = FixedCharacterChunker(chunk_size=100)

    document = ParsedDocument(
        filename="short.pdf",
        metadata={"page_count": 1, "title": "", "author": ""},
        pages=[DocumentPage(page_number=1, text="Hello")],
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 1
    assert chunks[0].text == "Hello"


def test_empty_page_produces_no_chunks():
    chunker = FixedCharacterChunker(chunk_size=5)

    document = ParsedDocument(
        filename="empty.pdf",
        metadata={"page_count": 1, "title": "", "author": ""},
        pages=[DocumentPage(page_number=7, text="")],
    )

    assert chunker.chunk(document) == []


def test_does_not_modify_original_document(document):
    chunker = FixedCharacterChunker(chunk_size=4)
    original_texts = [page.text for page in document.pages]

    chunker.chunk(document)

    assert [page.text for page in document.pages] == original_texts


@pytest.mark.parametrize(
    ("chunk_size", "overlap", "expected"),
    [
        (5, 0, ["ABCDE", "FGHIJ", "KLMNO"]),
        (5, 2, ["ABCDE", "DEFGH", "GHIJK", "JKLMN", "MNO"]),
        (5, 4, ["ABCDE", "BCDEF", "CDEFG", "DEFGH", "EFGHI",
                "FGHIJ", "GHIJK", "HIJKL", "IJKLM", "JKLMN",
                "KLMNO", "LMNO", "MNO", "NO", "O"]),
    ]
)
def test_chunks_with_overlap(chunk_size, overlap, expected):
    chunker = FixedCharacterChunker(chunk_size=chunk_size, overlap=overlap)

    document = ParsedDocument(
        filename="test.pdf",
        metadata={"page_count": 1, "title": "", "author": ""},
        pages=[DocumentPage(page_number=1, text="ABCDEFGHIJKLMNO")],
    )

    chunks = chunker.chunk(document)

    assert [chunk.text for chunk in chunks] == expected


@pytest.mark.parametrize("chunk_size", [0, -1])
def test_rejects_invalid_chunk_size(chunk_size):
    with pytest.raises(ValueError):
        FixedCharacterChunker(chunk_size=chunk_size)


@pytest.mark.parametrize("overlap", [-1, 5, 10])
def test_rejects_invalid_overlap(overlap):
    with pytest.raises(ValueError):
        FixedCharacterChunker(chunk_size=5, overlap=overlap)


@pytest.mark.parametrize("value", [1.5, "5", True])
def test_rejects_non_integer_chunk_size(value):
    with pytest.raises(TypeError):
        FixedCharacterChunker(chunk_size=value)


@pytest.mark.parametrize("value", [1.5, "2", True])
def test_rejects_non_integer_overlap(value):
    with pytest.raises(TypeError):
        FixedCharacterChunker(chunk_size=5, overlap=value)