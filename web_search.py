import os
from tavily import TavilyClient
class WebSearch:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY not found. Add it to your .env file."
            )
        self.client = TavilyClient(api_key=api_key)
    def search(self, query):
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
        context = ""
        for result in response["results"]:
            context += f"""
Title: {result["title"]}
URL: {result["url"]}
Content:
{result["content"]}
---------------------------------------
"""
        return context