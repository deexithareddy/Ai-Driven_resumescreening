"""Verify the new detect_ai_sentences response format with HIGH/MEDIUM/LOW levels."""
import requests

payload = {
    "resume": (
        "John Smith\njohn@example.com\n\nSUMMARY\n"
        "I am a proactive and innovative software engineer with a proven track record "
        "of leveraging cutting-edge technologies to streamline workflows and deliver "
        "impactful results. I collaborated closely with cross-functional teams to "
        "orchestrate end-to-end solutions.\n\n"
        "EXPERIENCE\nSoftware Engineer at TechCorp (2020-2024)\n"
        "Spearheaded the development of a data-driven analytics platform. "
        "Championed best-in-class coding practices and optimized system performance by 40 percent. "
        "I worked closely with stakeholders to deliver key milestones on time.\n\n"
        "SKILLS\nPython, JavaScript, React, AWS, Docker"
    ),
    "job_description": (
        "We need a proactive software engineer with Python and React skills "
        "who is innovative and data-driven."
    )
}

r = requests.post("http://localhost:5000/api/screen", json=payload, timeout=60)
data = r.json()
sa = data.get("sentence_analysis", [])

print(f"Status        : {r.status_code}")
print(f"Total sentences : {len(sa)}")

# Check new level field exists
has_level = all("level" in s for s in sa) if sa else False
print(f"Has 'level' field: {has_level}")
print()

high_c = sum(1 for s in sa if s.get("level") == "HIGH")
mid_c  = sum(1 for s in sa if s.get("level") == "MEDIUM")
low_c  = sum(1 for s in sa if s.get("level") == "LOW")
print(f"Levels: HIGH={high_c}  MEDIUM={mid_c}  LOW={low_c}")
print()

print("Per-sentence breakdown:")
print("-" * 80)
for s in sa:
    level = s.get("level", "???")
    score = s.get("score", 0)
    label = s.get("label", "?")
    excl  = "[EXCLUDED]" if s.get("is_excluded") else ""
    txt   = s["text"][:70]
    icon  = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(level, "❓")
    print(f"  {icon} [{level:6s}] score={score:5.1f}%  label={label:9s} {excl}")
    print(f"     {txt}")
    print()
