"""Compare human vs AI-enhanced resume scores."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Clear cached modules
for mod in list(sys.modules.keys()):
    if 'ai_detector' in mod or 'feature_extractor' in mod:
        del sys.modules[mod]

from ai_detector import detect_ai_content

HUMAN = """
Karan Iyer
karan.iyer1995@gmail.com | +91-97654-32109 | Pune, Maharashtra

ABOUT ME
Been coding since college, mostly self-taught beyond the basics. 3 years at a product company doing full-stack work, then moved to a startup last year where it's basically just me and one other dev handling everything. I enjoy the backend side more than frontend but I can do both when needed.

EXPERIENCE

Software Developer — Stackloop Technologies, Pune (Aug 2022 – Present)
- I'm one of two developers. We built the entire platform from scratch — Node.js backend, React frontend, PostgreSQL database.
- Wrote the billing module that integrates with Stripe. Took longer than expected because webhook handling is annoying but eventually got it solid.
- Set up deployments on AWS using EC2 and an RDS instance. No fancy infra, but it works and hasn't gone down unexpectedly in 8 months.
- Added Redis caching to our product search — page load dropped from 2.1s to 0.3s on average.
- Do almost all the code reviews since it's a small team.

Junior Developer — Infovista Solutions, Pune (Jun 2020 – Jul 2022)
- Worked on a CRM system used by about 15 clients. Stack was PHP with Laravel and MySQL.
- Fixed a long-standing bug in the reporting module where date filters were off by one day because of timezone handling. Took me 2 days to find it.
- Built a CSV import feature for bulk contact uploads.

SKILLS
Backend: Node.js, Express, PHP, Laravel
Frontend: React, basic HTML/CSS/JS
Databases: PostgreSQL, MySQL, Redis
Cloud: AWS (EC2, RDS, S3), Git, Docker

EDUCATION
B.E. Computer Engineering — Pune University (2016–2020). Aggregate: 68%.
"""

AI_ENHANCED = """
Karan Iyer
karan.iyer1995@gmail.com | +91-97654-32109 | Pune, Maharashtra

PROFESSIONAL SUMMARY
A highly motivated and results-driven Full Stack Developer with over 3 years of comprehensive experience in architecting and delivering scalable web solutions. Demonstrated expertise in leveraging modern technologies to optimize operational efficiency and facilitate seamless product delivery. Committed to executing high-impact technical initiatives that contribute to organizational success.

PROFESSIONAL EXPERIENCE

Software Developer — Stackloop Technologies, Pune (Aug 2022 – Present)
- Spearheaded the end-to-end development of a full-stack platform utilizing Node.js, React, and PostgreSQL, consequently establishing a robust technical foundation for the organization.
- Orchestrated the implementation of a comprehensive billing module integrated with the Stripe payment gateway, thereby facilitating secure and reliable financial transaction processing.
- Leveraged AWS infrastructure, including EC2 and RDS, to architect a deployment environment that has demonstrated exceptional stability over an 8-month operational period.
- Optimized product search performance through the strategic implementation of Redis caching, consequently reducing page load times from 2.1 seconds to 0.3 seconds and enhancing overall user experience.
- Furthermore, facilitated systematic code quality assurance by conducting comprehensive code reviews, thereby contributing to the maintenance of high development standards across the team.

Junior Developer — Infovista Solutions, Pune (Jun 2020 – Jul 2022)
- Executed the maintenance and enhancement of a CRM system serving approximately 15 enterprise clients, demonstrating consistent delivery of high-quality technical solutions.
- Spearheaded the identification and resolution of a critical reporting module defect attributable to timezone handling inconsistencies, consequently restoring full system accuracy.
- Moreover, orchestrated the development of a CSV import feature to facilitate bulk contact uploads, leveraging advanced PHP stream processing to optimize memory utilization.

TECHNICAL SKILLS
Backend Technologies: Node.js, Express, PHP, Laravel
Frontend Technologies: React, HTML5, CSS3, JavaScript
Database Management: PostgreSQL, MySQL, Redis
Cloud Infrastructure: AWS (EC2, RDS, S3), Docker, Git

EDUCATION
Bachelor of Engineering, Computer Engineering — Pune University (2016–2020). Aggregate Score: 68%.
"""

print("=" * 55)
print("  HUMAN vs AI-ENHANCED RESUME COMPARISON")
print("=" * 55)

h_score, h_det = detect_ai_content(HUMAN)
a_score, a_det = detect_ai_content(AI_ENHANCED)

print(f"\n  HUMAN RESUME")
print(f"    AI Score       : {h_score:.1f}%")
print(f"    Classification : {h_det.get('classification')}")
print(f"    ML score       : {h_det.get('ml_score', 'N/A')}")
print(f"    Heuristic      : {h_det.get('heuristic_score', 'N/A')}")
print(f"    Raw score      : {h_det.get('raw_ai_score', 'N/A')}")

print(f"\n  AI-ENHANCED RESUME")
print(f"    AI Score       : {a_score:.1f}%")
print(f"    Classification : {a_det.get('classification')}")
print(f"    ML score       : {a_det.get('ml_score', 'N/A')}")
print(f"    Heuristic      : {a_det.get('heuristic_score', 'N/A')}")
print(f"    Raw score      : {a_det.get('raw_ai_score', 'N/A')}")

print("\n" + "-" * 55)
diff = a_score - h_score
print(f"  Score difference : +{diff:.1f}% (AI vs Human)")
if h_score <= 20 and a_score >= 40:
    print("  PASS - System correctly differentiates human vs AI")
elif h_score < a_score:
    print(f"  PARTIAL - AI scores higher but gap may need tuning")
else:
    print("  FAIL - AI resume scoring same or lower than human")
print("=" * 55)
