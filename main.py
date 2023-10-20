import asyncio
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from dataclasses import dataclass

from aiohttp_client import client

URL = "https://www.foxnews.com/"


@dataclass
class Article:
    title: str
    summary: str
    time_published: str
    content: str


def normalize_url(extracted_url, base_url: str = URL) -> str:
    if extracted_url.startswith(("http:", "https:", "www.")):
        return extracted_url
    return urljoin(base_url, extracted_url)


async def get_news():
    response = await client.get(url=URL, headers={"Content-Type": "text/html"})
    soup = BeautifulSoup(response, "html.parser")

    blocks = soup.select(".info-header .title")
    information_articles = str(blocks)

    soup_urls = BeautifulSoup(information_articles, features="lxml")
    links = [
        index["href"]
        for index in soup_urls.find_all("a", href=True)
        if index["href"] != "#"
    ]
    links = list(set(links))

    all_articles = []
    for link in links:
        title = ""
        summary = ""
        time_published = ""
        article = ""

        link = normalize_url(link)
        response_article = await client.get(
            url=link, headers={"Content-Type": "text/html"}
        )
        soup_article = BeautifulSoup(response_article, "html.parser")

        if title := soup_article.find("h1"):
            title = title.text
        if summary := soup_article.find("h2", class_="sub-headline"):
            summary = summary.text
        if time_published := soup_article.find("div", class_="article-date"):
            time_published = time_published.text

        if content := soup_article.find_all("p", class_="speakable"):
            for sentence in range(len(content)):
                article = article + content[sentence].text

        all_articles.append(
            Article(
                title=title,
                summary=summary,
                time_published=time_published,
                content=article,
            )
        )

    return all_articles


def main():
    asyncio.get_event_loop().run_until_complete(get_news())


if __name__ == "__main__":
    main()
