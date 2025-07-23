import os, json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import OpenAI
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

# Import Gemini
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Input schema
class AnalyzeRequest(BaseModel):
    repo_url: str
    issue_number: int
    use_gemini: bool = False

# Fetch GitHub issue
def fetch_issue(owner: str, repo: str, num: int):
    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{num}"
    issue_resp = requests.get(issue_url, headers={"Accept": "application/vnd.github.v3+json"})
    if issue_resp.status_code != 200:
        raise HTTPException(404, detail="GitHub issue not found")
    issue_data = issue_resp.json()

    comments_url = issue_data.get("comments_url")
    comments = []
    if comments_url:
        comments_resp = requests.get(comments_url)
        if comments_resp.status_code == 200:
            comments = comments_resp.json()

    return issue_data, comments

# Build prompt
def build_prompt(title, body, comments):
    comment_text = "\n".join(f"- {c['body']}" for c in comments[:5])
    return f"""
You are an AI assistant analyzing a GitHub issue. Here is the data:

Title:
{title}

Body:
{body or "(none)"}

Comments:
{comment_text or "(none)"}

Please output JSON **exactly** in the following format:

{{
  "summary": "...",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "1-5, with justification",
  "suggested_labels": ["...", "..."],
  "potential_impact": "..."
}}
"""

# Call OpenAI
def call_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return json.loads(response.choices[0].message["content"])
    except Exception as e:
        raise HTTPException(500, detail=f"OpenAI call failed: {str(e)}")

# Call Gemini
def call_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(500, detail=f"Gemini call failed: {str(e)}")

# Endpoint
@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    owner, repo = req.repo_url.rstrip("/").split("/")[-2:]
    issue, comments = fetch_issue(owner, repo, req.issue_number)
    prompt = build_prompt(issue["title"], issue.get("body", ""), comments)

    if req.use_gemini:
        return call_gemini(prompt)
    else:
        return call_openai(prompt)
