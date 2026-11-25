from pathlib import Path

from main.research.sources.pdf import PDFDocumentLoader


loader = PDFDocumentLoader()

document = loader.load(
    Path("/Users/kmpandey/Desktop/Projects/Adaptive RAG/data/raw/tsla-10k.pdf")
)

print(document.source)
print(f"Pages extracted: {len(document.sections)}")

for section in document.sections[:2]:
    print(section.locator)
    print(section.text[:500])