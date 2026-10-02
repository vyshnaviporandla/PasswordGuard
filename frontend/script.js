const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");
const analyzeBtn = document.getElementById("analyzeBtn");

const results = document.getElementById("results");

const scoreElement = document.getElementById("score");
const strengthElement = document.getElementById("strength");
const scoreBar = document.getElementById("scoreBar");
const scoreDescription = document.getElementById("scoreDescription");

const lengthValue = document.getElementById("lengthValue");
const entropyValue = document.getElementById("entropyValue");

const checksPassed = document.getElementById("checksPassed");
const checksTotal = document.getElementById("checksTotal");

const checksList = document.getElementById("checksList");
const suggestionsList = document.getElementById("suggestionsList");

const warningsCard = document.getElementById("warningsCard");
const warningsList = document.getElementById("warningsList");


togglePassword.addEventListener("click", () => {
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        togglePassword.textContent = "Hide";
    } else {
        passwordInput.type = "password";
        togglePassword.textContent = "Show";
    }
});


function getStrengthDescription(strength) {

    const descriptions = {
        "Very Weak": "This password has significant security weaknesses.",
        "Weak": "This password needs several security improvements.",
        "Moderate": "This password has reasonable complexity but can be improved.",
        "Strong": "This password has good complexity and structure.",
        "Very Strong": "This password meets most of the analyzer's strength criteria."
    };

    return descriptions[strength] || "Analyze a password to see its security level.";
}


function updateScoreCircle(score) {
    const circle = document.querySelector(".score-circle");

    circle.style.background =
        `radial-gradient(circle, var(--card) 63%, transparent 64%),
         conic-gradient(var(--primary) ${score}%, #18334d ${score}%)`;
}


function renderChecks(checks) {

    checksList.innerHTML = "";

    let passed = 0;

    checks.forEach(check => {

        if (check.passed) {
            passed++;
        }

        const item = document.createElement("div");
        item.className = "check-item";

        item.innerHTML = `
            <span class="check-icon ${check.passed ? "pass" : "fail"}">
                ${check.passed ? "✓" : "✕"}
            </span>
            <span>${check.name}</span>
        `;

        checksList.appendChild(item);
    });

    checksPassed.textContent = passed;
    checksTotal.textContent = checks.length;
}


function renderSuggestions(suggestions) {

    suggestionsList.innerHTML = "";

    suggestions.forEach(suggestion => {

        const item = document.createElement("div");

        item.className = "suggestion-item";

        item.innerHTML = `
            <span>💡</span>
            <div>${suggestion}</div>
        `;

        suggestionsList.appendChild(item);
    });
}


function renderWarnings(warnings) {

    warningsList.innerHTML = "";

    if (!warnings || warnings.length === 0) {
        warningsCard.classList.add("hidden");
        return;
    }

    warningsCard.classList.remove("hidden");

    warnings.forEach(warning => {

        const item = document.createElement("div");

        item.className = "warning-item";

        item.innerHTML = `
            <span>⚠</span>
            <div>${warning}</div>
        `;

        warningsList.appendChild(item);
    });
}


async function analyzePassword() {

    const password = passwordInput.value;

    if (!password) {
        alert("Please enter a password first.");
        passwordInput.focus();
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";

    try {

        const response = await fetch("http://127.0.0.1:5000/api/analyze", {
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
            throw new Error(data.error || "Analysis failed.");
        }

        results.classList.remove("hidden");

        scoreElement.textContent = data.score;
        strengthElement.textContent = data.strength;

        scoreBar.style.width = `${data.score}%`;

        scoreDescription.textContent =
            getStrengthDescription(data.strength);

        lengthValue.textContent = data.length;
        entropyValue.textContent = data.entropy;

        updateScoreCircle(data.score);

        renderChecks(data.checks);
        renderSuggestions(data.suggestions);
        renderWarnings(data.warnings);

        results.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {

        alert(
            "Could not connect to the PasswordGuard backend.\n\n" +
            error.message
        );

    } finally {

        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyze Password";
    }
}


analyzeBtn.addEventListener("click", analyzePassword);


passwordInput.addEventListener("keydown", event => {

    if (event.key === "Enter") {
        analyzePassword();
    }

});