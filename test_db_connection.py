import pyodbc
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file (if used)
load_dotenv()

# ✅ Fetch environment variables
server = os.getenv("DATABASE_SERVER")
database = os.getenv("DATABASE_NAME")
username = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")

print("🔹 DATABASE_SERVER:", server)
print("🔹 DATABASE_NAME:", database)
print("🔹 DATABASE_USER:", username)

try:
    # ✅ Create database connection
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )
    print("✅ Database Connection Successful!")
except Exception as e:
    print("❌ Database Connection Failed:", str(e))
