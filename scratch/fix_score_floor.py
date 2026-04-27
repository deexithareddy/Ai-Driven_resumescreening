"""
fix_score_floor.py
------------------
Removes the hard 8% floor from _smooth_score() so truly human
resumes can score 0%. Also bypasses sigmoid distortion for raw
scores below 5 so they don't get bumped up artificially.
"""
import pathlib, shutil

target = pathlib.Path("ai_detector.py")
shutil.copy(target, target.with_suffix(".py.bak3"))

src = target.read_text(encoding="utf-8")

OLD = '''def _smooth_score(raw: float) -> float:
    """
    Apply advanced sigmoid smoothing to avoid extreme outputs.

    v3.2 improvements:
      - Gentler sigmoid (divisor=18 vs 15) to reduce sudden spikes
      - Exponential moving average (EMA) blend with raw score
        to prevent small input changes from causing large output jumps
      - Tighter clamp [8, 92] -- realistic range for probabilistic detection
    """
    # 1. Sigmoid mapping (gentler slope)
    x = (raw - 50) / 18.0  # v3.2: wider divisor = smoother transitions
    sigmoid = 1.0 / (1.0 + math.exp(-x))
    sigmoid_score = sigmoid * 100.0

    # 2. EMA-style blending: 70% sigmoid + 30% raw
    # This adds inertia -- the score doesn't jump wildly from
    # small differences in input features
    blended = 0.70 * sigmoid_score + 0.30 * raw

    # 3. Tighter clamping -- no resume should score below 8 or above 92
    return round(max(8.0, min(92.0, blended)), 2)'''

NEW = '''def _smooth_score(raw: float) -> float:
    """
    Apply sigmoid smoothing to avoid extreme outputs.

    v3.3 changes:
      - Floor removed: scores can now reach 0% for clearly human content
      - Raw scores < 5 are returned as-is (no sigmoid distortion)
      - Clamp is now [0, 95] instead of [8, 92]
    """
    # Pass-through for very low raw scores: avoid sigmoid bumping them up
    if raw <= 0:
        return 0.0
    if raw < 5:
        return round(raw, 2)

    # 1. Sigmoid mapping (gentler slope)
    x = (raw - 50) / 18.0
    sigmoid = 1.0 / (1.0 + math.exp(-x))
    sigmoid_score = sigmoid * 100.0

    # 2. EMA-style blending: 70% sigmoid + 30% raw
    blended = 0.70 * sigmoid_score + 0.30 * raw

    # 3. Clamp [0, 95] -- floor removed so human resumes can score 0%
    return round(max(0.0, min(95.0, blended)), 2)'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("[OK] Replaced _smooth_score (CRLF not needed)")
else:
    OLD_CRLF = OLD.replace('\n', '\r\n')
    NEW_CRLF = NEW.replace('\n', '\r\n')
    if OLD_CRLF in src:
        src = src.replace(OLD_CRLF, NEW_CRLF, 1)
        print("[OK] Replaced _smooth_score (CRLF)")
    else:
        print("[FAIL] Could not find _smooth_score block to replace")
        exit(1)

target.write_text(src, encoding="utf-8")

import py_compile
try:
    py_compile.compile(str(target), doraise=True)
    print("Syntax check: PASSED")
except py_compile.PyCompileError as e:
    print(f"Syntax check: FAILED - {e}")
    exit(1)

# Quick test
import sys, os
sys.path.insert(0, str(target.parent))

# Force reload
if 'ai_detector' in sys.modules:
    del sys.modules['ai_detector']

from ai_detector import _smooth_score
print(f"  _smooth_score(0)   = {_smooth_score(0)}")
print(f"  _smooth_score(2)   = {_smooth_score(2)}")
print(f"  _smooth_score(10)  = {_smooth_score(10)}")
print(f"  _smooth_score(50)  = {_smooth_score(50)}")
print(f"  _smooth_score(90)  = {_smooth_score(90)}")
print("Done.")
