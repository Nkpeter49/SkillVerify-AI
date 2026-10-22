import re
from typing import Dict, List, Set

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s\+#\.-]", " ", text)
    return text

def extract_skill_tokens(text: str) -> Set[str]:
    normalized = normalize_text(text)
    tokens = set(normalized.split())
    custom_patterns = [
        r"python", r"flask", r"sqlite", r"postgresql", r"react",
        r"node\.js", r"aws", r"docker", r"kubernetes", r"machine learning",
        r"data analysis", r"ci/cd", r"rest api", r"html5", r"css3", r"git"
    ]
    for pattern in custom_patterns:
        if re.search(pattern, normalized):
            tokens.add(pattern.replace(r"\.", "."))
    return tokens

def verify_llm_output(master_resume: str, llm_response: Dict) -> Dict[str, any]:
    resume_tokens = extract_skill_tokens(master_resume)
    claimed_skills = llm_response.get("claimed_skills_in_summary", [])
    tailored_summary = llm_response.get("tailored_summary", "")

    unsupported_claims: List[str] = []
    verified_claims: List[str] = []

    for skill in claimed_skills:
        normalized_skill = normalize_text(skill).strip()
        skill_words = set(normalized_skill.split())
        if skill_words.issubset(resume_tokens) or normalized_skill in normalize_text(master_resume):
            verified_claims.append(skill)
        else:
            unsupported_claims.append(skill)

    summary_tokens = extract_skill_tokens(tailored_summary)
    potential_hallucinations = summary_tokens - resume_tokens

    common_words = {
        "and", "the", "for", "with", "in", "to", "of", "a", "an", "experienced",
        "developer", "building", "built", "using", "systems", "applications",
        "experience", "strong", "demonstrated", "ability", "management", "project", "data"
    }
    suspect_terms = [term for term in potential_hallucinations if term not in common_words]

    return {
        "is_grounded": len(unsupported_claims) == 0,
        "verified_skills": verified_claims,
        "unsupported_skills": unsupported_claims,
        "suspect_summary_terms": suspect_terms,
        "tailored_summary": tailored_summary,
        "matched_skills": llm_response.get("matched_skills", []),
        "missing_skills": llm_response.get("missing_skills", [])
    }
