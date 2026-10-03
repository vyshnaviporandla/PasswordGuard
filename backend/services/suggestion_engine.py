def generate_suggestions(
    length_result,
    character_result,
    pattern_result,
    common_password
):
    """
    Generate specific, actionable security recommendations.
    """

    suggestions = []

    if length_result["length"] < 12:
        suggestions.append(
            "Consider using a longer password or passphrase of at least 12 characters."
        )

    if length_result["length"] < 16:
        suggestions.append(
            "Longer passwords generally provide more room for unpredictability."
        )

    if character_result["character_type_count"] < 3:
        suggestions.append(
            "Increase character variety where appropriate, but do not rely on "
            "composition rules alone."
        )

    if character_result["unique_character_ratio"] < 0.50:
        suggestions.append(
            "Your password contains substantial character repetition. "
            "Use more varied characters or words."
        )

    if common_password:
        suggestions.append(
            "Your password matches a commonly used password and should not be used."
        )

    if pattern_result["sequences"]["detected"]:
        suggestions.append(
            "Remove predictable ascending or descending sequences."
        )

    if pattern_result["keyboard"]["detected"]:
        suggestions.append(
            "Avoid predictable keyboard patterns such as qwerty or asdf."
        )

    if pattern_result["repetition"]["detected"]:
        suggestions.append(
            "Avoid repeated characters or repeated blocks."
        )

    if pattern_result["common_words"]["detected"]:
        suggestions.append(
            "Avoid relying on common dictionary words as the main password structure."
        )

    if pattern_result["predictable_structure"]["detected"]:
        suggestions.append(
            "Adding predictable numbers or years to a common word does not "
            "automatically make a password strong."
        )

    if pattern_result["personal_information"]["detected"]:
        suggestions.append(
            "Avoid including personal information such as names, college names, "
            "or birth years."
        )

    suggestions.append(
        "Use a unique password for every important account."
    )

    suggestions.append(
        "Consider using a password manager to generate and store unique passwords."
    )

    suggestions.append(
        "Enable multi-factor authentication (MFA) whenever available."
    )

    # Remove duplicate suggestions while preserving order.
    return list(dict.fromkeys(suggestions))