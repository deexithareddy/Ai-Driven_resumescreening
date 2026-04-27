"""
fix_scoring_pipeline.py
-----------------------
Redesigns the scoring pipeline so that:
1. Heuristic is dampened (not the full raw_score) for resume-style layouts
   - This preserves the ML signal that correctly detects AI writing
2. Force-to-zero (FIX 7) is REMOVED
   - It was zeroing out AI-enhanced resumes that have bullets + tool names
3. Human bonus is numbers-only (-5 pts, not -10)
   - Tool names exist in both human and AI resumes, so not a valid signal
"""
import pathlib, shutil

target = pathlib.Path("ai_detector.py")
shutil.copy(target, target.with_suffix(".py.bak4"))
src = target.read_text(encoding="utf-8")

# ── Find the block to replace ────────────────────────────────────────────────
# We'll use unique anchors that appear exactly once in the file.

START_ANCHOR = '    heuristic_score, heuristic_details = _compute_heuristic_score(text, sentences)'
END_ANCHOR   = '    # -- FIX 6: Classification (recalibrated for resume context)'

idx_s = src.find(START_ANCHOR)
idx_e = src.find(END_ANCHOR, idx_s)

assert idx_s != -1, "START_ANCHOR not found"
assert idx_e != -1, "END_ANCHOR not found"

print(f"Replacing bytes {idx_s}–{idx_e}")

# ── Replacement block ────────────────────────────────────────────────────────
lf = '\r\n' if '\r\n' in src else '\n'

NEW_BLOCK = lf.join([
    '    heuristic_score_raw, heuristic_details = _compute_heuristic_score(text, sentences)',
    '',
    '    # -- Resume-mode: dampen ONLY the heuristic, keep ML score intact --------',
    '    # Bullet points / short lines inflate heuristic signals but are normal in',
    '    # human resumes. We dampen only the heuristic so the ML model can still',
    '    # correctly flag AI-enhanced resumes that happen to use bullet formatting.',
    '    if is_resume_style(original_text):',
    '        logger.info("Resume-style layout detected - dampening heuristic by 30%%.")',
    '        heuristic_score = heuristic_score_raw * 0.30',
    '    else:',
    '        heuristic_score = heuristic_score_raw',
    '',
    '    # -- Hybrid Combination --------------------------------------------------',
    '    model_available = _ml_loaded is True',
    '',
    '    if model_available:',
    '        # 70% ML + 30% dampened heuristic',
    '        raw_score = 0.70 * ml_score + 0.30 * heuristic_score',
    '        model_used = "hybrid"',
    '    else:',
    '        raw_score = heuristic_score',
    '        model_used = "heuristic-only"',
    '',
    '    # -- Human-writing bonus (numbers only, -5 pts) --------------------------',
    '    # Concrete metrics like "30+", "50%", "2.1s" are signals of genuine human',
    '    # experience that AI tends to genericise. We do NOT bonus for tool names',
    '    # because both human and AI resumes mention the same tools (Python, AWS...).',
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
    '    if has_numbers:',
    '        raw_score = max(0.0, raw_score - 5.0)',
    '        logger.info(f"Human writing bonus applied (-5 pts): numbers present")',
    '',
    '    # -- Smoothing -----------------------------------------------------------',
    '    ai_score = _smooth_score(raw_score)',
    '',
    '    # NOTE: Force-to-zero removed -- it was incorrectly zeroing AI-enhanced',
    '    # resumes that also happen to have bullet points and tool names.',
    '',
])

new_src = src[:idx_s] + NEW_BLOCK + lf + '    ' + src[idx_e:]
target.write_text(new_src, encoding="utf-8")
print(f"Written: {target.stat().st_size:,} bytes")

# Syntax check
import py_compile
try:
    py_compile.compile(str(target), doraise=True)
    print("Syntax check: PASSED")
except py_compile.PyCompileError as e:
    print(f"Syntax check: FAILED - {e}")
    exit(1)

# Verify old patterns removed
src2 = target.read_text(encoding="utf-8")
checks = {
    "force-to-zero REMOVED":        "Force-to-zero" not in src2,
    "50% dampening REMOVED":        "raw_score *= 0.5" not in src2,
    "heuristic dampened":           "heuristic_score_raw * 0.30" in src2,
    "ML preserved in hybrid":       "0.70 * ml_score" in src2,
    "numbers-only bonus":           "has_numbers:" in src2,
    "no tool-name bonus":           'has_numbers or has_specific_tools' not in src2,
}
all_ok = True
for name, result in checks.items():
    status = "OK" if result else "FAIL"
    if not result: all_ok = False
    print(f"  [{status}] {name}")

print("All checks passed!" if all_ok else "SOME CHECKS FAILED")
