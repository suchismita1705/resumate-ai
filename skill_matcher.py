# Function to find missing skills (skill gap)
def find_skill_gap(resume_skills, jd_skills):
    missing_skills = []

    for skill in jd_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)

    return missing_skills


# Function to calculate match score
def calculate_match_score(resume_skills, jd_skills):
    if len(jd_skills) == 0:
        return 0

    matched = 0

    for skill in jd_skills:
        if skill in resume_skills:
            matched += 1

    score = (matched / len(jd_skills)) * 100
    return round(score, 2)