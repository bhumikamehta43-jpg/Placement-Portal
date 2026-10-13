
from modules.database import get_db_connection

connection = None

try:
    connection = get_db_connection()

    if connection.is_connected():
        print("SUCCESS: MySQL connected!")
        print("Database:", connection.database)

except Exception as error:
    print("Database connection failed.")
    print("Error:", error)

finally:
    if connection is not None and connection.is_connected():
        connection.close()
