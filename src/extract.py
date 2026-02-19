import fitz  # PyMuPDF

def extract_text(uploaded_file) -> str:
    # Important: reset file pointer.
    # Streamlit file objects may already be partially read.
    uploaded_file.seek(0)

    # Read raw bytes.
    raw = uploaded_file.read()

    # If file is empty, return early.
    if not raw:
        return ""

    text = ""

    # Open PDF from memory (not disk).
    # filetype="pdf" ensures correct parsing.
    with fitz.open(stream=raw, filetype="pdf") as doc:
        for page in doc:
            # Extract raw text per page.
            # This may not work well for scanned PDFs (OCR needed later).
            text += page.get_text()

    return text
