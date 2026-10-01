"""
nlp_analyzer.py
---------------
Skill extraction, ATS scoring, job-role matching,
and keyword gap analysis — all done with pure NLP/ML
(TF-IDF, cosine similarity, regex, n-gram matching).
No external model downloads required at runtime.
"""

import re
import math
from collections import Counter
from skills_data import SKILLS_DB, JOB_ROLES, STOP_WORDS


# ── n-gram helpers ────────────────────────────────────────────────────────────

def _ngrams(tokens: list[str], n: int) -> list[str]:
    return [" ".join(tokens[i: i + n]) for i in range(len(tokens) - n + 1)]


def _all_ngrams(tokens: list[str], max_n: int = 3) -> list[str]:
    result = []
    for n in range(1, max_n + 1):
        result.extend(_ngrams(tokens, n))
    return result


# ── skill extraction ──────────────────────────────────────────────────────────

def extract_skills(clean_text: str, tokens: list[str]) -> list[str]:
    """
    Match skills from SKILLS_DB against unigrams, bigrams, and trigrams
    found in the resume text.
    """
    candidate_phrases = set(_all_ngrams(tokens, 3))

    # also do a raw substring search for multi-word skills
    found = set()
    for skill in SKILLS_DB:
        if skill in candidate_phrases:
            found.add(skill)
        elif " " in skill and skill in clean_text:
            found.add(skill)

    return sorted(found)


# ── TF-IDF score for resume "richness" ───────────────────────────────────────

def compute_tfidf_score(tokens: list[str]) -> float:
    """
    Compute a normalised TF-IDF richness score (0-100) that rewards
    diverse, domain-specific vocabulary.
    """
    if not tokens:
        return 0.0

    tf = Counter(tokens)
    total = len(tokens)
    unique = len(tf)

    # lexical diversity ratio
    diversity = unique / total if total else 0

    # crude IDF boost: rare tokens score higher
    idf_sum = sum(math.log(1 + 1 / (c / total)) for c in tf.values())
    idf_avg = idf_sum / unique if unique else 0

    raw = diversity * idf_avg * 10
    return round(min(raw * 100, 100), 2)


# ── ATS score ─────────────────────────────────────────────────────────────────

_ATS_WEIGHTS = {
    "has_email":          5,
    "has_phone":          5,
    "has_linkedin":       5,
    "has_github":         3,
    "has_education":     10,
    "has_experience":    15,
    "has_skills":        15,
    "has_projects":       8,
    "has_summary":        5,
    "has_certifications": 4,
    "skill_count":       15,   # up to 15 pts based on # skills found
    "word_count":        10,   # ideal 300-800 words
}

def compute_ats_score(
    contact_info: dict,
    sections: dict,
    skills: list[str],
    tokens: list[str],
) -> dict:
    """
    ATS-style score (0-100) with per-category breakdown.
    """
    score = 0
    breakdown = {}

    def _give(key: float, pts: float, reason: str = ""):
        nonlocal score
        score += pts
        breakdown[key] = {"points": pts, "max": _ATS_WEIGHTS.get(key, pts), "note": reason}

    # contact
    if contact_info.get("email"):
        _give("has_email", 5, "Email found")
    if contact_info.get("phone"):
        _give("has_phone", 5, "Phone found")
    if contact_info.get("linkedin"):
        _give("has_linkedin", 5, "LinkedIn found")
    if contact_info.get("github"):
        _give("has_github", 3, "GitHub found")

    # sections
    def _section_present(key):
        return bool(sections.get(key, "").strip())

    if _section_present("education"):
        _give("has_education", 10, "Education section detected")
    if _section_present("experience"):
        _give("has_experience", 15, "Experience section detected")
    if _section_present("skills") or skills:
        _give("has_skills", 15, "Skills section detected")
    if _section_present("projects"):
        _give("has_projects", 8, "Projects section detected")
    if _section_present("summary"):
        _give("has_summary", 5, "Summary/Objective detected")
    if _section_present("certifications"):
        _give("has_certifications", 4, "Certifications detected")

    # skill count score (0-15)
    skill_pts = min(len(skills) / 20 * 15, 15)
    _give("skill_count", round(skill_pts, 1), f"{len(skills)} skills detected")

    # word count score (0-10)
    wc = len(tokens)
    if 250 <= wc <= 900:
        wc_pts = 10
        wc_note = f"Good length ({wc} tokens)"
    elif wc < 250:
        wc_pts = round(wc / 250 * 10, 1)
        wc_note = f"Resume may be too short ({wc} tokens)"
    else:
        wc_pts = round(max(10 - (wc - 900) / 300, 4), 1)
        wc_note = f"Resume may be too long ({wc} tokens)"
    _give("word_count", wc_pts, wc_note)

    return {
        "total": round(min(score, 100), 1),
        "breakdown": breakdown,
    }


# ── job-role matching (cosine similarity via TF-IDF bag-of-words) ─────────────

def _text_vector(text_tokens: list[str], vocab: set) -> dict[str, float]:
    counts = Counter(text_tokens)
    total = max(len(text_tokens), 1)
    return {w: counts[w] / total for w in vocab if counts[w]}


def _cosine(v1: dict, v2: dict) -> float:
    keys = set(v1) & set(v2)
    if not keys:
        return 0.0
    dot = sum(v1[k] * v2[k] for k in keys)
    mag1 = math.sqrt(sum(x * x for x in v1.values()))
    mag2 = math.sqrt(sum(x * x for x in v2.values()))
    return dot / (mag1 * mag2) if (mag1 * mag2) else 0.0


def match_job_roles(skills: list[str], tokens: list[str]) -> list[dict]:
    """
    Rank all job roles by how well the candidate's skills match
    required + preferred skills using cosine similarity.
    Returns a sorted list of role match objects.
    """
    skill_set = set(skills)
    results = []

    for role, spec in JOB_ROLES.items():
        required  = spec["required"]
        preferred = spec["preferred"]
        all_role_skills = required + preferred

        matched_req  = [s for s in required  if s in skill_set]
        matched_pref = [s for s in preferred if s in skill_set]
        missing      = [s for s in required  if s not in skill_set]

        # weighted match %
        req_score  = len(matched_req) / len(required)  if required  else 0
        pref_score = len(matched_pref) / len(preferred) if preferred else 0
        match_pct  = round((req_score * 0.7 + pref_score * 0.3) * 100, 1)

        # cosine similarity for ranking
        vocab = set(all_role_skills + tokens[:200])
        role_vec = _text_vector(all_role_skills, vocab)
        cand_vec = _text_vector(skills, vocab)
        cos_sim  = round(_cosine(role_vec, cand_vec) * 100, 1)

        results.append({
            "role":           role,
            "match_percent":  match_pct,
            "cosine_sim":     cos_sim,
            "matched_required":  matched_req,
            "matched_preferred": matched_pref,
            "missing_skills":    missing,
            "total_required":    len(required),
            "total_preferred":   len(preferred),
        })

    results.sort(key=lambda x: (x["match_percent"], x["cosine_sim"]), reverse=True)
    return results


# ── keyword gap analysis ──────────────────────────────────────────────────────

def keyword_gap_analysis(skills: list[str], top_role: str) -> dict:
    """
    Given the top matched role, produce a gap report with recommendations.
    """
    if top_role not in JOB_ROLES:
        return {}

    skill_set = set(skills)
    spec = JOB_ROLES[top_role]
    missing_req  = [s for s in spec["required"]  if s not in skill_set]
    missing_pref = [s for s in spec["preferred"] if s not in skill_set]

    recommendations = []
    for skill in missing_req[:5]:
        recommendations.append({
            "skill":    skill,
            "priority": "High",
            "reason":   f"'{skill}' is a core requirement for {top_role}",
        })
    for skill in missing_pref[:3]:
        recommendations.append({
            "skill":    skill,
            "priority": "Medium",
            "reason":   f"'{skill}' is preferred for {top_role}",
        })

    return {
        "role":                top_role,
        "missing_required":    missing_req,
        "missing_preferred":   missing_pref,
        "recommendations":     recommendations,
    }


# ── overall grade ─────────────────────────────────────────────────────────────

def compute_grade(ats_total: float) -> tuple[str, str]:
    if ats_total >= 85:
        return "A", "Excellent"
    elif ats_total >= 70:
        return "B", "Good"
    elif ats_total >= 55:
        return "C", "Average"
    elif ats_total >= 40:
        return "D", "Needs Improvement"
    else:
        return "F", "Poor"


# ── master analyze function ───────────────────────────────────────────────────

def analyze_resume(parsed: dict, contact: dict, sections: dict) -> dict:
    """
    Full NLP pipeline.  Takes output from resume_parser and returns
    a complete analysis result dict ready to JSON-serialize.
    """
    tokens = parsed["tokens"]
    clean  = parsed["clean_text"]

    skills       = extract_skills(clean, tokens)
    tfidf_score  = compute_tfidf_score(tokens)
    ats          = compute_ats_score(contact, sections, skills, tokens)
    role_matches = match_job_roles(skills, tokens)
    top_role     = role_matches[0]["role"] if role_matches else "General"
    gap          = keyword_gap_analysis(skills, top_role)
    grade, label = compute_grade(ats["total"])

    return {
        "skills":        skills,
        "skill_count":   len(skills),
        "tfidf_score":   tfidf_score,
        "ats_score":     ats,
        "role_matches":  role_matches,
        "top_role":      top_role,
        "gap_analysis":  gap,
        "grade":         grade,
        "grade_label":   label,
        "word_count":    len(tokens),
    }
