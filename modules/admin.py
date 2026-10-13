
from modules.database import get_db_connection


def _verify_admin(user_id):
    connection = get_db_connection()

    if connection is None:
        raise RuntimeError("Database connection failed.")

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT role FROM users WHERE user_id = %s",
            (user_id,)
        )
        record = cursor.fetchone()

        if not record or record["role"] != "admin":
            raise PermissionError("Admin access required.")

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_admin_statistics(user_id):
    _verify_admin(user_id)

    connection = get_db_connection()

    if connection is None:
        raise RuntimeError("Database connection failed.")

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM users")
        total_students = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM test_attempts")
        total_attempts = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM applications")
        total_applications = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT status, COUNT(*) AS total
            FROM applications
            GROUP BY status
        """)
        application_statuses = cursor.fetchall()

        return {
            "total_students": total_students,
            "total_attempts": total_attempts,
            "total_applications": total_applications,
            "application_statuses": application_statuses
        }

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_all_students(user_id):
    _verify_admin(user_id)

    connection = get_db_connection()

    if connection is None:
        raise RuntimeError("Database connection failed.")

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                u.user_id,
                u.full_name,
                u.email,
                u.created_at,
                p.branch,
                p.graduation_year,
                p.cgpa,
                p.preferred_role
            FROM users AS u
            LEFT JOIN student_profiles AS p
                ON p.user_id = u.user_id
            WHERE u.role = 'student'
            ORDER BY u.created_at DESC
        """)

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_all_applications(user_id):
    _verify_admin(user_id)

    connection = get_db_connection()

    if connection is None:
        raise RuntimeError("Database connection failed.")

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                a.application_id,
                a.user_id,
                u.full_name,
                a.company,
                a.job_title,
                a.location,
                a.status,
                a.applied_at,
                a.notes
            FROM applications AS a
            JOIN users AS u
                ON u.user_id = a.user_id
            ORDER BY a.applied_at DESC
        """)

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def admin_update_application_status(
    user_id,
    application_id,
    new_status
):
    allowed_statuses = [
        "Applied",
        "Shortlisted",
        "Interview",
        "Selected",
        "Rejected"
    ]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid application status.")

    _verify_admin(user_id)

    connection = get_db_connection()

    if connection is None:
        raise RuntimeError("Database connection failed.")

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE applications
            SET status = %s
            WHERE application_id = %s
        """, (new_status, application_id))

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
