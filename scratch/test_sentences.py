import requests, json

payload = {
    "resume": (
        "John Smith\njohn@email.com\n\nSUMMARY\n"
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
    "job_description": "We need a software engineer with Python and React skills who is innovative and proactive."
}

r = requests.post("http://localhost:5000/api/screen", json=payload, timeout=60)
data = r.json()
sa = data.get("sentence_analysis", [])

print(f"Status: {r.status_code}")
print(f"sentence_analysis count: {len(sa)}")
ai_c   = sum(1 for s in sa if s["label"] == "ai")
unc_c  = sum(1 for s in sa if s["label"] == "uncertain")
hum_c  = sum(1 for s in sa if s["label"] == "human")
print(f"Labels: ai={ai_c}  uncertain={unc_c}  human={hum_c}")
print()
for s in sa:
    lbl = s["label"].upper()
    scr = s["score"]
    txt = s["text"][:80]
    print(f"  [{lbl:9s}] {scr:5.1f}%  {txt}")
