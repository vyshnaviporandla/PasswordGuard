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

const API_URL = "https://passwordguard-api.onrender.com/api/analyze";


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
        "VERY WEAK": "This password has significant security weaknesses.",
        "WEAK": "This password needs several security improvements.",
        "MODERATE": "This password has reasonable complexity but can be improved.",
        "STRONG": "This password has good complexity and structure.",
        "VERY STRONG": "This password meets most of the analyzer's strength criteria."
    };

    return descriptions[strength] ||
        "Analyze a password to see its security level.";
}


function updateScoreCircle(score) {
    const circle = document.querySelector(".score-circle");

    if (!circle) return;

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


function renderWarnings(findings) {
    warningsList.innerHTML = "";

    if (!findings || findings.length === 0) {
        warningsCard.classList.add("hidden");
        return;
    }

    warningsCard.classList.remove("hidden");

    findings.forEach(finding => {
        const item = document.createElement("div");

        item.className = "warning-item";

        item.innerHTML = `
            <span>⚠</span>
            <div>
                <strong>${finding.type}</strong><br>
                ${finding.description}
            </div>
        `;

        warningsList.appendChild(item);
    });
}


function buildChecks(data) {
    const checks = data.checks || {};

    return [
        {
            name: "Lowercase letters",
            passed: checks.lowercase
        },
        {
            name: "Uppercase letters",
            passed: checks.uppercase
        },
        {
            name: "Numbers",
            passed: checks.number
        },
        {
            name: "Symbols",
            passed: checks.symbol
        },
        {
            name: "No common password",
            passed: !data.metrics.common_password
        },
        {
            name: "No sequence pattern",
            passed: !checks.sequence
        },
        {
            name: "No keyboard pattern",
            passed: !checks.keyboard_pattern
        },
        {
            name: "No repetition",
            passed: !checks.repetition
        },
        {
            name: "No predictable structure",
            passed: !checks.predictable_structure
        },
        {
            name: "No personal information",
            passed: !checks.personal_information
        }
    ];
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
            throw new Error(data.error || "Analysis failed.");
        }

        results.classList.remove("hidden");

        const score = data.score;
        const strength = data.classification;

        scoreElement.textContent = score;
        strengthElement.textContent = strength;

        scoreBar.style.width = `${score}%`;

        scoreDescription.textContent =
            getStrengthDescription(strength);

        lengthValue.textContent =
            data.metrics.length;

        entropyValue.textContent =
            data.metrics.entropy_bits;

        updateScoreCircle(score);

        const checks = buildChecks(data);

        renderChecks(checks);

        renderSuggestions(
            data.suggestions || []
        );

        renderWarnings(
            data.findings || []
        );

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