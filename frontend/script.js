const API_URL = "https://passwordguard-api.onrender.com/api/analyze";

const passwordInput = document.getElementById("password");
const analyzeButton = document.getElementById("analyze");
const toggleButton = document.getElementById("toggle");

const results = document.getElementById("results");
const statusText = document.getElementById("status");

const scoreText = document.getElementById("score");
const classificationText = document.getElementById("classification");
const barFill = document.getElementById("bar-fill");
const descriptionText = document.getElementById("description");

const lengthText = document.getElementById("length");
const uniqueText = document.getElementById("unique");
const entropyText = document.getElementById("entropy");
const typesText = document.getElementById("types");

const checksBox = document.getElementById("checks");
const suggestionsBox = document.getElementById("suggestions");
const findingsBox = document.getElementById("findings");

toggleButton.addEventListener("click", function () {
    passwordInput.type =
        passwordInput.type === "password" ? "text" : "password";

    toggleButton.textContent =
        passwordInput.type === "password" ? "Show" : "Hide";
});

function showResults(data) {
    const metrics = data.metrics || {};

    scoreText.textContent = data.score;
    classificationText.textContent = data.classification;

    barFill.style.width = data.score + "%";

    descriptionText.textContent =
        "This password received a score of " +
        data.score +
        " out of 100.";

    lengthText.textContent = metrics.length || 0;

    uniqueText.textContent =
        Math.round((metrics.unique_character_ratio || 0) * 100) + "%";

    entropyText.textContent =
        (metrics.entropy_bits || 0) + " bits";

    typesText.textContent =
        (metrics.character_type_count || 0) + "/4";

    checksBox.innerHTML = "";

    const checks = data.checks || {};

    const checkItems = [
        ["Lowercase letters", checks.lowercase],
        ["Uppercase letters", checks.uppercase],
        ["Numbers", checks.number],
        ["Symbols", checks.symbol],
        ["Not a common password", !metrics.common_password],
        ["No sequence pattern", !checks.sequence],
        ["No keyboard pattern", !checks.keyboard_pattern],
        ["No repetition", !checks.repetition],
        ["No predictable structure", !checks.predictable_structure]
    ];

    checkItems.forEach(function (item) {
        const div = document.createElement("div");

        div.className = item[1]
            ? "check pass"
            : "check fail";

        div.textContent =
            (item[1] ? "✓ " : "✕ ") + item[0];

        checksBox.appendChild(div);
    });

    suggestionsBox.innerHTML = "";

    (data.suggestions || []).forEach(function (suggestion) {
        const div = document.createElement("div");

        div.className = "suggestion";

        div.textContent = "💡 " + suggestion;

        suggestionsBox.appendChild(div);
    });

    findingsBox.innerHTML = "";

    (data.findings || []).forEach(function (finding) {
        const div = document.createElement("div");

        div.className = "finding";

        div.innerHTML =
            "<strong>" +
            finding.type +
            " — " +
            finding.severity +
            "</strong>" +
            "<div>" +
            finding.description +
            "</div>";

        findingsBox.appendChild(div);
    });

    if ((data.findings || []).length === 0) {
        findingsBox.textContent =
            "No major pattern findings detected.";
    }

    results.classList.remove("hidden");
}

async function analyzePassword() {
    const password = passwordInput.value;

    if (!password) {
        statusText.textContent =
            "Please enter a password first.";
        return;
    }

    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";
    statusText.textContent =
        "Connecting to PasswordGuard API...";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Analysis failed."
            );
        }

        showResults(data);

        statusText.textContent =
            "Analysis completed successfully.";

    } catch (error) {
        console.error(error);

        statusText.textContent =
            "Backend connection failed: " +
            error.message;

    } finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent =
            "Analyze Password";
    }
}

analyzeButton.addEventListener(
    "click",
    analyzePassword
);

passwordInput.addEventListener(
    "keydown",
    function (event) {
        if (event.key === "Enter") {
            analyzePassword();
        }
    }
);