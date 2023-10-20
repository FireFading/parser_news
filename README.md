## News Parser
    This Python script is a web scraper designed to extract articles and their details from the Fox News website. It utilizes asynchronous programming with the asyncio library and makes HTTP requests using aiohttp. The scraped data is parsed using the BeautifulSoup library to extract article titles, summaries, publication timestamps, and article content.

## Installation
Before using the Fox News Web Scraper, you need to ensure that you have the required Python libraries installed. You can do this using pip and the provided requirements.txt file.
1. Clone the repository:
```bash
    git clone https://github.com/FireFading/parser_news
```
2. Navigate to the project directory:
```bash
    cd parser_news
```
3. Install the required libraries:
```bash
    pip install -r requirements.txt
```

## Usage
To use the Fox News Web Scraper, you can run the main script, which will fetch the latest news articles from the Fox News website. You can specify a different URL if needed.

```bash
    python main.py`
```

## Data Structure
The script extracts article information and structures it as a list of Article objects. Each Article object contains the following attributes:
- `title`: The title of the article.
- `summary`: The summary of the article.
- `timestamp`: The publication timestamp of the article.
- `content`: The content of the article.

Here's an example of the data structure:

```python
    [
        Article(
            title="Sample Article Title",
            summary="A brief summary of the article.",
            time_published="October 20, 2023",
            content="The full article content goes here."
        ),
        # More Article objects
    ]
```