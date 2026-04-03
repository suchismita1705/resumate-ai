import streamlit as st
import json
import matplotlib.pyplot as plt

from resume_parser import extract_resume_text, extract_skills
from skill_matcher import find_skill_gap, calculate_ats_score
from recommender import recommend_courses

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

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# =========================
# JOB ROLE SELECT
# =========================
job_role = st.selectbox("Select Job Role", list(skill_data.keys()))

# =========================
# ANALYZE BUTTON
# =========================
if st.button("Analyze Resume"):

    if uploaded_file is not None:

        # Extract resume text
        resume_text = extract_resume_text(uploaded_file)

        # Get JD skills
        jd_skills = skill_data[job_role]["skills"]

        # Extract resume skills
        resume_skills = extract_skills(resume_text, jd_skills)

        # Match + gap
        matched_skills, missing_skills = find_skill_gap(resume_skills, jd_skills)

        # ATS Score
        ats_score = calculate_ats_score(matched_skills, jd_skills)

        # =========================
        # ATS SCORE DISPLAY
        # =========================
        st.markdown("## 📊 ATS Score")
        st.progress(int(ats_score))
        st.success(f"Your ATS Score: {ats_score}%")

        if ats_score >= 80:
            st.success("🔥 Excellent Resume!")
        elif ats_score >= 50:
            st.warning("⚡ Good, but can improve")
        else:
            st.error("❌ Needs improvement — try adding missing skills to your resume")

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

        # =========================
        # PIE CHART
        # =========================
        st.markdown("## 📊 Skill Analysis Chart")

        labels = ['Matched Skills', 'Missing Skills']
        sizes = [len(matched_skills), len(missing_skills)]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')

        st.pyplot(fig)

        # =========================
        # COURSE RECOMMENDATION
        # =========================
        st.markdown("## 📚 Recommended Courses")

        recommendations = recommend_courses(missing_skills)

        if recommendations:
            for skill, course in recommendations.items():
                st.markdown(f"🔹 **{skill.upper()}** → {course}")
        else:
            st.success("No courses needed 🎉")

    else:
        st.warning("Please upload a resume first!")