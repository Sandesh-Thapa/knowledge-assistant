from collections.abc import Collection, Iterator
from pathlib import Path
from app.ingestion.models import RawDocument


class DocumentLoader:
    def __init__(self, root_directory: Path, supported_extensions: Collection[str]):
        self.root_directory = root_directory
        self.supported_extensions = {ext.lower() for ext in supported_extensions}

    def load(self) -> Iterator[RawDocument]:
        if not self.root_directory.is_dir():
            raise FileNotFoundError(f"Directory {self.root_directory.name} does not exists!")
        
        for file in self.root_directory.rglob("*"):
            if file.is_file() and file.suffix.lower() in self.supported_extensions:
                yield RawDocument(
                    path=file,
                    filename=file.name,
                    extension=file.suffix.lower(),
                    category=file.parent.name
                )