import fitz  # PyMuPDF

def extract_text(uploaded_file) -> str:
    uploaded_file.seek(0)
    raw = uploaded_file.read()
    if not raw:
        return ""

    text = ""
    with fitz.open(stream=raw, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text