def evaluate_summary(extracted_text: str, summary: dict) -> dict:
    """
    Basic quality checks + a simple confidence score (0–100).
    """

    bullets = summary.get("bullets", []) or []
    one_liner = summary.get("one_liner", "") or ""

    issues = []

    # Checks
    if len(extracted_text.split()) < 80:
        issues.append("Document text is very short; extraction may be incomplete.")

    if not one_liner or len(one_liner.split()) < 8:
        issues.append("One-liner summary is missing or too short.")

    if len(bullets) < 3:
        issues.append("Too few bullet points (expected 5–7).")

    # Simple confidence score
    score = 100
    score -= 20 * len(issues)
    score = max(0, score)

    return {
        "confidence": score,
        "issues": issues
    }