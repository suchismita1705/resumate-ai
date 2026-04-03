import streamlit as st
from resume_parser import extract_resume_text, extract_skills, match_skills
from fpdf import FPDF
import json
import os

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
# JOB ROLE INPUT
# =========================
job_role = st.selectbox("Select Job Role", list(skill_data.keys()))

# =========================
# PROCESS BUTTON
# =========================
if st.button("Analyze Resume"):

    if uploaded_file is not None and job_role:

        # Extract text
        resume_text = extract_resume_text(uploaded_file)

        # Extract skills
        resume_skills = extract_skills(resume_text)

        # Match skills
        score, matched, missing = match_skills(resume_skills, job_role, skill_data)

        # =========================
        # DISPLAY RESULTS
        # =========================
        st.success("Analysis Complete ✅")

        st.markdown("### 📊 Match Score")
        st.progress(score / 100)
        st.write(f"**{score}% match for {job_role}**")

        st.markdown("### ✅ Matched Skills")
        st.write(matched if matched else "No matching skills found")

        st.markdown("### ❌ Missing Skills")
        st.write(missing if missing else "No missing skills 🎉")

        # =========================
        # GENERATE PDF REPORT
        # =========================
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="ResuMate AI Report", ln=True)

        pdf.cell(200, 10, txt=f"Job Role: {job_role}", ln=True)
        pdf.cell(200, 10, txt=f"Score: {score}%", ln=True)

        pdf.cell(200, 10, txt="Matched Skills:", ln=True)
        for skill in matched:
            pdf.cell(200, 10, txt=f"- {skill}", ln=True)

        pdf.cell(200, 10, txt="Missing Skills:", ln=True)
        for skill in missing:
            pdf.cell(200, 10, txt=f"- {skill}", ln=True)

        pdf.output("report.pdf")

        # =========================
        # DOWNLOAD BUTTON
        # =========================
        with open("report.pdf", "rb") as file:
            st.download_button(
                label="📥 Download Report",
                data=file,
                file_name="ResuMate_Report.pdf",
                mime="application/pdf"
            )

    else:
        st.error("⚠️ Please upload a resume and select a job role")