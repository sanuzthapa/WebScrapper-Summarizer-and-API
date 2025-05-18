from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from rss_parser.parser import extract_content_from_url, summarize_article

app = FastAPI()

class SummarizeRequest(BaseModel):
    urls: List[str]

@app.post("/summarize")
def summarize_articles(request: SummarizeRequest):
    results = []

    for url in request.urls:
        try:
            content = extract_content_from_url(url)

            if not content or len(content.strip()) < 50:
                results.append({
                    "url": url,
                    "error": "Content too short or could not be extracted.",
                    "content": content
                })
                continue

            summary = summarize_article(content)

            results.append({
                "url": url,
                "content": content,
                "summary": summary
            })
        except Exception as e:
            results.append({
                "url": url,
                "error": str(e),
                "content": ""
            })

    return {"results": results}
