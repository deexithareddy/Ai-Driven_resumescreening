"""
main.py
-------
CLI Entry Point for the AI-Powered Resume Screening System.

Usage:
    # Using file paths:
    python main.py --resume sample_resume.txt --jd sample_job_description.txt

    # Using inline text:
    python main.py --resume-text "Python developer with 5 years..." --jd-text "We need a Python dev..."

    # Mixed:
    python main.py --resume sample_resume.txt --jd-text "Looking for a data scientist..."
"""

import sys
import io

# Force UTF-8 output on Windows to support Unicode/emoji characters
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import argparse
import textwrap
from logger import get_logger
from utils import read_text_file, format_score
from resume_screener import compute_match_score, get_top_matching_terms
from ai_detector import detect_ai_content
from skill_extractor import compare_skills, categorize_skills
from decision_engine import get_decision_summary

logger = get_logger(__name__)

# ── ANSI Color Codes for Terminal Output ──────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
DIM    = "\033[2m"


def print_banner() -> None:
    """Print the application banner."""
    banner = f"""
{CYAN}{BOLD}
+--------------------------------------------------------------+
|       AI-POWERED RESUME SCREENING SYSTEM v1.0                |
|       Production-Ready NLP Recruitment Pipeline              |
+--------------------------------------------------------------+
{RESET}"""
    print(banner)


def print_separator(char: str = "-", width: int = 64) -> None:
    """Print a horizontal separator line."""
    print(f"{DIM}{char * width}{RESET}")


def print_result(result: dict, top_terms: list) -> None:
    """
    Pretty-print the full screening result to the terminal.

    Args:
        result (dict): Complete result from get_decision_summary().
        top_terms (list): Top matching keywords.
    """
    decision = result["decision"]
    is_shortlisted = decision == "SHORTLISTED"
    decision_color = GREEN if is_shortlisted else RED
    decision_icon  = "✅" if is_shortlisted else "❌"

    print_separator("=", 64)
    print(f"{BOLD}  SCREENING RESULTS{RESET}")
    print_separator("=", 64)

    # ── Core Scores ────────────────────────────────────────────────────────
    match_color = GREEN if result["match_passed"] else RED
    ai_color    = GREEN if result["ai_passed"]    else RED

    print(f"\n  {BOLD}📊 Core Scores{RESET}")
    print_separator()
    print(f"  Resume Match Score      : {match_color}{BOLD}{format_score(result['match_score'])}{RESET}")
    print(f"  AI Content Likelihood   : {ai_color}{BOLD}{format_score(result['ai_score'])}{RESET}")

    # ── Thresholds ─────────────────────────────────────────────────────────
    t = result["thresholds"]
    print(f"\n  {DIM}Thresholds → Match: >{t['match_threshold']}% | AI: <{t['ai_threshold']}%{RESET}")

    # ── Final Decision ─────────────────────────────────────────────────────
    print(f"\n  {BOLD}🎯 Final Decision{RESET}")
    print_separator()
    print(f"  {decision_icon} {decision_color}{BOLD}{decision}{RESET}")
    print(f"  Reason: {result['reason']}")

    # ── Skill Analysis ─────────────────────────────────────────────────────
    skills = result.get("skill_analysis", {})
    if skills.get("jd_skills"):
        print(f"\n  {BOLD}🔧 Skill Analysis{RESET}")
        print_separator()
        print(f"  JD Required Skills      : {len(skills['jd_skills'])}")
        print(f"  Resume Skills Found     : {len(skills['resume_skills'])}")
        print(f"  ✅ Matched Skills       : {', '.join(skills['matched_skills']) or 'None'}")
        if skills["missing_skills"]:
            print(f"  ⚠️  Missing Skills      : {', '.join(skills['missing_skills'])}")
        print(f"  Skill Coverage          : {GREEN}{skills['skill_match_pct']}%{RESET}")

    # ── Top Matching Keywords ──────────────────────────────────────────────
    if top_terms:
        print(f"\n  {BOLD}🔑 Top Matching Keywords{RESET}")
        print_separator()
        wrapped = textwrap.fill(", ".join(top_terms), width=58, initial_indent="  ")
        print(f"{CYAN}{wrapped}{RESET}")

    # ── AI Detection Details ───────────────────────────────────────────────
    ai_d = result.get("ai_details", {})
    if ai_d and ai_d.get("sentence_count") is not None:
        print(f"\n  {BOLD}🤖 AI Detection Details{RESET}")
        print_separator()
        print(f"  Sentences Analyzed      : {ai_d.get('sentence_count', 'N/A')}")
        if ai_d.get("sentence_length_variance") is not None:
            print(f"  Sentence Length Variance: {ai_d['sentence_length_variance']}")
            print(f"  Avg Sentence Length     : {ai_d.get('avg_sentence_length', 'N/A')} words")
            print(f"  Lexical Diversity (TTR) : {ai_d.get('lexical_diversity_ttr', 'N/A')}")

    print_separator("=", 64)
    print()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="AI-Powered Resume Screening System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python main.py --resume sample_resume.txt --jd sample_job_description.txt
          python main.py --resume-text "Python dev 5yr exp" --jd-text "Need Python dev"
        """),
    )

    # Resume input (mutually exclusive: file OR text)
    resume_group = parser.add_mutually_exclusive_group(required=True)
    resume_group.add_argument("--resume",      metavar="FILE", help="Path to resume .txt file")
    resume_group.add_argument("--resume-text", metavar="TEXT", help="Resume text as inline string")

    # JD input (mutually exclusive: file OR text)
    jd_group = parser.add_mutually_exclusive_group(required=True)
    jd_group.add_argument("--jd",      metavar="FILE", help="Path to job description .txt file")
    jd_group.add_argument("--jd-text", metavar="TEXT", help="Job description text as inline string")

    return parser.parse_args()


def run_screening(resume_text: str, jd_text: str) -> dict:
    """
    Execute the full screening pipeline.

    Args:
        resume_text (str): Resume content.
        jd_text (str): Job description content.

    Returns:
        dict: Complete screening result.
    """
    logger.info("=" * 60)
    logger.info("Starting full screening pipeline...")

    # ── Step 1: Match Score ────────────────────────────────────────────────
    match_score, match_details = compute_match_score(resume_text, jd_text)

    # ── Step 2: AI Detection ───────────────────────────────────────────────
    ai_score, ai_details = detect_ai_content(resume_text)

    # ── Step 3: Skill Extraction ───────────────────────────────────────────
    skill_data = compare_skills(resume_text, jd_text)

    # ── Step 4: Top Keywords ───────────────────────────────────────────────
    top_terms = get_top_matching_terms(resume_text, jd_text, top_n=10)

    # ── Step 5: Decision ───────────────────────────────────────────────────
    result = get_decision_summary(match_score, ai_score, match_details, ai_details, skill_data)

    logger.info("Screening pipeline complete.")
    logger.info("=" * 60)

    return result, top_terms


def main() -> None:
    """Main entry point for the CLI."""
    print_banner()
    args = parse_args()

    # ── Load Resume ────────────────────────────────────────────────────────
    if args.resume:
        resume_text = read_text_file(args.resume)
        if resume_text is None:
            print(f"{RED}Error: Could not read resume file '{args.resume}'.{RESET}")
            sys.exit(1)
    else:
        resume_text = args.resume_text

    # ── Load Job Description ───────────────────────────────────────────────
    if args.jd:
        jd_text = read_text_file(args.jd)
        if jd_text is None:
            print(f"{RED}Error: Could not read JD file '{args.jd}'.{RESET}")
            sys.exit(1)
    else:
        jd_text = args.jd_text

    # ── Run Pipeline ───────────────────────────────────────────────────────
    try:
        result, top_terms = run_screening(resume_text, jd_text)
        print_result(result, top_terms)
    except ValueError as e:
        print(f"\n{RED}Input Error: {e}{RESET}\n")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error during screening: {e}")
        print(f"\n{RED}Unexpected error: {e}{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
