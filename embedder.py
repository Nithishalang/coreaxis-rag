from sentence_transformers import SentenceTransformer
import chromadb
class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )
        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )
        try:
            self.client.delete_collection("coreaxis_handbooks")
        except:
            pass
        self.collection = self.client.create_collection(
            name="coreaxis_handbooks"
        )
    def embed_documents(self, chunks, batch_size=64):
        print(f"\nEmbedding {len(chunks)} chunks...\n")
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            texts = [
                chunk["text"]
                for chunk in batch
            ]
            embeddings = self.model.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=False
            ).tolist()
            ids = [
                chunk["metadata"]["chunk_id"]
                for chunk in batch
            ]
            metadatas = [
                chunk["metadata"]
                for chunk in batch
            ]
            self.collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas
            )
            print(
                f"Embedded {min(start + batch_size, len(chunks))}/{len(chunks)}"
            )
    def get_collection(self):
        return self.collection