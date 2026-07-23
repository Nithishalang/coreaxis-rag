import ollama
class OllamaClient:
    def __init__(self, model="llama3.2:3b"):
        self.model = model
    def generate(self, query, retrieved_chunks):
        context = ""
        for chunk in retrieved_chunks:
            metadata = chunk["metadata"]
            context += f"""
Source: {metadata['source']}
Department: {metadata['department']}
Page: {metadata['page']}
Section: {metadata['section']}
{chunk['text']}
----------------------------------------
"""
        prompt = f"""
You are an AI assistant for CoreAxis Technologies.

You MUST answer the user's question ONLY from the retrieved context.

Rules:

1. Every statement in your answer MUST be explicitly supported by the retrieved context.

2. NEVER use outside knowledge.

3. NEVER infer missing information.

4. NEVER guess.

5. NEVER combine retrieved facts with your own knowledge.

6. Do NOT answer based on what is usually true.
Answer only what is explicitly written.

7. Preserve names, numbers, dates, limits, roles, and conditions exactly as they appear in the context.

8. If multiple requirements, controls, steps, responsibilities, or entities are present, include ALL of them.

9. If the answer naturally consists of multiple items, return them as bullet points.

10. If the answer is a single fact, return a single sentence.

11. If the retrieved context contains only part of the answer, return ONLY that part.

12. If the retrieved context does NOT contain enough information to answer the question, reply with EXACTLY

INSUFFICIENT_CONTEXT

Do not explain why.

Do not apologize.

Do not mention the context.

Do not mention missing information.

Do not output markdown.

Context:
{context}
Question:
{query}
Answer:
"""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        except Exception as e:
            print("\nOllama Error:", repr(e))
            raise
        content = response["message"]["content"].strip()
        print("\nLLM Raw Response:")
        print(content)
        return content
    
    def generate_web_answer(self, query, web_context):
        prompt = f"""
You are an AI assistant.

The internal company knowledge base did not contain sufficient information.

Use the web search results below to answer accurately.

Do not invent information.

If the search results are insufficient, clearly say so.

Answer the user's question ONLY using the web search
results provided below.

If the search results are insufficient,
say that reliable information could not be found.

Web Search Results:
{web_context}
Question:
{query}
Answer:
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response["message"]["content"]