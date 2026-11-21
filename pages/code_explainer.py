import streamlit as st

from core.ai_client import ask_ai, AIError

MAX_CHARS = 6000

SYSTEM_PROMPT = """You are CodeMentor AI, a patient programming tutor for beginners.
Explain code in very simple English, like you are talking to a student who
started programming this month.

Follow this format:
1. **What this code does** - 1 or 2 simple sentences.
2. **Line by line** - go through the code in order. Quote each line (or small
   group of lines) in `backticks`, then explain it in simple words.
3. **Key concepts used** - list 2 to 4 programming ideas used here, each with a
   one-line meaning.
4. **Try it yourself** - give ONE small question or tiny change the student can
   try to check their understanding. Do not give the answer.

Rules: no hard words without explaining them. Do not rewrite the whole code.
If the text is not code, say so politely and ask for code."""

st.title("📖 Code Explainer")
st.write("Paste your code and get a simple, line-by-line explanation.")

language = st.selectbox(
    "Language",
    ["Python", "JavaScript", "Java", "C", "C++", "HTML/CSS", "SQL", "Other"],
)
code = st.text_area("Paste your code here", height=250, placeholder="print('Hello')")

if st.button("Explain my code", type="primary"):
    if not code.strip():
        st.warning("Please paste some code first.")
    elif len(code) > MAX_CHARS:
        st.warning(f"Your code is too long ({len(code)} characters). Please paste less than {MAX_CHARS}.")
    else:
        prompt = f"Language: {language}\n\nCode:\n{code}"
        with st.spinner("Reading your code..."):
            try:
                answer = ask_ai(prompt, system_instruction=SYSTEM_PROMPT)
                st.markdown(answer)
            except AIError as e:
                st.error(str(e))