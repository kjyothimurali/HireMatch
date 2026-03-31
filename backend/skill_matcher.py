# -------- SKILL DATABASE --------
role_skills = {
    "IT": [
        "python", "java", "sql", "machine learning", "data analysis",
        "html", "css", "javascript", "cloud", "aws", "git"
    ],
    
    "Finance": [
        "accounting", "excel", "financial analysis", "tax", "audit",
        "budgeting", "forecasting"
    ],
    
    "Healthcare": [
        "patient care", "clinical skills", "nursing", "medical knowledge",
        "diagnosis", "treatment"
    ],
    
    "Sales & Marketing": [
        "sales", "marketing", "communication", "negotiation",
        "seo", "branding", "lead generation"
    ]
}

def extract_skills(text, sector):
    text = text.lower()
    
    skills = role_skills.get(sector, [])
    
    found_skills = []
    
    for skill in skills:
        if skill in text:
            found_skills.append(skill)
    
    return found_skills

def match_skills(text, sector):
    extracted = extract_skills(text, sector)
    required = role_skills.get(sector, [])
    
    missing = list(set(required) - set(extracted))
    
    # Limit to top 5 only
    missing = missing[:5]
    match_score = len(extracted) / len(required) * 100
    print(f"Skill Match Score: {match_score:.2f}%")
    return extracted, missing

def suggest_improvements(missing_skills):
    suggestions = []

    skill_guidance = {
        "python": "Practice Python through projects (e.g., build APIs using Flask/Django)",
        "java": "Learn Java fundamentals and build backend applications using Spring Boot",
        "sql": "Practice SQL queries on platforms like LeetCode or HackerRank",
        "machine learning": "Take ML courses and build models using scikit-learn",
        "html": "Build simple websites to understand structure and semantics",
        "css": "Learn styling and responsive design using Flexbox and Grid",
        "javascript": "Build interactive web apps using JavaScript and DOM manipulation",
        "aws": "Learn AWS basics and deploy small projects using EC2/S3",
        "git": "Use GitHub regularly and practice version control in projects",
        "excel": "Practice data analysis using Excel functions and pivot tables",
        "financial analysis": "Learn financial modeling and ratio analysis",
        "marketing": "Work on real campaigns or learn digital marketing tools like Google Ads",
        "seo": "Practice SEO by optimizing websites and learning keyword strategies",
        "communication": "Improve through presentations, group discussions, and mock interviews"
    }

    for skill in missing_skills:
        if skill in skill_guidance:
            suggestions.append(skill_guidance[skill])
        else:
            suggestions.append(f"Gain practical experience in {skill} through real-world projects")

    return suggestions
if __name__ == "__main__":

    text = "I have experience in python, sql and machine learning"

    sector = "IT"

    matched, missing = match_skills(text, sector)

    print("Matched Skills:", matched)
    print("Missing Skills:", missing)
    print("Suggestions:", suggest_improvements(missing))
