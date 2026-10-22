import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

SYSTEM_PROMPT = """You are a strict, unbiased resume verification assistant. Your task is to analyze a candidate's Master Resume against a Target Job Description.

CRITICAL BOUNDING RULES:
1. ONLY use skills, tools, frameworks, and job titles explicitly listed in the MASTER RESUME.
2. DO NOT infer, extrapolate, or invent any experience, technologies, or metrics not directly stated in the MASTER RESUME.
3. If a skill is required by the Job Description but absent from the Master Resume, place it in the "missing_skills" array. DO NOT include it in the candidate summary.
4. Return ONLY valid JSON matching the exact schema below. Do not include markdown code blocks or additional conversational text.

Required JSON Schema:
{
  "tailored_summary": "3-4 sentence professional summary strictly using candidate's real experience",
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill3", "skill4"],
  "claimed_skills_in_summary": ["skill1", "skill2"]
}
"""

def generate_tailored_match(master_resume: str, job_description: str) -> dict:
    user_content = f"MASTER RESUME:\n{master_resume}\n\nTARGET JOB DESCRIPTION:\n{job_description}"
    payload = {
        "model": MODEL_NAME,
        "system": SYSTEM_PROMPT,
        "prompt": user_content,
        "stream": False,
        "format": "json"
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        raw_text = response.json().get("response", "{}")
        return json.loads(raw_text)
    except Exception as e:
        return {"error": f"LLM connection failed: {str(e)}. Make sure Ollama is running ('ollama serve')."}
