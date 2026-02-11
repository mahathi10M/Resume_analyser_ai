# 🚀 AI Resume Analyzer & ATS Enhancer

An intelligent Resume Analyzer built using **Python, Streamlit, and NLP** that evaluates resumes against job descriptions, calculates ATS scores, and generates enhanced professional resumes.

---

# 📌 Project Overview

The AI Resume Analyzer helps job seekers optimize their resumes by:

* Comparing resumes with Job Descriptions
* Calculating ATS Match Scores
* Identifying missing keywords
* Suggesting improvements
* Generating enhanced formatted resumes
* Providing downloadable resume versions

This tool simulates real Applicant Tracking System (ATS) screening used by companies.

---

# ✨ Features

✅ ATS Score Calculation
✅ Keyword Match Analysis
✅ Resume–JD Similarity Score
✅ Missing Skills Detection
✅ AI Enhanced Resume Generation
✅ PDF Resume Download
✅ TXT Resume Export
✅ Professional Formatting
✅ Dark Themed Dashboard UI

---

# 🛠️ Tech Stack

**Frontend / UI**

* Streamlit
* Custom CSS (Dark Theme)

**Backend / Processing**

* Python
* NLP Processing
* TF‑IDF Vectorization
* Cosine Similarity

**Libraries Used**

* streamlit
* scikit‑learn
* numpy
* pandas
* reportlab
* pypdf
* re (Regex)

---

# 📂 Project Structure

```
resume-analyzer/
│
├── app.py                  # Main Streamlit App
├── ats_analyser.py         # ATS Scoring Logic
├── resume_parser.py        # Resume Text Extraction
├── resume_generator.py     # AI Resume Enhancement
├── pdf_generator.py        # Professional PDF Creation
├── rag_engine.py           # Retrieval logic (if used)
├── requirements.txt        # Dependencies
└── README.md               # Project Documentation
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

## 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

## 4️⃣ Run Application

```bash
streamlit run app.py
```

App will open at:

```
http://localhost:8501
```

---

# 📊 How ATS Score Works

The ATS score is calculated using:

* **Keyword Match %** – Skills & tools overlap
* **Resume–JD Similarity** – TF‑IDF cosine similarity
* **Keyword Frequency** – Skill repetition weight

### Weighted Formula

```
Final Score =
(Keyword Match × 50%) +
(Similarity × 30%) +
(Frequency × 20%)
```

Score is normalized to simulate real ATS systems.

---

# 📄 Resume Enhancement

The system:

* Rewrites bullet points professionally
* Adds missing technical keywords
* Improves formatting
* Structures experience/projects

Download formats:

* PDF (Professional)
* TXT (Plain text)

---

# 🌐 Deployment

## Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Select repo
4. Deploy `app.py`

---

## Netlify / Vercel

Only frontend builds supported.
Python backends require Render/Railway.

---

# 🧪 Sample Use Cases

* Students optimizing resumes
* Internship applications
* Hackathon demos
* Placement preparation
* Career portals

---

# 🔮 Future Enhancements

* LLM Resume Feedback
* Interview Question Generator
* Portfolio Matching
* Recruiter Dashboard
* Multi‑Resume Comparison

---

# 👩‍💻 Author

**Mahathi Mahasivabhattu**
B.Tech AIML Student
Passionate about AI, GenAI & Healthcare Tech

GitHub: [https://github.com/mahathi10M](https://github.com/mahathi10M)
LinkedIn: [https://www.linkedin.com/in/mahathi-mahasivabhattu-bb7a8830a](https://www.linkedin.com/in/mahathi-mahasivabhattu-bb7a8830a)

---

# 📜 License

This project is for educational and research purposes.
Free to use with attribution.

---

⭐ If you like this project, consider giving it a star!
