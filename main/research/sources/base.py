from abc import ABC, abstractmethod
from pathlib import Path

from main.research.models import SourceDocument


class DocumentLoader(ABC):
    """
    Today, we're loading PDFs. Later we might load HTML pages, markdown documentation etc.
    The research service will work with SourceDocument regardless of where it originated
    Adapter pattern: different source formats adapted into a common representation
    """
    @abstractmethod
    def load(self, path: Path) -> SourceDocument:
        raise NotImplementedError