
from modules.database import get_db_connection


def save_profile(
    user_id,
    branch,
    graduation_year,
    cgpa,
    technical_skills,
    preferred_role
):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE student_profiles
            SET branch = %s,
                graduation_year = %s,
                cgpa = %s,
                technical_skills = %s,
                preferred_role = %s
            WHERE user_id = %s
            """,
            (
                branch,
                graduation_year,
                cgpa,
                technical_skills,
                preferred_role,
                user_id
            )
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def load_profile(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT branch, graduation_year, cgpa,
                   technical_skills, preferred_role
            FROM student_profiles
            WHERE user_id = %s
            """,
            (user_id,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()
