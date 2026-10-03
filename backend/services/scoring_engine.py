def calculate_score(
    length_result,
    character_result,
    pattern_result,
    common_password
):
    """
    Calculate a project-defined password strength score from 0-100.

    Important:
    Composition alone does not make a password strong.
    Common words, predictable structures, sequences,
    keyboard patterns, and repetition receive strong penalties.
    """

    score = 0

    # ---------------------------------------------------------
    # 1. LENGTH — maximum 35
    # ---------------------------------------------------------
    score += length_result.get("contribution", 0)

    password_length = length_result.get("length", 0)

    # ---------------------------------------------------------
    # 2. CHARACTER DIVERSITY — maximum 15
    # ---------------------------------------------------------
    type_count = character_result.get("character_type_count", 0)

    if type_count >= 4:
        score += 15
    elif type_count == 3:
        score += 10
    elif type_count == 2:
        score += 5

    # ---------------------------------------------------------
    # 3. UNIQUE CHARACTER RATIO — maximum 10
    # ---------------------------------------------------------
    unique_ratio = character_result.get(
        "unique_character_ratio",
        0
    )

    if unique_ratio >= 0.85:
        score += 10
    elif unique_ratio >= 0.70:
        score += 7
    elif unique_ratio >= 0.50:
        score += 4

    # ---------------------------------------------------------
    # Extract actual detection states
    # ---------------------------------------------------------
    sequence_detected = pattern_result.get(
        "sequences", {}
    ).get("detected", False)

    keyboard_detected = pattern_result.get(
        "keyboard", {}
    ).get("detected", False)

    repetition_detected = pattern_result.get(
        "repetition", {}
    ).get("detected", False)

    common_word_detected = pattern_result.get(
        "common_words", {}
    ).get("detected", False)

    predictable_detected = pattern_result.get(
        "predictable_structure", {}
    ).get("detected", False)

    personal_info_detected = pattern_result.get(
        "personal_information", {}
    ).get("detected", False)

    # ---------------------------------------------------------
    # 4. PATTERN RESISTANCE — maximum 20
    # ---------------------------------------------------------
    pattern_score = 20

    if sequence_detected:
        pattern_score -= 8

    if keyboard_detected:
        pattern_score -= 8

    if repetition_detected:
        pattern_score -= 8

    score += max(0, pattern_score)

    # ---------------------------------------------------------
    # 5. NON-COMMON PASSWORD — maximum 10
    # ---------------------------------------------------------
    if not common_password:
        score += 10

    # ---------------------------------------------------------
    # 6. ADDITIONAL UNPREDICTABILITY — maximum 10
    # ---------------------------------------------------------
    score += 10

    # ---------------------------------------------------------
    # 7. STRONG WEAKNESS PENALTIES
    # ---------------------------------------------------------

    # Common dictionary words
    if common_word_detected:
        score -= 25

    # Word + number/year structures
    if predictable_detected:
        score -= 25

    # Personal information supplied by the user
    if personal_info_detected:
        score -= 25

    # Exact common password
    if common_password:
        score -= 50

    # Sequential characters
    if sequence_detected:
        score -= 30

    # Keyboard patterns
    if keyboard_detected:
        score -= 30

    # Repeated characters/blocks
    if repetition_detected:
        score -= 35

    # ---------------------------------------------------------
    # 8. EXTREME CHARACTER REUSE
    # ---------------------------------------------------------
    if unique_ratio <= 0.20:
        score -= 20

    # ---------------------------------------------------------
    # 9. LOW DIVERSITY + SHORT PASSWORD
    # ---------------------------------------------------------
    if type_count == 1 and password_length < 12:
        score -= 15

    # ---------------------------------------------------------
    # 10. VERY SHORT PASSWORD
    # ---------------------------------------------------------
    if password_length < 8:
        score -= 20

    # ---------------------------------------------------------
    # 11. FINAL SCORE
    # ---------------------------------------------------------
    score = max(0, min(100, round(score)))

    # ---------------------------------------------------------
    # 12. PROJECT-DEFINED CLASSIFICATION
    # ---------------------------------------------------------
    if score <= 20:
        classification = "VERY WEAK"
    elif score <= 40:
        classification = "WEAK"
    elif score <= 60:
        classification = "MODERATE"
    elif score <= 80:
        classification = "STRONG"
    else:
        classification = "VERY STRONG"

    return {
        "score": score,
        "classification": classification
    }