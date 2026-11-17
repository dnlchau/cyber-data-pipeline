import requests
from bs4 import BeautifulSoup
import trafilatura


BASE_URL = "https://thehackernews.com/"


class HackerNewsCrawler:

    def __init__(self):
        self.news = []

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0 Safari/537.36"
            )
        }

    def get_homepage(self):

        response = requests.get(
            BASE_URL,
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        return BeautifulSoup(response.text, "lxml")

    def collect_news_links(self):

        soup = self.get_homepage()

        cards = soup.select("div.body-post")

        print(f"Encontrados {len(cards)} cards.")

        for card in cards:

            title = card.select_one("h2.home-title")
            link = card.select_one("a.story-link")
            date = card.select_one(".item-label")

            self.news.append({

                "title": title.get_text(strip=True) if title else None,

                "url": link["href"] if link else None,

                "date": date.get_text(strip=True) if date else None

            })

    def extract_article(self):

        for i, article in enumerate(self.news, start=1):

            print(f"[{i}/{len(self.news)}] {article['title']}")

            downloaded = trafilatura.fetch_url(article["url"])

            if downloaded:

                text = trafilatura.extract(
                    downloaded,
                    include_comments=False,
                    include_tables=False
                )

                article["content"] = text

            else:

                article["content"] = None

    def run(self):

        print("Coletando notícias...")

        self.collect_news_links()

        print(f"{len(self.news)} notícias encontradas.")

        print("Extraindo conteúdo...")

        self.extract_article()

        return self.news


if __name__ == "__main__":

    crawler = HackerNewsCrawler()

    noticias = crawler.run()

    print()

    print("=" * 100)

    print(f"TOTAL: {len(noticias)} notícias")

    print("=" * 100)

    for noticia in noticias[:3]:

        print()

        print("-" * 100)

        print("Título:", noticia["title"])

        print("Data:", noticia["date"])

        print("URL:", noticia["url"])

        print()

        if noticia["content"]:

            print(noticia["content"][:700])

        else:

            print("Sem conteúdo.")