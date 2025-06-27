# modules/web_surfer.py

import requests
from bs4 import BeautifulSoup

class WebSurfer:
    @staticmethod
    def fetch(url: str) -> str:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # strip scripts/styles
        for tag in soup(["script","style"]): tag.decompose()
        return soup.get_text(separator="\n", strip=True)
