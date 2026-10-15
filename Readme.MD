# 📄 ATS Resume Analyzer

A Streamlit web app that analyzes a resume and returns an **estimated ATS score**, a score
breakdown, missing keywords, and specific suggestions to improve it. Powered by Google
**Gemini Flash**.

## Features
- Upload a resume as **PDF, DOCX or TXT**
- Optional **job description** for a tailored score
- Overall ATS score (0-100) plus Formatting, Keywords, Content impact and Structure scores
- Strengths, weaknesses, missing keywords, improvement tips and example bullet rewrites
- Quick automatic checks (email, phone, LinkedIn, standard sections, word count)
- Download the report as JSON

> Scores are AI-generated estimates, not output from a real ATS.

## Tech stack
Python, Streamlit, Google Gemini API (`google-genai`), pypdf, python-docx

## Run locally (Windows + VS Code)
1. Install Python 3.10+ and open this folder in VS Code.
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Get a free API key at https://aistudio.google.com/apikey
5. Add the key (choose one):
   - Create `.streamlit/secrets.toml` containing: `GEMINI_API_KEY = "your-key-here"`
   - or paste it into the app's sidebar when it opens
6. Start the app:
   ```
   streamlit run app.py
   ```

## Configuration
| Setting | Purpose | Default |
|---|---|---|
| `GEMINI_API_KEY` | Gemini API key (secrets or env var) | none |
| `GEMINI_MODEL` | Gemini model name (env var) | `gemini-2.5-flash` |

## Deploy on Streamlit Community Cloud
1. Push this repo to GitHub (never commit `secrets.toml`).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, choose your repo, branch `main`, and main file `app.py`.
4. Open **Advanced settings → Secrets** and add: `GEMINI_API_KEY = "your-key-here"`
5. Click **Deploy**.

## Project structure
```
app.py            # Streamlit app
requirements.txt  # Dependencies
README.md         # This file
```

## Privacy
Resume text is sent to Google's Gemini API for analysis and is not stored by this app.
