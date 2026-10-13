
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent
JOBS_FILE = BASE_DIR / "data" / "jobs.csv"

print("PROJECT PATH:", BASE_DIR)
print("JOBS FILE PATH:", JOBS_FILE)
print("FILE EXISTS:", JOBS_FILE.exists())


def load_jobs():
    return pd.read_csv(JOBS_FILE).fillna("")


def match_jobs(student_skills):
    jobs = load_jobs()

    student_skills = [
        skill.strip().lower()
        for skill in student_skills
    ]

    student_text = " ".join(student_skills)

    job_texts = (
        jobs["job_title"].astype(str)
        + " "
        + jobs["required_skills"].astype(str).str.replace("|", " ", regex=False)
    ).tolist()

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(
        [student_text] + job_texts
    )

    similarity_scores = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    results = []

    for index, job in jobs.iterrows():
        required = [
            skill.strip().lower()
            for skill in str(job["required_skills"]).split("|")
            if skill.strip()
        ]

        matched = [
            skill for skill in required
            if skill in student_skills
        ]

        missing = [
            skill for skill in required
            if skill not in student_skills
        ]

        skill_score = (
            len(matched) / len(required) * 100
            if required else 0
        )

        similarity_score = float(
            similarity_scores[index] * 100
        )

        # Combine exact skill coverage and text similarity.
        final_score = round(
            0.7 * skill_score + 0.3 * similarity_score,
            2
        )

        results.append({
            "Company": job["company"],
            "Job Role": job["job_title"],
            "Location": job["location"],
            "Match Score (%)": final_score,
            "Matched Skills": ", ".join(matched) or "None",
            "Missing Skills": ", ".join(missing) or "None",
            "Eligibility": job["eligibility"]
        })

    results.sort(
        key=lambda item: item["Match Score (%)"],
        reverse=True
    )

    return results
