import chromadb
from sentence_transformers import SentenceTransformer
from src.retrieval.rrf import ReciprocalRankFusion
from src.retrieval.bm25_retriever import BM25Retriever
class Retriever:
    def __init__(self):
        print("Loading Vector Retriever...")
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )
        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )
        self.collection = self.client.get_collection(
            "coreaxis_handbooks"
        )
        print("Loading BM25 Retriever...")
        self.bm25 = BM25Retriever()
        self.rrf = ReciprocalRankFusion()
    def search(self, query, departments, top_k=20):
        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        ).tolist()
        vector_chunks = []
        for department in departments:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where={
                    "department": department
                }
            )
            documents = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0]
            for doc, meta, dist in zip(
                documents,
                metadatas,
                distances
            ):
                vector_chunks.append({
                    "text": doc,
                    "metadata": meta,
                    "distance": dist
                })
        bm25_chunks = self.bm25.search(
        query,
        departments=departments,
        top_k=top_k
    )
        bm25_chunks = [
            chunk
            for chunk in bm25_chunks
            if chunk["metadata"]["department"] in departments
        ]
        merged_chunks = self.rrf.fuse(
            vector_chunks,
            bm25_chunks
    )
        print(
            f"\nVector Results : {len(vector_chunks)}"
        )
        print(
            f"BM25 Results   : {len(bm25_chunks)}"
        )
        print(
            f"Merged Results : {len(merged_chunks)}"
        )
        return merged_chunks