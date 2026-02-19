# Streamlit is the UI framework. This is what turns my Python script into a web app.
import streamlit as st

# These are my pipeline steps. I separated them into src/ so this file
# stays clean and just orchestrates everything.
from src.extract import extract_text        # Step 1: Pull text out of the PDF
from src.export import save_text, save_json  # Step 2: Save outputs to disk
from src.summarize import summarize_text     # Step 3: Generate AI summary
from src.tag import tag_document             # Step 4: Classify / tag document
from src.evaluate import evaluate_summary    # Step 5: Reliability / quality check

# Configure the app settings. Title + layout.
# Centered keeps it clean and simple.
st.set_page_config(page_title="DocPipeline AI 📝", layout="centered")

# App header
st.title("DocPipeline AI ")
st.caption("Upload a PDF → Extract text → Summarize → Tag + Evaluate")

# This creates the file upload widget.
# Only accepts PDFs.
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# Everything below only runs IF a file has been uploaded.
if uploaded_file:
    # Just showing the filename for user clarity.
    st.write(f"**File:** {uploaded_file.name}")

    # STEP 1: EXTRACTION

    # This button triggers text extraction.
    if st.button("Run Extraction"):
        # Spinner just improves UX so user knows something is happening.
        with st.spinner("Extracting text..."):
            # Call my extraction function.
            # This should return a string of extracted text.
            text = extract_text(uploaded_file)

        # If extraction failed (empty text), show error.
        if not text:
            st.error("No text extracted. Try another PDF (some PDFs are scanned images).")
        else:
            # If successful:
            st.success("Extraction complete!")

            # Store the extracted text in session_state.
            # This is critical because Streamlit reruns the script top-to-bottom
            # every time something happens.
            st.session_state["extracted_text"] = text

            # Show preview so user can confirm it looks correct.
            st.subheader("Text Preview (first 1,000 characters)")
            st.write(text[:1000])

            # Quick sanity check for document size.
            st.write(f"**Word count:** {len(text.split())}")

            # Save extracted text to disk.
            # Good for debugging and auditability.
            saved_path = save_text(text, uploaded_file.name)
            st.info(f"Saved extracted text to: `{saved_path}`")

    # STEP 2: SUMMARIZE + TAG + EVALUATE

    # Only show summarize button if extraction already happened.
    # This prevents user from skipping steps.
    if "extracted_text" in st.session_state:

        if st.button("Summarize Document"):
            with st.spinner("Generating summary..."):

                # Call summarization model.
                # This returns structured JSON (ideally).
                result = summarize_text(st.session_state["extracted_text"])

                # IMPORTANT: Tagging + evaluation depend on summary existing.
                # So I only run them AFTER I have the summary result.

                # Tagging step (categorization).
                tags = tag_document(st.session_state["extracted_text"])

                # Reliability / quality check step.
                # This compares original text with generated summary.
                evaluation = evaluate_summary(
                    st.session_state["extracted_text"], 
                    result
                )

                # Attach tags + evaluation to the result JSON.
                result["tags"] = tags
                result["evaluation"] = evaluation

                # Store final result in session state so it persists.
                st.session_state["summary_result"] = result

                # Save final AI output to JSON file.
                json_path = save_json(result, uploaded_file.name)
                st.info(f"Saved AI summary to: `{json_path}`")

# DISPLAY SECTION

# If summary_result exists, display everything nicely.
if "summary_result" in st.session_state:
    st.subheader("AI Summary")

    # Short alias so code below is cleaner.
    res = st.session_state["summary_result"]

    # One-liner summary
    if res.get("one_liner"):
        st.write(f"**One-liner:** {res['one_liner']}")

    # Bullet points
    if res.get("bullets"):
        st.markdown("**Key Points**")
        for b in res["bullets"]:
            st.write(f"- {b}")

    # Named entities
    if res.get("entities"):
        st.markdown("**Key Entities**")
        st.write(", ".join(res["entities"]))

    # Risk flags (if model detected concerns)
    if res.get("risks") is not None:
        st.markdown("**Risks / Flags**")
        if len(res["risks"]) == 0:
            st.write("None detected.")
        else:
            for r in res["risks"]:
                st.write(f"- {r}")

    # Tags
    if res.get("tags"):
        st.markdown("**Tags**")
        st.write(", ".join(res["tags"]))

    # Reliability evaluation section
    if res.get("evaluation"):
        st.markdown("**Quality Check**")
        st.write(f"Confidence score: **{res['evaluation']['confidence']} / 100**")

        if res["evaluation"]["issues"]:
            st.write("Issues:")
            for i in res["evaluation"]["issues"]:
                st.write(f"- {i}")
        else:
            st.write("No issues detected.")

    # Fallback: If the model failed to return valid JSON
    if res.get("raw"):
        st.warning("Model response was not valid JSON. Showing raw output below:")
        st.write(res["raw"])
