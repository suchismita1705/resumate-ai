import pdfplumber

# =========================
# EXTRACT TEXT FROM PDF
# =========================
def extract_resume_text(uploaded_file):
    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


# =========================
# SKILL KEYWORDS LIST
# =========================
SKILL_KEYWORDS = [
    # Programming
    "python", "java", "c++", "c", "javascript",

    # Web
    "html", "css", "react", "angular", "node", "express",

    # Data / AI
    "machine learning", "deep learning", "nlp",
    "pandas", "numpy", "tensorflow", "pytorch",

    # Tools
    "git", "github", "docker",

    # Databases
    "sql", "mysql", "mongodb",

    # Cloud
    "aws", "azure"
]


# =========================
# EXTRACT SKILLS (NO SPACY)
# =========================
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILL_KEYWORDS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


# =========================
# MATCH SKILLS WITH JOB ROLE
# =========================
def match_skills(resume_skills, job_role, skill_data):
    job_role = job_role.lower()

    if job_role not in skill_data:
        return 0, [], []

    required_skills = skill_data[job_role]

    matched = []
    missing = []

    for skill in required_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    score = int((len(matched) / len(required_skills)) * 100)

    return score, matched, missing