# DocumentPipelineAI
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
