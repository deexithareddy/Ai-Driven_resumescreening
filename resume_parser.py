"""
resume_parser.py
----------------
Structured Resume Parser for the AI Resume Screening System.

Extracts structured sections from raw resume text:
  - Contact information (name, email, phone, LinkedIn, GitHub)
  - Education history
  - Work experience
  - Projects
  - Certifications
  - Skills (from the resume body, not the JD)

Each section is individually scored against its JD counterpart for
granular, section-level screening insights.
"""

import re
from typing import Dict, List, Optional, Tuple
from logger import get_logger

logger = get_logger(__name__)


# ── Section Header Patterns ────────────────────────────────────────────────────

SECTION_PATTERNS: Dict[str, List[str]] = {
    "contact":        ["contact", "personal information", "personal details"],
    "summary":        ["summary", "objective", "profile", "about me", "professional summary",
                       "career objective", "overview"],
    "education":      ["education", "academic background", "qualifications",
                       "academic qualifications", "educational background"],
    "experience":     ["experience", "work experience", "employment", "employment history",
                       "professional experience", "career history", "work history"],
    "skills":         ["skills", "technical skills", "core competencies", "competencies",
                       "key skills", "areas of expertise", "technologies", "tools"],
    "projects":       ["projects", "personal projects", "key projects", "academic projects",
                       "side projects", "portfolio"],
    "certifications": ["certifications", "certificates", "licenses", "achievements",
                       "awards", "accomplishments"],
    "publications":   ["publications", "research", "papers", "articles"],
    "languages":      ["languages", "language skills"],
    "interests":      ["interests", "hobbies", "extra-curricular", "activities"],
}

# ── Contact Extraction Patterns ────────────────────────────────────────────────

EMAIL_RE    = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", re.IGNORECASE)
PHONE_RE    = re.compile(
    r"(?:\+?\d{1,3}[\s\-.])?(?:\(?\d{2,4}\)?[\s\-.])\d{3,4}[\s\-.]?\d{3,4}"
)
LINKEDIN_RE = re.compile(r"linkedin\.com/in/[\w\-]+", re.IGNORECASE)
GITHUB_RE   = re.compile(r"github\.com/[\w\-]+", re.IGNORECASE)

# Degree keywords for education parsing
DEGREE_KEYWORDS = [
    "b.tech", "b.e.", "b.sc", "b.com", "b.a.", "bsc", "btech", "be ",
    "m.tech", "m.sc", "mba", "m.e.", "m.a.", "ms ", "msc", "mtech",
    "ph.d", "phd", "bachelor", "master", "doctorate", "diploma", "associate",
    "engineering", "science", "arts", "commerce", "technology",
]

# Experience markers
EXP_MARKERS = [
    r"\d{4}\s*[-–—]\s*(?:\d{4}|present|current|now|ongoing)",  # Date ranges
    r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{4}",  # Month Year
    r"\d+\+?\s*(?:year|yr)s?\s+(?:of\s+)?(?:experience|exp)",  # X years experience
]


# ── Core Parser Functions ──────────────────────────────────────────────────────

def _split_into_sections(text: str) -> Dict[str, str]:
    """
    Split resume text into labelled sections using header detection.

    Returns:
        dict mapping section_name -> section_text
    """
    lines = text.splitlines()
    sections: Dict[str, List[str]] = {"header": []}
    current_section = "header"

    for line in lines:
        stripped = line.strip()
        if not stripped:
            sections.setdefault(current_section, []).append("")
            continue

        matched_section = _detect_section_header(stripped)
        if matched_section and len(stripped) < 60:
            current_section = matched_section
            sections.setdefault(current_section, [])
        else:
            sections.setdefault(current_section, []).append(stripped)

    return {k: "\n".join(v).strip() for k, v in sections.items() if "\n".join(v).strip()}


def _detect_section_header(line: str) -> Optional[str]:
    """
    Check if a line looks like a section header and return the canonical name.
    """
    clean = re.sub(r"[^a-z\s]", "", line.lower()).strip()
    for section_name, keywords in SECTION_PATTERNS.items():
        for kw in keywords:
            if clean == kw or clean.startswith(kw + " ") or clean.endswith(" " + kw):
                return section_name
    return None


def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    """
    Extract contact information from resume text.

    Returns:
        dict with keys: name, email, phone, linkedin, github
    """
    email   = EMAIL_RE.search(text)
    phone   = PHONE_RE.search(text)
    linkedin = LINKEDIN_RE.search(text)
    github  = GITHUB_RE.search(text)

    name = _extract_name(text)

    return {
        "name":     name,
        "email":    email.group(0)    if email    else None,
        "phone":    phone.group(0)    if phone    else None,
        "linkedin": linkedin.group(0) if linkedin else None,
        "github":   github.group(0)   if github   else None,
    }


def _extract_name(text: str) -> Optional[str]:
    """
    Heuristically extract the candidate name from the top of the resume.

    Strategy:
        - Look at the first 5 non-empty lines
        - Pick the first line that looks like a proper name (2-4 words, title-case,
          no digits, not a known section header, not too long)
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()][:10]
    seen_headers = set()
    for section_keywords in SECTION_PATTERNS.values():
        seen_headers.update(kw.lower() for kw in section_keywords)

    for line in lines:
        clean = re.sub(r"[^a-zA-Z\s\.\-]", "", line).strip()
        words = clean.split()
        if (
            2 <= len(words) <= 4
            and all(w[0].isupper() for w in words if w)
            and not any(w.lower() in seen_headers for w in words)
            and len(clean) < 50
            and not re.search(r"\d", clean)
        ):
            return clean
    return None


def extract_education(text: str, sections: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Extract education entries from the education section.

    Returns:
        list of dicts: {degree, institution, year, gpa}
    """
    edu_text = sections.get("education", "")
    if not edu_text:
        # Fall back to searching full text
        edu_text = text

    entries: List[Dict[str, str]] = []

    # Split by blank lines or bullet points to get individual entries
    blocks = re.split(r"\n{2,}|(?=•|▪|◦|-\s)", edu_text)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        degree_found = any(kw in block.lower() for kw in DEGREE_KEYWORDS)
        if not degree_found:
            continue

        year_match = re.search(r"\b(19|20)\d{2}\b", block)
        gpa_match  = re.search(
            r"(?:gpa|cgpa|grade|percentage|score)[:\s]*(\d+\.?\d*)", block, re.IGNORECASE
        )

        entries.append({
            "raw":         block[:300],
            "year":        year_match.group(0) if year_match else None,
            "gpa":         gpa_match.group(1)  if gpa_match  else None,
            "has_degree":  True,
        })

    return entries


def extract_experience(sections: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Extract work experience entries from the experience section.

    Returns:
        list of dicts: {title, company, dates, description}
    """
    exp_text = sections.get("experience", "")
    if not exp_text:
        return []

    entries: List[Dict[str, str]] = []
    blocks = re.split(r"\n{2,}", exp_text)

    date_re = re.compile(
        r"((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\.?\s+\d{4}|"
        r"\d{4})\s*[-–—to]+\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\.?\s+\d{4}|"
        r"\d{4}|present|current|now|ongoing)",
        re.IGNORECASE,
    )

    for block in blocks:
        block = block.strip()
        if not block or len(block) < 10:
            continue

        dates_match = date_re.search(block)
        lines       = block.splitlines()
        title_line  = lines[0].strip() if lines else ""

        entries.append({
            "raw":         block[:500],
            "title":       title_line[:100],
            "dates":       dates_match.group(0) if dates_match else None,
            "line_count":  len(lines),
        })

    return entries


def extract_projects(sections: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Extract project entries from the projects section.

    Returns:
        list of dicts: {name, description, technologies}
    """
    proj_text = sections.get("projects", "")
    if not proj_text:
        return []

    entries   = []
    blocks    = re.split(r"\n{2,}|(?=•|▪|◦|-\s|\d+\.)", proj_text)
    tech_re   = re.compile(
        r"\b(python|java|javascript|typescript|react|node|flask|django|fastapi|"
        r"docker|kubernetes|aws|azure|gcp|tensorflow|pytorch|sql|mongodb|"
        r"redis|graphql|rest|html|css|vue|angular|spring|git)\b",
        re.IGNORECASE,
    )

    for block in blocks:
        block = block.strip()
        if not block or len(block) < 10:
            continue

        techs = list(set(m.lower() for m in tech_re.findall(block)))
        lines = block.splitlines()

        entries.append({
            "name":         lines[0].strip()[:150] if lines else "",
            "raw":          block[:500],
            "technologies": techs,
        })

    return entries


def extract_certifications(sections: Dict[str, str]) -> List[str]:
    """
    Extract certification/achievement entries from the certs section.
    """
    cert_text = sections.get("certifications", "")
    if not cert_text:
        return []

    lines = [
        re.sub(r"^[•▪◦\-\*\d\.]+\s*", "", l).strip()
        for l in cert_text.splitlines()
        if l.strip() and len(l.strip()) > 5
    ]
    return [l for l in lines if l]


def compute_section_scores(
    parsed: Dict,
    full_resume_text: str,
    full_score: float,
) -> Dict[str, float]:
    """
    Estimate contribution of each section to the overall match.

    Returns a dict of section_name -> estimated_score (0-100).
    """
    from utils import clean_text
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    section_scores: Dict[str, float] = {}
    raw_sections = parsed.get("raw_sections", {})

    jd_text = parsed.get("_jd_text", "")
    if not jd_text:
        return section_scores

    for section_name, section_text in raw_sections.items():
        if not section_text or len(section_text.split()) < 5:
            continue
        try:
            vec = TfidfVectorizer(stop_words="english", max_features=500)
            mat = vec.fit_transform([clean_text(section_text), clean_text(jd_text)])
            score = float(cosine_similarity(mat[0:1], mat[1:2])[0][0]) * 100
            section_scores[section_name] = round(score, 2)
        except Exception:
            pass

    return section_scores


# ── Main Public Function ───────────────────────────────────────────────────────

def parse_resume(resume_text: str, jd_text: str = "") -> Dict:
    """
    Parse a resume into structured sections and extract key information.

    Args:
        resume_text (str): Raw resume text (from TXT, PDF, or DOCX extraction).
        jd_text (str): Optional job description text for section-level scoring.

    Returns:
        dict with keys:
            contact       - name, email, phone, linkedin, github
            summary       - text of summary/objective section
            education     - list of education entries
            experience    - list of experience entries
            projects      - list of project entries
            certifications- list of certification strings
            raw_sections  - dict of all detected sections
            section_scores- per-section match scores (if jd_text provided)
            stats         - word count, section count, experience years estimate
    """
    logger.info("Starting structured resume parsing...")

    if not resume_text or not resume_text.strip():
        logger.warning("Empty resume text provided to parser.")
        return _empty_parse_result()

    # 1. Split into sections
    raw_sections = _split_into_sections(resume_text)
    logger.info(f"Detected {len(raw_sections)} sections: {list(raw_sections.keys())}")

    # 2. Extract structured data
    contact        = extract_contact_info(resume_text)
    education      = extract_education(resume_text, raw_sections)
    experience     = extract_experience(raw_sections)
    projects       = extract_projects(raw_sections)
    certifications = extract_certifications(raw_sections)
    summary        = raw_sections.get("summary", "")
    skills_text    = raw_sections.get("skills", "")

    # 3. Section-level scoring against JD
    section_scores: Dict[str, float] = {}
    if jd_text and jd_text.strip():
        parsed_temp = {"raw_sections": raw_sections, "_jd_text": jd_text}
        section_scores = compute_section_scores(parsed_temp, resume_text, 0)

    # 4. Stats
    total_words   = len(resume_text.split())
    exp_years     = _estimate_experience_years(raw_sections.get("experience", ""))

    result = {
        "contact":        contact,
        "summary":        summary,
        "education":      education,
        "experience":     experience,
        "projects":       projects,
        "certifications": certifications,
        "skills_section": skills_text,
        "raw_sections":   {k: v[:1000] for k, v in raw_sections.items()},  # Truncate for API
        "section_scores": section_scores,
        "stats": {
            "total_words":     total_words,
            "section_count":   len(raw_sections),
            "sections_found":  list(raw_sections.keys()),
            "education_count": len(education),
            "experience_count":len(experience),
            "project_count":   len(projects),
            "cert_count":      len(certifications),
            "exp_years_est":   exp_years,
        },
    }

    logger.info(
        f"Parse complete: {contact.get('name', 'Unknown')} | "
        f"{len(education)} edu | {len(experience)} exp | "
        f"{len(projects)} proj | ~{exp_years} yrs exp"
    )
    return result


def _estimate_experience_years(exp_text: str) -> int:
    """
    Estimate total years of experience from date ranges in experience section.
    """
    if not exp_text:
        return 0

    date_range_re = re.compile(
        r"(\d{4})\s*[-–—to]+\s*(\d{4}|present|current|now|ongoing)",
        re.IGNORECASE,
    )
    total_years = 0
    import datetime
    current_year = datetime.datetime.now().year

    for match in date_range_re.finditer(exp_text):
        try:
            start = int(match.group(1))
            end_raw = match.group(2).lower()
            end = current_year if end_raw in ("present", "current", "now", "ongoing") else int(end_raw)
            if 1960 <= start <= current_year and start <= end:
                total_years += max(0, end - start)
        except (ValueError, TypeError):
            pass

    # Also look for "X years of experience" pattern
    yrs_match = re.search(r"(\d+)\+?\s*(?:year|yr)s?\s*(?:of\s+)?(?:experience|exp)", exp_text, re.IGNORECASE)
    if yrs_match and total_years == 0:
        total_years = int(yrs_match.group(1))

    return min(total_years, 50)  # Cap at 50


def _empty_parse_result() -> Dict:
    """Return a safe empty parse result."""
    return {
        "contact":        {"name": None, "email": None, "phone": None, "linkedin": None, "github": None},
        "summary":        "",
        "education":      [],
        "experience":     [],
        "projects":       [],
        "certifications": [],
        "skills_section": "",
        "raw_sections":   {},
        "section_scores": {},
        "stats": {
            "total_words": 0, "section_count": 0, "sections_found": [],
            "education_count": 0, "experience_count": 0,
            "project_count": 0, "cert_count": 0, "exp_years_est": 0,
        },
    }
