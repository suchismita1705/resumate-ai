import pdfplumber
import spacy
from spacy.cli import download


# 🔥 Load spaCy model safely (auto-download if missing)
try:
    nlp = spacy.load("en_core_web_sm")
except:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# 📄 Extract text from PDF
def extract_resume_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


# 🧠 Extract skills using spaCy
def extract_skills(text):
    doc = nlp(text)

    # Basic skill keywords (you can expand later)
    skills_list = [
        "python", "java", "c++", "machine learning", "data science",
        "deep learning", "sql", "html", "css", "javascript",
        "react", "node", "django", "flask", "tensorflow",
        "pandas", "numpy", "opencv", "nlp", "ai"
    ]

    found_skills = []

    for token in doc:
        if token.text.lower() in skills_list:
            found_skills.append(token.text.lower())

    return list(set(found_skills))