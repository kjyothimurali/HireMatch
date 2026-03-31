from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import bcrypt
import pdfplumber
from db import get_db_connection

from predict import predict_sector
from job_title_predictor import predict_job_title
from skill_matcher import match_skills, suggest_improvements

app = Flask(__name__)
CORS(app)

FRONTEND_PATH = os.path.join(os.getcwd(), "..", "frontend")

# ---------------- AUTH APIs ----------------
@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"error": "All fields required"}), 400

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed.decode('utf-8'))
        )
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({
                "message": "Login successful",
                "user_id": user["id"],
                "name": user["name"]
            })
        else:
            return jsonify({"error": "Invalid password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- PAGE ROUTES ----------------
@app.route("/")
def start_page():
    return send_from_directory(FRONTEND_PATH, "start.html")

@app.route("/home")
def home():
    return send_from_directory(FRONTEND_PATH, "home.html")

@app.route("/login-page")
def login_page():
    return send_from_directory(FRONTEND_PATH, "login.html")

@app.route("/signup-page")
def signup_page():
    return send_from_directory(FRONTEND_PATH, "signup.html")

@app.route("/predict-page")
def job_page():
    return send_from_directory(FRONTEND_PATH, "index.html")

@app.route("/resume-page")
def resume_page():
    return send_from_directory(FRONTEND_PATH, "resume.html")

@app.route("/history-page")
def history_page():
    return send_from_directory(FRONTEND_PATH, "history.html")


# ---------------- PDF EXTRACT ----------------
def extract_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


# ---------------- JOB ANALYZER ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if 'file' in request.files:
            file = request.files['file']
            text = extract_pdf(file)
        else:
            data = request.json
            text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text extracted"}), 400

        sector = predict_sector(text)

        if sector == "Other / Unknown":
            return jsonify({"sector": sector})

        title = predict_job_title(text, sector)
        matched, missing = match_skills(text, sector)
        suggestions = suggest_improvements(missing)

        return jsonify({
            "sector": sector,
            "job_title": title,
            "matched_skills": matched,
            "missing_skills": missing,
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- RESUME ANALYSIS (STORE USER DATA) ----------------
@app.route("/resume", methods=["POST"])
def resume_analysis():
    try:
        if 'file' in request.files:
            file = request.files['file']
            text = extract_pdf(file)
            sector = request.form.get("sector")
            role = request.form.get("role")
            user_id = request.form.get("user_id")   # 🔥 NEW
            filename = file.filename
        else:
            data = request.json
            text = data.get("text", "").strip()
            sector = data.get("sector")
            role = data.get("role")
            user_id = data.get("user_id")          # 🔥 NEW
            filename = "text_input"

        if not text:
            return jsonify({"error": "No text found"}), 400

        if not sector or not role:
            return jsonify({"error": "Missing sector or role"}), 400

        matched, missing = match_skills(text, sector)
        suggestions = suggest_improvements(missing)

        total = len(matched) + len(missing)
        score = int((len(matched) / total) * 100) if total > 0 else 0

        matched_str = ", ".join(matched) if matched else ""
        missing_str = ", ".join(missing) if missing else ""
        skills_str = ", ".join(matched + missing) if (matched or missing) else ""

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO resume_analysis 
        (filename, predicted_role, extracted_skills, matched_skills, missing_skills, score, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            filename,
            role,
            skills_str,
            matched_str,
            missing_str,
            score,
            user_id   # 🔥 IMPORTANT
        )

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "sector": sector,
            "role": role,
            "matched": matched,
            "missing": missing,
            "suggestions": suggestions,
            "score": score
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ---------------- USER-SPECIFIC HISTORY ----------------
@app.route("/history/<int:user_id>", methods=["GET"])
def user_history(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM resume_analysis WHERE user_id=%s ORDER BY created_at DESC",
            (user_id,)
        )

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- RUN ----------------
if __name__ == "__main__":
    print("\n🚀 HireMatch Server is running...")
    print("👉 http://127.0.0.1:5000\n")
    app.run(debug=True)