# CodeMentor AI

An AI programming tutor for beginners. It teaches you **how to think and debug**, not just how to copy answers.

**Live app:** https://manasat1306-codementor-ai-app-ktobkc.streamlit.app/

Built for the "Build Your First AI App 2026" hackathon on Devpost.

## The problem

Beginners often paste their bug into an AI tool and copy the fix without learning anything. Next time, they are stuck again.

## The solution

CodeMentor AI gives help in small steps. You try first, you get hints, and the full answer comes last.

## Features

- **Code Explainer:** paste code and get a simple, line-by-line explanation in easy English.
- **Bug Detective:** paste buggy code. You get 3 hints one by one (the first two do not give the answer), then the full fix. If your code has no bug, it tells you so.
- **Practice Generator:** choose a language, topic and level, and get a small practice problem with a hint and a solution you can open when you are ready.

## Technologies

- Python
- [Streamlit](https://streamlit.io/) for the web app and hosting (Streamlit Community Cloud)
- [Google Gemini API](https://ai.google.dev/) (`google-genai`) for the AI
- `python-dotenv` for reading the API key locally

## AI models used

The app uses Gemini Flash-Lite models on the free tier: `gemini-3.5-flash-lite`, with `gemini-3.1-flash-lite` as a backup. If the first model is busy or its limit is reached, the app retries and then switches to the backup. The model names are kept in one place: `core/config.py`.

## How to run it on your computer

1. Install Python and clone this repo:

```
git clone https://github.com/manasat1306/codementor-ai.git
cd codementor-ai
```

2. Create and activate a virtual environment (Windows PowerShell):

```
python -m venv venv
.\venv\Scripts\activate
```

3. Install the packages:

```
pip install -r requirements.txt
```

4. Get a free Gemini API key from Google AI Studio. Copy `.env.example` to a new file named `.env` and put your key in it:

```
GEMINI_API_KEY=your-key-here
```

5. Start the app:

```
streamlit run app.py
```

Never upload your `.env` file or your key to GitHub. The `.gitignore` file already blocks `.env`.

## Project structure

```
app.py                      # page navigation
core/config.py              # model names and retry settings
core/ai_client.py           # talks to Gemini, handles retries and errors
pages/code_explainer.py     # Code Explainer page
pages/bug_detective.py      # Bug Detective page
pages/practice_generator.py # Practice Generator page
```

## My contribution and AI help

I am Manasa T, a BCA graduate. I built this project step by step, with Claude (by Anthropic) as my guide.

- **Claude** helped me plan the project and gave me the code and the AI prompts, one step at a time.
- **I** set up the project, created the files, ran every step, tested each page with my own buggy code, reported the problems I found, fixed my setup errors (for example my API key file), and set up Git, GitHub and the Streamlit deployment.
- **Gemini** is the AI inside the app itself.

## Credits

- [Streamlit](https://streamlit.io/) for the app framework and free hosting
- [Google Gemini](https://ai.google.dev/) for the AI models
- [Claude](https://www.anthropic.com/claude) for development guidance