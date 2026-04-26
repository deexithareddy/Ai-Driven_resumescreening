"""
config.py
---------
Global configuration constants for the AI-Powered Resume Screening System.
Centralizes all tunable parameters for easy maintenance.
"""

# ─── Decision Thresholds ────────────────────────────────────────────────────
MATCH_SCORE_THRESHOLD = 60.0       # Minimum match score (%) to consider shortlisting
AI_SCORE_THRESHOLD    = 80.0       # Maximum AI likelihood (%) allowed for shortlisting

# ─── TF-IDF Settings ────────────────────────────────────────────────────────
TFIDF_STOP_WORDS = "english"       # Remove common English stop words
TFIDF_NGRAM_RANGE = (1, 2)         # Unigrams and bigrams for richer matching
TFIDF_MAX_FEATURES = 5000          # Cap vocabulary size

# ─── AI Detection Settings ──────────────────────────────────────────────────
MIN_SENTENCES_FOR_DETECTION = 3    # Minimum sentences needed for reliable detection
AI_VARIANCE_LOW_BOUND  = 0.0       # Variance below this → very likely AI
AI_VARIANCE_HIGH_BOUND = 200.0     # Variance above this → very likely human

# ─── Input Validation ───────────────────────────────────────────────────────
MIN_WORD_COUNT = 10                # Minimum words required in resume/JD

# ─── Logging ────────────────────────────────────────────────────────────────
LOG_FILE = "screening.log"
LOG_LEVEL = "INFO"                 # DEBUG | INFO | WARNING | ERROR

# ─── Skill Library ──────────────────────────────────────────────────────────
TECH_SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
    "react", "angular", "vue", "node.js", "django", "flask", "fastapi", "spring",
    "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ci/cd",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow",
    "pytorch", "scikit-learn", "pandas", "numpy", "spark", "hadoop",
    "git", "linux", "rest api", "graphql", "microservices", "agile", "scrum",
    "data structures", "algorithms", "system design", "devops", "mlops",
]

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving", "critical thinking",
    "time management", "adaptability", "creativity", "collaboration", "mentoring",
    "project management", "analytical", "detail-oriented", "self-motivated",
]

ALL_SKILLS = TECH_SKILLS + SOFT_SKILLS

# ─── Email Configuration ────────────────────────────────────────────────────
SMTP_EMAIL    = "deexithareddy896@gmail.com"
SMTP_PASSWORD = "zetb ofzm czzl gmty"

# ─── Security Settings (Pro) ────────────────────────────────────────────────
JWT_SECRET_KEY = "recruitai_pro_secret_key_7788"   # Change in production
ADMIN_PASSWORD = "admin123"                         # Default password
JWT_EXPIRATION_HOURS = 24
