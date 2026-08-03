class ParserNotFoundError(Exception):
    """Exception raised when no parser is available for a document type."""


class ParsingError(Exception):
    """Base exception for document parsing."""


class PDFParsingError(ParsingError):
    """Exception raised for errors during PDF parsing."""