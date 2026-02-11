import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
def clean_text(text):
    """Normalize text"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s+#.\-/]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ---------------- TERM EXTRACTION ---------------- #

def extract_all_terms(text, min_length=2):
    """
    Extract meaningful terms:
    - Words
    - Bigrams
    - Trigrams
    """
    text = clean_text(text)

    stop_words = {
        'the','a','an','and','or','but','in','on','at','to','for','of',
        'with','by','from','as','is','was','are','be','been','have',
        'has','had','do','does','did','will','would','should','can',
        'this','that','these','those','it','its','their','our','your'
    }

    words = text.split()
    all_terms = set()

    # -------- Unigrams -------- #
    for w in words:
        if w not in stop_words and len(w) > min_length:
            all_terms.add(w)

    # -------- Bigrams -------- #
    for i in range(len(words)-1):
        phrase = f"{words[i]} {words[i+1]}"
        if len(phrase) > 5:
            all_terms.add(phrase)

    # -------- Trigrams -------- #
    for i in range(len(words)-2):
        phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
        if len(phrase) > 10:
            all_terms.add(phrase)

    # Limit explosion (IMPORTANT FIX)
    return set(list(all_terms)[:300])


# ---------------- TECH PATTERNS ---------------- #

def extract_technical_patterns(text):
    patterns = [
        r'\b[A-Z]{2,}\+?\+?\b',      # AWS, API, C++
        r'\b\w+\d+\b',               # Python3
        r'\b[A-Z][a-z]+(?:\.[a-z]+)+\b',  # Node.js
    ]

    tech_terms = set()
    for p in patterns:
        matches = re.findall(p, text)
        tech_terms.update([m.lower() for m in matches])

    return tech_terms


# ---------------- NORMALIZATION ---------------- #

def normalize_term(term):
    term = term.lower().strip()

    mapping = {
        'python': ['python', 'python3', 'py'],
        'machine learning': ['ml','machine learning'],
        'artificial intelligence': ['ai'],
        'deep learning': ['dl'],
        'natural language processing': ['nlp'],
        'react': ['react','reactjs','react.js'],
        'node': ['node','nodejs','node.js'],
        'aws': ['aws','amazon web services'],
    }

    for canon, variants in mapping.items():
        if term in variants:
            return canon

    return term


def create_normalized_set(terms):
    normalized = set()
    for t in terms:
        normalized.add(t.lower())
        normalized.add(normalize_term(t))
    return normalized


# ---------------- FUZZY MATCH ---------------- #

def fuzzy_match(term, text):
    """Loose phrase match"""
    return term.lower() in text.lower()


# ---------------- MATCH % ---------------- #

def calculate_match_percentage(resume_terms, jd_terms, resume_text):
    if not jd_terms:
        return 100.0

    matches = 0

    for term in jd_terms:
        norm = normalize_term(term)

        if (
            norm in resume_terms
            or term.lower() in resume_terms
            or fuzzy_match(norm, resume_text)
        ):
            matches += 1

    return (matches / len(jd_terms)) * 100


# ---------------- ATS SCORE ---------------- #

def ats_score(resume_text, jd_text):

    # ---- Extract terms ---- #
    jd_terms = extract_all_terms(jd_text)
    resume_terms = extract_all_terms(resume_text)

    jd_tech = extract_technical_patterns(jd_text)
    resume_tech = extract_technical_patterns(resume_text)

    jd_combined = jd_terms.union(jd_tech)
    resume_combined = resume_terms.union(resume_tech)

    # ---- Keyword Match (50%) ---- #
    keyword_match_pct = calculate_match_percentage(
        resume_combined,
        jd_combined,
        resume_text
    )

    # ---- TF-IDF Similarity (30%) ---- #
    try:
        vectorizer = TfidfVectorizer(
            ngram_range=(1,2),
            max_features=1500
        )

        vecs = vectorizer.fit_transform([
            clean_text(resume_text),
            clean_text(jd_text)
        ])

        similarity = cosine_similarity(vecs[0:1], vecs[1:2])[0][0]
        similarity_score = similarity * 100

    except:
        similarity_score = keyword_match_pct

    # ---- Frequency Match (20%) ---- #
    jd_freq = Counter(clean_text(jd_text).split())
    important = {
        w for w,c in jd_freq.items()
        if c >= 2 and len(w) > 3
    }

    resume_words = set(clean_text(resume_text).split())

    if important:
        freq_score = (
            len(important.intersection(resume_words))
            / len(important)
        ) * 100
    else:
        freq_score = keyword_match_pct

    # ---- FINAL WEIGHTED SCORE ---- #
    final_score = (
        (keyword_match_pct * 0.50) +
        (similarity_score * 0.30) +
        (freq_score * 0.20)
    )

    # ---- ATS NORMALIZATION BOOST ---- #
    if final_score < 40:
        final_score += 45
    elif final_score < 60:
        final_score += 45

    final_score = int(min(100, final_score))

    # ---------------- MISSING TERMS ---------------- #

    resume_norm = create_normalized_set(resume_combined)
    jd_norm = create_normalized_set(jd_combined)

    missing_norm = jd_norm - resume_norm

    missing_terms = []

    for term in jd_combined:
        if normalize_term(term) in missing_norm:
            missing_terms.append(term)

    missing_terms = sorted(
        missing_terms,
        key=len,
        reverse=True
    )[:40]

    return final_score, missing_terms


# ---------------- CATEGORIZATION ---------------- #

def categorize_keywords(keywords):

    categories = {
        "Technical Skills": [],
        "Soft Skills": [],
        "Tools & Platforms": [],
        "Other": []
    }

    tech_indicators = [
        'python','java','ai','ml','cloud','database',
        'react','node','api','tensorflow'
    ]

    soft_indicators = [
        'communication','leadership',
        'teamwork','management'
    ]

    tool_indicators = [
        'github','docker','aws',
        'jira','jenkins','git'
    ]

    for kw in keywords:
        k = kw.lower()

        if any(t in k for t in tech_indicators):
            categories["Technical Skills"].append(kw)

        elif any(s in k for s in soft_indicators):
            categories["Soft Skills"].append(kw)

        elif any(t in k for t in tool_indicators):
            categories["Tools & Platforms"].append(kw)

        else:
            categories["Other"].append(kw)

    return categories


# ---------------- COVERAGE ---------------- #

def analyze_coverage(resume_text, jd_text):

    jd_terms = extract_all_terms(jd_text)
    resume_terms = extract_all_terms(resume_text)

    jd_norm = create_normalized_set(jd_terms)
    resume_norm = create_normalized_set(resume_terms)

    covered = jd_norm.intersection(resume_norm)
    missing = jd_norm - resume_norm

    total = len(jd_norm)
    covered_n = len(covered)

    coverage_pct = (
        covered_n / total * 100
        if total > 0 else 0
    )

    return {
        "total_jd_terms": total,
        "covered_terms": covered_n,
        "missing_terms": len(missing),
        "coverage_percentage": coverage_pct,
        "covered_list": list(covered)[:20],
        "missing_list": list(missing)[:40],
    }
