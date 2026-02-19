from datetime import datetime
from pathlib import Path
import json

def save_text(text: str, original_filename: str) -> str:
    # Make sure the outputs directory exists.
    # exist_ok=True prevents crash if it already exists.
    Path("outputs").mkdir(exist_ok=True)

    # Add timestamp so files don’t overwrite each other.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Clean filename to avoid weird path issues.
    safe_name = original_filename.replace(" ", "_").replace(".pdf", "")

    # Build output file path.
    out_path = Path("outputs") / f"{safe_name}_{timestamp}.txt"

    # Write extracted text to disk.
    # utf-8 ensures proper encoding.
    out_path.write_text(text, encoding="utf-8")

    # Return path so UI can display it.
    return str(out_path)


def save_json(data: dict, original_filename: str) -> str:
    # Same logic as save_text — just JSON version.
    Path("outputs").mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = original_filename.replace(" ", "_").replace(".pdf", "")
    out_path = Path("outputs") / f"{safe_name}_{timestamp}.json"

    # indent=2 makes it human-readable.
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    return str(out_path)
