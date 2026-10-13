from modules.database import get_db_connection

connection = get_db_connection()

if connection is None:
    print("Database connection failed.")
else:
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        print("Connected database:", cursor.fetchone()[0])

        cursor.execute("SHOW TABLES LIKE 'test_attempts'")
        print("Test attempts table:", cursor.fetchone())

        cursor.close()
    finally:
        connection.close()