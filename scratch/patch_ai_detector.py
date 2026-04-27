"""
patch_ai_detector.py
--------------------
Replaces detect_ai_sentences() in ai_detector.py with the STRICT version:
  - Adds clean_resume_text() helper that strips emails/phones/first 2 lines
  - Lowers the trigger threshold from >25% to >0%
  - ALWAYS highlights at least one sentence when AI score > 0
  - Also updates classify_ai_level() thresholds (>=50 HIGH, >=25 MEDIUM)
"""
import re, sys, os

TARGET = os.path.join(os.path.dirname(__file__), '..', 'ai_detector.py')
TARGET = os.path.normpath(TARGET)

with open(TARGET, 'r', encoding='utf-8', errors='replace') as f:
    src = f.read()

# ─────────────────────────────────────────────────────────────────
# NEW CODE BLOCK (classify_ai_level + clean_resume_text + detect_ai_sentences)
# ─────────────────────────────────────────────────────────────────
NEW_BLOCK = r'''def classify_ai_level(score: float) -> str:
    """Map a 0-100 AI score to a HIGH / MEDIUM / LOW tier."""
    if score >= 50:
        return "HIGH"    # RED
    elif score >= 25:
        return "MEDIUM"  # YELLOW
    else:
        return "LOW"     # GREEN (fallback label only)


def clean_resume_text(text: str) -> str:
    """
    Strip personal information and header lines before sentence scoring.

    Removes emails, phones, URLs, LinkedIn/GitHub handles, and the first
    1-2 lines (typically name / contact header) so they never appear
    as highlighted AI-signal sentences.
    """
    import re as _re
    # Remove email addresses
    text = _re.sub(r'\S+@\S+', '', text)
    # Remove phone numbers (various international formats)
    text = _re.sub(r'\+?[\d][\d\s\-]{8,}', '', text)
    # Remove URLs
    text = _re.sub(r'https?://\S+', '', text, flags=_re.I)
    text = _re.sub(r'www\.\S+', '', text, flags=_re.I)
    # Remove LinkedIn / GitHub handles
    text = _re.sub(r'linkedin\.com/\S*', '', text, flags=_re.I)
    text = _re.sub(r'github\.com/\S*', '', text, flags=_re.I)
    # Drop first 1-2 lines (name / contact header)
    lines = text.split('\n')
    if len(lines) > 2:
        lines = lines[2:]
    return '\n'.join(lines)


def detect_ai_sentences(text: str) -> list:
    """
    STRICT per-sentence AI likelihood scoring.

    NON-NEGOTIABLE RULE:
        If doc AI score > 0 (even 1%), AT LEAST ONE sentence is highlighted.

    Steps:
        1. Strip personal/header content via clean_resume_text().
        2. Split cleaned text into sentences; score each individually.
        3. Get document-level score on the ORIGINAL raw text.
        4. If doc score > 0 and sentences exist: always return top-1
           (and top-2 when a second sentence exists).
        5. If doc score == 0: return empty list (genuinely clean document).

    Labels:
        score >= 50  ->  HIGH   (RED)
        score  < 50  ->  MEDIUM (YELLOW)

    Args:
        text: Raw resume text (full document).

    Returns:
        list[dict] -- [{text, score, level}, ...]
    """
    # Step 1: strip personal / header content
    cleaned_text = clean_resume_text(text)
    if not cleaned_text.strip():
        # Fallback to the broader remover if clean_resume_text wiped everything
        cleaned_text = remove_non_content(text)
    if not cleaned_text.strip():
        print("[detect_ai_sentences] Warning: all content stripped as metadata.")
        return []

    # Step 2: score individual sentences (already cleaned, skip re-cleaning)
    sentences = split_sentences(cleaned_text)
    scored = []
    for s in sentences:
        s = s.strip()
        if len(s) < 15:
            continue
        # _skip_clean=True avoids double-clean bug (short sentences would be
        # wiped by remove_non_content's 20-char line filter).
        # _single_sentence=True bypasses the MIN_SENTENCES guard.
        score, _ = detect_ai_content(s, _skip_clean=True, _single_sentence=True)
        scored.append((s, score))

    # Step 3: document-level AI score on original raw text
    ai_doc_score, _ = detect_ai_content(text)

    # Step 4: sort descending (highest contributors first)
    scored.sort(key=lambda x: x[1], reverse=True)

    results = []

    if ai_doc_score > 0 and scored:
        # STRICT RULE: ANY AI signal (even 1%) -> ALWAYS highlight top sentence
        top_s, top_sc = scored[0]
        results.append({
            "text":  top_s,
            "score": round(top_sc, 2),
            "level": "HIGH" if top_sc >= 50 else "MEDIUM",
        })
        # Also include second-highest sentence for better visibility
        if len(scored) > 1:
            s2, sc2 = scored[1]
            results.append({
                "text":  s2,
                "score": round(sc2, 2),
                "level": "HIGH" if sc2 >= 50 else "MEDIUM",
            })
    # else: doc_score == 0 -> clean document, nothing to highlight

    high_c = sum(1 for r in results if r["level"] == "HIGH")
    mid_c  = sum(1 for r in results if r["level"] == "MEDIUM")
    print(f"[detect_ai_sentences] doc_score={ai_doc_score:.1f}% | "
          f"{len(results)} sentences returned | HIGH={high_c} MEDIUM={mid_c}")

    return results
'''

# ─────────────────────────────────────────────────────────────────
# Replace the entire block from classify_ai_level to end of detect_ai_sentences
# ─────────────────────────────────────────────────────────────────
# Match from "def classify_ai_level" to the end of "return results\n\n" (last function)
pattern = re.compile(
    r'def classify_ai_level\(score.*?return results\s*\n',
    re.DOTALL
)

match = pattern.search(src)
if match:
    src = src[:match.start()] + NEW_BLOCK + '\n'
    with open(TARGET, 'w', encoding='utf-8') as f:
        f.write(src)
    print(f"SUCCESS: Patched {TARGET}")
    print(f"  Old block was {match.end()-match.start()} chars")
    print(f"  New block is  {len(NEW_BLOCK)} chars")
else:
    print("FAIL: Pattern 'def classify_ai_level ... return results' not found")
    # Debug: show what we found
    m2 = re.search(r'def classify_ai_level', src)
    if m2:
        print(f"  classify_ai_level found at char {m2.start()}")
        print(f"  Context: {repr(src[m2.start():m2.start()+100])}")
    m3 = re.search(r'def detect_ai_sentences', src)
    if m3:
        print(f"  detect_ai_sentences found at char {m3.start()}")
    sys.exit(1)
