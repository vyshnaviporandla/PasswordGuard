import math
import re


COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "123456789",
    "qwerty",
    "qwerty123",
    "admin",
    "admin123",
    "welcome",
    "letmein",
    "iloveyou",
    "abc123",
    "monkey",
    "dragon",
    "football",
    "login",
    "user",
    "test",
}


def calculate_entropy(password):
    if not password:
        return 0

    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"\d", password):
        charset += 10

    if re.search(r"[^A-Za-z0-9]", password):
        charset += 32

    if charset == 0:
        return 0

    return round(len(password) * math.log2(charset), 2)


def analyze_password(password):
    suggestions = []
    warnings = []
    checks = []

    length = len(password)

    checks.append({
        "name": "Minimum length",
        "passed": length >= 8
    })

    checks.append({
        "name": "12+ characters",
        "passed": length >= 12
    })

    checks.append({
        "name": "Uppercase letter",
        "passed": bool(re.search(r"[A-Z]", password))
    })

    checks.append({
        "name": "Lowercase letter",
        "passed": bool(re.search(r"[a-z]", password))
    })

    checks.append({
        "name": "Number",
        "passed": bool(re.search(r"\d", password))
    })

    checks.append({
        "name": "Special character",
        "passed": bool(re.search(r"[^A-Za-z0-9]", password))
    })

    lower_password = password.lower()

    if lower_password in COMMON_PASSWORDS:
        warnings.append("This password appears in a list of commonly used passwords.")

    if re.search(r"(.)\1{2,}", password):
        warnings.append("Repeated characters make the password easier to guess.")

    if re.search(r"(123|234|345|456|567|678|789)", password):
        warnings.append("Sequential numbers can make passwords easier to predict.")

    if re.search(r"(abc|qwerty|asdf)", lower_password):
        warnings.append("Common keyboard or alphabet patterns were detected.")

    if length < 8:
        suggestions.append("Use at least 8 characters. Longer passwords are generally stronger.")

    if length < 12:
        suggestions.append("Consider using 12 or more characters.")

    if not re.search(r"[A-Z]", password):
        suggestions.append("Add uppercase letters.")

    if not re.search(r"[a-z]", password):
        suggestions.append("Add lowercase letters.")

    if not re.search(r"\d", password):
        suggestions.append("Add numbers.")

    if not re.search(r"[^A-Za-z0-9]", password):
        suggestions.append("Add special characters such as !, @, #, or $.")

    if not suggestions and not warnings:
        suggestions.append("Good password structure. Avoid reusing it across different accounts.")

    score = 0

    if length >= 8:
        score += 15

    if length >= 12:
        score += 15

    if length >= 16:
        score += 10

    if re.search(r"[A-Z]", password):
        score += 15

    if re.search(r"[a-z]", password):
        score += 15

    if re.search(r"\d", password):
        score += 15

    if re.search(r"[^A-Za-z0-9]", password):
        score += 15

    if lower_password in COMMON_PASSWORDS:
        score = min(score, 20)

    if warnings:
        score = max(0, score - 10)

    if score < 30:
        strength = "Very Weak"
    elif score < 50:
        strength = "Weak"
    elif score < 70:
        strength = "Moderate"
    elif score < 90:
        strength = "Strong"
    else:
        strength = "Very Strong"

    entropy = calculate_entropy(password)

    return {
        "score": score,
        "strength": strength,
        "length": length,
        "entropy": entropy,
        "checks": checks,
        "warnings": warnings,
        "suggestions": suggestions
    }