# Function to extract skills from Job Description
def extract_jd_skills(jd_text, skills_list):
    jd_text = jd_text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in jd_text:
            found_skills.append(skill)

    return found_skills