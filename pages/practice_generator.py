import random
import re

import streamlit as st

from core.ai_client import ask_ai, AIError

SYSTEM_PROMPT = """You are CodeMentor AI, a patient programming tutor for beginners.
Create ONE small practice problem for a student. Use very simple English.

Write your answer in exactly 3 parts. Each part starts with a marker on its own line.
Write nothing before the first marker.

[[PROBLEM]]
A short title in bold, then the task in 2 to 4 simple sentences, then one example
with sample input and expected output. Do NOT include the solution or code that solves it.
The example output must match the task exactly. If the task says each item is printed
on a new line, show the example output with each item on its own line.

[[HINT]]
ONE gentle hint (1 or 2 sentences) that helps the student start thinking.
Do not write code and do not give the full answer.

[[SOLUTION]]
The full solution code inside a code block, then 2 or 3 simple sentences
explaining how it works.

Rules: the problem must match the language, topic and level given.
Keep it small, something a beginner can solve in 5 to 10 minutes.
You will be given a THEME. Build the problem story around that theme.
You will be given a list of problems NOT to repeat. Make a completely different one.
Do not use very common textbook problems like printing even numbers or the sum of 1 to 10."""

TOPICS = [
    "Variables and input/output",
    "If / else conditions",
    "Loops",
    "Lists / arrays",
    "Strings",
    "Functions",
    "Dictionaries / maps",
]

LEVELS = ["Beginner", "Easy", "Medium"]

THEMES = [
    "a video game score",
    "shopping and prices",
    "a school marks list",
    "a music playlist",
    "weather and temperature",
    "pets and animals",
    "a bus or train ticket",
    "a birthday party",
    "a cricket match",
    "a food menu",
    "a library book list",
    "a mobile phone battery",
    "a garden with plants",
    "a savings jar",
]


def parse_result(text):
    """Split the AI text into problem, hint, solution. Return None if something is missing."""
    parts = re.split(r"\[\[(PROBLEM|HINT|SOLUTION)\]\]", text)
    found = {}
    for i in range(1, len(parts) - 1, 2):
        found[parts[i]] = parts[i + 1].strip()
    if all(found.get(key) for key in ("PROBLEM", "HINT", "SOLUTION")):
        return found
    return None


def get_title(problem_text):
    """Take the first non-empty line of the problem as its title."""
    for line in problem_text.splitlines():
        line = line.strip().strip("*#").strip()
        if line:
            return line
    return "unknown"


def reset_state():
    st.session_state.pg_result = None
    st.session_state.pg_show_hint = False
    st.session_state.pg_show_solution = False


if "pg_result" not in st.session_state:
    reset_state()

# This list is NOT cleared by reset_state, so old titles are remembered
if "pg_old_titles" not in st.session_state:
    st.session_state.pg_old_titles = []

st.title("🎯 Practice Generator")
st.write("Get a small practice problem. Try it yourself first. Open the hint only if you are stuck.")

language = st.selectbox(
    "Language",
    ["Python", "JavaScript", "Java", "C", "C++"],
)
topic = st.selectbox("Topic", TOPICS)
level = st.selectbox("Level", LEVELS)

if st.button("Make a practice problem", type="primary"):
    reset_state()
    theme = random.choice(THEMES)
    old = st.session_state.pg_old_titles[-3:]
    old_text = "; ".join(old) if old else "none"
    prompt = (
        f"Language: {language}\n"
        f"Topic: {topic}\n"
        f"Level: {level}\n"
        f"THEME: {theme}\n"
        f"Problems NOT to repeat: {old_text}\n"
        f"Variation number: {random.randint(1, 100000)}"
    )
    with st.spinner("Creating your problem..."):
        try:
            answer = ask_ai(prompt, system_instruction=SYSTEM_PROMPT)
            result = parse_result(answer)
            if result is None:
                st.error("The AI answer came in a wrong format. Please click the button again.")
            else:
                st.session_state.pg_result = result
                st.session_state.pg_old_titles.append(get_title(result["PROBLEM"]))
        except AIError as e:
            st.error(str(e))

result = st.session_state.pg_result

if result:
    st.divider()
    st.subheader("Your problem")
    st.markdown(result["PROBLEM"])
    st.info("Try to solve it yourself first. Write it in your editor and run it.")

    if st.button("💡 Show hint"):
        st.session_state.pg_show_hint = True

    if st.session_state.pg_show_hint:
        st.warning(result["HINT"])

    if st.button("✅ Show solution"):
        st.session_state.pg_show_solution = True

    if st.session_state.pg_show_solution:
        st.success("Here is one possible solution:")
        st.markdown(result["SOLUTION"])

    if st.button("Start over"):
        reset_state()
        st.rerun()