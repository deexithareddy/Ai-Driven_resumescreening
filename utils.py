"""
utils.py
--------
Utility functions for the AI Resume Screening System.
Handles file I/O, text preprocessing, and input validation.
"""

import re
import os
from typing import Optional
from logger import get_logger
from config import MIN_WORD_COUNT

logger = get_logger(__name__)


def read_text_file(file_path: str) -> Optional[str]:
    """
    Safely read a plain text file and return its contents.

    Args:
        file_path (str): Absolute or relative path to the .txt file.

    Returns:
        str | None: File contents as a string, or None on failure.
    """
    if not os.path.isfile(file_path):
        logger.error(f"File not found: '{file_path}'")
        return None

    if not file_path.lower().endswith(".txt"):
        logger.warning(f"File '{file_path}' is not a .txt file. Attempting to read anyway.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            logger.warning(f"File '{file_path}' is empty.")
            return None
        logger.info(f"Successfully read file: '{file_path}' ({len(content)} chars)")
        return content
    except (OSError, UnicodeDecodeError) as e:
        logger.error(f"Error reading file '{file_path}': {e}")
        return None


def clean_text(text: str) -> str:
    """
    Normalize and clean raw text for NLP processing.

    Steps:
        - Lowercase
        - Remove URLs
        - Remove email addresses
        - Remove special characters (keep alphanumeric + spaces)
        - Collapse multiple whitespace

    Args:
        text (str): Raw input text.

    Returns:
        str: Cleaned text string.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)          # Remove URLs
    text = re.sub(r"\S+@\S+", " ", text)                    # Remove emails
    text = re.sub(r"[^a-z0-9\s\.\,\!\?]", " ", text)       # Keep basic punctuation
    text = re.sub(r"\s+", " ", text).strip()                # Collapse whitespace
    return text


def validate_input(text: str, label: str = "Input") -> bool:
    """
    Validate that input text meets minimum quality requirements.

    Args:
        text (str): Text to validate.
        label (str): Human-readable label for error messages.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not text or not isinstance(text, str):
        logger.error(f"{label} is empty or not a string.")
        return False

    word_count = len(text.split())
    if word_count < MIN_WORD_COUNT:
        logger.warning(
            f"{label} is too short ({word_count} words). "
            f"Minimum required: {MIN_WORD_COUNT} words. Results may be unreliable."
        )
        # Still return True — we warn but don't block processing
    return True


def format_score(score: float) -> str:
    """
    Format a float score as a percentage string.

    Args:
        score (float): Score between 0 and 100.

    Returns:
        str: Formatted string like '72.45%'
    """
    return f"{score:.2f}%"


# ─── PII Redaction for Blind Hiring (Pro) ───────────────────────────────────

PII_MASK_PATTERNS = {
    "email":  r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
    "phone":  r"\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}",
    "github": r"github\.com/[\w\-]+",
    "link":   r"linkedin\.com/in/[\w\-]+",
}

def redact_pii(text: str, mask_char: str = "*", name: Optional[str] = None) -> str:
    """
    Redact PII from text for unbiased screening.
    
    Args:
        text (str): Input text to redact.
        mask_char (str): Character to use for masking.
        name (str): Specific candidate name to mask if known.
        
    Returns:
        str: Redacted text.
    """
    if not text:
        return ""
        
    redacted = text
    
    # Mask specific name if provided
    if name:
        name_parts = name.split()
        for part in sorted(name_parts, key=len, reverse=True):
            if len(part) > 2:
                redacted = re.sub(re.escape(part), mask_char * len(part), redacted, flags=re.IGNORECASE)

    # Mask patterns
    for label, pattern in PII_MASK_PATTERNS.items():
        redacted = re.sub(pattern, f"[{label.upper()} REDACTED]", redacted)
        
    return redacted


def truncate_text(text: str, max_chars: int = 500) -> str:
    """
    Truncate text for display purposes.

    Args:
        text (str): Input text.
        max_chars (int): Maximum characters to display.

    Returns:
        str: Truncated text with ellipsis if needed.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."
