# 📄 Real-Time Resume Analyzer & Job Tracker

An end-to-end full-stack application that intelligently analyzes your resume against job descriptions using NLP and offers visual insights, keyword matching, and a human-in-the-loop learning system to enhance and personalize future matches.

---

## 🔍 Why This Project?

This project bridges **Data Engineering** and **Software Engineering**:

- 💡 **Data Engineering Angle**: Resume/Job Description parsing, keyword extraction, structuring data into categories (skills, tools, concepts), and updating skill ontologies in real-time (`skills.json`).
- 🛠️ **Software Engineering Angle**: Full backend API using FastAPI, frontend with Streamlit, clean architecture, interactive UI, REST API integration, persistent session state, error handling.
- 🤖 **Cutting Edge**: Uses HuggingFace transformers (NER), FastAPI, Streamlit, real-time analysis, and human-in-the-loop updates.
- 💸 **Free to Build**: Fully local. No paid services required.

---

## 🏗️ Architecture

```text
                           ┌─────────────────────┐
                           │  Streamlit Frontend │
                           └────────┬────────────┘
                                    │ REST (JSON)
                                    ▼
                          ┌──────────────────────┐
                          │      FastAPI API     │
                          ├────────┬─────────────┤
        ┌────────────┐    │        ▼             │   ┌────────────┐
        │ pdfplumber │───►│  Extract Text (PDF)  │◄──│ Uploads     │
        └────────────┘    │        ▼             │   └────────────┘
                          │  HuggingFace NER     │
                          │        ▼             │
                          │ Compare Resume ↔ JD  │
                          │        ▼             │
                          │ Categorize Keywords  │
                          │        ▼             │
                          │  Return Insights     │
                          └────────┬─────────────┘
                                   │
                          ┌────────▼─────────────┐
                          │ Human-in-the-Loop UI │
                          └────────┬─────────────┘
                                   ▼
                          ┌──────────────────────┐
                          │ Update skills.json   │
                          └──────────────────────┘


## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/res_analyzer.git
cd res_analyzer

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

cd backend
uvicorn main:app --reload --port 8001

cd frontend
streamlit run app.py
