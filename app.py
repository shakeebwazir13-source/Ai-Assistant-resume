"""AI Text Assistant - a beginner-friendly Streamlit app powered by Google Gemini Flash."""

import os

import streamlit as st
from google import genai
from google.genai import errors, types

# ---------- Settings ----------
MODEL_NAME = "gemini-3.5-flash"  # If Google renames the model, change it here only.
MAX_CHARS = 8000  # Keeps requests small and fast.

TASKS = {
    "Summarize": "Summarize the user's text clearly and concisely in a short paragraph "
                 "followed by 3-5 bullet points of key takeaways.",
    "Explain simply": "Explain the user's text in very simple language, as if to a beginner. "
                      "Use short sentences and a helpful everyday example.",
    "Improve writing": "Rewrite the user's text so it is clearer, more professional, and "
                       "free of grammar mistakes. Keep the original meaning. "
                       "Return only the improved text.",
    "Make quiz questions": "Create 5 multiple-choice questions based on the user's text. "
                           "Give 4 options (A-D) for each and list the correct answers at the end.",
}

st.set_page_config(page_title="AI Text Assistant", page_icon="✨", layout="centered")


# ---------- Helpers ----------
def get_api_key():
    """Read the key from Streamlit secrets (local file or Cloud), else an environment variable."""
    try:
        key = st.secrets["GEMINI_API_KEY"]
        if key:
            return key
    except Exception:
        pass  # No secrets file or no such key - fall through.
    return os.getenv("GEMINI_API_KEY")


@st.cache_resource
def get_client(api_key: str):
    """Create the Gemini client once and reuse it."""
    return genai.Client(api_key=api_key)


def run_gemini(client, task: str, text: str) -> str:
    """Send the text to Gemini and return the answer as plain text."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=TASKS[task],
            temperature=0.7,
        ),
    )
    if not response.text:
        raise ValueError("The model returned an empty answer (it may have been blocked). "
                         "Try rephrasing your text.")
    return response.text


def friendly_error(err: errors.APIError) -> str:
    """Turn API error codes into messages a beginner can act on."""
    code = getattr(err, "code", None)
    if code in (400, 401, 403):
        return "Your API key looks invalid or lacks permission. Check the key and try again."
    if code == 404:
        return f"The model '{MODEL_NAME}' was not found. Update MODEL_NAME in app.py."
    if code == 429:
        return "Too many requests (free-tier limit reached). Wait a minute and try again."
    if code and code >= 500:
        return "Google's servers are having trouble. Please try again shortly."
    return f"Gemini API error: {err}"


# ---------- UI ----------
st.title("✨ AI Text Assistant")
st.caption("Paste some text, pick a task, and let Gemini do the work.")

api_key = get_api_key()
if not api_key:
    st.error(
        "No API key found. Add `GEMINI_API_KEY` to `.streamlit/secrets.toml` "
        "(local) or to the app's Secrets (Streamlit Cloud). See the README."
    )
    st.stop()

task = st.selectbox("What should I do?", list(TASKS.keys()))
user_text = st.text_area(
    "Your text",
    height=220,
    max_chars=MAX_CHARS,
    placeholder="Paste an article, notes, an email, or anything you want help with...",
)
st.caption(f"{len(user_text)} / {MAX_CHARS} characters")

if st.button("Generate", type="primary"):
    if not user_text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            with st.spinner("Thinking..."):
                answer = run_gemini(get_client(api_key), task, user_text.strip())
            st.subheader("Result")
            st.markdown(answer)
            with st.expander("Copy as plain text"):
                st.code(answer, language=None)
        except errors.APIError as err:
            st.error(friendly_error(err))
        except ValueError as err:
            st.warning(str(err))
        except Exception as err:  # Last safety net so the app never crashes.
            st.error(f"Something unexpected happened: {err}")

st.divider()
st.caption("Built with Streamlit and Google Gemini.")
