import pdfplumber
import spacy
import os

# =========================
# LOAD SPACY MODEL SAFELY
# =========================
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except:
        # Download model if not present (for Streamlit Cloud)
        os.system("python -m spacy download en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()


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
    "python", "java", "c++", "c", "javascript", "typescript",

    # Web
    "html", "css", "react", "angular", "node", "express",

    # Data / AI
    "machine learning", "deep learning", "nlp", "data science",
    "pandas", "numpy", "tensorflow", "pytorch", "scikit-learn",

    # Tools
    "git", "github", "docker", "kubernetes",

    # Databases
    "sql", "mysql", "postgresql", "mongodb",

    # Cloud
    "aws", "azure", "gcp"
]


# =========================
# EXTRACT SKILLS USING NLP
# =========================
def extract_skills(text):
    doc = nlp(text.lower())
    found_skills = set()

    for token in doc:
        if token.text in SKILL_KEYWORDS:
            found_skills.add(token.text)

    return list(found_skills)


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