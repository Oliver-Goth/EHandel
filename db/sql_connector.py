import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_sql_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('SQL_SERVER_HOST')},{os.getenv('SQL_SERVER_PORT')};"
        f"DATABASE={os.getenv('SQL_SERVER_DB')};"
        f"UID={os.getenv('SQL_SERVER_USER')};"
        f"PWD={os.getenv('SQL_SERVER_PASSWORD')}"
    )
    return pyodbc.connect(conn_str)