def evaluate_summary(extracted_text: str, summary: dict) -> dict:
    """
    Basic quality checks + a simple confidence score (0–100).
    This is intentionally lightweight and deterministic.
    I’m not using an LLM judge here — this is a fast heuristic layer.
    """

    # Pull structured fields out of the summary.
    # If they don’t exist, default safely.
    bullets = summary.get("bullets", []) or []
    one_liner = summary.get("one_liner", "") or ""

    # I collect all problems here.
    # Instead of failing hard, I accumulate issues.
    issues = []

    # QUALITY CHECKS

    # If extracted text is very short, something might have gone wrong.
    # For example: scanned PDF, failed extraction, empty document.
    if len(extracted_text.split()) < 80:
        issues.append("Document text is very short; extraction may be incomplete.")

    # A one-liner summary should be meaningful.
    # If it's too short, the model probably underperformed.
    if not one_liner or len(one_liner.split()) < 8:
        issues.append("One-liner summary is missing or too short.")

    # I expect 5–7 bullets.
    # If there are fewer than 3, the summary is probably shallow.
    if len(bullets) < 3:
        issues.append("Too few bullet points (expected 5–7).")

    # SIMPLE SCORING SYSTEM

    # Start with perfect confidence.
    score = 100

    # Each issue reduces confidence by 20 points.
    # This is arbitrary but simple and interpretable.
    score -= 20 * len(issues)

    # Confidence can’t go below 0.
    score = max(0, score)

    # Return structured output.
    # I keep this JSON-friendly for UI display.
    return {
        "confidence": score,
        "issues": issues
    }
