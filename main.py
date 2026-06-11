import re
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
 
load_dotenv()
 
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
 
client = OpenAI(api_key=OPENAI_API_KEY)
 
 
def fetch_semantic_scholar(query="large language model", limit=3):
 url = "https://api.semanticscholar.org/graph/v1/paper/search"
 params = {
 "query": query,
 "limit": limit,
 "fields": "title,abstract,url,year,citationCount"
 }
 response = requests.get(url, params=params)
 return response.json()["data"]
 
 
def fetch_content(paper):
    arxiv_id = paper.get("paper", {}).get("id", "")
 
    # arXiv IDの形式チェック (例: 2401.12345)
    if re.match(r"^\d{4}\.\d{4,5}$", arxiv_id):
        response = requests.get(f"https://huggingface.co/papers/{arxiv_id}.md")
        if response.status_code == 200:
            return response.text
 
    # フォールバック: summaryフィールドを使う
    return paper.get("paper", {}).get("summary", "")
 
 
SUMMARY_PROMPT = """
以下の論文を日本語で要約してください。
前置きや説明は一切不要です。以下のフォーマットのみを出力してください。
 
*どんなもの？*
（1〜2文）
 
*先行研究と比べてどこがすごい？*
（1〜2文）
 
*技術や手法のキモはどこ？*
（1〜2文）
 
*どうやって有効だと検証した？*
（1〜2文）
 
*議論はある？*
（1〜2文）
 
*次に読むべき論文は？*
（論文名を1〜3件）
"""
 
 
def summarize(title, content):
    response = client.chat.completions.create(
        model="gpt-5.4-mini-2026-03-17",
        max_completion_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"{SUMMARY_PROMPT}\nタイトル: {title}\n\n{content}",
            }
        ],
    )
    return response.choices[0].message.content
 
 
def post_to_slack(message):
    response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
    response.raise_for_status()
 
 
def main():
    papers = fetch_papers(limit=3)
 
    for paper in papers:
        title = paper.get("paper", {}).get("title", "タイトル不明")
        arxiv_id = paper.get("paper", {}).get("id", "")
        url = f"https://huggingface.co/papers/{arxiv_id}" if arxiv_id else ""
 
        content = fetch_content(paper)
        summary = summarize(title, content)
 
        message = f"*{title}*\n{url}\n\n{summary}"
 
        post_to_slack(message)
        print(f"投稿完了: {title}")
 

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"エラー: {e}")
