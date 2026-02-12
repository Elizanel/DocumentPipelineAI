import streamlit as st
from src.extract import extract_text
from src.export import save_text, save_json
from src.summarize import summarize_text
from src.tag import tag_document
from src.evaluate import evaluate_summary

st.set_page_config(page_title="DocPipeline AI 📝", layout="centered")

st.title("DocPipeline AI ")
st.caption("Upload a PDF → Extract text → Summarize → Tag + Evaluate")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    st.write(f"**File:** {uploaded_file.name}")

    if st.button("Run Extraction"):
        with st.spinner("Extracting text..."):
            text = extract_text(uploaded_file)

        if not text:
            st.error("No text extracted. Try another PDF (some PDFs are scanned images).")
        else:
            st.success("Extraction complete!")
            st.session_state["extracted_text"] = text

            st.subheader("Text Preview (first 1,000 characters)")
            st.write(text[:1000])
            st.write(f"**Word count:** {len(text.split())}")

            saved_path = save_text(text, uploaded_file.name)
            st.info(f"Saved extracted text to: `{saved_path}`")

    # Only show summarize button if we have extracted text saved
    if "extracted_text" in st.session_state:
        if st.button("Summarize Document"):
            with st.spinner("Generating summary..."):
                result = summarize_text(st.session_state["extracted_text"])

                # Tag + Evaluate (must happen AFTER result exists)
                tags = tag_document(st.session_state["extracted_text"])
                evaluation = evaluate_summary(st.session_state["extracted_text"], result)

                result["tags"] = tags
                result["evaluation"] = evaluation

                st.session_state["summary_result"] = result

                json_path = save_json(result, uploaded_file.name)
                st.info(f"Saved AI summary to: `{json_path}`")

# Display summary if it exists
if "summary_result" in st.session_state:
    st.subheader("AI Summary")

    res = st.session_state["summary_result"]

    if res.get("one_liner"):
        st.write(f"**One-liner:** {res['one_liner']}")

    if res.get("bullets"):
        st.markdown("**Key Points**")
        for b in res["bullets"]:
            st.write(f"- {b}")

    if res.get("entities"):
        st.markdown("**Key Entities**")
        st.write(", ".join(res["entities"]))

    if res.get("risks") is not None:
        st.markdown("**Risks / Flags**")
        if len(res["risks"]) == 0:
            st.write("None detected.")
        else:
            for r in res["risks"]:
                st.write(f"- {r}")

    if res.get("tags"):
        st.markdown("**Tags**")
        st.write(", ".join(res["tags"]))

    if res.get("evaluation"):
        st.markdown("**Quality Check**")
        st.write(f"Confidence score: **{res['evaluation']['confidence']} / 100**")
        if res["evaluation"]["issues"]:
            st.write("Issues:")
            for i in res["evaluation"]["issues"]:
                st.write(f"- {i}")
        else:
            st.write("No issues detected.")

    if res.get("raw"):
        st.warning("Model response was not valid JSON. Showing raw output below:")
        st.write(res["raw"])