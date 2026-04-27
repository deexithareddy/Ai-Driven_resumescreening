"""
api.py
------
Flask REST API for the AI-Powered Resume Screening System.

Endpoints:
    POST /api/screen  — Screen a resume against a job description
    GET  /health      — Health check

Usage:
    python api.py
    # Then POST to http://localhost:5000/api/screen
"""

import jwt
import json
import io
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, Response
from logger import get_logger
from utils import validate_input, redact_pii
from resume_screener import compute_match_score, get_top_matching_terms
from ai_detector import detect_ai_content, detect_ai_sections, detect_ai_sentences
from skill_extractor import compare_skills
from decision_engine import get_decision_summary
from tips_generator import generate_tips, get_general_advice, generate_interview_questions
from resume_parser import parse_resume
from database import (
    save_screening, get_all_screenings, search_screenings, delete_screening, 
    clear_all_screenings, get_screening_stats, export_to_csv, get_screening_by_id,
    get_top_candidates, get_skill_distribution
)
from report_generator import generate_pdf_report
from semantic_matcher import compute_semantic_similarity, is_semantic_available
from domain_classifier import classify_both
from ner_extractor import compare_skills_ner, is_ner_available
from config import JWT_SECRET_KEY, ADMIN_PASSWORD, JWT_EXPIRATION_HOURS

logger = get_logger(__name__)

app = Flask(__name__, static_folder="frontend", static_url_path="/")
app.config["JSON_SORT_KEYS"] = False
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload

@app.route("/", methods=["GET"])
def index():
    """Serve the frontend index.html."""
    return app.send_static_file("index.html")


# ── Security Decorator (Pro) ──────────────────────────────────────────────────

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"success": False, "error": "Token is missing."}), 401

        try:
            jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return jsonify({"success": False, "error": "Token is invalid or expired."}), 401

        return f(*args, **kwargs)
    return decorated


# ── Authentication (Pro) ──────────────────────────────────────────────────────

@app.route("/api/login", methods=["POST"])
def login():
    """Authenticates a recruiter and returns a JWT token."""
    data = request.get_json(silent=True)
    if not data or "password" not in data:
        return error_response("Password is required.", 400)

    if data["password"] == ADMIN_PASSWORD:
        token = jwt.encode({
            "user": "admin",
            "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
        }, JWT_SECRET_KEY, algorithm="HS256")
        
        return jsonify({
            "success": True, 
            "token": token,
            "expires_in_hours": JWT_EXPIRATION_HOURS
        }), 200
        
    return error_response("Invalid credentials.", 401)


# ── Helper ─────────────────────────────────────────────────────────────────────

def error_response(message: str, status_code: int = 400):
    """Return a standardized JSON error response."""
    logger.warning(f"API error ({status_code}): {message}")
    return jsonify({"success": False, "error": message}), status_code


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.

    Returns:
        200 OK with system status.
    """
    return jsonify({
        "success": True,
        "status": "healthy",
        "service": "AI Resume Screening System",
        "version": "1.0.0",
    }), 200


@app.route("/api/screen", methods=["POST"])
def screen_resume():
    """
    Screen a resume against a job description.

    Request Body (JSON):
        {
            "resume": "<resume text>",
            "job_description": "<job description text>"
        }

    Returns:
        200 OK with full screening result:
        {
            "success": true,
            "match_score": 72.45,
            "ai_score": 35.20,
            "decision": "SHORTLISTED",
            "reason": "...",
            "skill_analysis": {...},
            "top_keywords": [...],
            "details": {...}
        }

    Error Codes:
        400 — Missing or invalid input
        422 — Input too short or empty after cleaning
        500 — Internal server error
    """
    logger.info(f"POST /api/screen — Request received from {request.remote_addr}")

    # ── Parse JSON Body ────────────────────────────────────────────────────
    if not request.is_json:
        return error_response("Request Content-Type must be application/json.", 415)

    data = request.get_json(silent=True)
    if data is None:
        return error_response("Invalid JSON body.", 400)

    resume_text = data.get("resume", "").strip()
    jd_text     = data.get("job_description", "").strip()

    # ── Custom Thresholds (optional) ──────────────────────────────────────
    from config import MATCH_SCORE_THRESHOLD, AI_SCORE_THRESHOLD
    match_threshold = data.get("match_threshold", MATCH_SCORE_THRESHOLD)
    ai_threshold    = data.get("ai_threshold", AI_SCORE_THRESHOLD)

    try:
        match_threshold = float(match_threshold)
        ai_threshold    = float(ai_threshold)
        match_threshold = max(0, min(100, match_threshold))
        ai_threshold    = max(0, min(100, ai_threshold))
    except (TypeError, ValueError):
        match_threshold = MATCH_SCORE_THRESHOLD
        ai_threshold    = AI_SCORE_THRESHOLD

    # ── Validate Inputs ────────────────────────────────────────────────────
    if not resume_text:
        return error_response("Field 'resume' is required and cannot be empty.", 400)
    if not jd_text:
        return error_response("Field 'job_description' is required and cannot be empty.", 400)

    if not validate_input(resume_text, "Resume"):
        return error_response("Resume text is too short (minimum 10 words required).", 422)
    if not validate_input(jd_text, "Job Description"):
        return error_response("Job description text is too short (minimum 10 words required).", 422)

    # ── Run Screening Pipeline ─────────────────────────────────────────────
    try:
        tfidf_score, match_details = compute_match_score(resume_text, jd_text)
        ai_score, ai_details       = detect_ai_content(resume_text)
        skill_data                 = compare_skills(resume_text, jd_text)
        top_terms                  = get_top_matching_terms(resume_text, jd_text, top_n=10)
        ai_sections                = detect_ai_sections(resume_text)
        sentence_analysis          = detect_ai_sentences(resume_text)
        print(f"SENTENCE ANALYSIS: {sentence_analysis}")
        print(f"DEBUG sentence_analysis: {len(sentence_analysis)} sentences | levels: {[s['level'] for s in sentence_analysis]}")
        parsed_resume              = parse_resume(resume_text, jd_text)

        # ── Semantic Similarity (Sentence-BERT) ───────────────────────────
        try:
            semantic_score, semantic_details = compute_semantic_similarity(resume_text, jd_text)
            match_method = semantic_details.get("method", "tfidf-fallback")
        except Exception as e:
            logger.warning(f"Semantic matching failed: {e}. Using TF-IDF only.")
            semantic_score = tfidf_score
            semantic_details = {"method": "tfidf-fallback", "error": str(e)}
            match_method = "tfidf-fallback"

        # ── Domain Classification ─────────────────────────────────────────
        try:
            domain_info = classify_both(resume_text, jd_text)
        except Exception as e:
            logger.warning(f"Domain classification failed: {e}")
            domain_info = {"primary": {"domain": "general", "label": "General", "icon": "📄", "is_general": True}, "candidate": None, "domain_match": True}

        # ── NER-based Skill Extraction ────────────────────────────────────
        try:
            ner_skill_data = compare_skills_ner(resume_text, jd_text)
            # Merge NER skills with keyword-based skills
            all_matched = sorted(set(skill_data.get("matched_skills", []) + ner_skill_data.get("matched_skills", [])))
            all_missing = sorted(set(skill_data.get("missing_skills", []) + ner_skill_data.get("missing_skills", [])) - set(all_matched))
            all_jd_skills = sorted(set(skill_data.get("jd_skills", []) + ner_skill_data.get("jd_skills", [])))
            skill_data["matched_skills"] = all_matched
            skill_data["missing_skills"] = all_missing
            skill_data["jd_skills"]      = all_jd_skills
            if all_jd_skills:
                skill_data["skill_match_pct"] = round(len(all_matched) / len(all_jd_skills) * 100, 2)
            skill_data["ner_method"]      = ner_skill_data.get("ner_method", "regex")
            skill_data["resume_years_exp"] = ner_skill_data.get("resume_years_exp")
            skill_data["jd_years_exp"]     = ner_skill_data.get("jd_years_exp")
        except Exception as e:
            logger.warning(f"NER skill extraction failed: {e}. Using keyword-only skills.")

        # ── Match Score: Combine Semantic + Skill Coverage ─────────────
        # When Sentence-BERT is available, use it as the primary match signal.
        # Skill coverage is blended in to reward exact skill matches.
        jd_skills_raw       = skill_data.get("jd_skills", [])
        skill_match_pct_raw = skill_data.get("skill_match_pct", tfidf_score)

        if match_method == "sentence-bert" and jd_skills_raw:
            # 60% semantic + 35% skill coverage + 5% TF-IDF bonus
            match_score = round(min(100.0,
                0.60 * semantic_score +
                0.35 * skill_match_pct_raw +
                0.05 * tfidf_score
            ), 2)
        elif jd_skills_raw:
            tfidf_bonus = tfidf_score * 0.05
            match_score = round(min(100.0, skill_match_pct_raw + tfidf_bonus), 2)
        else:
            match_score = semantic_score if match_method == "sentence-bert" else tfidf_score

        match_details["skill_match_pct"]  = skill_match_pct_raw
        match_details["tfidf_score"]      = tfidf_score
        match_details["semantic_score"]   = semantic_score
        match_details["match_method"]     = match_method
        match_details["final_score"]      = match_score

        result                     = get_decision_summary(
            match_score, ai_score, match_details, ai_details, skill_data,
            match_threshold=match_threshold, ai_threshold=ai_threshold
        )

        missing_skills  = skill_data.get("missing_skills", [])
        tips            = generate_tips(missing_skills, match_score)
        
        # ── Interview Intelligence (Pro) ──────────────────────────────────
        interview_questions = generate_interview_questions(missing_skills)
        
        jd_skills       = skill_data.get("jd_skills", [])
        skill_coverage  = (len(skill_data.get("matched_skills", [])) / len(jd_skills) * 100) if jd_skills else 100
        general_advice  = get_general_advice(match_score, ai_score, skill_coverage)

    except ValueError as e:
        return error_response(str(e), 422)
    except Exception as e:
        logger.exception(f"Unexpected error during screening: {e}")
        return error_response("Internal server error during screening.", 500)

    # ── Build Response ─────────────────────────────────────────────────────
    response = {
        "success"       : True,
        "match_score"   : result["match_score"],
        "ai_score"      : result["ai_score"],
        "decision"      : result["decision"],
        "reason"        : result["reason"],
        "match_passed"  : result["match_passed"],
        "ai_passed"     : result["ai_passed"],
        "skill_analysis": result["skill_analysis"],
        "top_keywords"  : top_terms,
        "ai_sections"   : ai_sections,
        "sentence_analysis": sentence_analysis,
        "parsed_resume" : parsed_resume,
        "thresholds"    : result["thresholds"],
        "details"       : {
            "match": result["match_details"],
            "ai"   : result["ai_details"],
        },
        "tips"          : tips,
        "interview_questions": interview_questions,
        "general_advice": general_advice,
        "domain"        : domain_info,
        "match_method"  : match_method,
        "semantic_score" : semantic_score,
    }

    # ── Blind Hiring Mode (Pro) ──────────────────────────────────────────
    if data.get("blind_mode"):
        logger.info("Blind Hiring Mode enabled — redacting PII from response.")
        candidate_name = response.get("parsed_resume", {}).get("contact", {}).get("name")
        
        # Redact contact info
        if "parsed_resume" in response and "contact" in response["parsed_resume"]:
            contact = response["parsed_resume"]["contact"]
            for key in ["name", "email", "phone", "linkedin", "github"]:
                if contact.get(key):
                    contact[key] = "[REDACTED]"
        
        # Redact occurrences in reason and advice
        response["reason"] = redact_pii(response["reason"], name=candidate_name)
        response["general_advice"] = [redact_pii(a, name=candidate_name) for a in response["general_advice"]]

    # Auto-save to database
    try:
        db_id = save_screening(response)
        response["db_id"] = db_id
    except Exception as e:
        logger.warning(f"Failed to auto-save screening to DB: {e}")

    logger.info(
        f"Screening complete: match={match_score:.2f}%, "
        f"ai={ai_score:.2f}%, decision={result['decision']}"
    )
    return jsonify(response), 200


# ── File Upload ────────────────────────────────────────────────────────────────

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_storage):
    """Extract plain text from an uploaded file (PDF, DOCX, TXT)."""
    filename = file_storage.filename.lower()
    file_bytes = file_storage.read()

    if filename.endswith('.txt'):
        return file_bytes.decode('utf-8', errors='replace')

    elif filename.endswith('.pdf'):
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return '\n'.join(text_parts)
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            raise ValueError(f"Could not extract text from PDF: {e}")

    elif filename.endswith('.docx') or filename.endswith('.doc'):
        try:
            from docx import Document
            doc = Document(io.BytesIO(file_bytes))
            text_parts = [para.text for para in doc.paragraphs if para.text.strip()]
            return '\n'.join(text_parts)
        except Exception as e:
            logger.error(f"DOCX extraction failed: {e}")
            raise ValueError(f"Could not extract text from DOCX: {e}")

    else:
        raise ValueError(f"Unsupported file type: {filename}")


@app.route("/api/upload", methods=["POST"])
def upload_file():
    """
    Upload a resume file (PDF, DOCX, TXT) and extract its text.

    Returns:
        200 OK with { "success": true, "text": "<extracted text>" }
    """
    if 'file' not in request.files:
        return error_response("No file provided. Use 'file' field.", 400)

    file = request.files['file']
    if file.filename == '':
        return error_response("No file selected.", 400)

    if not allowed_file(file.filename):
        return error_response(
            f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}", 415
        )

    try:
        text = extract_text_from_file(file)
        if not text or len(text.strip()) < 20:
            return error_response("Could not extract meaningful text from the file.", 422)

        logger.info(f"File uploaded: {file.filename} — {len(text)} chars extracted.")
        return jsonify({"success": True, "text": text.strip(), "filename": file.filename}), 200

    except ValueError as e:
        return error_response(str(e), 422)
    except Exception as e:
        logger.exception(f"File upload error: {e}")
        return error_response("Failed to process the uploaded file.", 500)


# ── Email Notification ─────────────────────────────────────────────────────────

@app.route("/api/send-email", methods=["POST"])
def send_email():
    """
    Send screening results to a candidate via email.

    Request Body (JSON):
        {
            "to_email": "candidate@example.com",
            "candidate_name": "John Doe",
            "decision": "SHORTLISTED",
            "match_score": 72.5,
            "ai_score": 35.2,
            "reason": "Candidate meets all criteria",
            "matched_skills": ["python", "react"],
            "missing_skills": ["docker"],
            "tips": [{"skill": "docker", "tip": "..."}],
            "general_advice": ["..."]
        }
    """
    from config import SMTP_EMAIL, SMTP_PASSWORD

    if not request.is_json:
        return error_response("Request Content-Type must be application/json.", 415)

    data = request.get_json(silent=True)
    if data is None:
        return error_response("Invalid JSON body.", 400)

    to_email        = data.get("to_email", "").strip()
    candidate_name  = data.get("candidate_name", "Candidate").strip()
    decision        = data.get("decision", "")
    match_score     = data.get("match_score", 0)
    ai_score        = data.get("ai_score", 0)
    reason          = data.get("reason", "")
    matched_skills  = data.get("matched_skills", [])
    missing_skills  = data.get("missing_skills", [])
    tips            = data.get("tips", [])
    general_advice  = data.get("general_advice", [])

    if not to_email:
        return error_response("Field 'to_email' is required.", 400)
    if not decision:
        return error_response("Field 'decision' is required.", 400)

    smtp_email    = SMTP_EMAIL
    smtp_password = SMTP_PASSWORD

    if not smtp_email or not smtp_password:
        return error_response("SMTP credentials not configured on server.", 500)

    is_accepted  = decision == "SHORTLISTED"
    status_color = "#059669" if is_accepted else "#dc2626"
    status_label = "SHORTLISTED &#9989;" if is_accepted else "NOT SHORTLISTED &#10060;"
    status_msg   = (
        "Congratulations! Your profile has been shortlisted for the next round."
        if is_accepted else
        "Thank you for your application. Unfortunately, your profile was not shortlisted at this time."
    )

    try:
        m_score = float(match_score)
        a_score = float(ai_score)
    except (TypeError, ValueError):
        m_score = 0.0
        a_score = 0.0

    m_score_str = f"{m_score:.1f}%"
    a_score_str = f"{a_score:.1f}%"

    matched_html = "".join(
        f'<span style="display:inline-block;background:#ecfdf5;color:#059669;border:1px solid #a7f3d0;border-radius:20px;padding:4px 12px;margin:3px;font-size:12px;font-weight:600">{s}</span>'
        for s in matched_skills
    ) or '<span style="color:#94a3b8;font-size:13px">None detected</span>'

    missing_html = "".join(
        f'<span style="display:inline-block;background:#fef2f2;color:#dc2626;border:1px solid #fecaca;border-radius:20px;padding:4px 12px;margin:3px;font-size:12px;font-weight:600">{s}</span>'
        for s in missing_skills
    ) or '<span style="color:#059669;font-size:13px">All skills matched! &#9989;</span>'

    tips_html = ""
    for tip in tips[:5]:
        tips_html += f'''
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;margin-bottom:8px">
            <strong style="color:#1e293b">{tip.get("skill", "")}</strong>
            <span style="font-size:10px;background:#fffbeb;color:#d97706;border-radius:10px;padding:2px 6px;margin-left:6px">{tip.get("priority", "")}</span>
            <div style="color:#64748b;font-size:13px;margin-top:4px">{tip.get("tip", "")}</div>
        </div>'''

    advice_html = "".join(
        f'<div style="color:#334155;font-size:14px;padding:6px 0">{a}</div>'
        for a in general_advice
    )

    tips_block = (
        f"<h3 style='color:#1e293b;font-size:15px;margin:0 0 10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px'>&#128203; Improvement Tips</h3>{tips_html}<div style='margin-bottom:20px'></div>"
        if tips_html else ""
    )
    advice_block = (
        f"<h3 style='color:#1e293b;font-size:15px;margin:0 0 10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px'>&#128161; General Advice</h3>{advice_html}<div style='margin-bottom:20px'></div>"
        if advice_html else ""
    )

    html_body = f"""
    <div style="max-width:600px;margin:0 auto;font-family:'Segoe UI',Arial,sans-serif;background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;overflow:hidden">
        <div style="background:linear-gradient(135deg,#2563eb,#1d4ed8);padding:32px 28px;text-align:center">
            <h1 style="color:#ffffff;margin:0;font-size:24px;font-weight:800">AI Driven Resume Screening</h1>
            <p style="color:rgba(255,255,255,0.8);margin:8px 0 0;font-size:14px">Screening Results Notification</p>
        </div>
        <div style="padding:28px">
            <p style="color:#334155;font-size:15px;line-height:1.6;margin:0 0 20px">Dear <strong>{candidate_name}</strong>,</p>
            <p style="color:#334155;font-size:15px;line-height:1.6;margin:0 0 24px">{status_msg}</p>
            <div style="background:{status_color};color:#fff;border-radius:12px;padding:20px;text-align:center;margin-bottom:24px">
                <div style="font-size:28px;font-weight:800;letter-spacing:1px">{status_label}</div>
                <div style="font-size:13px;opacity:0.9;margin-top:4px">{reason}</div>
            </div>
            <div style="display:flex;gap:12px;margin-bottom:24px">
                <div style="flex:1;background:#f0f9ff;border:1px solid #bae6fd;border-radius:12px;padding:16px;text-align:center">
                    <div style="font-size:11px;font-weight:700;color:#0369a1;text-transform:uppercase;letter-spacing:1px">Match Score</div>
                    <div style="font-size:32px;font-weight:800;color:#2563eb;margin-top:4px">{m_score_str}</div>
                </div>
                <div style="flex:1;background:#fffbeb;border:1px solid #fde68a;border-radius:12px;padding:16px;text-align:center">
                    <div style="font-size:11px;font-weight:700;color:#92400e;text-transform:uppercase;letter-spacing:1px">AI Content</div>
                    <div style="font-size:32px;font-weight:800;color:#d97706;margin-top:4px">{a_score_str}</div>
                </div>
            </div>
            <h3 style="color:#1e293b;font-size:15px;margin:0 0 10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px">&#9989; Matched Skills</h3>
            <div style="margin-bottom:20px">{matched_html}</div>
            <h3 style="color:#1e293b;font-size:15px;margin:0 0 10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px">&#9888; Skills to Improve</h3>
            <div style="margin-bottom:20px">{missing_html}</div>
            {tips_block}
            {advice_block}
        </div>
        <div style="background:#f8fafc;border-top:1px solid #e2e8f0;padding:16px 28px;text-align:center">
            <p style="color:#94a3b8;font-size:12px;margin:0">Sent by AI Driven Resume Screening - Intelligent Screening Engine</p>
        </div>
    </div>
    """

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Resume Screening Result: {decision}"
        msg["From"]    = smtp_email
        msg["To"]      = to_email
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, to_email, msg.as_string())

        logger.info(f"Email sent to {to_email} — Decision: {decision}")
        return jsonify({"success": True, "message": f"Email sent successfully to {to_email}"}), 200

    except smtplib.SMTPAuthenticationError:
        return error_response("SMTP authentication failed. Check your Gmail and App Password in config.py.", 401)
    except Exception as e:
        logger.exception(f"Email send error: {e}")
        return error_response(f"Failed to send email: {str(e)}", 500)



# ── Database History ───────────────────────────────────────────────────────────

@app.route("/api/history", methods=["GET"])
@token_required
def get_history():
    """Get screening history from the database (Protected)."""
    limit = request.args.get("limit", 100, type=int)
    offset = request.args.get("offset", 0, type=int)
    query = request.args.get("q", "").strip()

    if query:
        results = search_screenings(query, limit=limit)
    else:
        results = get_all_screenings(limit=limit, offset=offset)

    return jsonify({"success": True, "count": len(results), "screenings": results}), 200


@app.route("/api/history/stats", methods=["GET"])
def get_history_stats():
    """Get aggregate screening statistics."""
    stats = get_screening_stats()
    return jsonify({"success": True, **stats}), 200


@app.route("/api/history/<int:screening_id>", methods=["DELETE"])
@token_required
def delete_history_item(screening_id):
    """Delete a single screening from history (Protected)."""
    if delete_screening(screening_id):
        return jsonify({"success": True, "message": f"Screening #{screening_id} deleted."}), 200
    return error_response(f"Screening #{screening_id} not found.", 404)


@app.route("/api/history/clear", methods=["DELETE"])
@token_required
def clear_history():
    """Clear all screening history (Protected)."""
    count = clear_all_screenings()
    return jsonify({"success": True, "message": f"Cleared {count} screenings."}), 200


# ── Pro Analytics Endpoints (Pro) ─────────────────────────────────────────────

@app.route("/api/analytics", methods=["GET"])
@token_required
def get_pro_analytics():
    """Returns company-wide skill distribution and trends."""
    distribution = get_skill_distribution()
    stats = get_screening_stats()
    return jsonify({
        "success": True,
        "distribution": distribution,
        "overview": stats
    }), 200


@app.route("/api/ranking", methods=["GET"])
@token_required
def get_ranking():
    """Returns the top-performing candidates across all screenings."""
    limit = request.args.get("limit", 10, type=int)
    rankings = get_top_candidates(limit=limit)
    return jsonify({
        "success": True,
        "count": len(rankings),
        "rankings": rankings
    }), 200


# ── Export ─────────────────────────────────────────────────────────────────────

@app.route("/api/export/csv", methods=["GET"])
def export_csv():
    """Export all screenings as a CSV file download."""
    csv_content = export_to_csv()
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=screenings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
    )


@app.route("/api/export/pdf", methods=["POST"])
def export_pdf():
    """Generate a PDF report from screening results."""
    if not request.is_json:
        return error_response("Request Content-Type must be application/json.", 415)

    data = request.get_json(silent=True)
    if not data:
        return error_response("Invalid JSON body.", 400)

    try:
        pdf_bytes = generate_pdf_report(data)
        candidate_name = (data.get("parsed_resume", {}).get("contact", {}).get("name") or "candidate").replace(" ", "_")
        filename = f"screening_report_{candidate_name}_{datetime.now().strftime('%Y%m%d')}.pdf"

        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.exception(f"PDF generation failed: {e}")
        return error_response(f"PDF generation failed: {str(e)}", 500)


@app.errorhandler(404)
def not_found(e):
    return error_response(f"Endpoint not found: {request.path}", 404)


@app.errorhandler(405)
def method_not_allowed(e):
    return error_response(f"Method {request.method} not allowed on {request.path}.", 405)


# ── Run ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logger.info("Starting Flask API server on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
