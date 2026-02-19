# DocPipeline AI

DocPipeline AI is a lightweight document intelligence prototype that ingests PDFs, extracts text, generates structured AI summaries, tags the document, and runs basic quality evaluation.

## What it does
- Upload a PDF
- Extract text from the PDF
- Generate a structured summary (one-liner, bullets, entities, risks)
- Add rule-based document tags
- Compute a simple confidence score + issues list
- Save extracted text and summary artifacts to disk

## Tech stack
- Python
- Streamlit (UI)
- PyMuPDF (PDF text extraction)
- OpenAI API (LLM summarization)
- python-dotenv (local environment variables)

## Project structure

<img width="999" height="983" alt="Screenshot 2026-02-12 at 6 04 12 PM" src="https://github.com/user-attachments/assets/1e008bab-96d6-4c75-91d1-8bc7a345ede3" />

<img width="913" height="598" alt="Screenshot 2026-02-12 at 6 04 27 PM" src="https://github.com/user-attachments/assets/75e90999-f32e-4f9d-939e-940ad3260b7e" />

<img width="819" height="781" alt="Screenshot 2026-02-12 at 6 04 32 PM" src="https://github.com/user-attachments/assets/2c8c4a0e-35be-470e-a1e0-3fe3d175e7fb" />

