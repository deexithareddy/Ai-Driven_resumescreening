import requests, json

r = requests.post("http://localhost:5000/api/screen", json={
    "resume": "John Doe Software Engineer. I leveraged cutting-edge technologies to spearhead innovative projects. Experience with Python and React. Built scalable web applications using AWS cloud infrastructure.",
    "job_description": "Looking for a Software Engineer with Python and React experience."
})
d = r.json()
print("SUCCESS:", d.get("success"))
secs = d.get("ai_sections", [])
print(f"AI_SECTIONS: {len(secs)} sentences")
for s in secs:
    print(f"  [{s['label']}] {s['score']}% -> {s['sentence'][:80]}")
