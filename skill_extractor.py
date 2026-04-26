
import re
from typing import List, Dict
from logger import get_logger
from utils import clean_text
from config import TECH_SKILLS, SOFT_SKILLS, ALL_SKILLS
logger = get_logger(__name__)
def extract_skills(text: str, skill_list: List[str] = None) -> List[str]:
    if skill_list is None:
        skill_list = ALL_SKILLS
    cleaned = clean_text(text)
    matched = set()
    for skill in skill_list:
        pattern = re.escape(skill.lower())
        if re.search(r'\b' + pattern + r'\b', cleaned):
            matched.add(skill.lower())
    result = sorted(matched)
    logger.debug(f"Extracted {len(result)} skills from text.")
    return result
def compare_skills(resume_text: str, jd_text: str) -> Dict[str, List[str]]:
    resume_skills = set(extract_skills(resume_text))
    jd_skills     = set(extract_skills(jd_text))

    matched_skills = resume_skills & jd_skills
    missing_skills = jd_skills - resume_skills
    extra_skills   = resume_skills - jd_skills

    skill_match_pct = (
        round(len(matched_skills) / len(jd_skills) * 100, 2)
        if jd_skills else 0.0
    )

    logger.info(
        f"Skill comparison: {len(matched_skills)} matched, "
        f"{len(missing_skills)} missing, {len(extra_skills)} extra. "
        f"Coverage: {skill_match_pct:.1f}%"
    )
    matched_tech = [s for s in matched_skills if s in TECH_SKILLS]
    matched_soft = [s for s in matched_skills if s in SOFT_SKILLS]
    matched_other = [s for s in matched_skills if s not in TECH_SKILLS and s not in SOFT_SKILLS]
    missing_tech = [s for s in missing_skills if s in TECH_SKILLS]
    missing_soft = [s for s in missing_skills if s in SOFT_SKILLS]
    return {
        "resume_skills" : sorted(resume_skills),
        "jd_skills"     : sorted(jd_skills),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "extra_skills"  : sorted(extra_skills),
        "skill_match_pct": skill_match_pct,
        "categories": {
            "matched_tech": matched_tech,
            "matched_soft": matched_soft,
            "matched_other": matched_other,
            "missing_tech": missing_tech,
            "missing_soft": missing_soft
        }
    }


def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    
    tech_set = set(TECH_SKILLS)
    soft_set = set(SOFT_SKILLS)

    technical = [s for s in skills if s in tech_set]
    soft      = [s for s in skills if s in soft_set]

    return {"technical": technical, "soft": soft}
