import feedparser
from newspaper import Article
from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def summarize_article(text: str) -> str:
    if not client:
        raise Exception("OpenAI API key not set.")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = [
                {
                    "role": "user",
                    "content": f"""
Summarize the following article in a concise and informative way. 

Requirements:
- Include a clear **TL;DR** (in 1–2 sentences).
- Provide **key points** or insights (bullet points if applicable).
- Suggest the **most appropriate hashtags** based on the topic (3–8 tags, in the format #example).

Article:
{text}
"""
                }
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Error during summarization: {str(e)}")

def extract_content_from_url(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        if not article.text or len(article.text) < 20:
            raise Exception("Article content too short or empty.")
        return article.text
    except Exception as e:
        raise Exception(f"Failed to extract content: {str(e)}")

def parse_rss(url: str):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        content = ""
        if 'content' in entry and entry.content:
            content = entry.content[0].get('value', '')
        elif 'summary' in entry:
            content = entry.summary
        elif 'description' in entry:
            content = entry.description
        articles.append({
            'title': entry.title,
            'link': entry.link,
            'content': content
        })
    return articles
