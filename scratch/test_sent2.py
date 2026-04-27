import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for mod in list(sys.modules.keys()):
    if 'ai_detector' in mod:
        del sys.modules[mod]

from ai_detector import detect_ai_sentences

AI_ENHANCED = """Karan Iyer
karan.iyer1995@gmail.com

PROFESSIONAL SUMMARY
A highly motivated and results-driven Full Stack Developer with over 3 years of comprehensive experience in architecting and delivering scalable web solutions. Demonstrated expertise in leveraging modern technologies to optimize operational efficiency and facilitate seamless product delivery. Committed to executing high-impact technical initiatives that contribute to organizational success.

PROFESSIONAL EXPERIENCE
Software Developer - Stackloop Technologies, Pune (Aug 2022 - Present)
- Spearheaded the end-to-end development of a full-stack platform utilizing Node.js, React, and PostgreSQL, consequently establishing a robust technical foundation for the organization.
- Orchestrated the implementation of a comprehensive billing module integrated with the Stripe payment gateway, thereby facilitating secure and reliable financial transaction processing.
- Optimized product search performance through the strategic implementation of Redis caching, consequently reducing page load times from 2.1 seconds to 0.3 seconds and enhancing overall user experience.
- Furthermore, facilitated systematic code quality assurance by conducting comprehensive code reviews, thereby contributing to the maintenance of high development standards across the team.
"""

results = detect_ai_sentences(AI_ENHANCED)
high = [s for s in results if s['level'] == 'HIGH']
mid  = [s for s in results if s['level'] == 'MEDIUM']
low  = [s for s in results if s['level'] == 'LOW']

print(f"Total: {len(results)} | HIGH(RED): {len(high)} | MEDIUM(YELLOW): {len(mid)} | LOW(GREEN): {len(low)}")
print()
for s in results:
    tag = '[RED   ]' if s['level'] == 'HIGH' else '[YELLOW]' if s['level'] == 'MEDIUM' else '[GREEN ]'
    print(f"  {tag} {s['score']:5.1f}%  {s['text'][:65]}")
