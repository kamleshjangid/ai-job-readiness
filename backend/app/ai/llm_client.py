import os
import asyncio
from typing import Dict

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")  # "openai" or "mock"

async def analyze_resume_text(text: str) -> Dict:
    """
    Return structured JSON:
    {
      "overall_score": float,
      "skills_score": float,
      "communication_score": float,
      "technical_score": float,
      "details": {"strengths": [...], "improvements": [...], "keywords": [...]}
    }
    """
    if LLM_PROVIDER == "openai":
        return await _call_openai(text)
    else:
        return _mock_analysis(text)

def _mock_analysis(text):
    # simple heuristics for dev
    return {
        "overall_score": 75.2,
        "skills_score": 72.0,
        "communication_score": 78.0,
        "technical_score": 74.0,
        "details": {
            "strengths": ["clear summary", "keywords present"],
            "improvements": ["add measurable outcomes", "format achievements with bullets"],
            "keywords": ["python", "fastapi"]
        }
    }

async def _call_openai(text: str):
    # Example using openai package (async wrapper)
    import os
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Analyze this resume text and return JSON with scores and suggestions: {text[:4000]}"
    resp = await client.chat.completions.create(
        model="gpt-4o-mini", # example placeholder — replace by your chosen model
        messages=[{"role":"user","content":prompt}],
        max_tokens=600
    )
    # parse response: assume assistant returns JSON
    import json
    content = resp.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        # fallback: mock
        return _mock_analysis(text)
