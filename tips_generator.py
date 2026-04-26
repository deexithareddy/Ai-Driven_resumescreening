"""
tips_generator.py
-----------------
Resume Improvement Tips Generator.

Generates actionable, prioritized improvement suggestions based on
missing skills and screening results.
"""

from typing import List, Dict
from logger import get_logger

logger = get_logger(__name__)

# ── Skill → Learning Resource Mapping ─────────────────────────────────────────
SKILL_TIPS: Dict[str, str] = {
    # Programming Languages
    "python":           "Practice Python on LeetCode or build a project using FastAPI/Django.",
    "java":             "Complete the 'Java Programming Masterclass' on Udemy.",
    "javascript":       "Build a full-stack app with Node.js and React.",
    "typescript":       "Add TypeScript to an existing JS project for hands-on practice.",
    "go":               "Follow the official Go Tour at go.dev/tour.",
    "rust":             "Read 'The Rust Programming Language' book (free at doc.rust-lang.org).",
    "c++":              "Practice competitive programming on Codeforces using C++.",

    # Databases
    "sql":              "Practice SQL on Mode Analytics or SQLZoo.",
    "nosql":            "Build a MongoDB CRUD app with PyMongo or Mongoose.",
    "mongodb":          "Complete MongoDB University's free M001 course.",
    "postgresql":       "Try PostgreSQL exercises on pgexercises.com.",
    "redis":            "Build a caching layer with Redis in a Python/Node project.",
    "elasticsearch":    "Follow the Elasticsearch 'Getting Started' guide on elastic.co.",

    # Cloud & DevOps
    "aws":              "Get AWS Cloud Practitioner certified (free prep on AWS Skill Builder).",
    "azure":            "Complete Microsoft Learn's Azure Fundamentals path (free).",
    "gcp":              "Earn Google Cloud's free 'Cloud Digital Leader' badge.",
    "docker":           "Build and containerize a personal project using Docker.",
    "kubernetes":       "Complete 'Kubernetes for Beginners' on KodeKloud (free tier).",
    "terraform":        "Follow HashiCorp's official Terraform tutorials at developer.hashicorp.com.",
    "ci/cd":            "Set up a GitHub Actions pipeline for an existing project.",
    "devops":           "Study the DevOps Roadmap at roadmap.sh/devops.",
    "mlops":            "Take the MLOps Specialization on Coursera by deeplearning.ai.",

    # ML / AI
    "machine learning": "Complete Andrew Ng's Machine Learning Specialization on Coursera.",
    "deep learning":    "Take the Deep Learning Specialization on Coursera by deeplearning.ai.",
    "nlp":              "Study Hugging Face's free NLP course at huggingface.co/learn.",
    "computer vision":  "Follow fast.ai's Practical Deep Learning for Coders (free).",
    "tensorflow":       "Complete TensorFlow's official tutorials at tensorflow.org.",
    "pytorch":          "Follow PyTorch's 60-minute blitz tutorial at pytorch.org.",
    "scikit-learn":     "Work through scikit-learn's official user guide with real datasets.",
    "pandas":           "Practice data manipulation on Kaggle's Pandas micro-course (free).",
    "numpy":            "Complete the NumPy quickstart tutorial at numpy.org.",

    # Big Data
    "spark":            "Take Databricks' free 'Apache Spark Fundamentals' course.",
    "hadoop":           "Study the Hadoop ecosystem on Cloudera's free training portal.",

    # Web Frameworks
    "django":           "Build a blog or e-commerce site with Django (official tutorial).",
    "flask":            "Create a REST API with Flask and deploy it on Heroku or Render.",
    "fastapi":          "Follow FastAPI's official tutorial at fastapi.tiangolo.com.",
    "react":            "Complete the official React tutorial at react.dev.",
    "node.js":          "Build a REST API with Express.js and Node.",

    # Tools & Practices
    "git":              "Practice Git branching at learngitbranching.js.org.",
    "linux":            "Complete 'The Linux Command Line' book (free PDF available).",
    "rest api":         "Design and build a RESTful API following OpenAPI standards.",
    "graphql":          "Follow the official GraphQL tutorial at graphql.org/learn.",
    "microservices":    "Study microservices patterns at microservices.io.",
    "agile":            "Get a free Agile overview from the Scrum Alliance website.",
    "scrum":            "Study for the free Scrum.org Professional Scrum Master (PSM I) exam.",
    "system design":    "Study 'System Design Interview' by Alex Xu or use systemdesign.one.",
    "data structures":  "Practice on LeetCode's Data Structures & Algorithms study plan.",
    "algorithms":       "Complete 'Grokking Algorithms' book or NeetCode's free roadmap.",

    # Soft Skills
    "communication":    "Join Toastmasters or practice technical writing on a personal blog.",
    "leadership":       "Lead a team project or open-source initiative.",
    "teamwork":         "Contribute to open-source projects on GitHub.",
    "problem solving":  "Solve 3 LeetCode problems per week to sharpen analytical thinking.",
    "analytical":       "Practice data analysis with real datasets on Kaggle.",
    "project management": "Study PMP basics or try managing a personal project with Jira/Trello.",
}

DEFAULT_TIP = "Research this skill online and build a small project to demonstrate it."


def generate_tips(missing_skills: List[str], match_score: float) -> List[Dict[str, str]]:
    """
    Generate prioritized improvement tips for missing skills.

    Args:
        missing_skills (list): Skills the candidate is missing.
        match_score (float): Current match score (used to prioritize).

    Returns:
        list of dicts with 'skill' and 'tip' keys.
    """
    if not missing_skills:
        logger.info("No missing skills — no tips to generate.")
        return []

    logger.info(f"Generating tips for {len(missing_skills)} missing skills.")
    tips = []

    for skill in missing_skills:
        tip_text = SKILL_TIPS.get(skill.lower(), DEFAULT_TIP)
        tips.append({
            "skill": skill,
            "tip": tip_text,
            "priority": "🔴 High" if match_score < 40 else "🟡 Medium" if match_score < 60 else "🟢 Nice to Have",
        })

    return tips


def get_general_advice(match_score: float, ai_score: float, skill_coverage: float) -> List[str]:
    """
    Generate general advice based on overall screening results.

    Args:
        match_score (float): Resume-JD match score.
        ai_score (float): AI content likelihood score.
        skill_coverage (float): Percentage of JD skills found in resume.

    Returns:
        list of advice strings.
    """
    advice = []

    if match_score < 40:
        advice.append("📝 Your resume language doesn't closely mirror the job description. Try using similar keywords and phrases from the JD.")
    elif match_score < 60:
        advice.append("📝 Tailor your resume more specifically to this role by incorporating key terms from the job description.")

    if ai_score > 60:
        advice.append("🤖 Your resume shows signs of AI-generated content. Recruiters prefer authentic, personal writing — consider rewriting key sections in your own voice.")

    if skill_coverage < 50:
        advice.append("🎯 You're missing more than half the required skills. Focus on the top 3 missing skills before applying.")
    elif skill_coverage < 75:
        advice.append("🎯 Good skill coverage! Addressing the missing skills could significantly boost your chances.")

    if not advice:
        advice.append("✅ Your resume looks strong for this role! Make sure your cover letter reinforces your key achievements.")

    return advice


# ─── Pro Interview Question Generator ──────────────────────────────────────────

def generate_interview_questions(missing_skills: List[str]) -> List[Dict[str, str]]:
    """
    Generate tailored technical interview questions based on skill gaps.
    """
    if not missing_skills:
        return [
            {"skill": "General", "question": "Walk us through your most challenging technical project and how you solved a critical bug."},
            {"skill": "General", "question": "How do you stay updated with the latest trends and best practices in your primary tech stack?"}
        ]

    questions = []
    skill_patterns = {
        "python":     "Explain the difference between deep copy and shallow copy in Python, and when would you use each?",
        "sql":        "Describe a complex SQL query you've written involving multiple joins and window functions. How did you optimize it?",
        "docker":     "How do you optimize Docker image sizes for production deployment, and what are the benefits of multi-stage builds?",
        "react":      "Explain the React Reconciliation algorithm and how 'keys' help in optimizing the re-rendering process.",
        "aws":        "Compare AWS Lambda with EC2 for a high-traffic microservice. Which one would you choose and why?",
        "machine learning": "Explain the bias-variance tradeoff. How do you identify if a model is overfitting, and what techniques would you use to fix it?",
        "git":        "How do you resolve a complex merge conflict where multiple developers modified the same logic in different ways?",
        "system design": "How would you design a scalable notification system that needs to handle millions of real-time alerts?",
    }

    # Pick top 3-4 missing skills to generate specific questions
    for skill in missing_skills[:4]:
        skill_lower = skill.lower()
        question = skill_patterns.get(skill_lower, f"Can you describe your experience with {skill} and how you've applied it in a professional project?")
        questions.append({
            "skill": skill,
            "question": question
        })

    return questions
