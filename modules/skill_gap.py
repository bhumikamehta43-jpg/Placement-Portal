
def analyze_skill_gap(student_skills, required_skills):
    """
    Compare student skills with job requirements.
    Return matched skills, missing skills and coverage.
    """

    student_set = {
        skill.strip().lower()
        for skill in student_skills
        if skill.strip()
    }

    required_set = {
        skill.strip().lower()
        for skill in required_skills
        if skill.strip()
    }

    matched = sorted(student_set & required_set)
    missing = sorted(required_set - student_set)

    if required_set:
        coverage = round(
            len(matched) / len(required_set) * 100,
            2
        )
    else:
        coverage = 0.0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_coverage": coverage
    }
    
    
LEARNING_RESOURCES = {
    "python": [
        "Python syntax and data types",
        "Loops, functions and collections",
        "File handling and exception handling"
    ],
    "java": [
        "Java basics and OOP",
        "Collections Framework",
        "Exception handling"
    ],
    "sql": [
        "SELECT, WHERE and ORDER BY",
        "JOINs and GROUP BY",
        "Subqueries and database normalization"
    ],
    "git": [
        "Git init, add and commit",
        "Branches and merging",
        "GitHub repositories and pull requests"
    ],
    "aws": [
        "Cloud computing fundamentals",
        "AWS IAM and EC2 basics",
        "S3 storage and deployment"
    ],
    "docker": [
        "Containers and images",
        "Dockerfile and Docker commands",
        "Build and run a containerized application"
    ],
    "pandas": [
        "DataFrames and Series",
        "Data cleaning and filtering",
        "GroupBy and merging datasets"
    ],
    "numpy": [
        "Arrays and array operations",
        "Indexing and slicing",
        "Numerical computations"
    ],
    "scikit-learn": [
        "Train-test split and preprocessing",
        "Model training and prediction",
        "Evaluation metrics"
    ],
    "machine learning": [
        "Supervised and unsupervised learning",
        "Regression and classification",
        "Overfitting and model evaluation"
    ],
    "html": [
        "HTML document structure",
        "Forms, links and tables",
        "Semantic HTML"
    ],
    "css": [
        "Selectors and box model",
        "Flexbox and Grid",
        "Responsive web design"
    ],
    "javascript": [
        "Variables, functions and arrays",
        "DOM manipulation",
        "Async JavaScript and fetch API"
    ],
    "react": [
        "Components and JSX",
        "Props, state and hooks",
        "API integration"
    ]
}


def get_learning_plan(missing_skills):
    plan = {}

    for skill in missing_skills:
        normalized_skill = skill.strip().lower()

        plan[skill] = LEARNING_RESOURCES.get(
            normalized_skill,
            [
                f"Learn {skill} fundamentals",
                f"Practice {skill} with small exercises",
                f"Build a mini project using {skill}"
            ]
        )

    return plan

