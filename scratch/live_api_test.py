import urllib.request, json

payload = json.dumps({
    'resume': (
        'Leveraging cutting-edge technologies, I have spearheaded transformative initiatives '
        'that delivered measurable business impact across cross-functional teams. '
        'My proven track record demonstrates expertise in streamlining end-to-end workflows '
        'and optimizing stakeholder-driven outcomes. '
        'I collaborated closely with key stakeholders to implement data-driven solutions.'
    ),
    'job_description': 'We need a Python developer with experience in machine learning and REST APIs.'
}).encode()

req = urllib.request.Request(
    'http://localhost:5000/api/screen',
    data=payload,
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read())

    sa = data.get('sentence_analysis', [])
    ai = data.get('ai_score', 0)

    print(f"AI score:          {ai}%")
    print(f"Sentences returned: {len(sa)}")
    for s in sa:
        lvl   = s.get('level', '?')
        score = s.get('score', 0)
        text  = s.get('text', '')[:65]
        print(f"  [{lvl}] score={score} | {text}")

    print()
    if ai > 0 and len(sa) == 0:
        print("FAIL: AI score > 0 but sentence_analysis is empty!")
    elif ai > 0 and len(sa) >= 1:
        print("PASS: sentence_analysis correctly populated when AI score > 0")
    else:
        print(f"INFO: AI score={ai}%, sentences={len(sa)} (clean document path)")

except Exception as e:
    print(f"ERROR: {e}")
