# =========================
# SKILL MATCHING FUNCTIONS
# =========================

def find_skill_gap(resume_skills, jd_skills):
    resume_set = set([s.lower() for s in resume_skills])
    jd_set = set([s.lower() for s in jd_skills])

    matched = list(resume_set & jd_set)
    missing = list(jd_set - resume_set)

    return matched, missing


# =========================
# ATS SCORE FUNCTION
# =========================

def calculate_ats_score(matched_skills, jd_skills):
    if len(jd_skills) == 0:
        return 0

    score = (len(matched_skills) / len(jd_skills)) * 100
    return round(score, 2)