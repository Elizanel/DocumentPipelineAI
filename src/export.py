from datetime import datetime
from pathlib import Path
import json

def save_text(text: str, original_filename: str) -> str:
    Path("outputs").mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = original_filename.replace(" ", "_").replace(".pdf", "")
    out_path = Path("outputs") / f"{safe_name}_{timestamp}.txt"
    out_path.write_text(text, encoding="utf-8")
    return str(out_path)

def save_json(data: dict, original_filename: str) -> str:
    Path("outputs").mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = original_filename.replace(" ", "_").replace(".pdf", "")
    out_path = Path("outputs") / f"{safe_name}_{timestamp}.json"
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return str(out_path)