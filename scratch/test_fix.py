"""Quick smoke test for the _skip_clean fix."""
from ai_detector import detect_ai_content, detect_ai_sentences, remove_non_content

SAMPLE = (
    "Arjun Reddy\n"
    "arjun.reddy@email.com | +91 98765 43210 | Hyderabad, India\n\n"
    "Professional Summary\n"
    "I am a highly motivated software engineer with over 5 years of experience "
    "developing scalable distributed systems and cloud-native applications. "
    "I leverage cutting-edge technologies to deliver impactful solutions that drive business growth.\n\n"
    "Experience\n"
    "Led the end-to-end development of a microservices architecture that reduced system "
    "latency by 40 percent while ensuring seamless scalability across multiple cloud regions.\n"
    "Collaborated with cross-functional teams to design and implement RESTful APIs, "
    "enabling integration with third-party services and improving data throughput significantly.\n"
)

print("=== remove_non_content ===")
cleaned = remove_non_content(SAMPLE)
print(repr(cleaned[:200]))
print()

print("=== detect_ai_content (full doc) ===")
doc_score, _ = detect_ai_content(SAMPLE)
print(f"Document AI score: {doc_score:.1f}%")
print()

print("=== detect_ai_sentences ===")
results = detect_ai_sentences(SAMPLE)
print(f"Sentences returned: {len(results)}")
for r in results:
    print(f"  [{r['level']}] ({r['score']}%) {r['text'][:90]}")

assert len(results) >= 1, "FAIL: no sentences returned despite non-zero doc score"
assert all(r['level'] in ('HIGH', 'MEDIUM', 'LOW') for r in results), "FAIL: bad level"
print("\nALL ASSERTIONS PASSED")
