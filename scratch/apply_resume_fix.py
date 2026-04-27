"""
apply_resume_fix.py
-------------------
Patches ai_detector.py with the resume-mode calibration fixes:
  FIX 2  - 50% score dampening when resume-style layout detected
  FIX 5  - -10 pt human writing bonus for numbers / specific tools
  FIX 6  - New classification thresholds: <30 Human, 30-60 Mixed, 60+ AI
"""
import re
import pathlib
import shutil

TARGET = pathlib.Path("ai_detector.py")
assert TARGET.exists(), f"Cannot find {TARGET}"

# Back up the original
shutil.copy(TARGET, TARGET.with_suffix(".py.bak"))
print("[*] Backup saved to ai_detector.py.bak")

src = TARGET.read_text(encoding="utf-8")

# ─────────────────────────────────────────────────────────────────────────────
#  LOCATE the section we want to replace
#  Start:  the line "        # Heuristic-only fallback"
#  End:    the line "    feature_values = extract_features_dict(text)"
# ─────────────────────────────────────────────────────────────────────────────
ANCHOR_START = '        # Heuristic-only fallback\n        raw_score = heuristic_score\n        model_used = "heuristic-only"'
ANCHOR_END   = '    feature_values = extract_features_dict(text)'

idx_start = src.find(ANCHOR_START)
if idx_start == -1:
    # Try Windows line endings
    ANCHOR_START = ANCHOR_START.replace('\n', '\r\n')
    idx_start = src.find(ANCHOR_START)

assert idx_start != -1, "Could not locate ANCHOR_START in ai_detector.py"

idx_end = src.find(ANCHOR_END, idx_start)
assert idx_end != -1, "Could not locate ANCHOR_END in ai_detector.py"

print(f"[*] Found replacement region: bytes {idx_start}-{idx_end}")

# ─────────────────────────────────────────────────────────────────────────────
#  Replacement block  (everything between ANCHOR_START and ANCHOR_END)
# ─────────────────────────────────────────────────────────────────────────────
# Detect line ending style used in the file
lf = '\r\n' if '\r\n' in src else '\n'

NEW_MIDDLE = lf.join([
    '        # Heuristic-only fallback',
    '        raw_score = heuristic_score',
    '        model_used = "heuristic-only"',
    '',
    '    # -- FIX 2: Resume-mode dampening ----------------------------------------',
    '    # When the document is resume-style (bullets / short lines), the',
    '    # statistical signals are unreliable for flowing-prose AI detection.',
    '    # Halve the raw score so structural formatting does not inflate AI %.',
    '    if is_resume_style(text):',
    '        logger.info("Resume-style layout detected - applying 50%% score dampening.")',
    '        raw_score *= 0.5',
    '',
    '    # -- FIX 5: Human-writing bonus ------------------------------------------',
    '    # Concrete numbers (e.g. "30+", "50%") and specific tool names are strong',
    '    # signals of genuine human experience.  Deduct 10 points from raw score.',
    '    _SPECIFIC_TOOLS = [',
    '        "splunk", "python", "java", "javascript", "typescript", "react",',
    '        "angular", "vue", "node", "django", "flask", "fastapi", "spring",',
    '        "kubernetes", "docker", "terraform", "ansible", "jenkins", "git",',
    '        "aws", "azure", "gcp", "postgresql", "mysql", "mongodb", "redis",',
    '        "elasticsearch", "kafka", "spark", "hadoop", "tableau", "powerbi",',
    '        "excel", "figma", "jira", "confluence", "linux", "bash", "powershell",',
    '    ]',
    '    text_lower_bonus = text.lower()',
    r'    has_numbers = bool(re.search(r"\d+[+%]|\d{2,}", text))',
    '    has_specific_tools = any(tool in text_lower_bonus for tool in _SPECIFIC_TOOLS)',
    '    if has_numbers or has_specific_tools:',
    '        raw_score = max(0.0, raw_score - 10.0)',
    '        logger.info(',
    '            "Human writing bonus applied (-10 pts): "',
    '            f"numbers={has_numbers}, tools={has_specific_tools}"',
    '        )',
    '',
    '    # -- Smoothing ------------------------------------------------------------',
    '    ai_score = _smooth_score(raw_score)',
    '',
    '    # -- FIX 6: Classification (recalibrated for resume context) -------------',
    '    # Human-like / Mixed / AI-like thresholds aligned with expected ranges:',
    '    #   Human resume  ->  10-30 %',
    '    #   Mixed content ->  30-60 %',
    '    #   Clearly AI    ->  60 %+',
    '    if ai_score < 30:',
    '        classification = "Likely Human"',
    '    elif ai_score < 60:',
    '        classification = "Uncertain"',
    '    else:',
    '        classification = "Likely AI"',
    '',
    '    # -- Feature details (for API transparency) --',
    '    ',
])

new_src = src[:idx_start] + NEW_MIDDLE + lf + '    ' + src[idx_end:]
TARGET.write_text(new_src, encoding="utf-8")

print("[✓] Patch applied successfully!")
print(f"    File size: {TARGET.stat().st_size:,} bytes")

# ─────────────────────────────────────────────────────────────────────────────
#  Quick sanity check - confirm all expected identifiers are present
# ─────────────────────────────────────────────────────────────────────────────
checks = [
    "is_resume_style",
    "resume_style layout detected",
    "_SPECIFIC_TOOLS",
    "has_numbers",
    "has_specific_tools",
    'ai_score < 30',
    'ai_score < 60',
    '"Likely Human"',
    '"Uncertain"',
    '"Likely AI"',
]
src_new = TARGET.read_text(encoding="utf-8")
all_ok = True
for c in checks:
    if c not in src_new:
        print(f"  [MISSING] {c!r}")
        all_ok = False
    else:
        print(f"  [OK]      {c!r}")

if all_ok:
    print("\n[✓] All checks passed.")
else:
    print("\n[!] Some checks failed - inspect the file manually.")
