import requests
from bs4 import BeautifulSoup

def get_news():
    link = "https://www.foxnews.com/"

    response = requests.get(link)
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")

    blocks = soup.select(".collection.collection-article-list .content.article-list .article")
    information_articles = str(blocks)

    soup_urls = BeautifulSoup(information_articles, features="lxml")
    # links_articles = soup_urls.find_all("a")[0]["href"]
    project_href = [i['href'] for i in soup_urls.find_all('a', href=True) if i['href'] != "#"]
    project_href = list(set(project_href))
    print(len(project_href))

    all_articles = []
    for link_article in project_href:
        new_article = {}
        
        title = ""
        summary = ""
        time_published = ""
        
        response_article = requests.get(link_article)
        soup_article = BeautifulSoup(response_article.text, "html.parser")
        if title := soup_article.find("h1"):
            title = title.text
        if summary := soup_article.find("h2", class_="sub-headline"):
            summary = summary.text
        if time_published := soup_article.find("div", class_="article-date"):
            time_published = time_published.text
        content = soup_article.find_all("p", class_="speakable")
        article = ""
        if content:
            for sentence in range(len(content)):
                article = article + content[sentence].text
        print(article)
        
        new_article['title'] = title
        new_article['summary'] = summary
        new_article['time_published'] = time_published
        new_article['content'] = article
        
        all_articles.append(new_article)
    
    return all_articles

