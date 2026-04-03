from resume_parser import extract_resume_text, extract_skills
from jd_parser import extract_jd_skills
from skill_matcher import find_skill_gap, calculate_match_score
from recommender import recommend_courses

# Load skills list
with open("data/skills.txt") as f:
    skills_list = [line.strip().lower() for line in f]

# === INPUT ===
resume_path = input("Enter path of resume PDF: ")
jd_text = input("Enter Job Description: ")

# === PROCESS ===
resume_text = extract_resume_text(resume_path)

resume_skills = extract_skills(resume_text, skills_list)
jd_skills = extract_jd_skills(jd_text, skills_list)

missing_skills = find_skill_gap(resume_skills, jd_skills)
match_score = calculate_match_score(resume_skills, jd_skills)

recommendations = recommend_courses(missing_skills)

# === OUTPUT ===
print("\n===== RESULTS =====")

print("\nResume Skills Found:")
print(resume_skills)

print("\nJob Required Skills:")
print(jd_skills)

print("\nMissing Skills (Skill Gap):")
print(missing_skills)

print("\nMatch Score:")
print(str(match_score) + "%")

print("\nRecommendations:")
for skill, rec in recommendations.items():
    print(f"{skill} → {rec}")