def tag_document(text: str) -> list[str]:
    """
    Simple rule-based tagging (fast + reliable).
    Later we can add LLM-based tags.
    """

    # Lowercase for case-insensitive matching.
    t = text.lower()

    tags = []

    # Keyword dictionary for categories.
    rules = {
        "compliance": ["compliance", "regulation", "sec", "finra", "policy", "audit"],
        "tax": ["tax", "irs", "withholding", "1099", "k-1"],
        "investing": ["portfolio", "fund", "allocation", "returns", "risk", "advisor"],
        "health": ["health", "mental", "patient", "clinical", "care", "well-being"],
        "education": ["student", "course", "curriculum", "learning", "class"],
        "legal": ["agreement", "liability", "terms", "contract", "governing law"]
    }

    # Loop through each category.
    # If any keyword appears, assign that tag.
    for tag, keywords in rules.items():
        if any(k in t for k in keywords):
            tags.append(tag)

    # If no category matched, default to "general".
    if not tags:
        tags.append("general")

    return tags
