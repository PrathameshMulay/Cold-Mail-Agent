from ddgs import DDGS


class WebSearchTool:

    def search(self, query: str, max_results: int = 10):
        """
        Search the public web and return search results.
        """

        results = DDGS().text(
            query,
            region="us-en",
            safesearch="moderate",
            max_results=max_results,
        )

        return results