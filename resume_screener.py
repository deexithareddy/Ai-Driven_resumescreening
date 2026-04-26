"""
resume_screener.py
------------------
Resume-Job Matching Engine using TF-IDF Vectorization and Cosine Similarity.

This module computes a semantic similarity score between a resume and a job
description, indicating how well the candidate's profile matches the role.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Tuple
from logger import get_logger
from utils import clean_text, validate_input
from config import TFIDF_STOP_WORDS, TFIDF_NGRAM_RANGE, TFIDF_MAX_FEATURES

logger = get_logger(__name__)


def compute_match_score(resume_text: str, job_description: str) -> Tuple[float, dict]:
    """
    Compute the resume-to-job-description match score using TF-IDF + cosine similarity.

    Algorithm:
        1. Clean and normalize both texts.
        2. Vectorize using TF-IDF (removes stop words, uses n-grams).
        3. Compute cosine similarity between the two vectors.
        4. Scale to 0–100 range.

    Args:
        resume_text (str): Raw resume text.
        job_description (str): Raw job description text.

    Returns:
        Tuple[float, dict]:
            - match_score (float): Similarity score from 0.0 to 100.0.
            - details (dict): Diagnostic info (vocab size, raw similarity).

    Raises:
        ValueError: If either input is empty after cleaning.
    """
    logger.info("Starting resume-job match computation...")

    # ── Validate Inputs ────────────────────────────────────────────────────
    if not validate_input(resume_text, "Resume"):
        raise ValueError("Resume text is invalid or empty.")
    if not validate_input(job_description, "Job Description"):
        raise ValueError("Job description text is invalid or empty.")

    # ── Clean Text ─────────────────────────────────────────────────────────
    cleaned_resume = clean_text(resume_text)
    cleaned_jd     = clean_text(job_description)

    if not cleaned_resume.strip() or not cleaned_jd.strip():
        logger.error("Text became empty after cleaning.")
        raise ValueError("Text became empty after cleaning. Please provide more content.")

    # ── TF-IDF Vectorization ───────────────────────────────────────────────
    try:
        vectorizer = TfidfVectorizer(
            stop_words=TFIDF_STOP_WORDS,
            ngram_range=TFIDF_NGRAM_RANGE,
            max_features=TFIDF_MAX_FEATURES,
            sublinear_tf=True,          # Apply log normalization to term frequencies
        )
        tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
    except ValueError as e:
        logger.error(f"TF-IDF vectorization failed: {e}")
        raise ValueError(f"Vectorization error: {e}")

    # ── Cosine Similarity ──────────────────────────────────────────────────
    raw_similarity = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])

    # ── Score Rescaling ────────────────────────────────────────────────────
    # Raw cosine similarity between a resume and JD is inherently low because
    # they are two different document types (0.02 to 0.45 for real pairs).
    # Directly multiplying by 100 gives 2-15% even for strong matches.
    # We rescale to a realistic 0-100 range.
    LOW_ANCHOR  = 0.02
    HIGH_ANCHOR = 0.50
    clamped     = max(0.0, min(HIGH_ANCHOR, raw_similarity - LOW_ANCHOR))
    normalized  = clamped / (HIGH_ANCHOR - LOW_ANCHOR)
    tfidf_score = round(min(100.0, (normalized ** 0.65) * 100.0), 2)

    vocab_size = len(vectorizer.vocabulary_)
    logger.info(f"Match score computed: {tfidf_score:.2f}% (raw cosine: {raw_similarity:.4f}, vocab: {vocab_size})")

    details = {
        "raw_cosine_similarity": round(raw_similarity, 4),
        "tfidf_score":           round(tfidf_score, 2),
        "vocabulary_size":       vocab_size,
        "resume_word_count":     len(resume_text.split()),
        "jd_word_count":         len(job_description.split()),
    }

    return tfidf_score, details


def get_top_matching_terms(resume_text: str, job_description: str, top_n: int = 10) -> list:
    """
    Identify the top N terms that contribute most to the match score.

    Args:
        resume_text (str): Raw resume text.
        job_description (str): Raw job description text.
        top_n (int): Number of top terms to return.

    Returns:
        list[str]: Top matching terms sorted by combined TF-IDF weight.
    """
    cleaned_resume = clean_text(resume_text)
    cleaned_jd     = clean_text(job_description)

    try:
        vectorizer = TfidfVectorizer(
            stop_words=TFIDF_STOP_WORDS,
            ngram_range=TFIDF_NGRAM_RANGE,
            max_features=TFIDF_MAX_FEATURES,
        )
        tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
        feature_names = vectorizer.get_feature_names_out()

        # Sum TF-IDF weights across both documents for each term
        combined_weights = (tfidf_matrix[0] + tfidf_matrix[1]).toarray()[0]
        top_indices = combined_weights.argsort()[::-1][:top_n]
        top_terms = [feature_names[i] for i in top_indices if combined_weights[i] > 0]

        logger.debug(f"Top matching terms: {top_terms}")
        return top_terms
    except Exception as e:
        logger.warning(f"Could not extract top terms: {e}")
        return []
