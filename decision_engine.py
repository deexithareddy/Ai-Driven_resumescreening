"""
decision_engine.py
------------------
Decision Engine for the AI Resume Screening System.

Applies business rules to determine whether a candidate should be
shortlisted based on their match score and AI content likelihood.
"""

from typing import Dict
from logger import get_logger
from config import MATCH_SCORE_THRESHOLD, AI_SCORE_THRESHOLD

logger = get_logger(__name__)

# ── Decision Labels ────────────────────────────────────────────────────────────
DECISION_SHORTLISTED     = "SHORTLISTED"
DECISION_NOT_SHORTLISTED = "NOT SHORTLISTED"

# ── Rejection Reasons ──────────────────────────────────────────────────────────
REASON_LOW_MATCH    = f"Match score below threshold ({MATCH_SCORE_THRESHOLD}%)"
REASON_HIGH_AI      = f"AI content likelihood above threshold ({AI_SCORE_THRESHOLD}%)"
REASON_BOTH_FAILED  = f"Both match score and AI score failed thresholds"
REASON_SHORTLISTED  = "Candidate meets all criteria"


def make_decision(
    match_score: float,
    ai_score: float,
    match_threshold: float = MATCH_SCORE_THRESHOLD,
    ai_threshold: float = AI_SCORE_THRESHOLD,
) -> Dict[str, str]:
    """
    Apply the shortlisting decision rules.

    Args:
        match_score (float): Resume-JD similarity score (0-100).
        ai_score (float): AI content likelihood score (0-100).
        match_threshold (float): Custom match threshold (default from config).
        ai_threshold (float): Custom AI threshold (default from config).

    Returns:
        dict with keys: 'decision', 'reason', 'match_passed', 'ai_passed'
    """
    logger.info(f"Evaluating decision: match={match_score:.2f}%, ai={ai_score:.2f}%")

    match_passed = match_score > match_threshold
    ai_passed    = ai_score < ai_threshold

    reason_low_match   = f"Match score below threshold ({match_threshold}%)"
    reason_high_ai     = f"AI content likelihood above threshold ({ai_threshold}%)"
    reason_both_failed = "Both match score and AI score failed thresholds"

    if match_passed and ai_passed:
        decision = DECISION_SHORTLISTED
        reason   = REASON_SHORTLISTED
    elif not match_passed and not ai_passed:
        decision = DECISION_NOT_SHORTLISTED
        reason   = reason_both_failed
    elif not match_passed:
        decision = DECISION_NOT_SHORTLISTED
        reason   = reason_low_match
    else:
        decision = DECISION_NOT_SHORTLISTED
        reason   = reason_high_ai

    # ── Confidence Level ──────────────────────────────────────────
    # How confident are we in this decision?
    score_margin = abs(match_score - match_threshold)
    ai_margin    = abs(ai_score - ai_threshold)
    avg_margin   = (score_margin + ai_margin) / 2

    if avg_margin >= 20:
        confidence = "High"
    elif avg_margin >= 8:
        confidence = "Medium"
    else:
        confidence = "Low"

    logger.info(f"Decision: {decision} | Reason: {reason} | Confidence: {confidence}")

    return {
        "decision"     : decision,
        "reason"       : reason,
        "confidence"   : confidence,
        "match_passed" : match_passed,
        "ai_passed"    : ai_passed,
    }


def get_decision_summary(
    match_score: float,
    ai_score: float,
    match_details: dict,
    ai_details: dict,
    skill_data: dict,
    match_threshold: float = MATCH_SCORE_THRESHOLD,
    ai_threshold: float = AI_SCORE_THRESHOLD,
) -> Dict:
    """
    Compile a full screening result summary.

    Args:
        match_score (float): Resume-JD match score.
        ai_score (float): AI content likelihood score.
        match_details (dict): Diagnostic info from resume_screener.
        ai_details (dict): Diagnostic info from ai_detector.
        skill_data (dict): Skill comparison results.
        match_threshold (float): Custom match threshold.
        ai_threshold (float): Custom AI threshold.

    Returns:
        dict: Complete structured result for display or API response.
    """
    decision_result = make_decision(match_score, ai_score, match_threshold, ai_threshold)

    return {
        "match_score"     : match_score,
        "ai_score"        : ai_score,
        "decision"        : decision_result["decision"],
        "reason"          : decision_result["reason"],
        "confidence"      : decision_result["confidence"],
        "match_passed"    : decision_result["match_passed"],
        "ai_passed"       : decision_result["ai_passed"],
        "match_details"   : match_details,
        "ai_details"      : ai_details,
        "skill_analysis"  : skill_data,
        "thresholds"      : {
            "match_threshold": match_threshold,
            "ai_threshold"   : ai_threshold,
        },
    }
