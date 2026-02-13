# Resume Analyzer AI 🎯

An intelligent AI-powered resume optimization tool that analyzes, scores, and enhances resumes to match specific job descriptions using advanced NLP and generative AI.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7)](https://resume-analyser-ai-162n.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37.0-FF4B4B)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%20AI-4285F4)](https://ai.google.dev/)

## 🚀 Live Application

**Access the app here:** [https://resume-analyser-ai-162n.onrender.com](https://resume-analyser-ai-162n.onrender.com)

## 📋 Overview

Resume Analyzer AI helps job seekers optimize their resumes by:
- **Analyzing** resume compatibility with job descriptions
- **Identifying** missing keywords and skills
- **Generating** enhanced, ATS-optimized resumes

## ✨ Features

### 1. **Smart Resume Analysis**
- Upload your resume (PDF format)
- Paste target job description
- Get instant compatibility scoring
- Detailed breakdown of matching skills and experience

### 2. **Gap Identification**
- Identifies missing critical keywords
- Highlights skill gaps
- Provides actionable recommendations

### 3. **AI-Powered Resume Enhancement**
- Automatically rewrites resume content
- Optimizes for ATS (Applicant Tracking Systems)
- Maintains authentic experience while improving keyword density
- Download enhanced resume as PDF

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **AI/ML:** 
  - Google Gemini AI (Generative AI)
  - Sentence Transformers (Semantic understanding)
  - FAISS (Vector similarity search)
  - scikit-learn (Machine learning)
- **PDF Processing:** PyPDF, ReportLab
- **Backend:** Python 3.10

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Google Gemini API Key

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/mahathi10M/Resume_analyser_ai.git
cd Resume_analyser_ai
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your API key from: [Google AI Studio](https://aistudio.google.com/app/apikey)

5. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📝 Usage

1. **Upload Resume**: Click "Upload your resume" and select your PDF file
2. **Enter Job Description**: Paste the target job description in the text area
3. **Analyze**: Click "Analyze Resume" to see compatibility score and gaps
4. **Enhance**: Click "Generate Enhanced Resume" to create optimized version
5. **Download**: Save your enhanced resume as PDF

## 🏗️ Architecture
```
Resume Analyzer AI
│
├── RAG Engine (rag_engine.py)
│   ├── Vector Store (FAISS)
│   ├── Sentence Transformers
│   └── Semantic Retrieval
│
├── Resume Generator (resume_generator.py)
│   ├── Google Gemini AI
│   ├── Keyword Enhancement
│   └── PDF Generation (ReportLab)
│
└── Streamlit Interface (app.py)
    ├── File Upload
    ├── Analysis Dashboard
    └── Download Handler
```

## 🌐 Deployment

Deployed on [Render](https://render.com)

### Deploy Your Own

1. Fork this repository
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Add environment variable: `GEMINI_API_KEY`
5. Deploy!

**Build Command:** `pip install -r requirements.txt`  
**Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## 📄 Requirements
```txt
streamlit==1.37.0
pypdf==4.2.0
faiss-cpu==1.13.2
sentence-transformers==3.0.1
google-generativeai==0.7.2
reportlab==4.2.2
numpy==1.26.4
scikit-learn==1.5.1
tqdm==4.66.4
python-dotenv==1.0.0
torch==2.4.0
transformers==4.44.0
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

**Mahathi** - [@mahathi10M](https://github.com/mahathi10M)

Project Link: [https://github.com/mahathi10M/Resume_analyser_ai](https://github.com/mahathi10M/Resume_analyser_ai)

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Google Gemini AI for generative capabilities
- Streamlit for the amazing framework
- FAISS for efficient similarity search
- Hugging Face for Sentence Transformers

---

⭐ **Star this repo if you found it helpful!**

**Live Demo:** [https://resume-analyser-ai-162n.onrender.com](https://resume-analyser-ai-162n.onrender.com)
