"""Test sentence highlighting for human vs AI-enhanced resume."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for mod in list(sys.modules.keys()):
    if 'ai_detector' in mod: del sys.modules[mod]

from ai_detector import detect_ai_sentences

HUMAN = """Karan Iyer
karan.iyer1995@gmail.com | +91-97654-32109 | Pune, Maharashtra

ABOUT ME
Been coding since college, mostly self-taught beyond the basics. 3 years at a product company doing full-stack work, then moved to a startup last year where it's basically just me and one other dev handling everything. I enjoy the backend side more than frontend but I can do both when needed.

EXPERIENCE
Software Developer — Stackloop Technologies, Pune (Aug 2022 – Present)
- I'm one of two developers. We built the entire platform from scratch — Node.js backend, React frontend, PostgreSQL database.
- Wrote the billing module that integrates with Stripe. Took longer than expected because webhook handling is annoying but eventually got it solid.
- Added Redis caching to our product search — page load dropped from 2.1s to 0.3s on average.
"""

AI_ENHANCED = """Karan Iyer
karan.iyer1995@gmail.com | +91-97654-32109 | Pune, Maharashtra

PROFESSIONAL SUMMARY
A highly motivated and results-driven Full Stack Developer with over 3 years of comprehensive experience in architecting and delivering scalable web solutions. Demonstrated expertise in leveraging modern technologies to optimize operational efficiency and facilitate seamless product delivery.

PROFESSIONAL EXPERIENCE
Software Developer — Stackloop Technologies, Pune (Aug 2022 – Present)
- Spearheaded the end-to-end development of a full-stack platform utilizing Node.js, React, and PostgreSQL, consequently establishing a robust technical foundation for the organization.
- Orchestrated the implementation of a comprehensive billing module integrated with the Stripe payment gateway, thereby facilitating secure and reliable financial transaction processing.
- Optimized product search performance through the strategic implementation of Redis caching, consequently reducing page load times from 2.1 seconds to 0.3 seconds and enhancing overall user experience.
- Furthermore, facilitated systematic code quality assurance by conducting comprehensive code reviews, thereby contributing to the maintenance of high development standards.
"""

print("=" * 60)
print("  SENTENCE HIGHLIGHTING: HUMAN RESUME")
print("=" * 60)
h_sents = detect_ai_sentences(HUMAN)
if not h_sents:
    print("  ✅ No sentences returned — clean human resume")
else:
    for s in h_sents:
        print(f"  [{s['level']:6}] {s['score']:5.1f}%  {s['text'][:70]}")

print()
print("=" * 60)
print("  SENTENCE HIGHLIGHTING: AI-ENHANCED RESUME")
print("=" * 60)
a_sents = detect_ai_sentences(AI_ENHANCED)
if not a_sents:
    print("  ❌ No sentences returned — expected highlights!")
else:
    high = [s for s in a_sents if s['level'] == 'HIGH']
    mid  = [s for s in a_sents if s['level'] == 'MEDIUM']
    low  = [s for s in a_sents if s['level'] == 'LOW']
    print(f"  🔴 HIGH: {len(high)}  🟡 MEDIUM: {len(mid)}  🟢 LOW: {len(low)}")
    print()
    for s in a_sents:
        icon = '🔴' if s['level']=='HIGH' else '🟡' if s['level']=='MEDIUM' else '🟢'
        print(f"  {icon} {s['score']:5.1f}%  {s['text'][:70]}")
