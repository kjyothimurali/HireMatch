console.log("JS LOADED");

async function signupUser() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const errorMsg = document.getElementById("errorMsg");
    const successMsg = document.getElementById("successMsg");

    errorMsg.innerText = "";
    successMsg.innerText = "";

    if (!name || !email || !password) {
        errorMsg.innerText = "All fields are required";
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:5000/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, email, password })
        });

        const data = await res.json();

        if (data.error) {
            errorMsg.innerText = data.error;
        } else {
            successMsg.innerText = "Account created successfully! Redirecting...";

            setTimeout(() => {
                window.location.href = "/login-page";
            }, 1500);
        }

    } catch (err) {
        console.error(err);
        errorMsg.innerText = "Server error";
    }
}

async function loginUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("errorMsg");

    errorMsg.innerText = "";

    if (!email || !password) {
        errorMsg.innerText = "Please fill all fields";
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (data.error) {
            errorMsg.innerText = data.error;
        } else {
            // 🔥 STORE USER DATA
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("user_name", data.name);

            // 🔥 REDIRECT
            window.location.href = "/home";
        }

    } catch (err) {
        errorMsg.innerText = "Server error";
        console.error(err);
    }
}

/* ---------------- JOB ANALYSIS ---------------- */
async function analyzeJob() {
    const textInput = document.getElementById("jobText").value;
    const file = document.getElementById("jobPdf").files[0];
    const button = document.getElementById("analyzeBtn");
    const loader = document.getElementById("loading");

    if (!textInput && !file) {
        alert("Provide text or upload PDF");
        return;
    }

    loader.style.display = "block";
    button.disabled = true;
    button.innerText = "Processing...";

    try {
        let response;

        if (file) {
            const formData = new FormData();
            formData.append("file", file);

            response = await fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                body: formData
            });
        } else {
            response = await fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: textInput })
            });
        }

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("jobResult").innerHTML = `
        <div class="result-card fade-in">

            <h3 class="title"> Job Prediction</h3>

            <div class="info-grid">
                <div>
                    <p class="label">Sector</p>
                    <h5>${data.sector}</h5>
                </div>

                <div>
                    <p class="label">Role</p>
                    <h5>${data.job_title || "N/A"}</h5>
                </div>
            </div>

        </div>`;
    } catch (err) {
        console.error(err);
        alert("Server error");
    }

    loader.style.display = "none";
    button.disabled = false;
    button.innerText = "Analyze Job";
}


/* ---------------- ROLE MAPPING ---------------- */
const roleMap = {
    "IT": ["Software Developer", "Web Developer", "Data Scientist", "ML Engineer"],
    "Finance": ["Accountant", "Financial Analyst", "Auditor"],
    "Healthcare": ["Nurse", "Doctor", "Medical Assistant"],
    "Sales & Marketing": ["Sales Executive", "Marketing Manager", "Business Analyst"]
};

function loadRoles() {
    const sector = document.getElementById("sector").value;
    const roleDropdown = document.getElementById("role");

    roleDropdown.innerHTML = "<option>Select Role</option>";

    if (roleMap[sector]) {
        roleMap[sector].forEach(role => {
            const option = document.createElement("option");
            option.value = role;
            option.textContent = role;
            roleDropdown.appendChild(option);
        });
    }
}


/* ---------------- RESUME ANALYSIS ---------------- */
async function analyzeResume() {
    const user_id = localStorage.getItem("user_id");
    const textInput = document.getElementById("resumeText").value;
    const file = document.getElementById("pdfFile").files[0];
    const sector = document.getElementById("sector").value;
    const role = document.getElementById("role").value;

    if (!sector || !role) {
        alert("Select sector and role");
        return;
    }

    if (!textInput && !file) {
        alert("Provide resume text OR upload PDF");
        return;
    }

    try {
        let response;

        /* ---------- SEND TO FLASK (/resume) ---------- */
        if (file) {
            const formData = new FormData();
            formData.append("user_id", user_id);
            formData.append("file", file);
            formData.append("sector", sector);
            formData.append("role", role);

            response = await fetch("http://127.0.0.1:5000/resume", {
                method: "POST",
                body: formData
            });
        } else {
            response = await fetch("http://127.0.0.1:5000/resume", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: textInput, sector, role, user_id })
            });
        }

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        /* ---------- STORE RESULT IN MYSQL ---------- */
        if (file) {
            const saveData = new FormData();
            saveData.append("resume", file);

            await fetch("http://127.0.0.1:5000/analyze", {
                method: "POST",
                body: saveData
            });
        }

        /* ---------- UI OUTPUT ---------- */
        document.getElementById("resumeResult").innerHTML = `
        <div class="result-card fade-in">

            <h3 class="title"> Resume Analysis</h3>

            <!-- BASIC -->
            <div class="info-grid">
                <div>
                    <p class="label">Sector</p>
                    <h5>${data.sector}</h5>
                </div>
                <div>
                    <p class="label">Role</p>
                    <h5>${data.role}</h5>
                </div>
            </div>

            <!-- SCORE -->
            <div class="score-box">
                <p class="label">Match Score</p>
                <div class="progress">
                    <div class="progress-bar" style="width:${data.score}%">
                        ${data.score}%
                    </div>
                </div>
            </div>

            <!-- MATCHED -->
            <div class="skills-section">
                <h5> Matched Skills</h5>
                <div class="chips">
                    ${data.matched.map(s => `<span class="chip match">${s}</span>`).join("")}
                </div>
            </div>

            <!-- MISSING -->
            <div class="skills-section">
                <h5> Missing Skills</h5>
                <div class="chips">
                    ${data.missing.map(s => `<span class="chip missing">${s}</span>`).join("")}
                </div>
            </div>

            <!-- SUGGESTIONS -->
            <div class="skills-section">
                <h5> Suggestions</h5>
                <ul class="suggestions">
                    ${data.suggestions.map(s => `<li>${s}</li>`).join("")}
                </ul>
            </div>

        </div>`;
    } catch (err) {
        console.error(err);
        alert("Server error");
    }
}