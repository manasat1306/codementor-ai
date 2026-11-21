import re

import streamlit as st

from core.ai_client import ask_ai, AIError

MAX_CHARS = 6000
SECTIONS = ["HINT1", "HINT2", "HINT3", "FIX"]

SYSTEM_PROMPT = """You are CodeMentor AI, a patient debugging tutor for beginners.
The student gives you code that has a bug, and maybe an error message or a
description of what went wrong. Your job is to teach them HOW to find the bug,
not to hand over the answer.

Write your answer in exactly these 4 sections, using these exact markers on
their own lines, in this order:

[[HINT1]]
Ask the student ONE question that makes them check their own work. For example:
"What should this function return for the input [2, 4, 6]? Work it out by hand,
then compare it with the result you got." Do NOT name the line, the operator or
the bug type. Do NOT say what to change.

[[HINT2]]
Point to the AREA of the code where the problem is (for example, "the calculation
in the return statement") and say what KIND of mistake it could be in general
words (for example, "a part of the calculation that does not belong there").
Do NOT quote the wrong expression. Do NOT tell the student to remove, add or
change anything.

[[HINT3]]
Now be clear: say which line is wrong and why it gives the wrong result. Still
do NOT write the corrected code.

[[FIX]]
The full explanation: what the bug is, the corrected code in a code block,
and one tip to avoid this kind of bug next time.

Rules: use very simple English. Keep each hint short (1 to 3 sentences).
HINT1 and HINT2 must never contain corrected code and must never tell the
student what to remove, add or change. Never reveal the fix before the [[FIX]]
section.

If the code looks correct and you cannot find a bug, do NOT use the 4 sections.
Write only the marker [[NOBUG]] on its own line, then 2 or 3 simple sentences:
say honestly that you see no bug, and ask the student for the error message or
the output they expected."""


def parse_sections(text):
    """Split the AI answer into HINT1, HINT2, HINT3, FIX. Return None if broken."""
    if "[[NOBUG]]" in text:
        body = text.split("[[NOBUG]]", 1)[1].strip()
        return {"NOBUG": body} if body else None
    result = {}
    for i, name in enumerate(SECTIONS):
        if i + 1 < len(SECTIONS):
            pattern = rf"\[\[{name}\]\](.*?)(?=\[\[{SECTIONS[i + 1]}\]\])"
        else:
            pattern = rf"\[\[{name}\]\](.*)$"
        match = re.search(pattern, text, re.S)
        if not match or not match.group(1).strip():
            return None
        result[name] = match.group(1).strip()
    return result


def next_step():
    st.session_state.bug_level += 1


def start_over():
    st.session_state.pop("bug", None)
    st.session_state.bug_level = 0


if "bug_level" not in st.session_state:
    st.session_state.bug_level = 0

st.title("🐞 Bug Detective")
st.write(
    "Paste your buggy code. I will give you hints first, so you learn to find "
    "the bug yourself. The full fix comes last."
)

language = st.selectbox(
    "Language",
    ["Python", "JavaScript", "Java", "C", "C++", "HTML/CSS", "SQL", "Other"],
)
code = st.text_area("Your code", height=220, placeholder="Paste the code that is not working")
problem = st.text_area(
    "Error message or what went wrong (optional)",
    height=90,
    placeholder="Example: Expected 4.0 but got 5.0",
)

if st.button("Start debugging", type="primary"):
    if not code.strip():
        st.warning("Please paste your code first.")
    elif len(code) + len(problem) > MAX_CHARS:
        st.warning(f"Too long. Please keep code and message under {MAX_CHARS} characters.")
    else:
        prompt = (
            f"Language: {language}\n\nCode:\n{code}\n\n"
            f"Error or problem described by the student:\n{problem.strip() or '(none given)'}"
        )
        with st.spinner("Looking for the bug..."):
            try:
                answer = ask_ai(prompt, system_instruction=SYSTEM_PROMPT)
                parsed = parse_sections(answer)
                if parsed is None:
                    st.session_state.pop("bug", None)
                    st.error("The AI answer was in a wrong format. Please click the button again.")
                else:
                    st.session_state.bug = parsed
                    st.session_state.bug_level = 0
            except AIError as e:
                st.error(str(e))

bug = st.session_state.get("bug")
if bug and "NOBUG" in bug:
    st.divider()
    st.success("No bug found")
    st.write(bug["NOBUG"])
    st.button("🔄 Start over", on_click=start_over)
elif bug:
    level = st.session_state.bug_level
    st.divider()
    st.info("First, try to find the bug yourself for a minute. Then open a hint.")

    if level == 0:
        st.button("💡 Show Hint 1", on_click=next_step)
    if level >= 1:
        st.markdown("### 💡 Hint 1")
        st.write(bug["HINT1"])
        if level == 1:
            st.button("💡 Show Hint 2", on_click=next_step)
    if level >= 2:
        st.markdown("### 💡 Hint 2")
        st.write(bug["HINT2"])
        if level == 2:
            st.button("💡 Show Hint 3", on_click=next_step)
    if level >= 3:
        st.markdown("### 💡 Hint 3")
        st.write(bug["HINT3"])
        if level == 3:
            st.button("✅ Show the full fix", on_click=next_step)
    if level >= 4:
        st.markdown("### ✅ The fix")
        st.markdown(bug["FIX"])

    st.button("🔄 Start over", on_click=start_over)