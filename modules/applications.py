
from modules.database import get_db_connection


ALLOWED_STATUSES = [
    "Applied",
    "Shortlisted",
    "Interview",
    "Selected",
    "Rejected"
]


def add_application(user_id, company, job_title, location, notes=""):
    if not company or not job_title:
        raise ValueError("Company and job title are required.")

    connection = get_db_connection()

    if connection is None:
        raise RuntimeError("Database connection failed.")

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO applications
                (user_id, company, job_title, location, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                user_id,
                company,
                job_title,
                location,
                "Applied",
                notes
            )
        )

        connection.commit()
        return cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_applications(user_id):
    connection = get_db_connection()

    if connection is None:
        raise RuntimeError("Database connection failed.")

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                application_id,
                company,
                job_title,
                location,
                status,
                applied_at,
                notes
            FROM applications
            WHERE user_id = %s
            ORDER BY applied_at DESC, application_id DESC
        """

        cursor.execute(query, (user_id,))
        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def update_application_status(user_id, application_id, new_status):
    if new_status not in ALLOWED_STATUSES:
        raise ValueError("Invalid application status.")

    connection = get_db_connection()

    if connection is None:
        raise RuntimeError("Database connection failed.")

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            UPDATE applications
            SET status = %s
            WHERE application_id = %s AND user_id = %s
        """

        cursor.execute(
            query,
            (new_status, application_id, user_id)
        )

        updated_rows = cursor.rowcount
        connection.commit()

        return updated_rows

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def delete_application(user_id, application_id):
    connection = get_db_connection()

    if connection is None:
        raise RuntimeError("Database connection failed.")

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            DELETE FROM applications
            WHERE application_id = %s AND user_id = %s
        """

        cursor.execute(query, (application_id, user_id))

        deleted_rows = cursor.rowcount
        connection.commit()

        return deleted_rows

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()
