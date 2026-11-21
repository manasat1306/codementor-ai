import streamlit as st

st.set_page_config(page_title="CodeMentor AI", page_icon="🧑‍🏫", layout="wide")

pages = [
    st.Page("pages/code_explainer.py", title="Code Explainer", icon="📖"),
    st.Page("pages/bug_detective.py", title="Bug Detective", icon="🐞"),
    st.Page("pages/practice_generator.py", title="Practice Generator", icon="🎯"),
]

st.sidebar.title("CodeMentor AI")
st.sidebar.caption("Learn how to think, not just copy answers.")

current_page = st.navigation(pages)
current_page.run()