"""
feature_extractor.py
--------------------
Statistical Linguistic Feature Extraction for AI Content Detection.

Extracts 12 purely statistical features from text — no keyword lists,
no buzzword matching. These features capture the measurable writing-style
differences between human-authored and AI-generated text.

Features:
    1.  avg_sentence_length     — Mean words per sentence
    2.  sentence_length_std     — Std dev of sentence lengths (burstiness)
    3.  sentence_length_cv      — Coefficient of variation (normalized burstiness)
    4.  type_token_ratio        — Vocabulary richness (unique words / total words)
    5.  hapax_legomena_ratio    — Fraction of words appearing exactly once
    6.  word_entropy            — Shannon entropy of word frequency distribution
    7.  avg_word_length         — Mean character length per word
    8.  word_length_std         — Std dev of word lengths
    9.  punctuation_ratio       — Punctuation characters per total characters
   10.  punctuation_diversity   — Distinct punctuation types used (normalized 0-1)
   11.  stopword_ratio          — Fraction of words that are stopwords
   12.  word_repetition_rate    — Fraction of word occurrences that are repeated

Why these features work:
    AI-generated text has statistically uniform sentence lengths, lower entropy,
    more predictable vocabulary, and higher stopword density. These properties
    are structural — they survive paraphrasing, synonym swaps, and prompt changes
    that defeat keyword-based heuristics.
"""

import math
import re
import statistics
from typing import List, Dict
from collections import Counter

import nltk

from logger import get_logger

logger = get_logger(__name__)

# ── Feature Names (order matters — must match model training) ──────────────────

FEATURE_NAMES: List[str] = [
    "avg_sentence_length",
    "sentence_length_std",
    "sentence_length_cv",
    "type_token_ratio",
    "hapax_legomena_ratio",
    "word_entropy",
    "avg_word_length",
    "word_length_std",
    "punctuation_ratio",
    "punctuation_diversity",
    "stopword_ratio",
    "word_repetition_rate",
]

# ── Stopword Set (from NLTK, loaded once) ──────────────────────────────────────

_STOPWORDS = None

def _get_stopwords() -> set:
    global _STOPWORDS
    if _STOPWORDS is not None:
        return _STOPWORDS
    try:
        _STOPWORDS = set(nltk.corpus.stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        _STOPWORDS = set(nltk.corpus.stopwords.words("english"))
    return _STOPWORDS


# ── Tokenization Helpers ───────────────────────────────────────────────────────

def _tokenize_sentences(text: str) -> List[str]:
    """Split text into sentences using NLTK punkt tokenizer."""
    try:
        sents = nltk.sent_tokenize(text)
        return [s.strip() for s in sents if s.strip()]
    except Exception:
        return [s.strip() for s in text.split(".") if s.strip()]


def _tokenize_words(text: str) -> List[str]:
    """Extract alphabetic word tokens from text."""
    try:
        tokens = nltk.word_tokenize(text.lower())
        return [t for t in tokens if t.isalpha() and len(t) > 1]
    except Exception:
        return [w.lower() for w in re.findall(r"[a-zA-Z]{2,}", text)]


# ── Core Feature Extraction ───────────────────────────────────────────────────

def extract_features(text: str) -> List[float]:
    """
    Extract 12 statistical linguistic features from raw text.

    Args:
        text: Raw input text (resume or any document).

    Returns:
        List of 12 float feature values in the order defined by FEATURE_NAMES.
        Returns a list of 12 zeros if input is too short for reliable extraction.
    """
    if not text or len(text.strip()) < 50:
        return [0.0] * len(FEATURE_NAMES)

    sentences = _tokenize_sentences(text)
    words = _tokenize_words(text)

    if len(sentences) < 2 or len(words) < 10:
        return [0.0] * len(FEATURE_NAMES)

    # ── Sentence-level features ────────────────────────────────────────────
    sent_lengths = [len(_tokenize_words(s)) for s in sentences]
    sent_lengths = [sl for sl in sent_lengths if sl > 0]

    if len(sent_lengths) < 2:
        sent_lengths = [len(s.split()) for s in sentences if s.split()]

    avg_sent_len = statistics.mean(sent_lengths) if sent_lengths else 0.0
    sent_len_std = statistics.stdev(sent_lengths) if len(sent_lengths) >= 2 else 0.0
    sent_len_cv  = (sent_len_std / avg_sent_len) if avg_sent_len > 0 else 0.0

    # ── Vocabulary richness ────────────────────────────────────────────────
    word_counts = Counter(words)
    total_words = len(words)
    unique_words = len(word_counts)

    ttr = unique_words / total_words if total_words > 0 else 0.0

    # Hapax legomena: words appearing exactly once
    hapax = sum(1 for count in word_counts.values() if count == 1)
    hapax_ratio = hapax / total_words if total_words > 0 else 0.0

    # ── Shannon entropy of word distribution ───────────────────────────────
    # Higher entropy = more diverse/unpredictable word usage (human-like)
    # Lower entropy = more repetitive/predictable (AI-like)
    entropy = 0.0
    if total_words > 0:
        for count in word_counts.values():
            p = count / total_words
            if p > 0:
                entropy -= p * math.log2(p)

    # ── Word-level features ────────────────────────────────────────────────
    word_lengths = [len(w) for w in words]
    avg_word_len = statistics.mean(word_lengths) if word_lengths else 0.0
    word_len_std = statistics.stdev(word_lengths) if len(word_lengths) >= 2 else 0.0

    # ── Punctuation features ───────────────────────────────────────────────
    punct_chars = set(".,;:!?-()\"'—–…[]{}@#$%&*")
    punct_count = sum(1 for c in text if c in punct_chars)
    total_chars = len(text)
    punct_ratio = punct_count / total_chars if total_chars > 0 else 0.0

    # Punctuation diversity: how many distinct punctuation types are used
    punct_types_found = set()
    punct_categories = {
        ".": "period", ",": "comma", "!": "excl", "?": "question",
        ";": "semicolon", ":": "colon", "-": "dash", "(": "paren",
        "\"": "dquote", "'": "squote", "…": "ellipsis", "—": "emdash",
    }
    for c in text:
        if c in punct_categories:
            punct_types_found.add(punct_categories[c])
    # Normalize to 0-1 (max ~8 distinct types in typical resumes)
    punct_diversity = min(1.0, len(punct_types_found) / 8.0)

    # ── Stopword ratio ─────────────────────────────────────────────────────
    stopwords = _get_stopwords()
    stopword_count = sum(1 for w in words if w in stopwords)
    stopword_ratio = stopword_count / total_words if total_words > 0 else 0.0

    # ── Word repetition rate ───────────────────────────────────────────────
    # Fraction of word occurrences that are not unique (repeated at least once)
    repeated_occurrences = sum(c for c in word_counts.values() if c > 1)
    repetition_rate = repeated_occurrences / total_words if total_words > 0 else 0.0

    features = [
        avg_sent_len,       # 1
        sent_len_std,        # 2
        sent_len_cv,         # 3
        ttr,                 # 4
        hapax_ratio,         # 5
        entropy,             # 6
        avg_word_len,        # 7
        word_len_std,        # 8
        punct_ratio,         # 9
        punct_diversity,     # 10
        stopword_ratio,      # 11
        repetition_rate,     # 12
    ]

    return features


def extract_features_dict(text: str) -> Dict[str, float]:
    """
    Extract features and return as a named dictionary.

    Useful for debugging and display in API responses.
    """
    values = extract_features(text)
    return dict(zip(FEATURE_NAMES, values))
"""
    IMPORTANT: Extracts 12 statistical features. 
    These features are also used by the ML model. Train the model feature_extractor first.
"""
