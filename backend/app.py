from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import bcrypt
import pdfplumber

from db import get_db_connection
from predict import predict_sector
from job_title_predictor import predict_job_title
from skill_matcher import match_skills, suggest_improvements

# ---------------- INIT ----------------
app = Flask(__name__)
CORS(app)

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

        # 🔥 FIX: column name = username (NOT name)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed.decode('utf-8'))
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully"})

    except Exception as e:
        print("SIGNUP ERROR:", e)
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
                "name": user["username"]  # 🔥 FIX
            })
        else:
            return jsonify({"error": "Invalid password"}), 401

    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ---------------- FRONTEND ROUTES ----------------
@app.route("/")
def start_page():
    return render_template("start.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/signup-page")
def signup_page():
    return render_template("signup.html")

@app.route("/predict-page")
def job_page():
    return render_template("index.html")

@app.route("/resume-page")
def resume_page():
    return render_template("resume.html")

@app.route("/history-page")
def history_page():
    return render_template("history.html")


# ---------------- PDF EXTRACT ----------------
def extract_pdf(file):
    try:
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        print("PDF ERROR:", e)
        return ""


# ---------------- JOB ANALYZER ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        text = ""

        if 'file' in request.files:
            file = request.files['file']
            text = extract_pdf(file)
        else:
            data = request.json
            text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text"}), 400

        # 🔥 SAFE MODEL CALL
        try:
            sector = predict_sector(text)
        except Exception as e:
            print("MODEL ERROR:", e)
            return jsonify({"error": "Model failed"}), 500

        if sector == "Other / Unknown":
            return jsonify({"sector": sector})

        # 🔥 SAFE PIPELINE
        try:
            title = predict_job_title(text, sector)
            matched, missing = match_skills(text, sector)
            suggestions = suggest_improvements(missing)
        except Exception as e:
            print("PIPELINE ERROR:", e)
            return jsonify({"error": "Processing failed"}), 500

        return jsonify({
            "sector": sector,
            "job_title": title,
            "matched_skills": matched,
            "missing_skills": missing,
            "suggestions": suggestions
        })

    except Exception as e:
        print("PREDICT ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ---------------- RESUME ANALYSIS ----------------
@app.route("/resume", methods=["POST"])
def resume_analysis():
    try:
        text = ""
        filename = "text_input"

        if 'file' in request.files:
            file = request.files['file']
            text = extract_pdf(file)
            filename = file.filename
            sector = request.form.get("sector")
            role = request.form.get("role")
            user_id = request.form.get("user_id")
        else:
            data = request.json
            text = data.get("text", "")
            sector = data.get("sector")
            role = data.get("role")
            user_id = data.get("user_id")

        if not text or not sector or not role:
            return jsonify({"error": "Missing data"}), 400

        matched, missing = match_skills(text, sector)
        suggestions = suggest_improvements(missing)

        total = len(matched) + len(missing)
        score = int((len(matched) / total) * 100) if total > 0 else 0

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO resume_analysis 
            (filename, predicted_role, extracted_skills, matched_skills, missing_skills, score, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            filename,
            role,
            ", ".join(matched + missing),
            ", ".join(matched),
            ", ".join(missing),
            score,
            user_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "score": score,
            "matched": matched,
            "missing": missing,
            "suggestions": suggestions
        })

    except Exception as e:
        print("RESUME ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ---------------- HISTORY ----------------
@app.route("/history/<int:user_id>")
def history(user_id):
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
        print("HISTORY ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ---------------- DEBUG ----------------
@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        return "DB Connected ✅"
    except Exception as e:
        return str(e)


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)