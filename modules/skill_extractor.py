
import re

SKILL_LIST = [
    "python",
    "java",
    "c++",
    "c",
    "javascript",
    "html",
    "css",
    "react",
    "node.js",
    "flask",
    "django",
    "sql",
    "mysql",
    "mongodb",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "natural language processing",
    "tensorflow",
    "pytorch",
    "data analysis",
    "power bi",
    "excel",
    "aws",
    "docker",
    "git",
    "github",
    "data structures",
    "algorithms",
    "rest api",
    "streamlit"
]


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILL_LIST:
        pattern = (
            r"(?<![a-z0-9+#.])"
            + re.escape(skill.lower())
            + r"(?![a-z0-9+#.])"
        )

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))
