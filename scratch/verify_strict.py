"""
verify_strict.py
----------------
End-to-end verification that the new STRICT detect_ai_sentences rules work:
  1. AI-heavy resume → always returns >= 1 sentence
  2. Personal data (email/phone/name) never appears in highlighted sentences
  3. Low-AI resume → sentences still returned if doc score > 0
  4. 0% AI doc → empty list returned
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_detector import detect_ai_sentences, detect_ai_content, clean_resume_text

PASS = []
FAIL = []

def check(label, cond):
    if cond:
        PASS.append(label)
        print(f"  [OK]   {label}")
    else:
        FAIL.append(label)
        print(f"  [FAIL] {label}")

# ─────────────────────────────────────────────────
# SAMPLE 1: AI-heavy resume
# ─────────────────────────────────────────────────
AI_RESUME = """John Smith
john.smith@email.com | +1-555-0123

Leveraging cutting-edge technologies, I have spearheaded transformative initiatives
that delivered measurable business impact across cross-functional teams.
My proven track record demonstrates expertise in streamlining end-to-end workflows
and optimizing stakeholder-driven outcomes.

I collaborated closely with key stakeholders to implement data-driven solutions
that increased efficiency by 40 percent and reduced operational costs by 25 percent.
Furthermore, I championed agile methodologies to ensure seamless delivery of
high-priority projects.
"""

print("=== Test 1: AI-heavy resume ===")
doc_score, _ = detect_ai_content(AI_RESUME)
print(f"  Doc AI score: {doc_score:.1f}%")
results = detect_ai_sentences(AI_RESUME)
print(f"  Sentences returned: {len(results)}")
for r in results:
    print(f"    [{r['level']}] score={r['score']} | {r['text'][:75]}")

check("AI resume: doc score > 0", doc_score > 0)
check("AI resume: at least 1 sentence highlighted", len(results) >= 1)

# Personal data exclusion check
personal_leak = False
for r in results:
    t = r['text'].lower()
    if 'john.smith@email.com' in t or '+1-555-0123' in t or 'john smith' == t.strip():
        personal_leak = True
check("AI resume: personal data NOT in highlighted sentences", not personal_leak)

# Level check — should be HIGH or MEDIUM only
bad_level = any(r['level'] == 'LOW' for r in results)
check("AI resume: no LOW-level sentences returned", not bad_level)

print()

# ─────────────────────────────────────────────────
# SAMPLE 2: Low-AI / borderline resume (1–20%)
# ─────────────────────────────────────────────────
MEDIUM_RESUME = """Alex Chen
alex.chen@example.com

I built several web applications using React and Python during my three years
at TechCorp. I wrote RESTful APIs and worked with PostgreSQL databases.
I enjoy collaborating with product teams and have strong communication skills.
I am proficient in agile development practices.
"""

print("=== Test 2: Low-AI resume ===")
doc_score2, _ = detect_ai_content(MEDIUM_RESUME)
print(f"  Doc AI score: {doc_score2:.1f}%")
results2 = detect_ai_sentences(MEDIUM_RESUME)
print(f"  Sentences returned: {len(results2)}")
for r in results2:
    print(f"    [{r['level']}] score={r['score']} | {r['text'][:75]}")

if doc_score2 > 0:
    check("Low-AI resume: doc score > 0 yields >= 1 highlighted sentence", len(results2) >= 1)
else:
    check("Low-AI resume: doc score == 0, empty list returned", len(results2) == 0)

print()

# ─────────────────────────────────────────────────
# SAMPLE 3: clean_resume_text strips personal data
# ─────────────────────────────────────────────────
print("=== Test 3: clean_resume_text() ===")
RAW = "Jane Doe\njane.doe@gmail.com | +44 7700 900123\nhttps://linkedin.com/in/janedoe\nI built scalable microservices at Google."
cleaned = clean_resume_text(RAW)
print(f"  Cleaned: {repr(cleaned[:120])}")
check("clean_resume_text: removes email", 'jane.doe@gmail.com' not in cleaned)
check("clean_resume_text: removes URL", 'linkedin.com' not in cleaned)
check("clean_resume_text: drops first 2 lines (name/header)", 'Jane Doe' not in cleaned)
check("clean_resume_text: keeps content sentence", 'microservices' in cleaned or 'built' in cleaned)

print()

# ─────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────
print("=" * 50)
print(f"Results: {len(PASS)} passed / {len(FAIL)} failed")
if FAIL:
    print("FAILED checks:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("ALL CHECKS PASSED")
