"""
report_generator.py
-------------------
PDF Report Generator for the AI Resume Screening System.

Generates professional screening reports with:
  - Candidate profile summary
  - Match score and AI score gauges
  - Skills breakdown (matched vs missing)
  - AI detection signal analysis
  - Improvement tips and recommendations
"""

import io
from datetime import datetime
from typing import Dict, List
from fpdf import FPDF
from logger import get_logger

logger = get_logger(__name__)


# ── Color Palette ──────────────────────────────────────────────────────────────

class Colors:
    PRIMARY     = (37, 99, 235)     # Blue
    SUCCESS     = (5, 150, 105)     # Green
    DANGER      = (220, 38, 38)     # Red
    WARNING     = (217, 119, 6)     # Amber
    DARK        = (30, 41, 59)      # Slate-800
    MUTED       = (100, 116, 139)   # Slate-500
    LIGHT_BG    = (248, 250, 252)   # Slate-50
    WHITE       = (255, 255, 255)
    BORDER      = (226, 232, 240)   # Slate-200


# ── Custom PDF Class ───────────────────────────────────────────────────────────

class ScreeningReport(FPDF):
    """Custom FPDF subclass with branded header/footer."""

    def header(self):
        # Blue header bar
        self.set_fill_color(*Colors.PRIMARY)
        self.rect(0, 0, 210, 22, "F")

        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*Colors.WHITE)
        self.set_y(5)
        self.cell(0, 12, "AI Driven Resume Screening", align="C")

        self.set_font("Helvetica", "", 7)
        self.set_text_color(200, 210, 240)
        self.set_y(14)
        self.cell(0, 5, "Screening Report", align="C")

        self.ln(18)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*Colors.MUTED)
        self.cell(0, 10,
                  f"Generated on {datetime.now().strftime('%b %d, %Y at %I:%M %p')}  |  "
                  f"Page {self.page_no()}/{{nb}}",
                  align="C")

    def section_title(self, icon: str, title: str):
        """Draw a section header with icon and line."""
        self.ln(4)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*Colors.DARK)
        self.cell(0, 8, f"{icon}  {title}")
        self.ln(8)
        # Underline
        self.set_draw_color(*Colors.BORDER)
        self.line(self.l_margin, self.get_y(), 210 - self.r_margin, self.get_y())
        self.ln(4)

    def score_box(self, label: str, value: str, x: float, y: float,
                  w: float, color: tuple):
        """Draw a colored score box."""
        self.set_fill_color(*Colors.LIGHT_BG)
        self.set_draw_color(*Colors.BORDER)
        self.rect(x, y, w, 28, "DF")

        # Label
        self.set_xy(x, y + 3)
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*Colors.MUTED)
        self.cell(w, 5, label.upper(), align="C")

        # Value
        self.set_xy(x, y + 11)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*color)
        self.cell(w, 12, value, align="C")

    def chip(self, text: str, bg_color: tuple, text_color: tuple):
        """Draw a chip/tag inline."""
        self.set_font("Helvetica", "", 7)
        tw = self.get_string_width(text) + 8
        x = self.get_x()
        y = self.get_y()

        # Check if chip will overflow
        if x + tw > 210 - self.r_margin:
            self.ln(7)
            x = self.l_margin
            y = self.get_y()

        self.set_fill_color(*bg_color)
        self.set_text_color(*text_color)
        self.rect(x, y, tw, 6, "F")
        self.set_xy(x, y)
        self.cell(tw, 6, text, align="C")
        self.set_x(x + tw + 2)

    def progress_bar(self, x: float, y: float, w: float, pct: float,
                     color: tuple):
        """Draw a progress bar."""
        # Track
        self.set_fill_color(*Colors.BORDER)
        self.rect(x, y, w, 4, "F")
        # Fill
        fill_w = max(1, w * min(1.0, pct / 100.0))
        self.set_fill_color(*color)
        self.rect(x, y, fill_w, 4, "F")


# ── Report Generation ─────────────────────────────────────────────────────────

def generate_pdf_report(result: Dict) -> bytes:
    """
    Generate a professional PDF screening report.

    Args:
        result: Full screening result dict from the API.

    Returns:
        bytes: PDF file content as bytes.
    """
    logger.info("Generating PDF screening report...")

    pdf = ScreeningReport()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Decision Banner ────────────────────────────────────────────────────
    decision = result.get("decision", "UNKNOWN")
    is_pass = decision == "SHORTLISTED"
    banner_color = Colors.SUCCESS if is_pass else Colors.DANGER
    banner_icon = "SHORTLISTED" if is_pass else "NOT SHORTLISTED"

    pdf.set_fill_color(*banner_color)
    bx = pdf.l_margin
    by = pdf.get_y()
    pdf.rect(bx, by, 190, 18, "F")
    pdf.set_xy(bx, by + 2)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*Colors.WHITE)
    pdf.cell(190, 8, banner_icon, align="C")
    pdf.set_xy(bx, by + 11)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(190, 5, result.get("reason", ""), align="C")
    pdf.ln(22)

    # ── Score Boxes ────────────────────────────────────────────────────────
    match_score = result.get("match_score", 0)
    ai_score = result.get("ai_score", 0)
    skill_data = result.get("skill_analysis", {})
    skill_pct = skill_data.get("skill_match_pct", 0)

    match_color = Colors.SUCCESS if match_score >= 60 else Colors.WARNING if match_score >= 40 else Colors.DANGER
    ai_color = Colors.SUCCESS if ai_score < 40 else Colors.WARNING if ai_score < 70 else Colors.DANGER
    skill_color = Colors.SUCCESS if skill_pct >= 75 else Colors.WARNING if skill_pct >= 50 else Colors.DANGER

    y = pdf.get_y()
    pdf.score_box("Match Score", f"{match_score:.1f}%", 10, y, 60, match_color)
    pdf.score_box("AI Content", f"{ai_score:.1f}%", 75, y, 60, ai_color)
    pdf.score_box("Skill Coverage", f"{skill_pct:.0f}%", 140, y, 60, skill_color)
    pdf.ln(34)

    # ── Candidate Profile ──────────────────────────────────────────────────
    parsed = result.get("parsed_resume", {})
    contact = parsed.get("contact", {}) if parsed else {}
    stats = parsed.get("stats", {}) if parsed else {}

    if contact.get("name") or contact.get("email"):
        pdf.section_title("\u2709", "Candidate Profile")

        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*Colors.DARK)

        profile_lines = []
        if contact.get("name"):
            profile_lines.append(f"Name: {contact['name']}")
        if contact.get("email"):
            profile_lines.append(f"Email: {contact['email']}")
        if contact.get("phone"):
            profile_lines.append(f"Phone: {contact['phone']}")
        if stats.get("exp_years_est"):
            profile_lines.append(f"Est. Experience: ~{stats['exp_years_est']} years")
        if stats.get("total_words"):
            profile_lines.append(f"Resume Length: {stats['total_words']} words, {stats.get('section_count', 0)} sections")

        for line in profile_lines:
            pdf.cell(0, 5, line)
            pdf.ln(5)
        pdf.ln(2)

    # ── Skills Breakdown ───────────────────────────────────────────────────
    pdf.section_title("\u2705", "Skills Analysis")

    matched = skill_data.get("matched_skills", [])
    missing = skill_data.get("missing_skills", [])

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*Colors.DARK)
    pdf.cell(0, 5, f"Matched Skills ({len(matched)})")
    pdf.ln(6)

    if matched:
        for skill in matched:
            pdf.chip(skill, (236, 253, 245), Colors.SUCCESS)
        pdf.ln(8)
    else:
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(*Colors.MUTED)
        pdf.cell(0, 5, "No matched skills detected")
        pdf.ln(6)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*Colors.DARK)
    pdf.cell(0, 5, f"Missing Skills ({len(missing)})")
    pdf.ln(6)

    if missing:
        for skill in missing:
            pdf.chip(skill, (254, 242, 242), Colors.DANGER)
        pdf.ln(8)
    else:
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(*Colors.SUCCESS)
        pdf.cell(0, 5, "All required skills matched!")
        pdf.ln(6)

    # ── AI Detection Signals ───────────────────────────────────────────────
    ai_details = result.get("details", {}).get("ai", {})
    signal_breakdown = ai_details.get("signal_breakdown", {})

    if signal_breakdown:
        pdf.section_title("\U0001f916", "AI Detection Analysis")

        signal_names = {
            "buzzword_score":      "AI Buzzwords / Boilerplate",
            "fingerprint_score":   "ChatGPT Fingerprint Phrases",
            "hyper_polish_score":  "Hyper-polish / Superlatives",
            "generic_score":       "Generic Bullet Patterns",
            "transition_score":    "Transition Word Overuse",
            "variance_score":      "Sentence Length Uniformity",
            "diversity_score":     "Lexical Diversity",
            "punct_score":         "Punctuation Simplicity",
        }

        for key, label in signal_names.items():
            val = signal_breakdown.get(key, 0)
            bar_color = Colors.DANGER if val >= 60 else Colors.WARNING if val >= 35 else Colors.SUCCESS

            y = pdf.get_y()
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*Colors.DARK)
            pdf.cell(50, 5, label)

            pdf.progress_bar(65, y + 1, 100, val, bar_color)

            pdf.set_xy(168, y)
            pdf.set_font("Helvetica", "B", 8)
            color = Colors.DANGER if val >= 60 else Colors.WARNING if val >= 35 else Colors.SUCCESS
            pdf.set_text_color(*color)
            pdf.cell(20, 5, f"{val:.0f}%", align="R")
            pdf.ln(7)

    # ── Top Keywords ───────────────────────────────────────────────────────
    keywords = result.get("top_keywords", [])
    if keywords:
        pdf.section_title("\U0001f3f7", "Top Matching Keywords")
        for kw in keywords[:10]:
            pdf.chip(kw, (238, 242, 255), (79, 70, 229))
        pdf.ln(8)

    # ── Improvement Tips ───────────────────────────────────────────────────
    tips = result.get("tips", [])
    if tips:
        pdf.section_title("\U0001f4a1", "Improvement Recommendations")

        for i, tip in enumerate(tips[:8], 1):
            skill = tip.get("skill", "")
            tip_text = tip.get("tip", "")
            priority = tip.get("priority", "")

            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*Colors.DARK)
            pdf.cell(0, 5, f"{i}. {skill}")

            if "High" in priority:
                pdf.set_text_color(*Colors.DANGER)
                pdf.set_font("Helvetica", "B", 7)
                pdf.cell(0, 5, "  HIGH PRIORITY")
            pdf.ln(5)

            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*Colors.MUTED)
            pdf.multi_cell(0, 4, tip_text)
            pdf.ln(2)

    # ── General Advice ─────────────────────────────────────────────────────
    advice = result.get("general_advice", [])
    if advice:
        pdf.section_title("\u2728", "General Advice")
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*Colors.DARK)
        for a in advice:
            pdf.multi_cell(0, 4.5, f"  {a}")
            pdf.ln(2)

    # ── Output ─────────────────────────────────────────────────────────────
    pdf_bytes = pdf.output()
    logger.info(f"PDF report generated: {len(pdf_bytes)} bytes")
    return bytes(pdf_bytes)
