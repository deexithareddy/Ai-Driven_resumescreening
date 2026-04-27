"""Repair script for corrupted ai_detector.py."""
import os

FILEPATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ai_detector.py")

content = open(FILEPATH, "r", encoding="utf-8").read()

# Find corruption point: the broken Signal 3 line
CORRUPTION_MARKER = "        # -- Signal 3: Formal transition starters --\n        ai_on# ==="
idx = content.find(CORRUPTION_MARKER)
if idx == -1:
    print("ERROR: Corruption marker not found. File may already be fixed.")
    exit(1)

print(f"Corruption found at index {idx}")

good_prefix = content[:idx]

new_suffix = r"""        # -- Signal 3: Formal transition starters --
        ai_only_starters = [
            "furthermore", "moreover", "consequently",
            "in conclusion", "accordingly", "subsequently",
        ]
        for starter in ai_only_starters:
            if sent_lower.strip().startswith(starter):
                score += 4.0
                flags.append(f"Indicators suggest AI-typical sentence opener ('{starter}')")
                break

        # -- Signal 4: Adverb clustering --
        ai_adverbs = [
            "diligently", "meticulously", "seamlessly", "flawlessly",
            "proactively", "comprehensively", "holistically",
        ]
        adverb_matches = [a for a in ai_adverbs if a in sent_lower]
        if len(adverb_matches) >= 2:
            score += 8.0
            flags.append(
                "Indicators suggest AI-style phrasing: multiple formal adverbs detected "
                f"({', '.join(adverb_matches[:3])})"
            )
        elif len(adverb_matches) == 1:
            score += 2.0
            flags.append(f"Patterns observed: formal adverb usage ('{adverb_matches[0]}')")

        # -- Signal 5: Word length uniformity --
        if word_count >= 10:
            word_lens = [len(w) for w in words]
            try:
                wl_cv = statistics.stdev(word_lens) / statistics.mean(word_lens) if statistics.mean(word_lens) > 0 else 0
                if wl_cv < 0.22:
                    score += 4.0
                    flags.append(f"Patterns observed: unusually consistent word lengths (CV={wl_cv:.2f})")
            except statistics.StatisticsError:
                pass

        # -- Signal 6: Generic quantified impact claims --
        impact_patterns = [
            r"improved .{1,30} by \d",
            r"increased .{1,30} by \d",
            r"reduced .{1,30} by \d",
            r"resulting in .{1,20}\d+%",
        ]
        impact_matches = sum(1 for p in impact_patterns if re.search(p, sent_lower))
        if impact_matches >= 2:
            score += 5.0
            flags.append("Patterns observed: multiple templated impact claims in a single statement")

        # Finalize Score
        score = round(min(100.0, max(0.0, score)), 1)

        if score >= 25:
            label = "High"
        elif score >= 8:
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


# ==============================================================================
#  SENTENCE-LEVEL ANALYSIS  (public API helper)  v3.3
#
#  Uses detect_ai_sections() heuristic scores + per-sentence phrase matching.
#  When the ML model is loaded, a per-sentence ML probability is blended in.
#
#  Label thresholds (v3.3 - lowered for visible highlighting):
#      display score >= 35  -> "ai"         (RED)
#      display score >= 15  -> "uncertain"  (ORANGE)
#      display score <  15  -> "human"      (GREEN)
# ==============================================================================

_AI_PHRASE_PATTERNS = [
    r'\b(leveraged|spearheaded|championed|orchestrated|architected)\b',
    r'\b(synergized|streamlined|optimized|revolutionized|transformed)\b',
    r'\b(cutting[- ]edge|state[- ]of[- ]the[- ]art|best[- ]in[- ]class)\b',
    r'\b(proactive|strategic|innovative|dynamic|impactful)\b',
    r'\b(cross[- ]functional|stakeholder[- ]driven|data[- ]driven)\b',
    r'\b(passionate about|committed to|dedicated to|focused on)\b',
    r'\b(proven track record|demonstrated ability|strong foundation)\b',
    r'\b(collaborated (with|closely)|worked closely|partnered with)\b',
    r'\b(key (stakeholders|metrics|deliverables|milestones))\b',
    r'\b(end[- ]to[- ]end|full[- ]lifecycle|360[- ]degree)\b',
]


def _per_sentence_phrase_score(sentence: str) -> float:
    """Score a sentence for AI-typical buzzwords/phrases (0-100)."""
    s_lower = sentence.lower()
    hits = sum(1 for p in _AI_PHRASE_PATTERNS if re.search(p, s_lower))
    if hits >= 3:
        return 80.0
    elif hits == 2:
        return 55.0
    elif hits == 1:
        return 30.0
    return 0.0


def analyze_sentences(text: str) -> list:
    """
    Return sentence-level AI likelihood data for frontend colour highlighting.

    Each dict:
        {
            "text":        str,   -- sentence text
            "score":       float, -- AI likelihood 0-100 (display)
            "label":       str,   -- "ai" | "uncertain" | "human"
            "is_excluded": bool,  -- True for headers/bullets
        }

    v3.3 -- Lowered thresholds + phrase scoring + optional ML blending.
    """
    if not text or not text.strip():
        return []

    print(f"[analyze_sentences] Starting analysis on {len(text)} chars")

    sections = detect_ai_sections(text)
    print(f"[analyze_sentences] detect_ai_sections returned {len(sections)} entries")

    if not sections:
        print("[analyze_sentences] WARNING: No sections returned")
        return []

    results      = []
    ml_available = _load_ml_model()

    for s in sections:
        sentence_text = s.get("sentence", "").strip()
        if not sentence_text:
            continue

        raw_heuristic = float(s.get("score", 0.0))
        is_excluded   = bool(s.get("is_excluded", False))

        if is_excluded:
            results.append({
                "text":        sentence_text,
                "score":       0.0,
                "label":       "human",
                "is_excluded": True,
            })
            continue

        heuristic_component = min(100.0, raw_heuristic * 3.5)
        phrase_component    = _per_sentence_phrase_score(sentence_text)

        words = sentence_text.split()
        if ml_available and len(words) >= 8:
            try:
                ml_component = _predict_ml(sentence_text) * 100.0
            except Exception:
                ml_component = 0.0
            display_score = (
                0.40 * heuristic_component +
                0.35 * phrase_component +
                0.25 * ml_component
            )
        else:
            ml_component  = 0.0
            display_score = (
                0.55 * heuristic_component +
                0.45 * phrase_component
            )

        display_score = round(min(100.0, max(0.0, display_score)), 1)

        if display_score >= 35:
            label = "ai"
        elif display_score >= 15:
            label = "uncertain"
        else:
            label = "human"

        results.append({
            "text":        sentence_text,
            "score":       display_score,
            "label":       label,
            "is_excluded": False,
        })

    ai_c  = sum(1 for r in results if r["label"] == "ai")
    unc_c = sum(1 for r in results if r["label"] == "uncertain")
    hum_c = sum(1 for r in results if r["label"] == "human")
    print(f"[analyze_sentences] {len(results)} sentences | ai={ai_c} uncertain={unc_c} human={hum_c}")

    return results
"""

new_content = good_prefix + new_suffix
open(FILEPATH, "w", encoding="utf-8").write(new_content)
lines = new_content.count("\n")
print(f"SUCCESS: File written. Total lines: {lines}")
