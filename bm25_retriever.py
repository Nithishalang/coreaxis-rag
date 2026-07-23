from rank_bm25 import BM25Okapi
import pickle
import re
class BM25Retriever:
    def __init__(self):
        print("Loading BM25 Retriever...")
        with open("data/processed/chunks.pkl", "rb") as f:
            self.chunks = pickle.load(f)
        corpus = [
            self.tokenize(chunk["text"])
            for chunk in self.chunks
        ]
        self.bm25 = BM25Okapi(corpus)
        print(f"Indexed {len(self.chunks)} chunks.")
    def tokenize(self, text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return text.split()
    def search(
    self,
    query,
    departments=None,
    top_k=20
):
        scores = self.bm25.get_scores(
            self.tokenize(query)
        )
        ranked = sorted(
            zip(self.chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )
        results = []
        for chunk, score in ranked:
            if departments is not None:
                if chunk["metadata"]["department"] not in departments:
                    continue
            new_chunk = chunk.copy()
            new_chunk["bm25_score"] = float(score)
            results.append(new_chunk)
            if len(results) >= top_k:
                break
        return results