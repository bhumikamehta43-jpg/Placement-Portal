
import bcrypt

from modules.database import get_db_connection


def register_user(full_name, email, password):
    full_name = full_name.strip()
    email = email.strip().lower()

    if not full_name or not email or not password:
        return False, "All fields are required."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if len(password.encode("utf-8")) > 72:
        return False, "Password must be at most 72 UTF-8 bytes."

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users
                (full_name, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (full_name, email, password_hash)
        )

        user_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO student_profiles (user_id)
            VALUES (%s)
            """,
            (user_id,)
        )

        connection.commit()
        return True, "Registration successful!"

    except Exception as error:
        connection.rollback()

        if getattr(error, "errno", None) == 1062:
            return False, "This email is already registered."

        raise

    finally:
        cursor.close()
        connection.close()


def login_user(email, password):
    email = email.strip().lower()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT user_id, full_name, email, password_hash , role
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user is None:
            return None

        password_matches = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        )
        
        if password_matches:
            return {
                "user_id": user["user_id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "role": user["role"]
            }

        return None

    finally:
        cursor.close()
        connection.close()

     
     
