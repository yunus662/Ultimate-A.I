# web_surfer.py
"""
Web Surfer Module
=================
Allows the AI to intelligently search and extract web content using DuckDuckGo API or headless browsing.
"""

import requests
from bs4 import BeautifulSoup
from security import is_operation_safe

class WebSurfer:
    def __init__(self, search_engine="https://html.duckduckgo.com/html/"):
        self.engine = search_engine

    def search(self, query: str) -> list:
        if not is_operation_safe("search", query):
            return ["[Security] Search operation denied."]

        try:
            res = requests.post(self.engine, data={'q': query})
            soup = BeautifulSoup(res.text, 'html.parser')
            results = []

            for result in soup.find_all('a', class_='result__a', limit=5):
                results.append(result.get('href'))

            return results or ["[Info] No results found."]
        except Exception as e:
            return [f"[Error] Search failed: {e}"]

    def scrape_page(self, url: str) -> str:
        if not is_operation_safe("scrape_page", url):
            return "[Security] Scraping denied."

        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text()[:2000]  # Trim large pages
        except Exception as e:
            return f"[Error] Could not scrape {url}: {e}"
