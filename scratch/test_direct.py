"""Direct test of analyze_sentences to verify fix works locally."""
import sys
sys.path.insert(0, r"C:\Users\deexi\OneDrive\Desktop\Ai-driven-resumescreening")

from ai_detector import analyze_sentences, _per_sentence_phrase_score

text = (
    "I collaborated closely with cross-functional teams to orchestrate end-to-end solutions. "
    "Championed best-in-class coding practices and optimized system performance by 40 percent. "
    "Spearheaded the development of a data-driven analytics platform. "
    "I worked closely with stakeholders to deliver key milestones on time. "
    "I am passionate about building innovative, data-driven systems that transform business processes."
)

print("=== Direct phrase scorer test ===")
for sent in text.split(". "):
    s = sent.strip()
    if s:
        score = _per_sentence_phrase_score(s)
        print(f"  phrase_score={score:.1f}  {s[:80]}")

print("\n=== analyze_sentences result ===")
results = analyze_sentences(text)
for r in results:
    lbl = r["label"]
    scr = r["score"]
    txt = r["text"][:80]
    print(f"  [{lbl:9s}] {scr:5.1f}%  {txt}")
