"""
ai_detector.py
--------------
AI Content Detection Engine for the Resume Screening System.

Implements a resume-specific detection strategy using 10 signals tuned
specifically for AI-generated career documents (ChatGPT / Claude / Gemini).

RECALIBRATED (v2) — Reduces false positives on human-written resumes by:
  • Removing common human phrases from buzzword/fingerprint lists
  • Shifting weight toward statistical signals (burstiness, variance)
  • Gentler calibration curve (x^0.70 instead of x^0.45)
  • Higher signal-floor activation threshold
  • Skipping short sentences (names, emails, titles) in per-sentence analysis
  • Confidence-based classification: Likely Human / Uncertain / Likely AI

Signals (v2 weights):
   1. AI Buzzword / Boilerplate Density      — 18%  (was 27%)
   2. ChatGPT Fingerprint Phrases            — 18%  (was 23%)
   3. Hyper-polish / superlative patterns     —  8%  (was 14%)
   4. Generic impact claim patterns           —  8%  (was  9%)
   5. Transition word density                 —  6%  (was  7%)
   6. Sentence length variance                — 10%  (was  5%)
   7. Lexical diversity (TTR)                 —  5%  (was  4%)
   8. Punctuation diversity                   —  3%  (was  3%)
   9. Burstiness (AI phrase distribution)     — 14%  (was  5%)
  10. Predictability (common-word density)    — 10%  (was  3%)
"""

import statistics
import math
import re
from typing import Tuple, List, Dict
from collections import Counter
import nltk
from logger import get_logger
from utils import validate_input
from config import (
    MIN_SENTENCES_FOR_DETECTION,
    AI_VARIANCE_LOW_BOUND,
    AI_VARIANCE_HIGH_BOUND,
)

logger = get_logger(__name__)


# ── NLTK Setup ─────────────────────────────────────────────────────────────────

def _ensure_nltk_data() -> None:
    datasets = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
    ]
    for path, name in datasets:
        try:
            nltk.data.find(path)
        except LookupError:
            logger.info(f"Downloading NLTK dataset: '{name}'...")
            nltk.download(name, quiet=True)

_ensure_nltk_data()


# ── Tokenization Helpers ───────────────────────────────────────────────────────

def _tokenize_sentences(text: str) -> list:
    try:
        sentences = nltk.sent_tokenize(text)
        return [s.strip() for s in sentences if s.strip()]
    except Exception as e:
        logger.warning(f"Sentence tokenization failed: {e}. Falling back to period split.")
        return [s.strip() for s in text.split(".") if s.strip()]


def _tokenize_words(sentence: str) -> list:
    try:
        tokens = nltk.word_tokenize(sentence)
        return [t for t in tokens if t.isalpha()]
    except Exception as e:
        logger.warning(f"Word tokenization failed: {e}. Falling back to split.")
        return sentence.split()


# ── Contact / Header Detection Helper ─────────────────────────────────────────
# Used to skip names, emails, phone numbers, URLs in per-sentence analysis.
# These are NOT indicators of AI content and should never be flagged.

_EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
_PHONE_RE = re.compile(r'[\+]?[\d\s\-().]{7,15}')
_URL_RE   = re.compile(r'https?://|www\.|linkedin\.com|github\.com', re.I)

def _is_contact_or_header(sentence: str) -> bool:
    """Return True if the sentence looks like contact info or a short header."""
    stripped = sentence.strip()
    words = stripped.split()

    # Very short lines are usually names, titles, or section headers
    if len(words) <= 4:
        return True

    # Contains email address
    if _EMAIL_RE.search(stripped):
        return True

    # Contains URL
    if _URL_RE.search(stripped):
        return True

    # Looks like a phone number (mostly digits/symbols, few alpha words)
    alpha_words = [w for w in words if any(c.isalpha() for c in w)]
    if len(alpha_words) <= 2 and _PHONE_RE.search(stripped):
        return True

    # Section headers: all-caps or common header keywords
    header_keywords = [
        "education", "experience", "skills", "projects", "certifications",
        "summary", "objective", "references", "awards", "publications",
        "work history", "professional experience", "technical skills",
        "contact", "personal details", "qualifications",
    ]
    if stripped.lower().rstrip(':').strip() in header_keywords:
        return True
    if stripped.isupper() and len(words) <= 5:
        return True

    return False


# ── Signal 1: AI Buzzword / Boilerplate Density ────────────────────────────────
# These are words and phrases AI models default to when writing resumes.
# CLEANED: Removed common human phrases that caused false positives
# (e.g., "team player", "hands-on experience", "proficient in", "ability to")

AI_BUZZWORDS = [
    # Classic AI resume openers — humans rarely stack these
    "results-driven", "results driven", "detail-oriented", "detail oriented",
    "highly motivated",
    "dynamic professional", "seasoned professional", "accomplished professional",
    "passionate professional", "dedicated professional",

    # Action verb clichés heavily overused by AI (not standard career-coach verbs)
    "spearheaded", "orchestrated", "championed", "pioneered", "architected",
    "synergized", "galvanized", "spurred", "propelled", "catalyzed",
    "forged", "harnessed", "masterminded", "revamped", "overhauled",

    # Vague competency claims — AI stacks these; humans pick one or two
    "proven track record", "strong foundation", "deep understanding",
    "extensive experience", "comprehensive knowledge", "solid understanding",
    "keen insight", "robust knowledge", "in-depth knowledge",
    "diverse skill set", "versatile skill", "strong background",

    # AI filler adjectives — rarely seen in genuine human resumes
    "cutting-edge", "state-of-the-art", "industry-leading", "world-class",
    "best-in-class", "best practices", "innovative solutions", "forward-thinking",
    "data-driven", "value-added", "mission-critical", "high-impact",
    "scalable solutions", "end-to-end", "holistic approach", "strategic approach",
    "actionable insights", "key stakeholders", "cross-functional teams",

    # Soft-skill AI filler (kept only the clearly AI-heavy patterns)
    "passionate about", "dedicated to", "committed to excellence",
    "thrives in", "excels at", "adept at",
    "exceptional ability",

    # Generic achievement language
    "played a pivotal role", "significant contributor", "key contributor",
    "valuable asset", "integral part", "vital role", "crucial role",
    "impactful results", "tangible results", "measurable results",
    "substantial improvements", "notable improvements", "impressive results",
]


def _compute_buzzword_score(text: str) -> float:
    """
    Signal 1: AI buzzword / boilerplate density (0-100, higher = more AI-like).
    Counts distinct AI phrases in the text, normalized by text length.

    v2 FIX: Lowered multiplier from 18→14 and removed common human phrases
    from the list so that a typical professional resume with 1-2 matches
    scores < 15 instead of 30-40.
    """
    text_lower = text.lower()
    word_count = len(text_lower.split())
    if word_count < 10:
        return 0.0

    matched = [p for p in AI_BUZZWORDS if p in text_lower]
    distinct_matches = len(matched)

    # Per 200 words, expect 0-1 buzzwords from humans, 5-15+ from AI
    density = distinct_matches / max(1, word_count / 200)

    # v2: Lowered multiplier (14 vs 18) so 1-2 matches/200w → 14-28 not 18-36
    score = min(100.0, density * 14.0)
    logger.debug(f"Buzzword: {distinct_matches} matches, density={density:.2f}, score={score:.1f}")
    return score


# ── Signal 2: ChatGPT Fingerprint Phrases ─────────────────────────────────────
# Structural and semantic patterns near-exclusive to AI-generated resumes.
# CLEANED: Removed standard English phrases that humans commonly use
# (e.g., "successfully", "as well as", "not only...but also")

CHATGPT_FINGERPRINTS = [
    # Typical ChatGPT resume summary openers
    "i am a", "i am an", "as a dedicated", "as a passionate", "as an experienced",
    "as a highly", "as a results-driven", "as a motivated", "as a skilled",
    "i bring", "i excel", "i thrive", "i strive", "i leverage",
    "with a passion for", "with a strong background", "with expertise in",
    "with extensive experience", "with a proven track",

    # ChatGPT-specific narrative transitions (kept only AI-heavy ones)
    # REMOVED: "not only", "but also", "as well as", "in addition to",
    #          "while also", "alongside" — these are standard English
    "whilst also",  # dead giveaway for AI (Claude especially)

    # ChatGPT superlative / boast patterns — humans rarely self-praise this way
    "consistently", "effectively managed", "efficiently managed",
    "diligently", "meticulously", "seamlessly", "flawlessly",
    "strategically", "proactively identified", "proactively managed",

    # ChatGPT closing / objective lines — very AI-specific patterns
    "seeking to leverage", "looking to leverage", "eager to contribute",
    "committed to driving", "dedicated to achieving", "poised to",
    "aiming to", "aspiring to", "with a focus on delivering",
    "to drive organizational", "to contribute to the",

    # Common ChatGPT phrase structure in bullets (kept only AI-heavy combos)
    # REMOVED: "developed and implemented", "designed and implemented",
    #          "worked closely with" — humans write these too
    "led and managed", "built and deployed", "created and maintained",
    "analyzed and optimized", "identified and resolved", "managed and coordinated",
    "collaborated with cross",
    "responsible for overseeing", "responsible for managing",
    "responsible for developing", "responsible for leading",
]


def _compute_fingerprint_score(text: str) -> float:
    """
    Signal 2: ChatGPT fingerprint phrases (0-100, higher = more AI-like).

    v2 FIX: Lowered multiplier from 16→12 and removed standard English
    phrases from the list. Human resumes with normal transitions now
    score near 0 instead of 20-30.
    """
    text_lower = text.lower()
    word_count = len(text_lower.split())
    if word_count < 10:
        return 0.0

    matched = [p for p in CHATGPT_FINGERPRINTS if p in text_lower]
    distinct_matches = len(matched)

    # Per 200 words: 0 from humans, 4-12+ from AI
    density = distinct_matches / max(1, word_count / 200)
    # v2: Lowered multiplier (12 vs 16)
    score = min(100.0, density * 12.0)

    logger.debug(f"Fingerprint: {distinct_matches} matches, density={density:.2f}, score={score:.1f}")
    return score


# ── Signal 3: Hyper-polish / Superlative Patterns ─────────────────────────────
# AI resumes use extreme superlatives and self-praise that humans rarely write.

HYPER_POLISH_PATTERNS = [
    r"\bexceptional\b", r"\boutstanding\b", r"\bexemplary\b", r"\bimpeccable\b",
    r"\binvaluable\b", r"\bphenomenal\b", r"\bgroundbreaking\b", r"\brevolutionary\b",
    r"\btransformative\b", r"\bgame-changing\b", r"\bgame changing\b",
    r"\btrailblazing\b", r"\bcutting.edge\b", r"\bworld.class\b",
    r"\bstate.of.the.art\b", r"\bindustry.leading\b", r"\bbest.in.class\b",
    r"\bhighly skilled\b", r"\bhighly experienced\b", r"\bhighly proficient\b",
    r"\bextremely proficient\b", r"\bextremely skilled\b",
    r"\bpassionate about\b", r"\bpassionate learner\b",
    r"\bdriven by\b", r"\bfueled by\b",
    r"\btrack record of success\b", r"\bconsistently exceed\b",
    r"\bconsistently deliver\b", r"\bconsistently achiev\b",
]


def _compute_hyper_polish_score(text: str) -> float:
    """
    Signal 3: Count hyper-polish / superlative patterns (0-100).

    v2 FIX: Lowered multiplier from 15→12. A human resume with 1 match
    (e.g., "outstanding") now scores ~8 instead of ~15.
    """
    text_lower = text.lower()
    word_count = len(text_lower.split())
    if word_count < 10:
        return 0.0

    matches = sum(1 for p in HYPER_POLISH_PATTERNS if re.search(p, text_lower))
    density = matches / max(1, word_count / 150)
    # v2: Lowered multiplier (12 vs 15)
    score = min(100.0, density * 12.0)

    logger.debug(f"Hyper-polish: {matches} patterns, score={score:.1f}")
    return score


# ── Signal 4: Generic Impact Claim Patterns ────────────────────────────────────
# AI generates impact claims using the same templates (improved X by Y%).
# Without real numbers these patterns are a strong AI signal.

GENERIC_IMPACT_PATTERNS = [
    r"improved .{1,40} by \d",          # improved X by N%
    r"increased .{1,40} by \d",          # increased X by N%
    r"reduced .{1,40} by \d",            # reduced X by N%
    r"decreased .{1,40} by \d",          # decreased X by N%
    r"boosted .{1,40} by \d",            # boosted X by N%
    r"enhanced .{1,40} by \d",           # enhanced X by N%
    r"achieved .{1,20} \d+%",            # achieved N%
    r"delivered .{1,20} \d+%",           # delivered N%
    r"saved .{1,20} \$\d",               # saved $N
    r"\d+\s*%\s*(improvement|increase|reduction|decrease|growth)",
    # Bullet point openers AI loves
    r"^\s*[-•]\s*(developed|designed|led|managed|built|created|implemented|optimized|streamlined|spearheaded|orchestrated|championed)",
]

# Also check for the generic "no specifics" pattern — AI often writes very
# vague bullets without projects, company names, or real metrics.
VAGUE_PATTERNS = [
    r"\bvarious\b", r"\bnumerous\b", r"\bmultiple\b", r"\bseveral\b",
    r"\bmany\b", r"\bdiverse\b", r"\brange of\b", r"\bvariety of\b",
]


def _compute_generic_impact_score(text: str) -> float:
    """
    Signal 4: Generic impact claim & vague quantifier patterns (0-100).

    v2 FIX: Added a 50% baseline threshold for bullet openers — humans
    normally start 40-60% of bullets with action verbs, so only score
    when the ratio exceeds 60%. This prevents penalizing well-written
    human resumes that follow standard career-coach advice.
    """
    text_lower = text.lower()
    word_count = len(text_lower.split())
    if word_count < 10:
        return 0.0

    # Count bullet opener patterns (AI overuses action verbs at bullet starts)
    bullet_openers = [
        "developed", "designed", "led", "managed", "built", "created",
        "implemented", "optimized", "streamlined", "spearheaded",
        "orchestrated", "championed", "delivered", "drove", "established",
        "collaborated", "coordinated", "executed", "maintained", "deployed",
    ]
    lines = text.split("\n")
    ai_bullet_count = 0
    total_bullets = 0
    for line in lines:
        line = line.strip().lstrip("•-–*").strip()
        if len(line.split()) >= 4:
            total_bullets += 1
            first_word = line.split()[0].lower().rstrip("d").rstrip("ed") if line.split() else ""
            for opener in bullet_openers:
                if line.lower().startswith(opener):
                    ai_bullet_count += 1
                    break

    bullet_ratio = ai_bullet_count / max(1, total_bullets)
    # v2 FIX: Only score when >50% of bullets start with AI openers.
    # Humans typically have 30-50%, so a 50% baseline is generous.
    bullet_score = max(0.0, (bullet_ratio - 0.50) * 120.0)

    # Count vague quantifiers (AI avoids specificity)
    vague_count = sum(1 for p in VAGUE_PATTERNS if re.search(p, text_lower))
    vague_score = min(40.0, vague_count * 5.0)

    score = min(100.0, bullet_score + vague_score)
    logger.debug(f"Generic impact: bullet_ratio={bullet_ratio:.2f}, vague={vague_count}, score={score:.1f}")
    return score


# ── Signal 5: Transition Word Density ─────────────────────────────────────────

TRANSITION_WORDS = [
    "furthermore", "moreover", "additionally", "consequently",
    "nevertheless", "in addition", "in conclusion", "as a result",
    "on the other hand", "in particular", "specifically",
    "notably", "significantly", "effectively", "essentially",
    "ultimately", "overall", "accordingly", "thus", "hence",
    "therefore", "meanwhile", "subsequently", "in summary",
    "to summarize", "in other words", "for instance", "for example",
    "in fact", "as such", "to that end", "with that said",
    "it is worth noting", "it should be noted", "it is important",
    "in this regard", "in light of", "with respect to",
]


def _compute_transition_density(text: str) -> float:
    """Signal 5: Transition word density (0-100, higher = more AI-like)."""
    text_lower = text.lower()
    word_count = len(text_lower.split())
    if word_count < 10:
        return 0.0

    matches = sum(1 for tw in TRANSITION_WORDS if tw in text_lower)
    density = matches / max(1, word_count / 50)
    return min(100.0, density * 20.0)


# ── Signal 6: Sentence Length Variance ────────────────────────────────────────

def _compute_sentence_length_variance(sentences: list) -> float:
    """Signal 6: Sentence length variance. Low = AI-like (0-100)."""
    word_counts = [len(_tokenize_words(s)) for s in sentences]
    word_counts = [wc for wc in word_counts if wc > 0]

    if len(word_counts) < 2:
        return 50.0

    try:
        var = statistics.variance(word_counts)
        if var <= AI_VARIANCE_LOW_BOUND:
            return 100.0
        elif var >= AI_VARIANCE_HIGH_BOUND:
            return 0.0
        log_max = math.log(AI_VARIANCE_HIGH_BOUND + 1)
        log_var = math.log(var + 1)
        return max(0.0, min(100.0, 100.0 * (1.0 - log_var / log_max)))
    except statistics.StatisticsError:
        return 50.0


# ── Signal 7: Lexical Diversity (TTR) ─────────────────────────────────────────

def _compute_lexical_diversity(text: str) -> float:
    """Signal 7: Low TTR = repetitive = AI-like. Score 0-100."""
    try:
        words = nltk.word_tokenize(text.lower())
        words = [w for w in words if w.isalpha() and len(w) > 2]
        if not words:
            return 50.0
        ttr = len(set(words)) / len(words)
        # AI resumes have TTR in 0.55-0.75 range; humans vary more
        # Score higher (more AI) when TTR is in typical AI range
        if ttr < 0.45:   # extremely repetitive — very likely AI list-style
            return 80.0
        elif ttr < 0.60:  # moderately repetitive
            return 55.0
        elif ttr < 0.75:  # typical AI resume TTR range
            return 35.0
        else:             # high diversity — more human-like
            return 15.0
    except Exception:
        return 50.0


# ── Signal 8: Punctuation Diversity ───────────────────────────────────────────

def _compute_punctuation_diversity(text: str) -> float:
    """Signal 8: Low punctuation diversity = AI-like (0-100)."""
    punct_types = set()
    punct_map = {
        ".": "period", ",": "comma", "!": "exclamation", "?": "question",
        ";": "semicolon", ":": "colon", "-": "dash", "(": "paren",
        "\"": "quote", "'": "apostrophe",
    }
    for char in text:
        if char in punct_map:
            punct_types.add(punct_map[char])
    if "..." in text or "…" in text:
        punct_types.add("ellipsis")
    if "—" in text or " -- " in text:
        punct_types.add("em_dash")

    max_types = 8
    diversity = len(punct_types) / max_types
    return max(0.0, min(100.0, (1.0 - diversity) * 100.0))


# ── Signal 9: Burstiness Score ────────────────────────────────────────────────
# AI-generated text distributes buzzwords/phrases EVENLY throughout the text.
# Human-written text clusters topic-specific language in bursts.

def _compute_burstiness_score(text: str) -> float:
    """
    Signal 9: Low burstiness = AI-like (phrases spread evenly). 0-100.
    Measures whether AI buzzwords are distributed uniformly (AI) or clustered (human).
    """
    text_lower = text.lower()
    words = text_lower.split()
    if len(words) < 30:
        return 50.0

    # Detect buzzword positions
    all_markers = AI_BUZZWORDS[:30] + CHATGPT_FINGERPRINTS[:20]  # Use top patterns
    positions = []
    for marker in all_markers:
        idx = text_lower.find(marker)
        while idx != -1:
            # Convert char position to approximate word position
            word_pos = len(text_lower[:idx].split())
            positions.append(word_pos / len(words))  # Normalized 0-1 position
            idx = text_lower.find(marker, idx + len(marker))

    if len(positions) < 3:
        return 30.0  # Not enough data

    positions.sort()
    # Compute gaps between consecutive positions
    gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
    if not gaps:
        return 50.0

    mean_gap = sum(gaps) / len(gaps)
    if mean_gap == 0:
        return 50.0

    # Coefficient of variation — low CV = evenly spaced = AI
    variance = sum((g - mean_gap)**2 for g in gaps) / len(gaps)
    std = variance ** 0.5
    cv = std / mean_gap  # Coefficient of variation

    # AI: CV < 0.5 (evenly spread) → high score
    # Human: CV > 1.0 (clustered/bursty) → low score
    if cv < 0.3:
        return 90.0
    elif cv < 0.6:
        return 65.0
    elif cv < 1.0:
        return 40.0
    else:
        return 15.0


# ── Signal 10: Predictability Score ───────────────────────────────────────────
# Perplexity proxy: AI text uses more common, predictable words.
# Human text has more unique, unexpected word choices.

HIGH_FREQUENCY_WORDS = {
    "the", "and", "to", "of", "in", "a", "for", "is", "with", "that",
    "on", "was", "are", "as", "by", "an", "be", "at", "from", "or",
    "this", "which", "it", "have", "has", "had", "not", "but", "all",
    "their", "been", "will", "can", "more", "also", "its", "into",
    "through", "including", "ensuring", "across", "while", "within",
    "both", "between", "during", "such", "various", "effectively",
    "successfully", "resulting", "leading", "contributing",
}

def _compute_predictability_score(text: str) -> float:
    """
    Signal 10: High proportion of common/predictable words = AI-like. 0-100.
    Acts as a lightweight perplexity proxy without a language model.
    """
    words = [w.lower().strip('.,;:!?()"\'—') for w in text.split()]
    words = [w for w in words if len(w) > 1]
    if len(words) < 20:
        return 50.0

    common_count = sum(1 for w in words if w in HIGH_FREQUENCY_WORDS)
    ratio = common_count / len(words)

    # AI text typically has 35-45% common words (very predictable)
    # Human text: 25-35% common words (more varied)
    if ratio >= 0.45:
        return 90.0
    elif ratio >= 0.38:
        return 65.0
    elif ratio >= 0.30:
        return 40.0
    else:
        return 15.0


# ── Main Detection Function ───────────────────────────────────────────────────

def detect_ai_content(text: str) -> Tuple[float, dict]:
    """
    Detect the likelihood that resume text was AI-generated.

    Uses 10 resume-specific signals with RECALIBRATED weights (v2).
    Fully AI-generated resumes should score 65-95%.
    Human resumes should score 5-35%.

    v2 SIGNAL WEIGHTS (rebalanced to reduce false positives):
        1. AI Buzzword / Boilerplate Density     (18%) ← reduced
        2. ChatGPT Fingerprint Phrases           (18%) ← reduced
        3. Hyper-polish / superlatives           ( 8%) ← reduced
        4. Generic impact / bullet patterns      ( 8%)
        5. Transition word density               ( 6%)
        6. Sentence length variance              (10%) ← increased
        7. Lexical diversity (TTR)               ( 5%) ← increased
        8. Punctuation diversity                 ( 3%)
        9. Burstiness (AI phrase distribution)   (14%) ← increased
       10. Predictability (common-word density)  (10%) ← increased

    v2 CLASSIFICATION (confidence-based):
        0-50  → "Likely Human"
        50-75 → "Uncertain"
        75-100 → "Likely AI"

    Returns:
        Tuple[float, dict]: (ai_score 0-100, signal details dict)
    """
    logger.info("Starting AI content detection (resume-specific, 10 signals, v2 calibration)...")

    if not validate_input(text, "AI Detection Input"):
        raise ValueError("Input text is invalid or empty.")

    sentences = _tokenize_sentences(text)
    sentence_count = len(sentences)

    if sentence_count < MIN_SENTENCES_FOR_DETECTION:
        logger.warning(
            f"Only {sentence_count} sentence(s) found. "
            f"Minimum {MIN_SENTENCES_FOR_DETECTION} required. "
            "Returning neutral score of 30.0."
        )
        return 30.0, {
            "sentence_count": sentence_count,
            "classification": "Likely Human",
            "note": "Insufficient sentences for reliable detection",
        }

    # ── Compute all signals ────────────────────────────────────────────────
    buzzword_score      = _compute_buzzword_score(text)
    fingerprint_score   = _compute_fingerprint_score(text)
    hyper_polish_score  = _compute_hyper_polish_score(text)
    generic_score       = _compute_generic_impact_score(text)
    transition_score    = _compute_transition_density(text)
    variance_score      = _compute_sentence_length_variance(sentences)
    diversity_score     = _compute_lexical_diversity(text)
    punct_score         = _compute_punctuation_diversity(text)
    burstiness_score    = _compute_burstiness_score(text)
    predictability_score = _compute_predictability_score(text)

    # ── v2 Weighted combination (rebalanced — 10 signals, 100%) ────────────
    # Key change: Reduced weight on pattern-matching signals (buzzword,
    # fingerprint, hyper-polish) which trigger on common professional language.
    # Increased weight on statistical signals (burstiness, variance,
    # predictability) which better distinguish AI's uniform style.
    weighted_avg = (
        0.18 * buzzword_score       +   # Signal 1 — reduced from 27%
        0.18 * fingerprint_score    +   # Signal 2 — reduced from 23%
        0.08 * hyper_polish_score   +   # Signal 3 — reduced from 14%
        0.08 * generic_score        +   # Signal 4 — similar
        0.06 * transition_score     +   # Signal 5 — similar
        0.10 * variance_score       +   # Signal 6 — increased from 5%
        0.05 * diversity_score      +   # Signal 7 — slightly increased
        0.03 * punct_score          +   # Signal 8 — same
        0.14 * burstiness_score     +   # Signal 9 — increased from 5%
        0.10 * predictability_score     # Signal 10 — increased from 3%
    )

    # ── v2 Semantic Signal Floor (multi-signal aware) ────────────────────
    # PROBLEM FIXED: Old floor activated at 40, pushing scores up for human
    # resumes that happened to use a few common buzzwords.
    # NEW: Floor requires strong evidence (signal >= 60) to activate.
    # When MULTIPLE semantic signals converge (2+ above 60), the floor
    # is higher — this catches obvious AI content that maxes out several
    # signals. Single-signal cases remain conservative.
    semantic_signals = sorted([
        buzzword_score, fingerprint_score, hyper_polish_score, generic_score
    ], reverse=True)

    strong_count = sum(1 for s in semantic_signals if s >= 60)

    if strong_count >= 2:
        # Multiple strong AI signals — use average of top-2 as floor base
        top2_avg = (semantic_signals[0] + semantic_signals[1]) / 2
        signal_floor = top2_avg * 0.55
        raw_score = max(weighted_avg, signal_floor)
    elif strong_count == 1:
        # Single strong signal — conservative floor
        signal_floor = semantic_signals[0] * 0.50
        raw_score = max(weighted_avg, signal_floor)
    else:
        raw_score = weighted_avg

    # ── v2 Calibration: gentler power curve ───────────────────────────────
    # OLD: x^0.45 was too aggressive — raw=10 → final=28, raw=20 → final=40
    # NEW: x^0.70 is much gentler — raw=10 → final=20, raw=20 → final=33
    #
    # Mapping (approximate):
    #   raw= 5 → final≈ 12  (clearly human)
    #   raw=10 → final≈ 20  (human with some buzzwords)
    #   raw=20 → final≈ 33  (human, professional language)
    #   raw=35 → final≈ 49  (borderline — right at the Uncertain threshold)
    #   raw=50 → final≈ 62  (AI-leaning)
    #   raw=70 → final≈ 78  (obvious AI)
    #   raw=90 → final≈ 93  (very obvious AI)

    def _calibrate(raw: float) -> float:
        normalized = raw / 100.0
        boosted    = normalized ** 0.70   # v2: gentler curve (was 0.45)
        return round(min(100.0, max(0.0, boosted * 100.0)), 2)

    ai_score = _calibrate(raw_score)

    # ── v2 Confidence Classification ──────────────────────────────────────
    if ai_score < 50:
        classification = "Likely Human"
    elif ai_score < 75:
        classification = "Uncertain"
    else:
        classification = "Likely AI"

    logger.info(
        f"AI score: {ai_score:.2f}% [{classification}] (raw={raw_score:.2f}%) | "
        f"Buzzword={buzzword_score:.1f} | Fingerprint={fingerprint_score:.1f} | "
        f"HyperPolish={hyper_polish_score:.1f} | Generic={generic_score:.1f} | "
        f"Transition={transition_score:.1f} | Variance={variance_score:.1f} | "
        f"Diversity={diversity_score:.1f} | Punct={punct_score:.1f} | "
        f"Burstiness={burstiness_score:.1f} | Predictability={predictability_score:.1f}"
    )

    details = {
        "sentence_count":        sentence_count,
        "raw_ai_score":          round(raw_score, 2),
        "classification":        classification,
        "buzzword_score":        round(buzzword_score, 2),
        "fingerprint_score":     round(fingerprint_score, 2),
        "hyper_polish_score":    round(hyper_polish_score, 2),
        "generic_score":         round(generic_score, 2),
        "transition_score":      round(transition_score, 2),
        "variance_score":        round(variance_score, 2),
        "diversity_score":       round(diversity_score, 2),
        "punct_score":           round(punct_score, 2),
        "burstiness_score":      round(burstiness_score, 2),
        "predictability_score":  round(predictability_score, 2),
        "signal_breakdown": {
            "buzzword_score":       round(buzzword_score, 2),
            "fingerprint_score":    round(fingerprint_score, 2),
            "hyper_polish_score":   round(hyper_polish_score, 2),
            "generic_score":        round(generic_score, 2),
            "transition_score":     round(transition_score, 2),
            "variance_score":       round(variance_score, 2),
            "diversity_score":      round(diversity_score, 2),
            "punct_score":          round(punct_score, 2),
            "burstiness_score":     round(burstiness_score, 2),
            "predictability_score": round(predictability_score, 2),
        },
    }

    return ai_score, details


# ── Per-Sentence Analysis ──────────────────────────────────────────────────────

def detect_ai_sections(text: str) -> list:
    """
    Analyze each sentence and return a per-sentence AI likelihood score (0-100).

    v2 MAJOR FIXES:
      • SKIPS contact info, names, emails, short headers (< 5 words)
      • REMOVED bullet opener signal — standard resume verbs are NOT AI indicators
      • REMOVED sentence length signal — 12-30 word sentences are universal
      • LOWERED all per-sentence weights to prevent over-flagging
      • FIXED labels to use "High"/"Medium"/"Low"/"Clean" (matching app.py display)

    3-tier labelling:
        High   (≥ 35) — Strong AI signals, multiple indicators present
        Medium (≥ 12) — Some AI indicators detected
        Low    (<  12) — Minimal or no AI signals (includes "Clean" = 0)
    """
    if not text or not text.strip():
        return []

    sentences = _tokenize_sentences(text)
    results = []

    # Additional micro-signals for per-sentence detection
    FILLER_ADVERBS = [
        # REMOVED "successfully" — humans use it constantly
        "effectively", "efficiently", "consistently",
        "diligently", "meticulously", "seamlessly", "flawlessly",
        "strategically", "proactively", "significantly", "substantially",
        "dramatically", "exponentially", "comprehensively", "holistically",
    ]

    VAGUE_QUANTIFIERS = [
        "various", "numerous", "multiple", "several", "many",
        "diverse", "extensive", "broad", "wide range", "key",
    ]

    for idx, sent in enumerate(sentences):
        if not sent.strip():
            continue

        sentence_number = idx + 1

        # ── v2 FIX: Skip contact info, names, emails, section headers ──
        # Names, emails, phones, URLs, section titles are NEVER AI signals.
        # They are always real — never flagged.
        if _is_contact_or_header(sent):
            results.append({
                "sentence": sent,
                "sentence_number": sentence_number,
                "score": 0.0,
                "label": "Low",
                "flags": [],
                "is_excluded": True,   # Personal info — excluded from AI analysis
            })
            continue

        words = _tokenize_words(sent)
        word_count = len(words)
        sent_lower = sent.lower()
        flags = []
        score = 0.0

        # ── Signal 1: AI buzzwords in this sentence ──
        # v2: Lowered weight from 15→8 per match, cap from 40→25
        bz_matches = [p for p in AI_BUZZWORDS if p in sent_lower]
        if bz_matches:
            score += min(25.0, len(bz_matches) * 8.0)
            flags.append(f"AI buzzwords: '{', '.join(bz_matches[:4])}'")

        # ── Signal 2: ChatGPT fingerprint phrases ──
        # v2: Lowered weight from 14→8 per match, cap from 35→25
        fp_matches = [p for p in CHATGPT_FINGERPRINTS if p in sent_lower]
        if fp_matches:
            score += min(25.0, len(fp_matches) * 8.0)
            flags.append(f"ChatGPT fingerprints: '{', '.join(fp_matches[:3])}'")

        # ── Signal 3: Hyper-polish superlatives ──
        # v2: Lowered weight from 12→7 per match, cap from 25→18
        hp_matches = []
        for p in HYPER_POLISH_PATTERNS:
            m = re.search(p, sent_lower)
            if m:
                hp_matches.append(m.group(0))
        if hp_matches:
            score += min(18.0, len(hp_matches) * 7.0)
            flags.append(f"Hyper-polish: '{', '.join(hp_matches[:3])}'")

        # ── Signal 4: REMOVED — Bullet opener verbs ──
        # v2 FIX: Standard action verbs (developed, managed, led, built)
        # are taught by every career counselor and used in ALL professional
        # resumes. Flagging them caused massive false positives on human
        # resumes. This signal has been completely removed.

        # ── Signal 5: Filler adverbs (AI loves these) ──
        # v2: Lowered weight from 5→3 per match
        adverb_matches = [a for a in FILLER_ADVERBS if a in sent_lower]
        if adverb_matches:
            score += min(10.0, len(adverb_matches) * 3.0)
            flags.append(f"AI filler adverbs: '{', '.join(adverb_matches[:3])}'")

        # ── Signal 6: Vague quantifiers (AI avoids specifics) ──
        vague_matches = [v for v in VAGUE_QUANTIFIERS if v in sent_lower]
        if vague_matches:
            score += min(6.0, len(vague_matches) * 2.0)
            flags.append(f"Vague quantifiers: '{', '.join(vague_matches[:3])}'")

        # ── Signal 7: REMOVED — Sentence length in AI-typical range ──
        # v2 FIX: 12-30 word sentences are the norm in ALL professional
        # writing. This added 3 points of noise to every normal sentence.
        # Removed entirely.

        # ── Signal 8: Generic impact claim patterns ──
        impact_patterns = [
            r"improved .{1,30} by \d",
            r"increased .{1,30} by \d",
            r"reduced .{1,30} by \d",
            r"boosted .{1,30} by \d",
            r"resulting in",
            r"leading to",
            r"contributing to",
            r"achieving .{1,20}%",
            r"achieved .{0,20}\d+%",    # e.g. "achieved 84% accuracy"
            r"delivered .{0,20}\d+%",
            r"\d+%\s*(accuracy|efficiency|recall|precision|f1|auc|roc)",  # ML metrics
        ]
        imp_matches = [p for p in impact_patterns if re.search(p, sent_lower)]
        if imp_matches:
            score += min(8.0, len(imp_matches) * 3.0)
            flags.append("AI-style quantified impact claim")

        # ── Signal 9: Transition phrase starters ──
        transition_starters = [
            "furthermore", "moreover", "additionally", "consequently",
            "in addition", "as a result", "overall", "notably",
            "in particular", "specifically", "accordingly",
        ]
        for ts in transition_starters:
            if sent_lower.strip().startswith(ts):
                score += 5.0
                flags.append(f"AI transition opener: '{ts}'")
                break

        # ── Signal 10: Resume-style structured phrases (AI patterns) ──
        resume_patterns = [
            r"\d+\+?\s*years?\s*(of\s+)?experience",       # "5+ years experience"
            r"team\s+of\s+\d+",                              # "team of 12"
            r"\d+\+?\s*(engineers|developers|members|people|staff|nurses|doctors)",
            r"across\s+\d+",                                  # "across 15 projects"
            r"with\s+\d+\+?\s*(years|clients|projects|members|patients|students)",
            r"\d+%\s*(accuracy|improvement|reduction|increase|growth|compliance|completion)",
        ]
        rp_matches = [p for p in resume_patterns if re.search(p, sent_lower)]
        if rp_matches:
            score += min(5.0, len(rp_matches) * 2.0)
            flags.append("Structured resume metric pattern")

        # ── Signal 11: Per-sentence word predictability (mirrors document-level signal) ──
        # AI-generated text uses more common/high-frequency English words per sentence.
        # This signal bridges the gap between the overall statistical AI score and
        # per-sentence highlighting — so the heatmap reflects what the overall score sees.
        if word_count >= 6:
            common_count = sum(1 for w in words if w.lower() in HIGH_FREQUENCY_WORDS)
            common_ratio = common_count / word_count
            if common_ratio >= 0.42:
                score += 7.0
                flags.append(f"High word predictability ({common_ratio:.0%} common words — AI-typical)")
            elif common_ratio >= 0.32:
                score += 4.0
                flags.append(f"Moderate word predictability ({common_ratio:.0%} common words)")
            elif common_ratio >= 0.25:
                score += 2.0
                flags.append(f"Slight predictability ({common_ratio:.0%} common words)")

        score = round(min(100.0, max(0.0, score)), 1)

        # SENSITIVITY: Even tiny signals get flagged so the heatmap matches
        # the overall AI score. Document-level statistical signals (predictability,
        # burstiness, variance) manifest as moderate per-sentence scores.
        # High   (≥ 20): definite AI signals — shown in RED
        # Medium (≥  3): suspicious / borderline — shown in AMBER
        # Low    (<  3): appears human — shown in GREEN
        if score >= 20:
            label = "High"
        elif score >= 3:
            label = "Medium"
        else:
            label = "Low"

        results.append({
            "sentence": sent,
            "sentence_number": sentence_number,
            "score": score,
            "label": label,
            "flags": flags,
            "is_excluded": False,
        })

    return results
