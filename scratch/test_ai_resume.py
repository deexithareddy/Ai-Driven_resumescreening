"""Test detect_ai_sentences with a strongly AI-written resume to verify HIGH/MEDIUM triggering."""
import requests

payload = {
    "resume": (
        "Alexandra Chen\nalexandra.chen@email.com | linkedin.com/in/alexchen\n\n"
        "PROFESSIONAL SUMMARY\n"
        "A highly motivated and results-driven software engineer with a proven track record "
        "of leveraging cutting-edge technologies to spearhead innovative solutions. "
        "I am passionate about orchestrating cross-functional collaboration and championing "
        "data-driven decision making to transform business outcomes. "
        "My demonstrated ability to streamline end-to-end workflows has consistently delivered "
        "impactful results and optimized operational efficiency across all stakeholder engagements.\n\n"
        "EXPERIENCE\n"
        "Senior Software Engineer | TechVision Corp (2021-2024)\n"
        "Spearheaded the development of a state-of-the-art analytics platform, "
        "proactively collaborating with key stakeholders to deliver strategic milestones. "
        "Architected scalable microservices infrastructure, revolutionizing system performance "
        "and achieving best-in-class reliability metrics. "
        "Leveraged data-driven insights to optimize resource allocation, "
        "resulting in a 40 percent improvement in operational efficiency. "
        "Championed best practices in software development, "
        "fostering a culture of innovation and continuous improvement.\n\n"
        "SKILLS\n"
        "Python, JavaScript, React, AWS, Docker, Kubernetes, TensorFlow"
    ),
    "job_description": (
        "We need a proactive senior software engineer with strong Python skills "
        "who can drive innovation and work with cross-functional teams."
    )
}

r = requests.post("http://localhost:5000/api/screen", json=payload, timeout=60)
data = r.json()
sa = data.get("sentence_analysis", [])

print(f"Status: {r.status_code} | AI Score: {data.get('ai_score', '?')}%")
print(f"Sentences: {len(sa)}")

has_level = all("level" in s for s in sa) if sa else False
print(f"Has 'level' field: {has_level}\n")

high_c = sum(1 for s in sa if s.get("level") == "HIGH")
mid_c  = sum(1 for s in sa if s.get("level") == "MEDIUM")
low_c  = sum(1 for s in sa if s.get("level") == "LOW")
print(f"=== LEVELS: HIGH={high_c}  MEDIUM={mid_c}  LOW={low_c} ===\n")

for s in sa:
    level = s.get("level", "???")
    score = s.get("score", 0)
    excl  = " [EXCLUDED]" if s.get("is_excluded") else ""
    txt   = s["text"][:80]
    marker = ">>" if level in ("HIGH", "MEDIUM") else "  "
    print(f"{marker} [{level:6s}] {score:5.1f}%{excl}")
    print(f"   {txt}")
    print()
