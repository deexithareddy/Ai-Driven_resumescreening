"""
semantic_matcher.py
-------------------
Semantic Similarity Engine using Sentence-BERT (all-MiniLM-L6-v2).

Replaces TF-IDF with contextual embeddings for domain-independent resume
matching that understands meaning, synonyms, and context rather than just
exact keyword overlap.

Features:
  - Lazy-loads Sentence-BERT model on first use
  - Chunks long documents with overlap for accurate embedding
  - Calibrated cosine similarity → 0–100 score
  - Automatic fallback to TF-IDF if sentence-transformers unavailable
"""

import numpy as np
from typing import Tuple, List, Dict, Optional
from sklearn.metrics.pairwise import cosine_similarity
from logger import get_logger

logger = get_logger(__name__)

# ── Model Configuration ────────────────────────────────────────────────────────
SEMANTIC_MODEL_NAME = "all-MiniLM-L6-v2"   # ~90MB, CPU-friendly, excellent quality
MAX_CHUNK_WORDS     = 256                     # Max words per embedding chunk
CHUNK_OVERLAP       = 0.5                     # 50% overlap between chunks

# ── Lazy-Loaded Model ──────────────────────────────────────────────────────────
_model      = None
_model_ok   = None   # None = untested, True = loaded, False = failed


def _get_model():
    """Lazy-load the Sentence-BERT model. Returns None if unavailable."""
    global _model, _model_ok

    if _model_ok is True:
        return _model
    if _model_ok is False:
        return None

    try:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading Sentence-BERT model '{SEMANTIC_MODEL_NAME}'…")
        _model    = SentenceTransformer(SEMANTIC_MODEL_NAME)
        _model_ok = True
        logger.info("Sentence-BERT model loaded successfully.")
        return _model
    except ImportError:
        logger.warning(
            "sentence-transformers not installed. "
            "Install with: pip install sentence-transformers\n"
            "Falling back to TF-IDF matching."
        )
        _model_ok = False
        return None
    except Exception as e:
        logger.error(f"Failed to load Sentence-BERT model: {e}. Falling back to TF-IDF.")
        _model_ok = False
        return None


# ── Text Chunking ──────────────────────────────────────────────────────────────

def _chunk_text(text: str, max_words: int = MAX_CHUNK_WORDS) -> List[str]:
    """
    Split long text into overlapping chunks for embedding.
    Overlap prevents loss of context at chunk boundaries.
    """
    words = text.split()
    if len(words) <= max_words:
        return [text]

    step   = int(max_words * (1 - CHUNK_OVERLAP))
    chunks = []
    for i in range(0, len(words), step):
        chunk = " ".join(words[i : i + max_words])
        chunks.append(chunk)
        if i + max_words >= len(words):
            break
    return chunks


def _embed_text(text: str, model) -> np.ndarray:
    """
    Embed text using Sentence-BERT.
    For long texts, embed chunked segments and return a length-weighted average.
    """
    chunks    = _chunk_text(text)
    embs      = model.encode(chunks, show_progress_bar=False, convert_to_numpy=True)

    # Weight each chunk by its word count for fair averaging
    weights   = np.array([len(c.split()) for c in chunks], dtype=float)
    weights  /= weights.sum()
    return np.average(embs, axis=0, weights=weights)


# ── Calibration ────────────────────────────────────────────────────────────────

def _calibrate(raw_cosine: float) -> float:
    """
    Map raw cosine similarity [0, 1] to a user-facing [0, 100] score.

    Sentence-BERT cosine similarity between a resume and a JD typically falls
    in the 0.30–0.80 range:
        0.30 → unrelated  → ~25%
        0.50 → partial     → ~55%
        0.65 → good match  → ~75%
        0.80 → excellent   → ~95%
    """
    c = max(0.0, float(raw_cosine))

    # Piecewise linear calibration
    if c >= 0.85:
        return 100.0
    elif c >= 0.70:
        return 85.0 + ((c - 0.70) / 0.15) * 15.0
    elif c >= 0.50:
        return 55.0 + ((c - 0.50) / 0.20) * 30.0
    elif c >= 0.30:
        return 20.0 + ((c - 0.30) / 0.20) * 35.0
    else:
        return max(0.0, c / 0.30) * 20.0


# ── Public API ─────────────────────────────────────────────────────────────────

def compute_semantic_similarity(resume_text: str, jd_text: str) -> Tuple[float, Dict]:
    """
    Compute semantic similarity between a resume and job description.

    Uses Sentence-BERT embeddings and cosine similarity for domain-independent
    matching.  Automatically falls back to TF-IDF if the model is unavailable.

    Args:
        resume_text: Raw resume text.
        jd_text:     Raw job description text.

    Returns:
        Tuple[float, dict]: (similarity_score 0–100, details dict)

    Raises:
        RuntimeError: Only if both BERT and TF-IDF fallback fail.
    """
    model = _get_model()

    if model is None:
        # ── TF-IDF fallback ────────────────────────────────────────────────
        logger.info("Using TF-IDF fallback for similarity computation.")
        return _tfidf_fallback(resume_text, jd_text)

    try:
        resume_emb = _embed_text(resume_text, model).reshape(1, -1)
        jd_emb     = _embed_text(jd_text,     model).reshape(1, -1)

        cos_sim    = float(cosine_similarity(resume_emb, jd_emb)[0][0])
        score      = round(_calibrate(cos_sim), 2)

        logger.info(
            f"Semantic match: cosine={cos_sim:.4f} → score={score:.1f}%"
        )
        return score, {
            "cosine_similarity" : round(cos_sim, 4),
            "semantic_score"    : score,
            "model"             : SEMANTIC_MODEL_NAME,
            "method"            : "sentence-bert",
        }

    except Exception as e:
        logger.error(f"Sentence-BERT similarity failed ({e}). Falling back to TF-IDF.")
        return _tfidf_fallback(resume_text, jd_text)


def is_semantic_available() -> bool:
    """Return True if the Sentence-BERT model is loaded and ready."""
    return _get_model() is not None


# ── TF-IDF Fallback ────────────────────────────────────────────────────────────

def _tfidf_fallback(resume_text: str, jd_text: str) -> Tuple[float, Dict]:
    """TF-IDF cosine similarity as fallback when sentence-transformers is absent."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from utils import clean_text

    cleaned_resume = clean_text(resume_text)
    cleaned_jd     = clean_text(jd_text)

    vectorizer   = TfidfVectorizer(stop_words="english", ngram_range=(1, 2),
                                   max_features=5000, sublinear_tf=True)
    matrix       = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
    raw          = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])

    # Rescale to realistic 0-100 range (TF-IDF cosine for resume/JD is 0.02–0.50)
    LOW, HIGH = 0.02, 0.50
    clamped   = max(0.0, min(HIGH, raw - LOW))
    score     = round(min(100.0, ((clamped / (HIGH - LOW)) ** 0.65) * 100.0), 2)

    logger.info(f"TF-IDF fallback match: raw={raw:.4f} → score={score:.1f}%")
    return score, {
        "raw_cosine_similarity" : round(raw, 4),
        "tfidf_score"           : score,
        "vocabulary_size"       : len(vectorizer.vocabulary_),
        "method"                : "tfidf-fallback",
    }
