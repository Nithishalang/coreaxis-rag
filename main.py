from src.retrieval.retriever import Retriever
from src.llm.ollama_client import OllamaClient
from src.routing.department_router import DepartmentRouter
from src.reranking.reranker import Reranker 
from src.web.web_search import WebSearch
from dotenv import load_dotenv
load_dotenv()
class CoreAxisRAG:
    def __init__(self):
        print("Loading Retriever...")
        self.retriever = Retriever()
        print("Loading Llama 3.2...")
        self.llm = OllamaClient()
        print("CoreAxis Assistant Ready!\n")
        self.router = DepartmentRouter()
        self.reranker = Reranker()
        self.web_search = WebSearch()
    def ask(self, question):
        departments, scores = self.router.route(question)
        chunks = self.retriever.search(
        question,
        departments,
        top_k=15
    )
        chunks = self.reranker.rerank(
        question,
        chunks,
        top_k=5
    )
        print("\nFirst reranked chunk:")
        print(chunks[0])
        if chunks[0]["rerank_score"] < 0:
            print("\nLow rerank score. Searching the Web...")
            web_context = self.web_search.search(question)
            return {
        "answer": self.llm.generate_web_answer(question, web_context),
        "source": "web"
    }
        answer = self.llm.generate(question, chunks)
        print("LLM Returned:")
        print(repr(answer))
        if "INSUFFICIENT_CONTEXT" in answer.upper():
            print("\nSearching the Web...")
            web_context = self.web_search.search(question)
            answer = self.llm.generate_web_answer(
            question,
            web_context
        )
            return {
            "answer": answer,
            "source": "web"
        }
        return {
        "answer": answer,
        "source": "documents"
    }
if __name__ == "__main__":
    assistant = CoreAxisRAG()
    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            break
        answer = assistant.ask(question)
        print("\nAssistant:\n")
        print(answer)
        print("\n" + "=" * 70 + "\n")