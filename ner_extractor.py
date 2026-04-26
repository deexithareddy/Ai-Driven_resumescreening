"""
ner_extractor.py
----------------
Named Entity Recognition for skills, qualifications, and experience extraction.

Uses spaCy (en_core_web_sm) with a custom EntityRuler for 100+ tech skills,
frameworks, cloud tools, databases, and domain keywords.

Falls back to regex-based extraction if spaCy is not installed.
"""

import re
from typing import Dict, List, Set
from logger import get_logger

logger = get_logger(__name__)

# ── Lazy-Loaded spaCy Pipeline ─────────────────────────────────────────────────
_nlp      = None
_spacy_ok = None   # None = untested, True = loaded, False = failed

# ── Custom Skill Vocabulary ────────────────────────────────────────────────────
# Expanded across all major domains for domain-independent matching

SKILL_VOCAB: Set[str] = {
    # ── Programming Languages ──
    "python", "java", "javascript", "typescript", "c++", "c#", "c",
    "go", "golang", "rust", "scala", "kotlin", "swift", "r", "matlab",
    "php", "ruby", "perl", "bash", "shell", "powershell", "vba",
    # ── Web / Frontend ──
    "react", "angular", "vue", "nextjs", "html", "css", "sass", "webpack",
    "redux", "graphql", "rest", "soap", "oauth", "jwt",
    # ── Backend & Frameworks ──
    "node.js", "express", "django", "flask", "fastapi", "spring", "rails",
    "laravel", "asp.net", "hibernate", "grpc",
    # ── Data & ML ──
    "tensorflow", "pytorch", "keras", "sklearn", "scikit-learn", "pandas",
    "numpy", "scipy", "matplotlib", "seaborn", "spark", "hadoop", "kafka",
    "airflow", "mlflow", "hugging face", "transformers", "bert", "gpt",
    "computer vision", "nlp", "machine learning", "deep learning",
    "reinforcement learning", "feature engineering", "xgboost", "lightgbm",
    # ── Cloud & DevOps ──
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "gitlab", "github", "ci/cd", "devops", "mlops", "linux",
    "nginx", "apache", "prometheus", "grafana", "datadog",
    # ── Databases ──
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "dynamodb", "cassandra", "oracle", "sqlite", "neo4j", "snowflake",
    "bigquery", "redshift", "databricks",
    # ── Healthcare Domain ──
    "hipaa", "hl7", "fhir", "ehr", "emr", "icd-10", "cpt", "clinical trials",
    "gcp compliance", "fda", "medical coding", "nursing", "pharmacy",
    # ── Finance Domain ──
    "bloomberg", "excel", "vba", "tableau", "power bi", "quickbooks",
    "sap", "oracle financials", "gaap", "ifrs", "cpa", "cfa", "frm",
    "risk management", "derivatives", "portfolio management",
    # ── Marketing Domain ──
    "seo", "sem", "google analytics", "adwords", "facebook ads",
    "crm", "salesforce", "hubspot", "marketo", "mailchimp",
    "content marketing", "email marketing", "a/b testing",
    # ── Design Domain ──
    "figma", "sketch", "adobe xd", "photoshop", "illustrator",
    "indesign", "invision", "zeplin", "ux research", "wireframing",
    # ── Soft Skills (detectable by NER context) ──
    "communication", "leadership", "teamwork", "problem solving",
    "project management", "agile", "scrum", "kanban", "jira", "confluence",
    "time management", "critical thinking", "collaboration",
    # ── Engineering Domain ──
    "autocad", "solidworks", "catia", "ansys", "matlab", "plc", "scada",
    "cad", "pcb", "embedded systems", "robotics", "automation",
}

# ── Degree & Qualification Patterns ───────────────────────────────────────────
DEGREE_PATTERNS = [
    r'\b(b\.?s\.?c?|b\.?e\.?|b\.?tech|b\.?a\.?|b\.?b\.?a|b\.?c\.?a)\b',
    r'\b(m\.?s\.?c?|m\.?e\.?|m\.?tech|m\.?b\.?a|m\.?a\.?|m\.?c\.?a)\b',
    r'\b(ph\.?d\.?|m\.?d\.?|d\.?o\.?|j\.?d\.?)\b',
    r'\b(bachelor(?:\'?s)?|master(?:\'?s)?|doctorate|associate|diploma)\b',
    r'\b(b\.?eng|m\.?eng|b\.?sc|m\.?sc)\b',
]

# ── Experience Pattern ─────────────────────────────────────────────────────────
EXP_PATTERN = re.compile(
    r'(\d+)\+?\s*(?:–|-|to)?\s*(?:\d+)?\+?\s*(?:years?|yrs?)\s*'
    r'(?:of\s+)?(?:experience|exp(?:erience)?|working)',
    re.IGNORECASE
)


def _get_nlp():
    """Lazy-load the spaCy pipeline with custom EntityRuler."""
    global _nlp, _spacy_ok

    if _spacy_ok is True:
        return _nlp
    if _spacy_ok is False:
        return None

    try:
        import spacy

        # Try to load the pre-installed model — never download during a request
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning(
                "spaCy model 'en_core_web_sm' not found. Using regex fallback. "
                "Install with: python -m pip install "
                "en_core_web_sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl"
            )
            _spacy_ok = False
            return None

        # Build custom EntityRuler patterns for skill vocabulary
        patterns = [
            {"label": "SKILL", "pattern": skill}
            for skill in SKILL_VOCAB
        ]
        # Multi-word patterns need special handling
        multi_word_patterns = [
            {"label": "SKILL", "pattern": [{"LOWER": word} for word in skill.split()]}
            for skill in SKILL_VOCAB if " " in skill
        ]

        ruler = _nlp.add_pipe("entity_ruler", before="ner",
                               config={"overwrite_ents": False})
        ruler.add_patterns(patterns + multi_word_patterns)

        _spacy_ok = True
        logger.info("spaCy NER pipeline loaded successfully.")
        return _nlp

    except ImportError:
        _spacy_ok = False
        logger.warning("spaCy not installed. Using regex-only skill extraction. "
                       "Install with: pip install spacy && python -m spacy download en_core_web_sm")
        return None
    except Exception as e:
        _spacy_ok = False
        logger.error(f"Failed to load spaCy: {e}")
        return None


# ── Regex Fallback Skill Extractor ─────────────────────────────────────────────

def _extract_skills_regex(text: str) -> List[str]:
    """Extract skills from text using regex boundary matching."""
    text_lower = text.lower()
    found = set()
    for skill in SKILL_VOCAB:
        # Build pattern; handle multi-word with flexible whitespace
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill)
    return sorted(found)


# ── Public API ─────────────────────────────────────────────────────────────────

def extract_entities(text: str) -> Dict:
    """
    Extract named entities and structured information from resume or JD text.

    Returns:
        dict with keys:
            skills, organizations, degrees, locations, persons,
            years_experience, method ("spacy" | "regex")
    """
    result: Dict = {
        "skills"          : [],
        "organizations"   : [],
        "degrees"         : [],
        "locations"       : [],
        "persons"         : [],
        "years_experience": None,
        "method"          : "regex",
    }

    text_lower = text.lower()

    # ── Degrees via regex (reliable regardless of spaCy) ──
    degrees_found = []
    for pat in DEGREE_PATTERNS:
        matches = re.findall(pat, text_lower, re.IGNORECASE)
        degrees_found.extend(m.upper() for m in matches)
    result["degrees"] = list(dict.fromkeys(degrees_found))

    # ── Years of experience ──
    exp_match = EXP_PATTERN.search(text)
    if exp_match:
        result["years_experience"] = int(exp_match.group(1))

    # ── Try spaCy for richer extraction ──
    nlp = _get_nlp()
    if nlp is not None:
        try:
            # Limit to 12k chars for performance
            doc = nlp(text[:12000])
            skills, orgs, locs, persons = set(), [], [], []

            for ent in doc.ents:
                lbl  = ent.label_
                text_ = ent.text.strip()
                if lbl == "SKILL":
                    skills.add(text_.lower())
                elif lbl == "ORG" and len(text_) > 1:
                    orgs.append(text_)
                elif lbl in ("GPE", "LOC") and len(text_) > 1:
                    locs.append(text_)
                elif lbl == "PERSON" and len(text_) > 1:
                    persons.append(text_)

            result["skills"]        = sorted(skills)
            result["organizations"] = list(dict.fromkeys(orgs))[:15]
            result["locations"]     = list(dict.fromkeys(locs))[:10]
            result["persons"]       = list(dict.fromkeys(persons))[:5]
            result["method"]        = "spacy"

        except Exception as e:
            logger.warning(f"spaCy entity extraction failed: {e}. Using regex fallback.")
            result["skills"] = _extract_skills_regex(text)
    else:
        result["skills"] = _extract_skills_regex(text)

    return result


def compare_skills_ner(resume_text: str, jd_text: str) -> Dict:
    """
    Compare skills between resume and JD using NER-based extraction.

    Provides richer, domain-independent skill matching compared to
    simple keyword lookup against a fixed list.

    Returns:
        dict with matched_skills, missing_skills, skill_match_pct, etc.
    """
    resume_ents = extract_entities(resume_text)
    jd_ents     = extract_entities(jd_text)

    resume_skills = set(resume_ents["skills"])
    jd_skills     = set(jd_ents["skills"])

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    extra   = sorted(resume_skills - jd_skills)

    coverage = round(len(matched) / len(jd_skills) * 100, 2) if jd_skills else 100.0

    logger.info(
        f"NER skill comparison: {len(matched)} matched, {len(missing)} missing | "
        f"method={resume_ents['method']}"
    )

    return {
        "matched_skills"   : matched,
        "missing_skills"   : missing,
        "extra_skills"     : extra,
        "jd_skills"        : sorted(jd_skills),
        "resume_skills"    : sorted(resume_skills),
        "skill_match_pct"  : coverage,
        "resume_years_exp" : resume_ents.get("years_experience"),
        "jd_years_exp"     : jd_ents.get("years_experience"),
        "resume_degrees"   : resume_ents.get("degrees", []),
        "jd_degrees"       : jd_ents.get("degrees", []),
        "ner_method"       : resume_ents.get("method", "regex"),
    }


def is_ner_available() -> bool:
    """Return True if spaCy NER is loaded and ready."""
    return _get_nlp() is not None
