from pathlib import Path

from main.research.models import SourceDocument, DocumentSection, SourceReference
from main.research.sources.base import DocumentLoader
import fitz
import logging
import hashlib

logger = logging.getLogger(__name__)

class PDFDocumentLoader(DocumentLoader):
    @staticmethod
    def calculate_file_hash(path: Path) -> str:
        digest = hashlib.sha256()

        with path.open("rb") as file:
            for block in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(block)

        return digest.hexdigest()
    
    def load(self, path: Path) -> SourceDocument:
        if not path.is_file():
            logger.error(f"The file does not exist at path: {path}")
            raise ValueError(f"The file at path: {path} does not exist for loading pdf")

        
        with fitz.open(path) as pdf:
            # one page is one section in this case
            document_sections: list[DocumentSection] = []
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text()
                if not text or not text.strip():
                    logger.info(f"Got an empty page: {page_number}, ignoring")
                    continue

                section = DocumentSection(
                    text=text,
                    locator=f"page: {page_number}"
                )
                document_sections.append(section)
            
            if not document_sections:
                # maybe we can add ocr ability for documents containing images but not text
                raise ValueError(
                    f"No extractable text found in PDF: {path}. "
                    "It may be a scanned document requiring OCR."
                )
            
            file_hash = self.calculate_file_hash(path)
            crafted_doc_id = f"sha256:{file_hash}"
            document = SourceDocument(
                sections=tuple(document_sections),
                source=SourceReference(
                    source_id=crafted_doc_id,
                    title=crafted_doc_id,
                    source_type="PDF document",
                    uri=path.resolve().as_uri(),
                    metadata={
                        "path": str(path.resolve()),
                        "filename": path.name,
                        "sha256": file_hash
                    }
                )
            )
            return document