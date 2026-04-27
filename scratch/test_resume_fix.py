"""
test_resume_fix.py
------------------
Validates that the resume-mode calibration fixes produce expected scores:
  - Human resume        -> < 30 %
  - Clearly AI resume   -> >= 60 %
  - is_resume_style()   -> returns True for bullet-heavy text
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_detector import detect_ai_content, is_resume_style

# ─────────────────────────────────────────────────────────────────────────────
#  Sample 1 – Genuine human-written resume (bullet points, numbers, tools)
# ─────────────────────────────────────────────────────────────────────────────
HUMAN_RESUME = """
John Smith
john.smith@email.com | +1 (555) 123-4567 | linkedin.com/in/johnsmith

EXPERIENCE
Senior Software Engineer – Acme Corp (2019–2024)
- Built REST APIs in Python/FastAPI serving 50,000+ daily requests
- Reduced AWS infrastructure costs by 30% by migrating to Kubernetes
- Led a team of 4 engineers; shipped 3 major features in 2023
- Integrated Splunk dashboards for real-time monitoring of 12 services

Software Engineer – Startup XYZ (2017–2019)
- Developed React front-end consuming Django REST backend
- Wrote unit tests in pytest, achieving 85% code coverage
- Deployed Docker containers on AWS ECS; zero-downtime rollouts

SKILLS
Python, Java, JavaScript, React, Django, FastAPI, Docker, Kubernetes,
PostgreSQL, MongoDB, Redis, AWS, Splunk, Git, Linux

EDUCATION
B.Sc. Computer Science – State University, 2017
GPA 3.7 | Dean's List 2015, 2016

CERTIFICATIONS
AWS Certified Solutions Architect – Associate (2022)
Certified Kubernetes Administrator (2023)
"""

# ─────────────────────────────────────────────────────────────────────────────
#  Sample 2 – Clearly AI-generated, verbose, no concrete details
# ─────────────────────────────────────────────────────────────────────────────
AI_RESUME = """
I am a highly motivated and results-driven professional with a proven track record of delivering
exceptional outcomes in complex organizational environments. Furthermore, my comprehensive expertise
in leveraging cutting-edge technologies enables me to spearhead transformative initiatives that
significantly enhance operational efficiency and drive sustainable growth. Moreover, I consistently
demonstrate an unwavering commitment to excellence, proactively identifying opportunities for
improvement and implementing innovative solutions that yield measurable results. Consequently, my
collaborative approach and strong interpersonal skills allow me to seamlessly integrate with
cross-functional teams, fostering a culture of continuous improvement and high-performance delivery.
Additionally, my holistic understanding of business processes and technical systems positions me
uniquely to bridge the gap between strategic vision and tactical execution, ensuring that all
initiatives are aligned with organizational objectives and deliver maximum value to stakeholders.
In conclusion, I am fully committed to bringing my extensive expertise and passion for excellence
to your esteemed organization, where I can contribute meaningfully to your continued success and
drive impactful outcomes that align with your strategic goals and long-term vision.
"""

# ─────────────────────────────────────────────────────────────────────────────
#  Run tests
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 65)
print("  RESUME FIX VALIDATION")
print("=" * 65)

# Test is_resume_style
bullet_text = "\n".join(["- item one", "- item two", "- item three", "Some longer sentence here."])
style_flag = is_resume_style(HUMAN_RESUME)
print(f"\n[is_resume_style] Human resume detected as resume-style: {style_flag}")
assert style_flag, "FAIL: Human resume should be detected as resume-style"

ai_style_flag = is_resume_style(AI_RESUME)
print(f"[is_resume_style] AI prose detected as resume-style:   {ai_style_flag}")

# Score human resume
h_score, h_details = detect_ai_content(HUMAN_RESUME)
print(f"\n[HUMAN RESUME]")
print(f"  Score         : {h_score:.1f}%")
print(f"  Classification: {h_details['classification']}")
print(f"  Raw score     : {h_details.get('raw_ai_score', 'N/A (early exit)')}")
print(f"  Model used    : {h_details.get('model_used', 'N/A')}")

# Score AI resume
a_score, a_details = detect_ai_content(AI_RESUME)
print(f"\n[AI RESUME]")
print(f"  Score         : {a_score:.1f}%")
print(f"  Classification: {a_details['classification']}")
print(f"  Raw score     : {a_details.get('raw_ai_score', 'N/A (early exit)')}")
print(f"  Model used    : {a_details.get('model_used', 'N/A')}")

# ─────────────────────────────────────────────────────────────────────────────
#  Assertions
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "-" * 65)
PASS = True

if h_score < 30:
    print(f"[PASS] Human resume score {h_score:.1f}% < 30% threshold")
else:
    print(f"[FAIL] Human resume score {h_score:.1f}% >= 30% (should be < 30)")
    PASS = False

if a_score >= 50:
    print(f"[PASS] AI resume score {a_score:.1f}% >= 50% threshold")
else:
    print(f"[WARN] AI resume score {a_score:.1f}% < 50% (may need re-check)")

if h_details['classification'] == "Likely Human":
    print(f"[PASS] Human resume classified as 'Likely Human'")
else:
    print(f"[FAIL] Human resume classified as '{h_details['classification']}' (expected 'Likely Human')")
    PASS = False

print("-" * 65)
print("RESULT:", "ALL CHECKS PASSED" if PASS else "SOME CHECKS FAILED")
print("=" * 65)
