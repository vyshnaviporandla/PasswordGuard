import math
import string


def estimate_theoretical_entropy(password):
    """
    Calculate a theoretical entropy-style estimate.

    Formula:

        entropy ≈ L × log2(N)

    L = password length
    N = estimated character pool

    IMPORTANT:
    This assumes random character selection.

    Human-created passwords are often predictable, so this value
    must NOT be treated as a guaranteed measure of security.
    """

    if not password:
        return {
            "bits": 0.0,
            "character_pool": 0,
            "explanation": "No password was entered."
        }

    pool = 0

    if any(char.islower() for char in password):
        pool += 26

    if any(char.isupper() for char in password):
        pool += 26

    if any(char.isdigit() for char in password):
        pool += 10

    if any(char in string.punctuation for char in password):
        pool += len(string.punctuation)

    if any(char.isspace() for char in password):
        pool += 1

    pool = max(pool, 1)

    bits = len(password) * math.log2(pool)

    return {
        "bits": round(bits, 2),
        "character_pool": pool,
        "explanation": (
            "This is a theoretical estimate assuming random character "
            "selection. Human-generated passwords may be much more "
            "predictable than this estimate suggests."
        )
    }