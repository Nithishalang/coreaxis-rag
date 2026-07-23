from src.loaders.pdf_loader import PDFLoader
from src.preprocess.cleaner import TextCleaner
from src.chunking.chunker import Chunker
from src.embeddings.embedder import Embedder
import pickle
import os
def main():
    print("=" * 60)
    print("Building CoreAxis Vector Database")
    print("=" * 60)
    print("\nLoading PDFs...")
    loader = PDFLoader()
    documents = loader.load_directory("data/raw")
    print(f"\nLoaded {len(documents)} pages")
    print("\nCleaning documents...")
    cleaner = TextCleaner()
    documents = cleaner.clean_documents(documents)
    print("\nChunking documents...")
    chunker = Chunker()
    chunks = chunker.chunk_documents(documents)
    print(f"Generated {len(chunks)} chunks")
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    print(f"Saved {len(chunks)} chunks.")
    print("\nGenerating embeddings...")
    embedder = Embedder()
    embedder.embed_documents(chunks)
    print("\n" + "=" * 60)
    print("Database built successfully!")
    print("=" * 60)
if __name__ == "__main__":
    main()