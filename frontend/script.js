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

togglePassword.onclick = function () {
if (passwordInput.type === "password") {
passwordInput.type = "text";
togglePassword.textContent = "Hide";
} else {
passwordInput.type = "password";
togglePassword.textContent = "Show";
}
};

function getStrengthDescription(strength) {
switch (strength) {
case "VERY WEAK":
return "This password has significant security weaknesses.";

    case "WEAK":
        return "This password needs several security improvements.";

    case "MODERATE":
        return "This password has reasonable complexity but can be improved.";

    case "STRONG":
        return "This password has good complexity and structure.";

    case "VERY STRONG":
        return "This password meets most of the analyzer's strength criteria.";

    default:
        return "Analyze a password to see its security level.";
}


}

function updateScoreCircle(score) {
const circle = document.querySelector(".score-circle");


if (!circle) {
    return;
}

circle.style.background =
    "radial-gradient(circle, var(--card) 63%, transparent 64%)," +
    "conic-gradient(var(--primary) " +
    score +
    "%, #18334d " +
    score +
    "%)";


}

function buildChecks(data) {
const checks = data.checks || {};
const metrics = data.metrics || {};


return [
    {
        name: "Lowercase letters",
        passed: checks.lowercase === true
    },
    {
        name: "Uppercase letters",
        passed: checks.uppercase === true
    },
    {
        name: "Numbers",
        passed: checks.number === true
    },
    {
        name: "Symbols",
        passed: checks.symbol === true
    },
    {
        name: "No common password",
        passed: metrics.common_password !== true
    },
    {
        name: "No sequence pattern",
        passed: checks.sequence !== true
    },
    {
        name: "No keyboard pattern",
        passed: checks.keyboard_pattern !== true
    },
    {
        name: "No repetition",
        passed: checks.repetition !== true
    },
    {
        name: "No predictable structure",
        passed: checks.predictable_structure !== true
    },
    {
        name: "No personal information",
        passed: checks.personal_information !== true
    }
];


}

function renderChecks(checks) {
checksList.innerHTML = "";


let passed = 0;

checks.forEach(function (check) {
    if (check.passed) {
        passed++;
    }

    const item = document.createElement("div");

    item.className = "check-item";

    item.innerHTML =
        '<span class="check-icon ' +
        (check.passed ? "pass" : "fail") +
        '">' +
        (check.passed ? "✓" : "✕") +
        "</span>" +
        "<span>" +
        check.name +
        "</span>";

    checksList.appendChild(item);
});

checksPassed.textContent = passed;
checksTotal.textContent = checks.length;


}

function renderSuggestions(suggestions) {
suggestionsList.innerHTML = "";


if (!Array.isArray(suggestions)) {
    return;
}

suggestions.forEach(function (suggestion) {
    const item = document.createElement("div");

    item.className = "suggestion-item";

    item.innerHTML =
        "<span>💡</span>" +
        "<div>" +
        suggestion +
        "</div>";

    suggestionsList.appendChild(item);
});


}

function renderWarnings(findings) {
warningsList.innerHTML = "";


if (!Array.isArray(findings) || findings.length === 0) {
    warningsCard.classList.add("hidden");
    return;
}

warningsCard.classList.remove("hidden");

findings.forEach(function (finding) {
    const item = document.createElement("div");

    item.className = "warning-item";

    item.innerHTML =
        "<span>⚠</span>" +
        "<div>" +
        "<strong>" +
        (finding.type || "Security Finding") +
        "</strong><br>" +
        (finding.description || "") +
        "</div>";

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
            data.error || "Password analysis failed."
        );
    }

    results.classList.remove("hidden");

    const score = Number(data.score) || 0;

    const strength =
        data.classification || "VERY WEAK";

    scoreElement.textContent = score;

    strengthElement.textContent = strength;

    scoreBar.style.width = score + "%";

    scoreDescription.textContent =
        getStrengthDescription(strength);

    const metrics = data.metrics || {};

    lengthValue.textContent =
        metrics.length || 0;

    entropyValue.textContent =
        metrics.entropy_bits || 0;

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
    console.error(
        "PasswordGuard error:",
        error
    );

    alert(
        "Could not connect to the PasswordGuard backend.\n\n" +
        error.message
    );
}

analyzeBtn.disabled = false;
analyzeBtn.textContent = "Analyze Password";
}

analyzeBtn.onclick = analyzePassword;

passwordInput.onkeydown = function (event) {
    if (event.key === "Enter") {
        analyzePassword();
    }
};