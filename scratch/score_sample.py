"""
score_sample.py
---------------
Scores sample_resume.txt through the updated ai_detector and prints a
full breakdown so we can confirm human resumes land below 30%.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_detector import detect_ai_content, is_resume_style

resume_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_resume.txt")

with open(resume_path, encoding="utf-8") as f:
    text = f.read()

print("=" * 60)
print("  SCORING: sample_resume.txt")
print("=" * 60)
print(f"  Characters : {len(text)}")
print(f"  Lines      : {text.count(chr(10))}")
print(f"  Is resume  : {is_resume_style(text)}")
print()

score, details = detect_ai_content(text)

print(f"  AI Score       : {score:.1f}%")
print(f"  Classification : {details.get('classification', 'N/A')}")
print(f"  Model used     : {details.get('model_used', 'N/A')}")
print(f"  Sentence count : {details.get('sentence_count', 'N/A')}")
print(f"  Raw AI score   : {details.get('raw_ai_score', 'N/A')}")
print()

hs = details.get("heuristic_signals", {})
if hs:
    print("  Signal breakdown:")
    for k, v in hs.items():
        print(f"    {k}: {v}")
    print()

sb = details.get("signal_breakdown", {})
if sb:
    print("  Signal breakdown (weighted):")
    for k, v in sb.items():
        print(f"    {k}: {v}")
    print()

print("-" * 60)
if score < 30:
    print(f"  PASS  - {score:.1f}% is below the 30% human threshold")
elif score < 60:
    print(f"  WARN  - {score:.1f}% lands in Mixed zone (30-60%)")
else:
    print(f"  FAIL  - {score:.1f}% is still above 60% on a human resume")
print("=" * 60)
