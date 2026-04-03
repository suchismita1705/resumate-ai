import streamlit as st
import json

from resume_parser import extract_resume_text, extract_skills
from jd_parser import extract_jd_skills
from skill_matcher import find_skill_gap

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="ResuMate AI", page_icon="📄", layout="centered")

st.title("📄 ResuMate AI")
st.subheader("AI-Powered Resume Analyzer")

# =========================
# LOAD SKILLS DATA
# =========================
with open("data/skills.json", "r") as f:
    skill_data = json.load(f)

# Flatten skills list from JSON
skills_list = []
for category in skill_data:
    skills_list.extend(skill_data[category]["roadmap"])

skills_list = [s.lower() for s in skills_list]

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# =========================
# JOB ROLE INPUT
# =========================
job_role = st.selectbox(
    "Select Job Role",
    ["machine learning", "data science", "web development", "data analyst"]
)

# =========================
# ANALYZE BUTTON
# =========================
if st.button("Analyze Resume"):

    if uploaded_file is not None:

        # Extract resume text
        resume_text = extract_resume_text(uploaded_file)

        # Extract skills
        resume_skills = extract_skills(resume_text, skills_list)
        jd_skills = extract_jd_skills(job_role)

        # Find missing skills
        missing_skills = find_skill_gap(resume_skills, jd_skills)

        # =========================
        # ATS SCORE CALCULATION
        # =========================
        matched_skills = list(set(resume_skills) & set(jd_skills))

        if len(jd_skills) > 0:
            ats_score = int((len(matched_skills) / len(jd_skills)) * 100)
        else:
            ats_score = 0

        # =========================
        # DISPLAY RESULTS
        # =========================
        st.markdown("## 📊 ATS Score")
        st.progress(ats_score / 100)
        st.write(f"### {ats_score}% Match")

        # =========================
        # SKILLS DISPLAY
        # =========================
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Matched Skills")
            if matched_skills:
                for skill in matched_skills:
                    st.success(skill)
            else:
                st.warning("No matching skills found")

        with col2:
            st.markdown("### ❌ Missing Skills")
            if missing_skills:
                for skill in missing_skills:
                    st.error(skill)
            else:
                st.success("No missing skills 🎉")

    else:
        st.warning("Please upload a resume first!")