# The ONLY place where model names are set.
# The first one is the main model. The others are backups,
# used automatically if the main one is busy or fails.
# Free limits (checked 21 Nov 2026): flash-lite = 15 per minute, 500 per day.
MODEL_CANDIDATES = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]

MAX_RETRIES_PER_MODEL = 2   # tries per model when the server is busy (503)
RETRY_WAIT_SECONDS = 2      # wait time between tries