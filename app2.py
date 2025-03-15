import sys
import os
import pyodbc
from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
from dotenv import load_dotenv  # Import dotenv to load environment variables
from urllib.parse import quote as url_quote

# ✅ Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enables CORS for frontend integration

# ✅ Function to create a new database connection
def get_db_connection():
    try:
        # Fetch environment variables
        server = os.getenv("DATABASE_SERVER")
        database = os.getenv("DATABASE_NAME")
        username = os.getenv("DATABASE_USER")
        password = os.getenv("DATABASE_PASSWORD")

        # Debugging logs (avoid printing password)
        print("🔹 DATABASE_SERVER:", server)
        print("🔹 DATABASE_NAME:", database)
        print("🔹 DATABASE_USER:", username)

        # Ensure environment variables are set
        if not all([server, database, username, password]):
            print("❌ ERROR: Missing database environment variables!")
            return None

        # Create database connection
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
        return conn

    except Exception as e:
        print("❌ Database Connection Failed:", str(e))
        return None

# ✅ Serve index.html (Frontend)
@app.route('/')
def home():
    return render_template("index.html")  # Ensure index.html is inside 'templates' folder

# ✅ Route to add a new product
@app.route('/products', methods=['POST'])
def add_product():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        data = request.json
        print("📥 Received data:", data)  # Debugging log

        # Check if required fields exist
        if not all(k in data for k in ("name", "description", "price")):
            print("❌ Missing fields in request:", data)
            return jsonify({"error": "Missing required fields"}), 400

        # Convert price to float (Fixing type issues)
        data['price'] = float(data['price'])

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Products (name, description, price) VALUES (?, ?, ?)",
            (data['name'], data['description'], data['price'])
        )
        conn.commit()

        print("✅ Product added successfully")
        return jsonify({"message": "Product added successfully"}), 201

    except Exception as e:
        print("❌ Error in /products route:", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

# ✅ Route to list all products
@app.route('/products', methods=['GET'])
def list_products():
    print("🔄 /products route called")  # Debugging log
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, price FROM Products")
        rows = cursor.fetchall()

        # ✅ Fix: Convert Decimal to float
        products = [
            {"id": row[0], "name": row[1], "description": row[2], "price": float(row[3])}  # Convert Decimal to float
            for row in rows
        ]

        print("✅ JSON Response:", products)  # Debugging log
        return jsonify(products)
    except Exception as e:
        print("❌ Error in /products route:", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

# ✅ Run Flask App
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # Default to port 8000
    print(f"🚀 Running Flask on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
