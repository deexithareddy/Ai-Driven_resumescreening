"""Debug: check how NLTK tokenizes the resume and why all sections are excluded."""
import sys
sys.path.insert(0, r"C:\Users\deexi\OneDrive\Desktop\Ai-driven-resumescreening")

from ai_detector import detect_ai_sections, _tokenize_sentences, _is_contact_or_header, _is_skills_or_bullet

resume = (
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
)

sentences = _tokenize_sentences(resume)
print(f"\nNLTK tokenized into {len(sentences)} sentences:\n")
for i, s in enumerate(sentences):
    words = len(s.split())
    is_hdr = _is_contact_or_header(s)
    is_blt = _is_skills_or_bullet(s)
    label = "EXCLUDED(header)" if is_hdr else ("EXCLUDED(bullet)" if is_blt else "ANALYZED")
    print(f"  [{i+1:2d}] {words:3d} words | {label}")
    print(f"       {repr(s[:100])}")
    print()

sections = detect_ai_sections(resume)
print(f"\ndetect_ai_sections returned {len(sections)} entries:")
for s in sections:
    print(f"  excluded={s['is_excluded']}  score={s['score']}  label={s['label']}  text={repr(s['sentence'][:80])}")
