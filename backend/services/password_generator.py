import secrets
import string


SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"


def generate_secure_password(
    length=20,
    use_uppercase=True,
    use_lowercase=True,
    use_numbers=True,
    use_symbols=True
):
    """
    Generate a password using Python's cryptographically secure
    secrets module.

    Generated passwords are returned transiently and are not stored.
    """

    try:
        length = int(length)
    except (TypeError, ValueError):
        length = 20

    length = max(12, min(length, 128))

    character_sets = []

    if use_lowercase:
        character_sets.append(string.ascii_lowercase)

    if use_uppercase:
        character_sets.append(string.ascii_uppercase)

    if use_numbers:
        character_sets.append(string.digits)

    if use_symbols:
        character_sets.append(SYMBOLS)

    if not character_sets:
        character_sets.append(string.ascii_letters + string.digits)

    # Guarantee at least one character from every selected set.
    password_characters = [
        secrets.choice(charset)
        for charset in character_sets
    ]

    all_characters = "".join(character_sets)

    while len(password_characters) < length:
        password_characters.append(
            secrets.choice(all_characters)
        )

    # Securely shuffle the generated characters.
    for i in range(len(password_characters) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_characters[i], password_characters[j] = (
            password_characters[j],
            password_characters[i]
        )

    return "".join(password_characters)