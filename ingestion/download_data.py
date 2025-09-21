import os
import requests
from bs4 import BeautifulSoup

WIKI_URLS = [
    "https://en.wikipedia.org/wiki/Myanmar",
    "https://en.wikipedia.org/wiki/Burmese_cuisine",
]

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}

def download_wikipedia():
    for url in WIKI_URLS:
        page = requests.get(url, headers=HEADERS)
        if page.status_code != 200:
            print(f"Failed to download {url}")
            continue

        soup = BeautifulSoup(page.content, "html.parser")
        paragraphs = soup.find_all('p')
        text = "\n".join([p.get_text() for p in paragraphs if p.get_text(strip=True)])

        filename = url.split("/")[-1] + ".txt"
        with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Downloaded {filename}")

if __name__ == "__main__":
    download_wikipedia()
