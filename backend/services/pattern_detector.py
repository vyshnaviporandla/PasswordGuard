import re


KEYBOARD_PATTERNS = [
    "qwerty",
    "asdf",
    "zxcv",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
    "1qaz",
    "2wsx",
    "3edc",
    "qaz",
    "wsx",
    "edc"
]


COMMON_WORDS = [
    "password",
    "admin",
    "welcome",
    "letmein",
    "hello",
    "login",
    "user",
    "secret",
    "football",
    "dragon",
    "monkey",
    "master",
    "summer",
    "winter",
    "spring",
    "autumn"
]


def detect_sequences(password):
    """
    Detect ascending and descending character sequences.
    """

    value = password.lower()
    sequences = []

    for i in range(len(value) - 3):
        chunk = value[i:i + 4]

        if all(
            ord(chunk[j + 1]) == ord(chunk[j]) + 1
            for j in range(3)
        ):
            sequences.append(chunk)

        elif all(
            ord(chunk[j + 1]) == ord(chunk[j]) - 1
            for j in range(3)
        ):
            sequences.append(chunk)

    # Numeric sequences such as 1234 or 9876
    for i in range(len(value) - 3):
        chunk = value[i:i + 4]

        if chunk.isdigit():
            numbers = [int(x) for x in chunk]

            if all(
                numbers[j + 1] == numbers[j] + 1
                for j in range(3)
            ) or all(
                numbers[j + 1] == numbers[j] - 1
                for j in range(3)
            ):
                if chunk not in sequences:
                    sequences.append(chunk)

    return {
        "detected": bool(sequences),
        "patterns": list(dict.fromkeys(sequences))
    }


def detect_keyboard_patterns(password):
    """
    Detect common keyboard walks.
    """

    value = password.lower()
    found = []

    for pattern in KEYBOARD_PATTERNS:
        if pattern in value:
            found.append(pattern)

        if pattern[::-1] in value:
            found.append(pattern[::-1])

    return {
        "detected": bool(found),
        "patterns": list(dict.fromkeys(found))
    }


def detect_repetition(password):
    """
    Detect repeated characters and repeated substrings.
    """

    repeated_characters = []

    matches = re.findall(r"(.)\1{2,}", password)

    for match in matches:
        repeated_characters.append(match)

    repeated_substrings = []

    # Detect simple repeated blocks such as:
    # ababab
    # abcabcabc
    for size in range(2, min(6, len(password) // 2 + 1)):
        for start in range(len(password) - (size * 2) + 1):
            block = password[start:start + size]

            if len(block) < 2:
                continue

            repetitions = len(password[start:]) // size

            if repetitions >= 2:
                candidate = block * repetitions

                if password[start:start + len(candidate)] == candidate:
                    repeated_substrings.append(block)

    return {
        "detected": bool(repeated_characters or repeated_substrings),
        "repeated_characters": list(dict.fromkeys(repeated_characters)),
        "repeated_substrings": list(dict.fromkeys(repeated_substrings))
    }


def detect_predictable_structure(password):
    """
    Detect common predictable combinations such as:

    password123
    welcome123
    admin2026
    hello1234
    """

    value = password.lower()

    patterns = []

    if re.search(
        r"(password|welcome|admin|hello|login|secret|user)"
        r"\d{2,6}",
        value
    ):
        patterns.append("common word followed by numbers")

    if re.search(r"[a-zA-Z]{3,}(19|20)\d{2}", value):
        patterns.append("word followed by a year")

    if re.search(r"\d{4}", value):
        year_matches = re.findall(r"(19|20)\d{2}", value)

        if year_matches:
            patterns.append("year-like number")

    return {
        "detected": bool(patterns),
        "patterns": list(dict.fromkeys(patterns))
    }


def detect_common_words(password):
    """
    Detect common dictionary-style words inside a password.

    This is an educational local detector, not a full dictionary.
    """

    value = password.lower()
    found = []

    for word in COMMON_WORDS:
        if word in value:
            found.append(word)

    return {
        "detected": bool(found),
        "words": list(dict.fromkeys(found))
    }


def detect_personal_information(password, context=None):
    """
    Compare the password against optional user-provided demo context.

    Context is processed only in memory and should never be stored.
    """

    if not context:
        return {
            "detected": False,
            "matches": []
        }

    value = password.lower()
    matches = []

    for key, item in context.items():

        if not item:
            continue

        item = str(item).strip().lower()

        if len(item) >= 3 and item in value:
            matches.append(key)

    return {
        "detected": bool(matches),
        "matches": list(dict.fromkeys(matches))
    }


def analyze_patterns(password, context=None):
    """
    Run all pattern detectors.
    """

    return {
        "sequences": detect_sequences(password),
        "keyboard": detect_keyboard_patterns(password),
        "repetition": detect_repetition(password),
        "predictable_structure": detect_predictable_structure(password),
        "common_words": detect_common_words(password),
        "personal_information": detect_personal_information(
            password,
            context
        )
    }