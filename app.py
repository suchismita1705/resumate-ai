import streamlit as st
import json
import os
from fpdf import FPDF

from resume_parser import extract_resume_text, extract_skills
from jd_parser import extract_jd_skills
from skill_matcher import find_skill_gap, calculate_match_score

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="ResuMate AI", layout="centered")

st.title("🚀 ResuMate AI")
st.subheader("Smart Resume Analyzer & Skill Gap Finder")

# ------------------ LOAD DATA ------------------
with open("data/skills.txt") as f:
    skills_list = [line.strip().lower() for line in f]

with open("data/skills.json") as f:
    skill_data = json.load(f)

# ------------------ SKILL NORMALIZATION ------------------
skill_alias = {
    "ml": "machine learning",
    "ai": "machine learning",
    "js": "javascript"
}

def normalize_skills(skills):
    normalized = []
    for skill in skills:
        skill = skill.lower()
        if skill in skill_alias:
            normalized.append(skill_alias[skill])
        else:
            normalized.append(skill)
    return list(set(normalized))

# ------------------ PDF FUNCTION ------------------
def create_pdf(score, have, missing):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="ResuMate AI - Resume Report", ln=True)
    pdf.cell(200, 10, txt=f"Match Score: {score}%", ln=True)

    pdf.cell(200, 10, txt=" ", ln=True)

    pdf.cell(200, 10, txt="Skills You Have:", ln=True)
    pdf.multi_cell(0, 10, ", ".join(have) if have else "None")

    pdf.cell(200, 10, txt=" ", ln=True)

    pdf.cell(200, 10, txt="Missing Skills:", ln=True)
    pdf.multi_cell(0, 10, ", ".join(missing) if missing else "None")

    pdf.output("report.pdf")

# ------------------ INPUT ------------------
resume_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("💼 Enter Job Description or Job Role")

# ------------------ ANALYSIS ------------------
if st.button("🚀 Analyze Resume"):

    if resume_file is not None and jd_text.strip() != "":

        # Save temp file
        with open("temp.pdf", "wb") as f:
            f.write(resume_file.read())

        # Extract
        resume_text = extract_resume_text("temp.pdf")
        resume_skills = extract_skills(resume_text, skills_list)
        jd_skills = extract_jd_skills(jd_text, skills_list)

        # Normalize
        resume_skills = normalize_skills(resume_skills)
        jd_skills = normalize_skills(jd_skills)

        # Analysis
        missing = find_skill_gap(resume_skills, jd_skills)
        score = calculate_match_score(resume_skills, jd_skills)

        # ------------------ OUTPUT ------------------
        st.success("Analysis Complete ✅")

        st.subheader("📊 Match Score")
        st.progress(score / 100)
        st.write(f"### {score}% match")

        st.subheader("✅ Skills You Have")
        st.write(resume_skills if resume_skills else "No skills detected")

        st.subheader("❌ Missing Skills")
        st.write(missing if missing else "No missing skills 🎉")

        # ------------------ SMART ROADMAP ------------------
        st.subheader("📚 Smart Learning Roadmap")

        if missing:
            for skill in missing:
                st.markdown(f"## 🔹 {skill}")

                if skill in skill_data:
                    data = skill_data[skill]

                    st.markdown("### 📘 Roadmap")
                    for step in data.get("roadmap", []):
                        st.write(f"- {step}")

                    st.markdown("### 🚀 Project Idea")
                    st.write(data.get("project", "Build a project using this skill"))

                    st.markdown("### 🔗 Best Resources")
                    for link in data.get("resources", []):
                        st.markdown(f"[Open Resource]({link})")

                else:
                    st.write("Basic learning recommended")
                    st.markdown(f"[🔍 Search {skill}](https://www.google.com/search?q=learn+{skill})")

        else:
            st.write("🎉 You are well matched for this role!")

        # ------------------ PDF DOWNLOAD ------------------
        st.subheader("📥 Download Report")

        if st.button("Generate PDF"):
            create_pdf(score, resume_skills, missing)

            with open("report.pdf", "rb") as file:
                st.download_button(
                    label="📄 Download PDF",
                    data=file,
                    file_name="ResuMate_Report.pdf",
                    mime="application/pdf"
                )

        # Cleanup
        if os.path.exists("temp.pdf"):
            os.remove("temp.pdf")

    else:
        st.error("⚠️ Please upload a resume and enter job role")