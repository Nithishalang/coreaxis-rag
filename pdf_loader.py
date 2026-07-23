import fitz
from pathlib import Path
class PDFLoader:
    def load_pdf(self, pdf_path: str):
        document = fitz.open(pdf_path)
        pages = []
        for page_number, page in enumerate(document):
            pages.append({
                "text": page.get_text("text"),
                "metadata": {
                    "source": Path(pdf_path).name,
                    "page": page_number + 1
                }
            })
        document.close()
        return pages
    def load_directory(self, directory: str):
        all_pages = []
        pdf_files = Path(directory).glob("*.pdf")
        for pdf in pdf_files:
            print(f"Loading {pdf.name}...")
            pages = self.load_pdf(str(pdf))
            all_pages.extend(pages)
        return all_pages

if __name__ == "__main__":
    loader = PDFLoader()
    documents = loader.load_directory("data/raw")
    print(f"\nLoaded {len(documents)} pages.\n")
    print(documents[0]["metadata"])
    print("-" * 50)
    print(documents[0]["text"][:500])