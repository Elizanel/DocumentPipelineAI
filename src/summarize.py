import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Pull API key from environment.
API_KEY = os.getenv("OPENAI_API_KEY")

# Fail fast if key is missing.
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Add it to your .env file.")

# Initialize OpenAI client once.
client = OpenAI(api_key=API_KEY)

def summarize_text(text: str) -> dict:
    """
    Returns structured summary dict:
    {
      "bullets": [...],
      "entities": [...],
      "risks": [...],
      "one_liner": "..."
    }
    """

    # Hard limit text to avoid token overflow.
    # This is temporary until chunking is added.
    text = text[:6000]

    # Structured prompt with explicit JSON schema.
    # This increases reliability and reduces hallucinated formats.
    prompt = f"""
You are a professional document analyst.

Extract the following from the document and return ONLY valid JSON with this schema:
{{
  "one_liner": "One sentence summary",
  "bullets": ["5-7 bullet points max"],
  "entities": ["people, companies, funds, products"],
  "risks": ["key risks or issues mentioned (if none, empty list)"]
}}

Document:
{text}
"""

    # Low temperature = more deterministic outputs.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    import re

    # Grab model output.
    content = response.choices[0].message.content.strip()

    # Remove markdown code fences if model adds them.
    content = re.sub(r"^```json", "", content)
    content = re.sub(r"^```", "", content)
    content = re.sub(r"```$", "", content)
    content = content.strip()

    try:
        # Parse JSON safely.
        return json.loads(content)

    except json.JSONDecodeError:
        # If parsing fails, return fallback structure.
        # This prevents the app from crashing.
        return {
            "one_liner": "",
            "bullets": [],
            "entities": [],
            "risks": [],
            "raw": content  # Save raw model output for debugging.
        }
