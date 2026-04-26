"""
domain_classifier.py
--------------------
Multi-Domain Classifier for Resume and Job Description Analysis.

Identifies the professional domain (Software, Healthcare, Finance, etc.)
to provide domain-specific insights, scoring context, and screening advice.

Supports 10 professional domains:
  Software & Tech, Healthcare, Finance, Marketing, Education,
  Engineering, HR, Legal, Data Science & AI, Design & Creative
"""

import re
from typing import Dict, List, Tuple
from logger import get_logger

logger = get_logger(__name__)


# ── Domain Knowledge Base ──────────────────────────────────────────────────────

DOMAINS: Dict[str, Dict] = {
    "software": {
        "label"   : "Software & Technology",
        "icon"    : "💻",
        "keywords": [
            "software", "developer", "engineer", "programming", "code", "coding",
            "algorithm", "api", "database", "python", "java", "javascript", "react",
            "frontend", "backend", "fullstack", "devops", "cloud", "aws", "azure",
            "microservices", "agile", "scrum", "git", "deployment", "containers",
            "docker", "kubernetes", "ci/cd", "unit testing", "rest api",
        ],
        "advice": (
            "Focus on technical depth, relevant project portfolio, system design "
            "experience, and proficiency with the specific tech stack listed."
        ),
    },
    "data_science": {
        "label"   : "Data Science & AI/ML",
        "icon"    : "🤖",
        "keywords": [
            "data science", "machine learning", "deep learning", "nlp", "llm",
            "computer vision", "model training", "neural network", "tensorflow",
            "pytorch", "sklearn", "scikit-learn", "pandas", "numpy", "statistics",
            "regression", "classification", "clustering", "feature engineering",
            "mlops", "model deployment", "a/b testing", "experimentation",
            "hugging face", "bert", "gpt", "data pipeline", "etl",
        ],
        "advice": (
            "Evaluate production ML experience, statistical depth, model deployment "
            "skills, and familiarity with modern LLM/transformer frameworks."
        ),
    },
    "healthcare": {
        "label"   : "Healthcare & Medical",
        "icon"    : "🏥",
        "keywords": [
            "healthcare", "medical", "clinical", "patient", "hospital", "nursing",
            "physician", "doctor", "nurse", "diagnosis", "treatment", "pharmacy",
            "medical records", "ehr", "emr", "hipaa", "fda", "clinical trials",
            "radiology", "surgery", "therapy", "laboratory", "pathology",
            "vital signs", "medication", "chronic", "acute", "icd", "cpt",
        ],
        "advice": (
            "Verify clinical certifications, HIPAA compliance knowledge, "
            "patient care experience, and familiarity with EHR/EMR systems."
        ),
    },
    "finance": {
        "label"   : "Finance & Banking",
        "icon"    : "💰",
        "keywords": [
            "finance", "financial", "accounting", "investment", "banking", "portfolio",
            "equity", "audit", "tax", "cpa", "cfa", "budget", "forecasting",
            "revenue", "balance sheet", "trading", "risk management",
            "compliance", "regulatory", "fintech", "insurance", "actuarial",
            "derivatives", "quantitative", "capital markets", "gaap", "ifrs",
        ],
        "advice": (
            "Check for relevant certifications (CPA, CFA, FRM), regulatory compliance "
            "knowledge, quantitative skills, and experience with financial modeling."
        ),
    },
    "marketing": {
        "label"   : "Marketing & Communications",
        "icon"    : "📣",
        "keywords": [
            "marketing", "brand", "campaign", "digital marketing", "seo", "sem",
            "social media", "content", "advertising", "market research", "analytics",
            "crm", "lead generation", "conversion", "email marketing", "influencer",
            "copywriting", "creative", "growth hacking", "engagement", "pr",
            "public relations", "media", "audience", "impressions", "roas",
        ],
        "advice": (
            "Evaluate campaign ROI results, digital channels expertise, "
            "brand strategy experience, and data-driven decision making ability."
        ),
    },
    "education": {
        "label"   : "Education & Training",
        "icon"    : "🎓",
        "keywords": [
            "education", "teaching", "teacher", "professor", "curriculum",
            "student", "classroom", "school", "university", "academic",
            "pedagogy", "learning", "instruction", "training", "assessment",
            "educational technology", "faculty", "course", "lecture", "tutoring",
            "e-learning", "lms", "canvas", "blackboard", "moodle",
        ],
        "advice": (
            "Assess teaching credentials, curriculum development expertise, "
            "student outcome metrics, and technology integration skills."
        ),
    },
    "engineering": {
        "label"   : "Engineering & Manufacturing",
        "icon"    : "⚙️",
        "keywords": [
            "mechanical", "electrical", "civil", "structural", "manufacturing",
            "cad", "autocad", "solidworks", "design", "drawings", "specifications",
            "materials", "testing", "quality control", "production", "maintenance",
            "robotics", "automation", "embedded systems", "pcb", "circuits",
            "thermodynamics", "fluid dynamics", "finite element", "plc", "scada",
        ],
        "advice": (
            "Verify professional licenses (PE), domain-specific software proficiency, "
            "project scale experience, and safety compliance knowledge."
        ),
    },
    "hr": {
        "label"   : "Human Resources",
        "icon"    : "👥",
        "keywords": [
            "human resources", "hr", "recruitment", "talent acquisition",
            "onboarding", "payroll", "compensation", "benefits", "employee relations",
            "performance management", "organizational development", "diversity",
            "inclusion", "hris", "applicant tracking", "workforce planning",
            "labor relations", "succession planning", "shrm", "sphr",
        ],
        "advice": (
            "Look for HRIS proficiency, employment law knowledge, SHRM/PHR certification, "
            "and experience with large-scale talent acquisition or HR transformation."
        ),
    },
    "legal": {
        "label"   : "Legal & Compliance",
        "icon"    : "⚖️",
        "keywords": [
            "legal", "lawyer", "attorney", "law", "litigation", "contract",
            "compliance", "regulatory", "intellectual property", "corporate law",
            "employment law", "jurisdiction", "court", "counsel", "paralegal",
            "legal research", "negotiation", "bar exam", "statutes", "tort",
            "due diligence", "mergers", "acquisitions", "gdpr", "privacy",
        ],
        "advice": (
            "Check bar admission status, practice area specialization, "
            "case management experience, and firm/in-house counsel background."
        ),
    },
    "design": {
        "label"   : "Design & Creative",
        "icon"    : "🎨",
        "keywords": [
            "design", "ux", "ui", "user experience", "figma", "sketch", "adobe",
            "creative", "visual", "typography", "graphic design", "wireframe",
            "prototype", "usability", "accessibility", "branding", "illustration",
            "photoshop", "illustrator", "indesign", "motion", "animation",
            "design system", "atomic design", "human-centered",
        ],
        "advice": (
            "Review portfolio quality, UX research methodology depth, "
            "design systems experience, and cross-functional collaboration skills."
        ),
    },
}


# ── Classifier ─────────────────────────────────────────────────────────────────

def classify_domain(text: str) -> Dict:
    """
    Classify the professional domain of a resume or job description.

    Uses keyword density scoring across 10 professional domains.
    Returns the top domain with confidence score and keyword evidence.

    Args:
        text: Raw resume or job description text.

    Returns:
        dict with: domain, label, icon, confidence, top_domains, keywords_matched,
                   advice, is_general
    """
    text_lower = text.lower()
    scores: Dict[str, float] = {}
    keyword_hits: Dict[str, List[str]] = {}

    for domain_key, info in DOMAINS.items():
        hits  = [kw for kw in info["keywords"] if kw in text_lower]
        count = len(hits)
        # Normalize by keyword list size for fair comparison
        density         = count / max(1, len(info["keywords"]))
        scores[domain_key]      = density
        keyword_hits[domain_key] = hits

    # Sort by score descending
    sorted_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_key, top_score = sorted_domains[0]

    # Treat as "general" if no strong signal
    is_general = top_score < 0.05

    if is_general:
        logger.info("Domain classification: No strong domain signal — returning 'general'.")
        return {
            "domain"          : "general",
            "label"           : "General / Multi-Domain",
            "icon"            : "📄",
            "confidence"      : 0.0,
            "top_domains"     : [],
            "keywords_matched": [],
            "advice"          : (
                "Evaluate candidate against the specific role requirements. "
                "No dominant professional domain was detected."
            ),
            "is_general"      : True,
        }

    # Confidence = ratio of top domain score vs sum of top-3
    top3_sum    = sum(s for _, s in sorted_domains[:3]) or 1e-9
    confidence  = round((top_score / top3_sum) * 100, 1)

    top_domains_list = [
        {
            "domain"   : d,
            "label"    : DOMAINS[d]["label"],
            "icon"     : DOMAINS[d]["icon"],
            "score"    : round(s * 100, 1),
            "keywords" : keyword_hits[d][:5],
        }
        for d, s in sorted_domains[:3] if s > 0
    ]

    info = DOMAINS[top_key]
    logger.info(
        f"Domain classified: {top_key} ({info['label']}) | "
        f"confidence={confidence}% | hits={len(keyword_hits[top_key])}"
    )

    return {
        "domain"          : top_key,
        "label"           : info["label"],
        "icon"            : info["icon"],
        "confidence"      : confidence,
        "top_domains"     : top_domains_list,
        "keywords_matched": keyword_hits[top_key][:8],
        "advice"          : info["advice"],
        "is_general"      : False,
    }


def classify_both(resume_text: str, jd_text: str) -> Dict:
    """
    Classify domains for both resume and job description.

    Returns a merged result using the JD domain as primary
    (the JD defines the role requirements) with resume domain for context.
    """
    jd_domain     = classify_domain(jd_text)
    resume_domain = classify_domain(resume_text)

    # Check for domain mismatch (candidate applying outside their domain)
    mismatch = (
        not jd_domain["is_general"]
        and not resume_domain["is_general"]
        and jd_domain["domain"] != resume_domain["domain"]
    )

    return {
        "primary"           : jd_domain,       # Based on JD (defines the role)
        "candidate"         : resume_domain,    # Based on resume
        "domain_match"      : not mismatch,
        "domain_mismatch"   : mismatch,
        "mismatch_note"     : (
            f"Resume appears to be from {resume_domain['label']} background "
            f"but role targets {jd_domain['label']}."
        ) if mismatch else None,
    }
