# 🤖 AI-Powered Resume Screening System

A production-ready NLP pipeline that automatically evaluates resumes against job descriptions using TF-IDF vectorization, cosine similarity, and AI content detection.

## ✨ New Premium UI (v2.0)
- **Neon Glassmorphism Design**: Modern, futuristic aesthetic with animated gradients.
- **Interactive Charts**: Plotly gauges for Match Score and AI Probability.
- **Smooth Animations**: CSS keyframe animations for background and cards.
- **Enhanced Typography**: Uses 'Outfit' font for a clean, tech-forward look.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Web App (Recommended)

```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

### 3. Run via CLI

```bash
# Using sample files
python main.py --resume sample_resume.txt --jd sample_job_description.txt

# Using inline text
python main.py --resume-text "Python dev 5yr exp..." --jd-text "Need Python dev..."
```

### 4. Run the REST API

```bash
python api.py
```

Then POST to `http://localhost:5000/api/screen`:

```bash
curl -X POST http://localhost:5000/api/screen \
  -H "Content-Type: application/json" \
  -d '{"resume": "Python developer...", "job_description": "Looking for Python dev..."}'
```

---

## 📊 Decision Rules

```
Match Score > 60%  AND  AI Score < 80%  →  ✅ SHORTLISTED
Otherwise                               →  ❌ NOT SHORTLISTED
```

---

## 🗂️ Project Structure

```
Ai-driven-resumescreening/
├── config.py               # Global constants & thresholds
├── logger.py               # Centralized logging
├── utils.py                # File I/O, text cleaning, validation
├── resume_screener.py      # TF-IDF + cosine similarity engine
├── ai_detector.py          # AI content detection (NLTK)
├── skill_extractor.py      # Skill extraction & comparison
├── decision_engine.py      # Shortlisting decision logic
├── main.py                 # CLI entry point
├── app.py                  # Streamlit web interface (New UI!)
├── api.py                  # Flask REST API
├── requirements.txt        # Dependencies
├── sample_resume.txt       # Sample resume for testing
└── sample_job_description.txt  # Sample JD for testing
```

---

## 🔌 API Reference

### `POST /api/screen`

**Request:**
```json
{
  "resume": "Candidate resume text...",
  "job_description": "Job requirements text..."
}
```

**Response:**
```json
{
  "success": true,
  "match_score": 72.45,
  "ai_score": 35.20,
  "decision": "SHORTLISTED",
  "reason": "Candidate meets all criteria",
  "skill_analysis": {
    "matched_skills": ["python", "docker", "aws"],
    "missing_skills": ["kubernetes"],
    "skill_match_pct": 75.0
  },
  "top_keywords": ["python", "machine learning", "api"],
  "thresholds": { "match_threshold": 60.0, "ai_threshold": 80.0 }
}
```

### `GET /health`

Returns system status.

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
MATCH_SCORE_THRESHOLD = 60.0   # Minimum match % to shortlist
AI_SCORE_THRESHOLD    = 80.0   # Maximum AI % allowed
TFIDF_NGRAM_RANGE     = (1, 2) # Unigrams + bigrams
MIN_WORD_COUNT        = 10     # Minimum input length
```

---

## 📦 Dependencies

- `scikit-learn` — TF-IDF vectorization & cosine similarity
- `nltk` — Sentence/word tokenization
- `streamlit` — Web interface
- `flask` — REST API
- `plotly` — Interactive charts
- `statistics` — Variance computation (Python stdlib)
