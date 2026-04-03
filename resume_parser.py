import pdfplumber

# =========================
# EXTRACT TEXT FROM PDF
# =========================
def extract_resume_text(uploaded_file):
    text = ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print("Error reading PDF:", e)

    return text.lower()


# =========================
# EXTRACT SKILLS
# =========================
def extract_skills(text, skills_list):
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))