from pathlib import Path

from services.length_analyzer import analyze_length
from services.pattern_detector import (
    analyze_patterns
)
from services.entropy_estimator import (
    estimate_theoretical_entropy
)
from services.scoring_engine import calculate_score
from services.suggestion_engine import generate_suggestions


BASE_DIR = Path(__file__).resolve().parent.parent
COMMON_PASSWORD_FILE = BASE_DIR / "data" / "common_passwords.txt"


def load_common_passwords():
    """
    Load the local educational common-password list.

    Passwords entered by users are never written to this file.
    """

    if not COMMON_PASSWORD_FILE.exists():
        return set()

    try:
        with open(
            COMMON_PASSWORD_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return {
                line.strip().lower()
                for line in file
                if line.strip()
            }
    except OSError:
        return set()


COMMON_PASSWORDS = load_common_passwords()
def is_common_password(password):
    """
    Detect common passwords and simple variations.

    Examples:
    password
    Password
    password123
    Password123!
    PASSWORD123
    """

    normalized = password.strip().lower()

    # Direct match
    if normalized in COMMON_PASSWORDS:
        return True

    # Remove non-alphanumeric characters.
    # This catches variations such as Password123!
    simplified = "".join(
        character
        for character in normalized
        if character.isalnum()
    )

    # Compare with the local common-password list.
    for common_password in COMMON_PASSWORDS:
        common_simplified = "".join(
            character
            for character in common_password.lower()
            if character.isalnum()
        )

        if simplified == common_simplified:
            return True

    return False


def analyze_characteristics(password):
    """
    Analyze character types and uniqueness.
    """

    has_lowercase = any(
        character.islower()
        for character in password
    )

    has_uppercase = any(
        character.isupper()
        for character in password
    )

    has_digit = any(
        character.isdigit()
        for character in password
    )

    has_symbol = any(
        not character.isalnum() and not character.isspace()
        for character in password
    )

    has_space = any(
        character.isspace()
        for character in password
    )

    character_type_count = sum([
        has_lowercase,
        has_uppercase,
        has_digit,
        has_symbol
    ])

    unique_character_count = len(set(password))

    unique_character_ratio = (
        unique_character_count / len(password)
        if password
        else 0
    )

    return {
        "has_lowercase": has_lowercase,
        "has_uppercase": has_uppercase,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
        "has_space": has_space,
        "character_type_count": character_type_count,
        "unique_character_count": unique_character_count,
        "unique_character_ratio": round(
            unique_character_ratio,
            2
        )
    }


def build_findings(
    password,
    length_result,
    character_result,
    pattern_result,
    common_password
):
    """
    Convert analysis signals into human-readable findings.
    """

    findings = []

    if length_result["length"] < 8:
        findings.append({
            "type": "length",
            "severity": "HIGH",
            "description": "Password is very short."
        })

    elif length_result["length"] < 12:
        findings.append({
            "type": "length",
            "severity": "MEDIUM",
            "description": "Password length could be increased."
        })

    if common_password:
        findings.append({
            "type": "common_password",
            "severity": "HIGH",
            "description": (
                "Password matches a commonly used password."
            )
        })

    if pattern_result["sequences"]["detected"]:
        patterns = ", ".join(
            pattern_result["sequences"]["patterns"]
        )

        findings.append({
            "type": "sequence",
            "severity": "HIGH",
            "description": (
                f"Predictable sequence detected: {patterns}"
            )
        })

    if pattern_result["keyboard"]["detected"]:
        patterns = ", ".join(
            pattern_result["keyboard"]["patterns"]
        )

        findings.append({
            "type": "keyboard",
            "severity": "HIGH",
            "description": (
                f"Keyboard pattern detected: {patterns}"
            )
        })

    if pattern_result["repetition"]["detected"]:
        findings.append({
            "type": "repetition",
            "severity": "HIGH",
            "description": "Repeated characters or substrings detected."
        })

    if pattern_result["common_words"]["detected"]:
        words = ", ".join(
            pattern_result["common_words"]["words"]
        )

        findings.append({
            "type": "dictionary",
            "severity": "MEDIUM",
            "description": (
                f"Common word detected: {words}"
            )
        })

    if pattern_result["predictable_structure"]["detected"]:
        findings.append({
            "type": "predictable_structure",
            "severity": "HIGH",
            "description": (
                "Predictable word-and-number structure detected."
            )
        })

    if pattern_result["personal_information"]["detected"]:
        findings.append({
            "type": "personal_information",
            "severity": "HIGH",
            "description": (
                "Password appears to contain provided personal context."
            )
        })

    if character_result["unique_character_ratio"] < 0.50:
        findings.append({
            "type": "character_reuse",
            "severity": "MEDIUM",
            "description": (
                "Password contains substantial character repetition."
            )
        })

    return findings


def analyze_password(password, context=None):
    """
    Main PasswordGuard analysis function.

    IMPORTANT PRIVACY DESIGN:
    The raw password exists only in memory during analysis.
    This function does not write the password to disk,
    database, logs, URLs, or external services.
    """

    if not isinstance(password, str):
        raise ValueError("Password must be a string.")

    if len(password) > 128:
        raise ValueError(
            "Password exceeds the maximum supported length of 128 characters."
        )

    length_result = analyze_length(password)

    character_result = analyze_characteristics(password)

    pattern_result = analyze_patterns(
        password,
        context
    )

    common_password = is_common_password(
        password
    )

    entropy_result = estimate_theoretical_entropy(
        password
    )

    score_result = calculate_score(
        length_result,
        character_result,
        pattern_result,
        common_password
    )

    findings = build_findings(
        password,
        length_result,
        character_result,
        pattern_result,
        common_password
    )

    suggestions = generate_suggestions(
        length_result,
        character_result,
        pattern_result,
        common_password
    )

    return {
        "score": score_result["score"],
        "classification": score_result["classification"],

        "findings": findings,

        "suggestions": suggestions,

        "metrics": {
            "length": length_result["length"],
            "length_category": length_result["category"],
            "character_type_count": (
                character_result["character_type_count"]
            ),
            "unique_character_count": (
                character_result["unique_character_count"]
            ),
            "unique_character_ratio": (
                character_result["unique_character_ratio"]
            ),
            "common_password": common_password,
            "entropy_bits": entropy_result["bits"],
            "estimated_character_pool": (
                entropy_result["character_pool"]
            )
        },

        "checks": {
            "lowercase": character_result["has_lowercase"],
            "uppercase": character_result["has_uppercase"],
            "number": character_result["has_digit"],
            "symbol": character_result["has_symbol"],
            "space": character_result["has_space"],
            "sequence": (
                pattern_result["sequences"]["detected"]
            ),
            "keyboard_pattern": (
                pattern_result["keyboard"]["detected"]
            ),
            "repetition": (
                pattern_result["repetition"]["detected"]
            ),
            "common_word": (
                pattern_result["common_words"]["detected"]
            ),
            "predictable_structure": (
                pattern_result["predictable_structure"]["detected"]
            ),
            "personal_information": (
                pattern_result["personal_information"]["detected"]
            )
        },

        "entropy_explanation": entropy_result["explanation"]
    }