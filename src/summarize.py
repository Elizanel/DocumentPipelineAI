import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Add it to your .env file.")

client = OpenAI(api_key=API_KEY)

def summarize_text(text: str) -> dict:
    """
    Returns a structured summary dict:
    {
      "bullets": [...],
      "entities": [...],
      "risks": [...],
      "one_liner": "..."
    }
    """

    # Keep it small to avoid token overload (we’ll add chunking later)
    text = text[:6000]

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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    import re

    content = response.choices[0].message.content.strip()

    # Remove markdown code fences if they exist
    content = re.sub(r"^```json", "", content)
    content = re.sub(r"^```", "", content)
    content = re.sub(r"```$", "", content)
    content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
        "one_liner": "",
        "bullets": [],
        "entities": [],
        "risks": [],
        "raw": content
    }