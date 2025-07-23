import streamlit as st
import requests

st.title("GitHub Issue Analyzer")
repo_url = st.text_input("GitHub Repository URL")
issue_number = st.number_input("Issue Number", min_value=1, step=1)
use_gemini = st.checkbox("Use Gemini instead of OpenAI")

if st.button("Analyze"):
    if not repo_url or not issue_number:
        st.error("Please enter a valid repository URL and issue number.")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={"repo_url": repo_url, "issue_number": issue_number, "use_gemini": use_gemini}
                )
                response.raise_for_status()
                st.success("Analysis Complete")
                st.json(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e.response.status_code} - {e.response.text}")
