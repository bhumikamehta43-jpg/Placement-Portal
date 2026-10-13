
import os

import mysql.connector
import streamlit as st


def get_db_connection():
    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv(
            "DB_NAME", "placement_portal"
        ),
    }

    # Optional: read credentials from Streamlit secrets.
    if "mysql" in st.secrets:
        config.update(dict(st.secrets["mysql"]))

    return mysql.connector.connect(**config)
