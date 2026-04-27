import urllib.request, json

payload = json.dumps({
    "resume": (
        "John Smith | john.smith@email.com\n\n"
        "SUMMARY\n"
        "I am a results-driven software engineer with extensive expertise in leveraging cutting-edge technologies.\n"
        "Furthermore, I consistently optimized performance metrics, achieving remarkable improvements across all KPIs.\n"
        "Moreover, I collaborated seamlessly with cross-functional teams to drive synergistic outcomes and holistic growth.\n\n"
        "SKILLS\nPython, Java, SQL, React, Docker, AWS\n\n"
        "EXPERIENCE\nSenior Software Engineer | TechCorp | 2021-Present\n"
        "- Led development of microservices using Python and Docker.\n"
        "Consequently, I delivered exceptional value by meticulously aligning technical solutions with strategic business objectives.\n"
        "I proactively spearheaded enterprise-grade infrastructure holistically transforming the engineering culture.\n"
    ),
    "job_description": (
        "Senior Software Engineer with 3+ years Python, Docker, AWS. "
        "Microservices, REST APIs, team leadership required."
    )
}).encode()

req = urllib.request.Request(
    "http://localhost:5000/api/screen",
    data=payload,
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req, timeout=60) as resp:
    data = json.loads(resp.read())

sa = data.get("sentence_analysis", [])
print(f"sentence_analysis: {len(sa)} sentences")
for s in sa:
    print(f"  [{s['label']:9}] {s['score']:5.1f}%  {s['text'][:55]}")

from collections import Counter
counts = Counter(s['label'] for s in sa)
print(f"\nLabel counts: {dict(counts)}")
print(f"Overall ai_score: {data.get('ai_score', 0):.1f}%")
print(f"Decision: {data.get('decision')}")
print("SUCCESS: sentence_analysis working" if sa else "FAIL: no sentence data")
