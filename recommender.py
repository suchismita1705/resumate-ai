# =========================
# COURSE RECOMMENDER
# =========================

def recommend_courses(missing_skills):
    recommendations = {}

    for skill in missing_skills:
        recommendations[skill] = f"Search online courses to learn {skill}"

    return recommendations