
from modules.database import get_db_connection


def save_test_attempt(
    user_id,
    subject,
    total_questions,
    correct_answers
):
    if total_questions <= 0:
        raise ValueError("Total questions must be greater than zero.")

    if not 0 <= correct_answers <= total_questions:
        raise ValueError("Invalid number of correct answers.")

    score_percent = round(
        correct_answers / total_questions * 100,
        2
    )

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO test_attempts (
                user_id,
                subject,
                total_questions,
                correct_answers,
                score_percent
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                user_id,
                subject,
                total_questions,
                correct_answers,
                score_percent
            )
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def get_test_history(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                attempt_id,
                subject,
                total_questions,
                correct_answers,
                score_percent,
                attempted_at
            FROM test_attempts
            WHERE user_id = %s
            ORDER BY attempted_at DESC, attempt_id DESC
            """,
            (user_id,)
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()
