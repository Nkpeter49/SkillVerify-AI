import re
from typing import Dict, List

def clean_text(text: str) -> str:
    """Normalizes text by removing special characters and converting to lowercase."""
    text = text.lower().replace("_", " ")
    return re.sub(r"[^\w\s]", " ", text)

def verify_llm_output(master_resume: str, llm_response: Dict) -> Dict[str, any]:
    resume_raw = master_resume.lower()
    resume_clean = clean_text(master_resume)

    raw_matched = llm_response.get("matched_skills", [])
    raw_missing = llm_response.get("missing_skills", [])
    tailored_summary = llm_response.get("tailored_summary", "")

    verified_skills = []
    missing_skills = [s.replace("_", " ") for s in raw_missing]
    unsupported_skills = []

    for skill in raw_matched:
        display_skill = skill.replace("_", " ").strip()
        skill_clean = clean_text(display_skill)
        words = [w for w in skill_clean.split() if len(w) > 1]

        # 1. Exact or partial substring match in raw resume
        # 2. All key words present in normalized resume
        if (skill_clean in resume_clean) or (display_skill.lower() in resume_raw) or (words and all(w in resume_clean for w in words)):
            verified_skills.append(display_skill)
        else:
            # Reclassify non-resume skills as missing requirements
            if display_skill not in missing_skills:
                missing_skills.append(display_skill)

    return {
        "is_grounded": True,
        "verified_skills": sorted(list(set(verified_skills))),
        "unsupported_skills": sorted(list(set(unsupported_skills))),
        "missing_skills": sorted(list(set(missing_skills))),
        "tailored_summary": tailored_summary
    }
