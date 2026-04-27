"""
train_model.py
--------------
Training Pipeline for the ML-based AI Content Detection Model.

Trains a Logistic Regression classifier on statistical linguistic features
to distinguish human-written from AI-generated resume text.

Usage:
    # Train with synthetic data (bootstrap):
    python train_model.py

    # Train with real labeled data:
    python train_model.py --csv path/to/data.csv

    CSV Format:
        text,label
        "Resume text content...",0       # 0 = human
        "AI generated resume...",1       # 1 = AI

Output:
    models/ai_detector_model.pkl — trained model + scaler + metadata
"""

import os
import sys
import pickle
import random
import argparse
import numpy as np
from typing import List, Tuple

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from feature_extractor import extract_features, FEATURE_NAMES

# ── Configuration ──────────────────────────────────────────────────────────────

MODEL_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "ai_detector_model.pkl")
RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ══════════════════════════════════════════════════════════════════════════════
#  SYNTHETIC DATA GENERATOR
#  Generates training samples that capture the statistical differences between
#  human-written and AI-generated resume text. NOT keyword matching — these
#  samples differ in sentence structure, vocabulary diversity, and rhythm.
# ══════════════════════════════════════════════════════════════════════════════

# ── Building blocks for synthetic resumes ──────────────────────────────────────

HUMAN_EXPERIENCE_BULLETS = [
    "Worked with the marketing team to redesign the company website, which was a pretty messy project but we got it done in about 6 weeks.",
    "Managed a small team of 3 developers. We built an internal dashboard using React and Flask that replaced a bunch of spreadsheets.",
    "Handled customer support tickets during peak season — roughly 50-80 per day. Got pretty good at spotting recurring issues.",
    "Set up CI/CD pipelines for our backend services. Took a while to get Docker configs right but it saved us hours every week.",
    "Wrote Python scripts to automate monthly reporting. Nothing fancy, just pandas and some email automation.",
    "Led the migration from on-prem servers to AWS. Had some scary moments with data transfer but zero downtime in the end.",
    "Helped interview and onboard 4 new engineers. Created a getting-started guide that people actually used.",
    "Fixed a long-standing memory leak in our Java service that had been bugging us for months. Turned out to be a connection pool issue.",
    "Built a recommendation engine prototype for our e-commerce site. Used collaborative filtering — accuracy was decent but latency needed work.",
    "Ran weekly standup meetings. Tried to keep them under 15 minutes. Usually failed.",
    "Collaborated with the data science team on churn prediction model. My part was building the feature pipeline in Spark.",
    "Debugged production issues at 2am more times than I'd like to admit. Got better at writing alerting rules after that.",
    "Refactored our authentication module from session-based to JWT. Breaking change but worth it for the mobile app.",
    "Managed client relationships for 3 key accounts. Lots of calls, some difficult conversations, but retention stayed at 95%.",
    "Created training materials for junior devs on Git workflows. Turns out most people find rebasing confusing.",
    "Optimized SQL queries that were taking 30+ seconds. Proper indexing brought most down to under 500ms.",
    "Presented quarterly results to stakeholders. Not my favorite thing but got better at simplifying technical concepts.",
    "Developed mobile app features using React Native. The iOS build process was painful but users loved the dark mode.",
    "Configured monitoring dashboards in Grafana. Having real-time metrics changed how we did releases.",
    "Contributed to open-source tools our team used. Submitted 3 PRs that got merged — felt great.",
    "Dealt with a security incident where a dependency had a known vulnerability. Patched it within hours.",
    "Built data pipelines using Airflow. DAGs got complex but we documented everything.",
    "Worked on compliance documentation for SOC 2 audit. Tedious but learned a lot about security practices.",
    "Integrated Stripe payments into our SaaS product. Edge cases around failed payments were tricky.",
    "Wrote unit tests for legacy code that had zero coverage. Not glamorous but prevented regressions.",
    "Maintained a WordPress site for the marketing team. Not my cup of tea but kept things running.",
    "Designed database schema for a new feature. Went through 3 iterations before settling on the final design.",
    "Automated deployment process — what used to take 2 hours of manual steps now runs in 10 minutes.",
    "Participated in code reviews daily. Learned more from reviewing others' code than writing my own.",
    "Implemented caching layer using Redis. Reduced API response times from 800ms to under 100ms.",
]

HUMAN_SUMMARIES = [
    "Software engineer with about 4 years of experience, mostly in backend development. Comfortable with Python and JavaScript. Looking for a role where I can grow into system design.",
    "Full-stack developer. Been working with React and Node for 3 years. I like building things that people actually use. Previous company was a fintech startup.",
    "Recent CS grad from State University. Did two internships — one at a startup, one at a bank. Strongest in Python and SQL. Eager to learn, not afraid of messy codebases.",
    "Data analyst transitioning to data engineering. Self-taught a lot of this — Spark, Airflow, dbt. Currently working on getting AWS certified.",
    "5 years in QA/testing, now moving to development. Already doing a lot of test automation in Python. Built a few internal tools that the team relies on.",
    "DevOps engineer who used to be a sysadmin. Docker, Kubernetes, Terraform are my daily tools. I automate everything I can.",
    "Frontend developer specializing in React. I care about accessibility and performance. My sites load fast and work with screen readers.",
    "Backend engineer at a healthcare startup. Java and Spring Boot mostly. HIPAA compliance is something I deal with every day.",
    "Mobile developer with 2 years of Flutter experience. Published 3 apps on the Play Store. One has 50k+ downloads.",
    "ML engineer working on NLP projects. Finetuned BERT models for text classification. Comfortable with PyTorch and Hugging Face.",
    "Project manager turned developer. I understand both sides — business requirements and technical constraints. Currently learning Go.",
    "Self-taught programmer. Started with online courses, built several personal projects, now working professionally for 2 years.",
    "Database administrator with MongoDB and PostgreSQL experience. Performance tuning is my specialty — I've rescued some truly terrible queries.",
    "Embedded systems programmer. C and C++ are my main languages. Worked on IoT devices for industrial monitoring.",
    "Security-focused developer. OWASP top 10 is second nature. I do penetration testing as a side gig.",
]

HUMAN_SKILLS_SECTIONS = [
    "Python, JavaScript, SQL. Some experience with Go. Git, Docker, basic AWS.",
    "React, TypeScript, Node.js. Familiar with PostgreSQL, Redis. Learning GraphQL.",
    "Java, Spring Boot, Maven. Oracle DB, MongoDB. Jenkins for CI/CD.",
    "Python, pandas, scikit-learn, TensorFlow. SQL, Jupyter, Matplotlib.",
    "C#, .NET, Azure DevOps. SQL Server. REST APIs. Some PowerShell scripting.",
    "HTML/CSS, JavaScript, React. Figma for design. Some Python for scripting.",
    "Kubernetes, Terraform, Ansible. AWS (EC2, S3, Lambda). Linux administration.",
    "Swift, Xcode, UIKit, SwiftUI. Firebase. Some Objective-C legacy code.",
    "PHP, Laravel, MySQL. Redis for caching. Basic Docker. jQuery (legacy projects).",
    "Rust, WebAssembly, C++. Linux, embedded systems. Some Python for tooling.",
]

HUMAN_EDUCATION = [
    "B.S. Computer Science, State University, 2021. GPA: 3.4. Took extra courses in distributed systems.",
    "B.A. Mathematics, Liberal Arts College, 2019. Minor in CS. Did most of my coding outside of class.",
    "M.S. Data Science, Tech University, 2022. Thesis on anomaly detection in time series data.",
    "Self-taught. Completed freeCodeCamp, CS50, and several Coursera specializations. No formal CS degree.",
    "Bootcamp graduate, General Assembly (2020). 12-week intensive. Prior career in accounting.",
    "B.S. Electrical Engineering, University of Michigan, 2018. Switched to software after graduation.",
    "Community college Associates degree (2017), then transferred to University of Washington for B.S. in CS (2019).",
    "Ph.D. in Computational Linguistics (dropped out after 3 years). Published 2 papers on sentiment analysis.",
]

AI_EXPERIENCE_BULLETS = [
    "Spearheaded the development of a comprehensive, enterprise-grade web application utilizing React, Node.js, and AWS cloud infrastructure, resulting in a 45% increase in operational efficiency and a 30% reduction in deployment time.",
    "Orchestrated the implementation of a robust microservices architecture, leveraging Docker and Kubernetes to achieve seamless scalability and high availability across distributed environments.",
    "Championed the adoption of cutting-edge CI/CD practices, building automated deployment pipelines that reduced release cycles from weeks to hours, enhancing overall team productivity.",
    "Pioneered the development of innovative machine learning solutions using TensorFlow and PyTorch, achieving state-of-the-art accuracy on benchmark datasets and driving data-driven decision-making.",
    "Architected and deployed scalable data processing pipelines using Apache Spark and Apache Kafka, enabling real-time analytics and actionable insights for key business stakeholders.",
    "Led and managed a cross-functional team of 12 engineers, fostering a collaborative environment and consistently delivering high-quality solutions aligned with strategic business objectives.",
    "Designed and implemented a comprehensive RESTful API framework, ensuring seamless integration with third-party services and facilitating efficient data exchange across the organization.",
    "Developed and maintained a sophisticated monitoring and alerting system using Prometheus and Grafana, proactively identifying and resolving potential issues before they impacted end users.",
    "Delivered impactful results by optimizing database performance through strategic indexing, query optimization, and schema redesign, resulting in a 60% improvement in response times.",
    "Built and deployed a comprehensive automated testing framework encompassing unit, integration, and end-to-end tests, significantly enhancing code quality and reducing production defects.",
    "Successfully managed the end-to-end migration of legacy monolithic applications to a modern, cloud-native microservices architecture, ensuring zero downtime and seamless transition.",
    "Effectively collaborated with product management and UX design teams to translate complex business requirements into elegant, user-centric technical solutions.",
    "Strategically implemented comprehensive security measures including OAuth 2.0 authentication, role-based access control, and data encryption, ensuring compliance with industry standards.",
    "Consistently exceeded performance targets by leveraging innovative approaches to problem-solving and maintaining a strong focus on delivering exceptional results.",
    "Proactively identified and resolved critical scalability bottlenecks, implementing innovative caching strategies and load balancing techniques that improved system throughput by 200%.",
    "Meticulously documented all technical processes, architectural decisions, and best practices, creating a comprehensive knowledge base that enhanced team onboarding and knowledge sharing.",
    "Seamlessly integrated machine learning models into production systems, building robust inference pipelines that processed millions of predictions daily with sub-millisecond latency.",
    "Diligently maintained code quality standards through comprehensive code reviews, automated static analysis, and continuous integration practices, fostering a culture of technical excellence.",
    "Orchestrated the successful implementation of a data-driven customer segmentation system, leveraging advanced analytics to deliver personalized experiences and drive revenue growth.",
    "Championed the adoption of DevOps best practices across the organization, establishing infrastructure-as-code standards and automated provisioning that reduced operational overhead by 40%.",
    "Demonstrated exceptional ability to analyze complex technical challenges and develop innovative solutions that consistently delivered measurable business value.",
    "Strategically designed and implemented a comprehensive API gateway solution, enabling secure and efficient communication between microservices and external consumers.",
    "Effectively managed multiple concurrent projects while maintaining high quality standards and consistently meeting tight deadlines in a fast-paced agile environment.",
    "Pioneered the implementation of advanced machine learning pipelines for natural language processing, achieving remarkable improvements in text classification accuracy and processing speed.",
    "Masterfully coordinated cross-functional collaboration between engineering, data science, and product teams to deliver cutting-edge solutions aligned with organizational strategic goals.",
]

AI_SUMMARIES = [
    "Results-driven and highly motivated software engineer with extensive experience in full-stack development, cloud computing, and agile methodologies. Proven track record of delivering innovative, scalable solutions that drive business growth and operational efficiency. Passionate about leveraging cutting-edge technologies to solve complex challenges and create impactful results.",
    "Dynamic and accomplished professional with a strong foundation in data science, machine learning, and artificial intelligence. Demonstrated expertise in developing state-of-the-art models and deploying end-to-end ML pipelines. Committed to driving data-driven decision-making and delivering actionable insights that create measurable business value.",
    "Seasoned and detail-oriented DevOps engineer with comprehensive knowledge of cloud infrastructure, containerization, and continuous integration/deployment. Adept at architecting robust, scalable systems and fostering cross-functional collaboration. Dedicated to driving operational excellence and implementing industry-leading best practices.",
    "Highly skilled and versatile backend developer with deep understanding of distributed systems, microservices architecture, and database optimization. Recognized for exceptional ability to translate complex business requirements into elegant technical solutions. Eager to contribute expertise to innovative, forward-thinking organizations.",
    "Accomplished and passionate full-stack developer with a proven track record of spearheading the development of enterprise-grade applications. Strong background in React, Node.js, and cloud-native technologies. Committed to excellence in code quality, performance optimization, and delivering exceptional user experiences.",
    "Forward-thinking and results-oriented machine learning engineer with extensive experience in deep learning, natural language processing, and computer vision. Demonstrated ability to develop innovative AI solutions that drive transformative business outcomes. Passionate about pushing the boundaries of artificial intelligence.",
    "Dedicated and proactive software architect with robust knowledge of system design, performance engineering, and technical leadership. Consistently delivers high-impact solutions that exceed stakeholder expectations. Thrives in collaborative environments and excels at mentoring junior developers.",
    "Strategic and innovative data engineer with a strong foundation in big data technologies, ETL pipeline development, and data warehouse design. Proven ability to architect scalable data solutions that enable actionable insights and drive organizational growth.",
]

AI_SKILLS_SECTIONS = [
    "Programming Languages: Python, Java, JavaScript, TypeScript, C++, Go, Rust. Frameworks: React, Angular, Vue.js, Django, Flask, Spring Boot, Express.js. Cloud: AWS (EC2, S3, Lambda, RDS, CloudFormation), Azure, GCP. DevOps: Docker, Kubernetes, Jenkins, Terraform, Ansible, CI/CD. Databases: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, DynamoDB.",
    "Core Competencies: Full-Stack Development, Microservices Architecture, Cloud Computing, Agile Methodologies, Test-Driven Development, RESTful API Design, GraphQL, System Design, Performance Optimization, Technical Leadership. Tools: Git, JIRA, Confluence, Datadog, New Relic, Splunk.",
    "Machine Learning: TensorFlow, PyTorch, Scikit-learn, Keras, Hugging Face Transformers. Data: Apache Spark, Apache Kafka, Airflow, dbt, Snowflake, BigQuery. Visualization: Tableau, Power BI, Matplotlib, Seaborn, Plotly. Languages: Python, R, SQL, Scala.",
    "Technical Skills: Object-Oriented Programming, Functional Programming, Design Patterns, Software Architecture, Distributed Systems, Event-Driven Architecture, Domain-Driven Design, Clean Code Principles, SOLID Principles, Microservices, Server-Side Rendering.",
    "Infrastructure: AWS Solutions Architect (Certified), Kubernetes Administrator (CKA), Docker, Terraform, Ansible, CloudFormation, Helm Charts. Monitoring: Prometheus, Grafana, ELK Stack, Datadog. Security: OAuth 2.0, SAML, JWT, RBAC, SSL/TLS, WAF.",
]


def _build_human_resume() -> str:
    """Build a realistic human-style resume with natural variation."""
    sections = []

    # Name and contact (brief, informal)
    names = ["Alex Johnson", "Sam Rivera", "Jordan Chen", "Taylor Kim",
             "Casey O'Brien", "Morgan Stewart", "Riley Patel", "Jamie Wu",
             "Drew Thompson", "Quinn Murphy", "Chris Nakamura", "Pat Dubois"]
    sections.append(random.choice(names))
    sections.append(f"{random.choice(names).split()[0].lower()}@gmail.com | (555) {random.randint(100,999)}-{random.randint(1000,9999)}")
    sections.append("")

    # Summary (short and conversational)
    sections.append(random.choice(HUMAN_SUMMARIES))
    sections.append("")

    # Experience (variable number of bullets, natural language)
    sections.append("Experience")
    companies = ["Acme Corp", "TechStart Inc", "DataFlow", "CloudBase",
                  "Nexus Digital", "Pinnacle Health", "GreenLine Energy",
                  "Velocity Labs", "UrbanGrid", "Sierra Analytics"]
    titles = ["Software Developer", "Backend Engineer", "Full Stack Dev",
              "Data Analyst", "Junior Developer", "Senior Engineer",
              "DevOps Engineer", "QA Engineer", "Tech Lead", "ML Engineer"]

    num_jobs = random.randint(2, 4)
    for _ in range(num_jobs):
        company = random.choice(companies)
        title = random.choice(titles)
        year_end = random.randint(2021, 2025)
        year_start = year_end - random.randint(1, 3)
        sections.append(f"{title} — {company} ({year_start}–{year_end})")
        num_bullets = random.randint(2, 5)
        bullets = random.sample(HUMAN_EXPERIENCE_BULLETS,
                                min(num_bullets, len(HUMAN_EXPERIENCE_BULLETS)))
        for b in bullets:
            sections.append(f"- {b}")
        sections.append("")

    # Skills (terse list)
    sections.append("Skills")
    sections.append(random.choice(HUMAN_SKILLS_SECTIONS))
    sections.append("")

    # Education
    sections.append("Education")
    sections.append(random.choice(HUMAN_EDUCATION))

    return "\n".join(sections)


def _build_ai_resume() -> str:
    """Build a typical AI-generated resume with uniform patterns."""
    sections = []

    # Name and contact (polished format)
    names = ["Alexander Jonathan Mitchell", "Samantha Elizabeth Rodriguez",
             "Benjamin Christopher Thompson", "Victoria Marie Anderson",
             "Nicholas James Patterson", "Katherine Anne Williams",
             "Christopher David Martinez", "Elizabeth Grace Johnson"]
    sections.append(random.choice(names))
    contact = (f"Email: {random.choice(names).split()[0].lower()}.{random.choice(names).split()[-1].lower()}@email.com | "
               f"Phone: (555) {random.randint(100,999)}-{random.randint(1000,9999)} | "
               f"LinkedIn: linkedin.com/in/{random.choice(names).split()[0].lower()}-{random.choice(names).split()[-1].lower()} | "
               f"GitHub: github.com/{random.choice(names).split()[0].lower()}{random.choice(names).split()[-1].lower()}")
    sections.append(contact)
    sections.append("")

    # Summary (elaborate, buzzword-heavy)
    sections.append("Professional Summary")
    sections.append(random.choice(AI_SUMMARIES))
    sections.append("")

    # Experience (consistent, structured bullets)
    sections.append("Professional Experience")
    companies = ["TechVision Global", "InnovateTech Solutions", "Digital Dynamics Inc.",
                  "Quantum Analytics Corp", "NextGen Software LLC",
                  "Apex Technology Partners", "Pinnacle Data Systems"]
    titles = ["Senior Software Engineer", "Lead Full-Stack Developer",
              "Principal Engineer", "Staff Software Architect",
              "Senior Machine Learning Engineer", "Lead DevOps Engineer"]

    num_jobs = random.randint(2, 3)
    for _ in range(num_jobs):
        company = random.choice(companies)
        title = random.choice(titles)
        year_end = random.randint(2022, 2025)
        year_start = year_end - random.randint(2, 4)
        sections.append(f"{title} | {company} | {year_start} - {year_end}")
        num_bullets = random.randint(4, 6)
        bullets = random.sample(AI_EXPERIENCE_BULLETS,
                                min(num_bullets, len(AI_EXPERIENCE_BULLETS)))
        for b in bullets:
            sections.append(f"• {b}")
        sections.append("")

    # Skills (comprehensive, structured)
    sections.append("Technical Skills")
    sections.append(random.choice(AI_SKILLS_SECTIONS))
    sections.append("")

    # Education (polished)
    degrees = [
        "Master of Science in Computer Science | Stanford University | 2019\nGPA: 3.95/4.0 | Thesis: Advanced Machine Learning Techniques for Distributed Systems",
        "Bachelor of Science in Software Engineering | Massachusetts Institute of Technology | 2017\nGPA: 3.87/4.0 | Dean's List | Summa Cum Laude",
        "Master of Science in Data Science | Carnegie Mellon University | 2020\nSpecialization: Natural Language Processing and Deep Learning",
        "Bachelor of Science in Computer Science | University of California, Berkeley | 2018\nGPA: 3.92/4.0 | Honors Program | Research Assistant",
    ]
    sections.append("Education")
    sections.append(random.choice(degrees))
    sections.append("")

    # Certifications (AI loves listing these)
    certs = [
        "Certifications\n• AWS Solutions Architect Professional\n• Certified Kubernetes Administrator (CKA)\n• Google Cloud Professional Data Engineer\n• HashiCorp Certified Terraform Associate",
        "Certifications & Achievements\n• AWS Certified DevOps Engineer Professional\n• Microsoft Azure Solutions Architect Expert\n• Certified Scrum Master (CSM)\n• Published Author: 'Modern Software Architecture Patterns'",
    ]
    sections.append(random.choice(certs))

    return "\n".join(sections)


def generate_synthetic_dataset(n_samples: int = 200) -> Tuple[List[str], List[int]]:
    """
    Generate a balanced synthetic dataset of human and AI resume text.

    Args:
        n_samples: Total number of samples (split 50/50).

    Returns:
        (texts, labels): Lists of text samples and binary labels (0=human, 1=AI).
    """
    n_each = n_samples // 2
    texts = []
    labels = []

    print(f"Generating {n_each} human-style resumes...")
    for _ in range(n_each):
        texts.append(_build_human_resume())
        labels.append(0)

    print(f"Generating {n_each} AI-style resumes...")
    for _ in range(n_each):
        texts.append(_build_ai_resume())
        labels.append(1)

    return texts, labels


def load_csv_dataset(csv_path: str) -> Tuple[List[str], List[int]]:
    """
    Load a labeled dataset from CSV.

    Expected columns: text, label
    Label: 0 = human, 1 = AI

    Args:
        csv_path: Path to CSV file.

    Returns:
        (texts, labels): Lists of samples.
    """
    import csv
    texts = []
    labels = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get("text", "").strip()
            label = int(row.get("label", 0))
            if text and label in (0, 1):
                texts.append(text)
                labels.append(label)

    print(f"Loaded {len(texts)} samples from {csv_path}")
    print(f"  Human: {labels.count(0)}, AI: {labels.count(1)}")
    return texts, labels


# ══════════════════════════════════════════════════════════════════════════════
#  TRAINING PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def train_model(texts: List[str], labels: List[int]) -> dict:
    """
    Train a Logistic Regression model on extracted features.

    Args:
        texts: List of input text samples.
        labels: Corresponding binary labels (0=human, 1=AI).

    Returns:
        dict with model, scaler, metrics, and feature names.
    """
    print(f"\n{'='*60}")
    print("  EXTRACTING FEATURES")
    print(f"{'='*60}\n")

    # Extract features for all samples
    X = np.array([extract_features(text) for text in texts])
    y = np.array(labels)

    print(f"Feature matrix shape: {X.shape}")
    print(f"Labels distribution: Human={sum(y==0)}, AI={sum(y==1)}")

    # ── Train/Test Split ───────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    # ── Feature Scaling ────────────────────────────────────────────────────
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # ── Train Logistic Regression ──────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  TRAINING LOGISTIC REGRESSION")
    print(f"{'='*60}\n")

    model = LogisticRegression(
        C=1.0,                   # Regularization strength
        l1_ratio=0,              # Pure L2 (ridge) regularization
        solver="lbfgs",          # Fast solver for small datasets
        max_iter=1000,
        random_state=RANDOM_SEED,
        class_weight="balanced", # Handle any class imbalance
    )
    model.fit(X_train_scaled, y_train)

    # ── Evaluation ─────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  EVALUATION RESULTS")
    print(f"{'='*60}\n")

    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec  = recall_score(y_test, y_pred, zero_division=0)
    f1   = f1_score(y_test, y_pred, zero_division=0)
    cm   = confusion_matrix(y_test, y_pred)

    print(f"  Accuracy:  {acc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall:    {rec:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print(f"\n  Confusion Matrix:")
    print(f"    TN={cm[0][0]:3d}  FP={cm[0][1]:3d}")
    print(f"    FN={cm[1][0]:3d}  TP={cm[1][1]:3d}")
    print()
    print(classification_report(y_test, y_pred, target_names=["Human", "AI"]))

    # ── Cross-Validation ───────────────────────────────────────────────────
    print("Cross-validation (5-fold):")
    X_scaled_full = scaler.fit_transform(X)
    cv_scores = cross_val_score(model, X_scaled_full, y, cv=5, scoring="f1")
    print(f"  F1 scores: {[f'{s:.3f}' for s in cv_scores]}")
    print(f"  Mean F1:   {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    # Refit on full dataset for final model
    model.fit(X_scaled_full, y)

    # ── Feature Importance ─────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  FEATURE IMPORTANCE (Model Coefficients)")
    print(f"{'='*60}\n")

    coefs = model.coef_[0]
    sorted_idx = np.argsort(np.abs(coefs))[::-1]
    for rank, idx in enumerate(sorted_idx, 1):
        direction = "-> AI" if coefs[idx] > 0 else "-> Human"
        print(f"  {rank:2d}. {FEATURE_NAMES[idx]:25s}  coef={coefs[idx]:+.4f}  ({direction})")

    return {
        "model": model,
        "scaler": scaler,
        "feature_names": FEATURE_NAMES,
        "metrics": {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
            "cv_f1_mean": float(cv_scores.mean()),
        },
    }


def save_model(result: dict) -> str:
    """
    Save trained model, scaler, and metadata to disk.

    Args:
        result: Output from train_model().

    Returns:
        Path to saved model file.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)

    payload = {
        "model":         result["model"],
        "scaler":        result["scaler"],
        "feature_names": result["feature_names"],
        "metrics":       result["metrics"],
        "version":       "3.0-ml-hybrid",
    }

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)

    size_kb = os.path.getsize(MODEL_PATH) / 1024
    print(f"\nModel saved to: {MODEL_PATH} ({size_kb:.1f} KB)")
    return MODEL_PATH


# ══════════════════════════════════════════════════════════════════════════════
#  CLI ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Train the AI content detection model for resume screening."
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Path to a labeled CSV dataset (columns: text, label). "
             "If not provided, synthetic data is generated.",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=200,
        help="Number of synthetic samples to generate (default: 200). "
             "Ignored if --csv is provided.",
    )
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("  AI CONTENT DETECTION - MODEL TRAINING")
    print(f"{'='*60}\n")

    # Load or generate data
    if args.csv:
        texts, labels = load_csv_dataset(args.csv)
    else:
        print("No CSV provided -- generating synthetic training data...")
        texts, labels = generate_synthetic_dataset(n_samples=args.samples)

    if len(texts) < 20:
        print("ERROR: Need at least 20 samples for training.")
        sys.exit(1)

    # Train
    result = train_model(texts, labels)

    # Save
    save_model(result)

    print(f"\n{'='*60}")
    print("  TRAINING COMPLETE")
    print(f"{'='*60}")
    print(f"\n  Next steps:")
    print(f"  1. Run 'python api.py' to start the API")
    print(f"  2. The model will be loaded automatically")
    print(f"  3. To retrain with real data: python train_model.py --csv data.csv\n")


if __name__ == "__main__":
    main()
