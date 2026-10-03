def analyze_length(password):
    """
    Analyze password length.

    Length contributes to strength, but length alone does not
    guarantee that a password is secure.
    """
    length = len(password)

    if length == 0:
        category = "EMPTY"
        contribution = 0
        finding = "No password was entered."

    elif length < 8:
        category = "VERY SHORT"
        contribution = 5
        finding = "Password is shorter than 8 characters."

    elif length < 12:
        category = "SHORT"
        contribution = 15
        finding = "Password is short. A longer password or passphrase is recommended."

    elif length < 16:
        category = "BETTER"
        contribution = 25
        finding = "Password has a reasonable length."

    else:
        category = "STRONG LENGTH"
        contribution = 35
        finding = "Password has a strong length contribution."

    return {
        "length": length,
        "category": category,
        "contribution": contribution,
        "finding": finding
    }