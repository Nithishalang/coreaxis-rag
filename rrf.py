class ReciprocalRankFusion:
    def __init__(self, k=60):
        self.k = k
    def fuse(self, vector_chunks, bm25_chunks):
        scores = {}
        for rank, chunk in enumerate(vector_chunks, start=1):
            chunk_id = chunk["metadata"]["chunk_id"]
            if chunk_id not in scores:
                scores[chunk_id] = {
                    "chunk": chunk,
                    "score": 0.0
                }
            scores[chunk_id]["score"] += 1 / (self.k + rank)
        for rank, chunk in enumerate(bm25_chunks, start=1):
            chunk_id = chunk["metadata"]["chunk_id"]
            if chunk_id not in scores:
                scores[chunk_id] = {
                    "chunk": chunk,
                    "score": 0.0
                }
            scores[chunk_id]["score"] += 1 / (self.k + rank)
        fused = sorted(
            scores.values(),
            key=lambda x: x["score"],
            reverse=True
        )
        return [item["chunk"] for item in fused]