# 🏗️ BewerbungsBot AEC

A Python-powered web app that automatically generates professional German CV and cover letter documents tailored for the AEC (Architecture, Engineering, Construction) industry — powered by Google Gemini AI.

🔗 **Live App:** [bewerbungsbot-aec.streamlit.app](https://bewerbungsbot-aec.streamlit.app)

---

## What It Does

- Reads your existing CV (PDF or DOCX) and extracts real work experience
- Takes a job advertisement as input
- Uses Google Gemini AI to rewrite and tailor your CV and cover letter
- Outputs professionally formatted German `.docx` files (DIN 5008 compliant)
- Injects AEC-specific keywords (ISO 19650, HOAI, VOB) automatically when relevant

---

## Project Structure

```
bewerbungsbot-aec/
│
├── app.py                # Streamlit UI — browser interface
├── models.py             # UserProfile data model (Pydantic)
├── generator.py          # Gemini API calls + prompt engineering
├── document_builder.py   # Word document formatter (python-docx)
├── cv_extractor.py       # PDF/DOCX text extraction (pdfplumber)
│
├── .env                  # Local API keys (never pushed to GitHub)
├── .gitignore            # Excludes .env, .venv, __pycache__
└── requirements.txt      # All Python dependencies
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI / Frontend | Streamlit |
| AI / LLM | Google Gemini 2.5 Flash |
| Document Generation | python-docx |
| PDF Parsing | pdfplumber |
| Data Validation | Pydantic |
| Deployment | Streamlit Community Cloud |

---

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/bewerbungsbot-aec.git
cd bewerbungsbot-aec
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_google_aistudio_key_here
```
Get a free key at [aistudio.google.com](https://aistudio.google.com)

### 5. Run the app
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

---

## How to Use

1. Fill in your personal information in the sidebar
2. Upload your existing CV (PDF or DOCX)
3. Paste the full job advertisement text
4. Click **Generate CV** or **Generate Cover Letter**
5. Download the tailored `.docx` file

---

## Deployment (Streamlit Community Cloud)

1. Push code to GitHub (`.env` is excluded via `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository → select `app.py`
4. Add your API key under **Settings → Secrets**:
```toml
GEMINI_API_KEY = "your_key_here"
```

---

## Roadmap

- [ ] PDF export option
- [ ] Photo upload integration into CV document
- [ ] Multi-language cover letter support
- [ ] Automatic keyword matching score
- [ ] Batch generation for multiple job applications

---

## Author

**Yasir Kazmi** — BIM Specialist & Python Developer  
[yasirkazmi.com](https://www.yasirkazmi.com) · [LinkedIn](https://linkedin.com/in/yasirhkazmi)

---

*Built as part of a Python + AI learning journey — January 2026*
