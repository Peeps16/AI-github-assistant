import streamlit as st, requests, os

st.set_page_config("GitHub Issue AI Assistant")
st.title("🧠 GitHub Issue AI Assistant")
st.markdown("Submit a GitHub issue (URL + number) to get a structured JSON summary.")

repo = st.text_input("Repository URL", "https://github.com/facebook/react")
issue_num = st.number_input("Issue Number", min_value=1)
if st.button("Analyze"):
    if not repo or not issue_num: st.warning("Both fields required")
    else:
        with st.spinner("Analyzing..."):
            try:
                resp = requests.post("http://localhost:8000/analyze", json={"repo_url": repo, "issue_number": int(issue_num)})
                if resp.status_code == 200:
                    st.subheader("✅ Analysis Result")
                    st.json(resp.json())
                    st.download_button("💾 Save JSON", data=resp.text, file_name="analysis.json")
                else:
                    st.error(f"Error {resp.status_code}: {resp.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
