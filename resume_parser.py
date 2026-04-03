import pdfplumber
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from resume PDF
def extract_resume_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

# Function to extract skills from text
def extract_skills(text, skills_list):
    doc = nlp(text.lower())
    found_skills = []

    for token in doc:
        if token.text in skills_list:
            found_skills.append(token.text)

    return list(set(found_skills))