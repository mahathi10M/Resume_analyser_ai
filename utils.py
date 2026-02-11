# ---------------- IMPORTS ----------------
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    """
    Clean resume text by removing extra spaces
    and unwanted special characters.
    """
    if not text:
        return ""

    # Remove extra spaces and newlines
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted symbols but keep useful ones
    text = re.sub(r"[^A-Za-z0-9.,+/# ]", "", text)

    return text.strip()


# ---------------- TEXT CHUNKING ----------------
def chunk_text(text, chunk_size=300, overlap=50):
    """
    Split text into overlapping chunks for RAG retrieval.
    """
    if not text:
        return []

    words = text.split()
    chunks = []

    step = chunk_size - overlap
    if step <= 0:
        step = chunk_size  # safety fix

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# ---------------- KEYWORD EXTRACTION ----------------
def extract_keywords(text):
    """
    Basic keyword extraction using stopword removal.
    """
    if not text:
        return []

    words = text.lower().split()

    stopwords = {
        "and", "or", "the", "a", "an",
        "to", "for", "of", "in", "on",
        "with", "at", "by", "from",
        "is", "are", "was", "were"
    }

    keywords = [
        word for word in words
        if word not in stopwords and len(word) > 2
    ]

    return list(set(keywords))


# ---------------- SECTION DETECTION ----------------
def detect_sections(resume_text):
    """
    Detect important resume sections.
    Returns found and missing sections.
    """
    if not resume_text:
        return [], []

    sections = {
        "education": "Education",
        "experience": "Experience",
        "projects": "Projects",
        "skills": "Skills",
        "certifications": "Certifications",
        "achievements": "Achievements"
    }

    found = []
    missing = []

    text_lower = resume_text.lower()

    for key, value in sections.items():
        if key in text_lower:
            found.append(value)
        else:
            missing.append(value)

    return found, missing


# ---------------- PDF GENERATOR ----------------
def generate_pdf(text, output_path="enhanced_resume.pdf"):
    """
    Convert enhanced resume text into a downloadable PDF.
    """
    if not text:
        raise ValueError("No text provided for PDF generation.")

    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    content = []

    for line in text.split("\n"):
        para = Paragraph(line, styles["BodyText"])
        content.append(para)
        content.append(Spacer(1, 8))

    doc.build(content)

    return output_path


# ---------------- TEST RUN (OPTIONAL) ----------------
if __name__ == "__main__":
    sample_text = """
    Education: BTech in AI & ML
    Skills: Python, Machine Learning, NLP
    Projects: Resume Analyzer, Chatbot
    """

    cleaned = clean_text(sample_text)
    print("Cleaned Text:\n", cleaned)

    chunks = chunk_text(cleaned)
    print("\nChunks:\n", chunks)

    keywords = extract_keywords(cleaned)
    print("\nKeywords:\n", keywords)

    found, missing = detect_sections(cleaned)
    print("\nFound Sections:", found)
    print("Missing Sections:", missing)

    pdf_path = generate_pdf(sample_text)
    print("\nPDF Generated:", pdf_path)
