import os, json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import openai  # or google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# 📥 Input schema
class AnalyzeRequest(BaseModel):
    repo_url: str
    issue_number: int

# GitHub fetch
def fetch_issue(owner: str, repo: str, num: int):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{num}"
    r = requests.get(url, headers={"Accept":"application/vnd.github.v3+json"})
    if r.status_code != 200: raise HTTPException(404, detail="Issue not found")
    return r.json()

# Gemini (comment/uncomment whichever you want)
USE_GEMINI = False

if USE_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    def call_llm(prompt):
        model = genai.GenerativeModel("gemini-pro")
        resp = model.generate_content(prompt)
        return json.loads(resp.text)
else:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    def call_llm(prompt):
        resp = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content":prompt}], temperature=0.2)
        return json.loads(resp.choices[0].message["content"])

# Prompt constructor
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
  "potential_impact": "...",
}}
"""

# Main endpoint
@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    owner, repo = req.repo_url.rstrip("/").split("/")[-2:]
    issue = fetch_issue(owner, repo, req.issue_number)
    prompt = build_prompt(issue["title"], issue.get("body",""), issue.get("comments", []))
    return call_llm(prompt)
