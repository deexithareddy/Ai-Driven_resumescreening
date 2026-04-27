"""Score the human_resume_sample.txt"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_detector import detect_ai_content, is_resume_style

path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "human_resume_sample.txt")
with open(path, encoding="utf-8") as f:
    text = f.read()

print("=" * 55)
print("  HUMAN RESUME SAMPLE SCORING")
print("=" * 55)
print(f"  Is resume style : {is_resume_style(text)}")

score, details = detect_ai_content(text)
print(f"  AI Score        : {score:.1f}%")
print(f"  Classification  : {details.get('classification','N/A')}")
print(f"  Model used      : {details.get('model_used','N/A')}")
print(f"  Raw AI score    : {details.get('raw_ai_score','N/A')}")

hs = details.get("heuristic_signals", {})
if hs:
    print()
    for k, v in hs.items():
        print(f"    {k}: {v}")

print()
if score < 30:
    print(f"  PASS - {score:.1f}% is within the expected human range")
else:
    print(f"  FAIL - {score:.1f}% is too high for a human resume")
print("=" * 55)
