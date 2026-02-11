import streamlit as st
import os
from dotenv import load_dotenv

# Import custom modules
from resume_parser import extract_text_from_pdf
from ats_analyser import ats_score, categorize_keywords, analyze_coverage
from resume_generator import generate_enhanced_resume, verify_enhancement, extract_missing_critical_keywords
from pdf_generator import create_professional_pdf
from rag_engine import build_vector_store, retrieve

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ResumeAI - Intelligent ATS Optimization",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Exceptional UI Design with distinctive aesthetics
st.markdown("""
<style>

/* ========== GLOBAL ========== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {
    visibility: hidden;
}

/* ========== BACKGROUND ========== */
.main {
    background: radial-gradient(circle at top, #1E293B 0%, #0F172A 60%, #020617 100%);
    color: #E5E7EB;
}

/* ========== CONTAINER ========== */
.block-container {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 2.5rem;
    margin: 2rem auto;
    max-width: 1300px;
    border: 1px solid rgba(148,163,184,0.15);
}

/* ========== HEADER ========== */
.main-header {
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    color: #E5E7EB;
    letter-spacing: -1px;
}

.subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* ========== SIDEBAR ========== */
section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #1F2937;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #E5E7EB !important;
}

section[data-testid="stSidebar"] p {
    color: #9CA3AF !important;
}

/* ========== CARDS ========== */
.modern-card {
    background: rgba(30,41,59,0.65);
    border-radius: 16px;
    padding: 1.8rem;
    margin: 1rem 0;
    border: 1px solid rgba(148,163,184,0.15);
}

/* ========== SCORE DISPLAY ========== */
.score-display {
    background: rgba(30,41,59,0.7);
    border-radius: 20px;
    padding: 2.5rem;
    margin: 2rem auto;
    text-align: center;
    border: 1px solid rgba(148,163,184,0.2);
}

.score-number {
    font-size: 3.5rem;
    font-weight: 800;
    color: #E5E7EB;
}

.score-label {
    color: #9CA3AF;
    font-weight: 600;
}

/* Score borders (subtle) */
.score-excellent { border-left: 5px solid #22C55E; }
.score-good { border-left: 5px solid #3B82F6; }
.score-average { border-left: 5px solid #F59E0B; }
.score-needs-work { border-left: 5px solid #EF4444; }

/* ========== BUTTONS ========== */
.stButton>button {
    background: #111827;
    color: #E5E7EB;
    border: 1px solid #374151;
    padding: 0.8rem 2rem;
    border-radius: 10px;
    font-weight: 600;
}

.stButton>button:hover {
    background: #1F2937;
    border: 1px solid #4B5563;
}

/* ========== METRICS ========== */
[data-testid="stMetric"] {
    background: rgba(30,41,59,0.7);
    padding: 1.5rem;
    border-radius: 14px;
    border: 1px solid rgba(148,163,184,0.15);
    text-align: center;
}

[data-testid="stMetricValue"] {
    color: #E5E7EB;
    font-size: 2.2rem;
}

[data-testid="stMetricLabel"] {
    color: #9CA3AF;
}

/* ========== INPUTS ========== */
.stTextArea textarea,
.stFileUploader {
    background: rgba(30,41,59,0.65) !important;
    color: #E5E7EB !important;
    border-radius: 12px;
    border: 1px solid rgba(148,163,184,0.2) !important;
}

/* ========== EXPANDERS ========== */
.streamlit-expanderHeader {
    background: rgba(30,41,59,0.7);
    color: #E5E7EB !important;
    border-radius: 10px;
    border: 1px solid rgba(148,163,184,0.2);
}

/* ========== KEYWORD PILLS ========== */
.keyword-pill {
    display: inline-block;
    background: #1F2937;
    color: #E5E7EB;
    padding: 0.4rem 1rem;
    margin: 0.3rem;
    border-radius: 20px;
    font-size: 0.85rem;
    border: 1px solid #374151;
}

/* ========== TABS ========== */
.stTabs [data-baseweb="tab-list"] {
    background: #020617;
    border-radius: 12px;
    padding: 0.4rem;
}

.stTabs [aria-selected="true"] {
    background: #1F2937 !important;
    color: #E5E7EB !important;
}

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #374151;
    border-radius: 6px;
}

</style>
""", unsafe_allow_html=True)
# Header
st.markdown('<h1 class="main-header">🎯 ResumeAI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligent ATS Optimization Platform • AI-Powered • Industry-Leading Accuracy</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🚀 Quick Start")
    st.markdown("""
    <div class='sidebar-card'>
    <p style='margin: 0.5rem 0;'><strong>1.</strong> Upload Resume PDF</p>
    <p style='margin: 0.5rem 0;'><strong>2.</strong> Paste Job Description</p>
    <p style='margin: 0.5rem 0;'><strong>3.</strong> Analyze Compatibility</p>
    <p style='margin: 0.5rem 0;'><strong>4.</strong> AI Enhancement</p>
    <p style='margin: 0.5rem 0;'><strong>5.</strong> Download Resume</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Score Guide")
    st.markdown("""
    <div class='sidebar-card'>
    <p style='margin: 0.5rem 0;'><span style='color: #00E676;'>●</span> <strong>75-100%</strong> Excellent</p>
    <p style='margin: 0.5rem 0;'><span style='color: #00C6FF;'>●</span> <strong>60-74%</strong> Good</p>
    <p style='margin: 0.5rem 0;'><span style='color: #FFC107;'>●</span> <strong>45-59%</strong> Average</p>
    <p style='margin: 0.5rem 0;'><span style='color: rgba(255,255,255,0.5);'>●</span> <strong>Below 45%</strong> Needs Work</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Pro Tips")
    st.markdown("""
    <div class='sidebar-card'>
    <p style='margin: 0.5rem 0;'>✓ Match exact keywords</p>
    <p style='margin: 0.5rem 0;'>✓ Include variations</p>
    <p style='margin: 0.5rem 0;'>✓ Add metrics & data</p>
    <p style='margin: 0.5rem 0;'>✓ Simple formatting</p>
    <p style='margin: 0.5rem 0;'>✓ No graphics/tables</p>
    </div>
    """, unsafe_allow_html=True)

# Main Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload & Analyze", "🔍 Analysis", "✨ Enhancement", "📚 Guide"])

with tab1:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📄 Resume Upload")
        resume_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"], key="resume")
        
        if resume_file:
            st.success(f"✅ {resume_file.name}")
            resume_text = extract_text_from_pdf(resume_file)
            st.session_state.resume_text = resume_text
            
            with st.expander("👁️ Preview Content"):
                st.text_area("", resume_text, height=200, disabled=True, label_visibility="collapsed")
    
    with col2:
        st.markdown("### 📋 Job Description")
        jd_text = st.text_area(
            "Paste complete job posting",
            height=300,
            placeholder="Paste the full job description including:\n• Role overview\n• Requirements\n• Responsibilities\n• Qualifications",
            label_visibility="collapsed"
        )
        
        if jd_text:
            st.session_state.jd_text = jd_text
            st.caption(f"📊 {len(jd_text.split())} words • {len(jd_text)} characters")
    
    st.markdown("---")
    
    if st.button("🎯 Analyze ATS Compatibility", type="primary", use_container_width=True):
        if 'resume_text' not in st.session_state or not st.session_state.resume_text:
            st.error("Please upload your resume first")
        elif not jd_text:
            st.error("Please paste the job description")
        else:
            with st.spinner("🔄 Analyzing compatibility..."):
                score, missing_keywords = ats_score(st.session_state.resume_text, jd_text)
                st.session_state.ats_score = score
                st.session_state.missing_keywords = missing_keywords
                
                # Score display
                if score >= 75:
                    score_class = "score-excellent"
                    emoji = "🌟"
                    message = "Excellent Match"
                elif score >= 60:
                    score_class = "score-good"
                    emoji = "✅"
                    message = "Good Match"
                elif score >= 45:
                    score_class = "score-average"
                    emoji = "⚠️"
                    message = "Average Match"
                else:
                    score_class = "score-needs-work"
                    emoji = "📊"
                    message = "Needs Enhancement"
                
                st.markdown(f"""
                <div class="score-display {score_class}">
                    <div class="score-circle">
                        <div class="score-number">{score}%</div>
                    </div>
                    <div class="score-label">{emoji} {message}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("ATS Score", f"{score}%", delta="Target: 75%+")
                with col2:
                    st.metric("Missing Keywords", len(missing_keywords))
                with col3:
                    status = "Ready!" if score >= 75 else "Needs Work"
                    st.metric("Status", status)
                
                # Missing keywords
                if missing_keywords:
                    st.markdown("---")
                    st.markdown("### 🔑 Missing Keywords")
                    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                    keywords_html = ""
                    for kw in missing_keywords[:25]:
                        keywords_html += f'<span class="keyword-pill">{kw}</span>'
                    st.markdown(keywords_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if score < 75:
                    st.markdown("""
                    <div class="info-banner">
                    <h3>💡 Next Step: AI Enhancement</h3>
                    <p>Our AI can automatically boost your score to 75%+ by intelligently integrating missing keywords, optimizing your summary, and enhancing experience descriptions.</p>
                    <p><strong>→ Go to Enhancement tab to get started!</strong></p>
                    </div>
                    """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔍 Detailed Analysis")
    
    if 'ats_score' in st.session_state:
        if 'resume_text' in st.session_state and 'jd_text' in st.session_state:
            coverage = analyze_coverage(st.session_state.resume_text, st.session_state.jd_text)
            
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                st.markdown('<div class="modern-card"><h3>📊 Statistics</h3></div>', unsafe_allow_html=True)
                st.metric("Total JD Keywords", coverage['total_jd_terms'])
                st.metric("Matched Keywords", coverage['covered_terms'])
                st.metric("Missing Keywords", coverage['missing_terms'])
            
            with col2:
                st.markdown('<div class="modern-card"><h3>📈 Coverage Rate</h3></div>', unsafe_allow_html=True)
                st.metric("Coverage", f"{coverage['coverage_percentage']:.1f}%")
                st.progress(coverage['coverage_percentage'] / 100)
            
            st.markdown("---")
            st.markdown("### 📋 Missing Keywords by Category")
            
            if 'missing_keywords' in st.session_state:
                categorized = categorize_keywords(st.session_state.missing_keywords[:30])
                
                for category, keywords in categorized.items():
                    if keywords:
                        with st.expander(f"**{category}** ({len(keywords)} items)"):
                            st.write(", ".join(keywords))
    else:
        st.info("👆 Complete the analysis in Upload & Analyze tab first")

with tab3:
    st.markdown("### ✨ AI Enhancement")
    
    if 'ats_score' not in st.session_state:
        st.info("⚠️ Please complete the ATS analysis first")
    else:
        current_score = st.session_state.ats_score
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Score", f"{current_score}%")
        with col2:
            target = max(75, current_score + 15)
            st.metric("Target Score", f"{target}%")
        with col3:
            st.metric("Expected Boost", f"+{target - current_score}%")
        
        st.markdown("---")
        
        enhancement_level = st.select_slider(
            "Enhancement Level",
            options=["Conservative", "Moderate", "Aggressive"],
            value="Aggressive",
            help="Aggressive mode provides maximum keyword integration"
        )
        
        st.markdown("---")
        
        if st.button("🚀 Generate Enhanced Resume", type="primary", use_container_width=True):
            if 'resume_text' not in st.session_state or 'jd_text' not in st.session_state:
                st.error("Missing required data")
            else:
                with st.spinner("🤖 AI is enhancing your resume... This may take 30-60 seconds"):
                    enhanced_resume = generate_enhanced_resume(
                        st.session_state.resume_text,
                        st.session_state.jd_text
                    )
                    
                    st.session_state.enhanced_resume = enhanced_resume
                    
                    if "ERROR" in enhanced_resume or "TROUBLESHOOTING" in enhanced_resume:
                        st.error("⚠️ Enhancement service temporarily unavailable")
                        with st.expander("Error Details"):
                            st.code(enhanced_resume)
                    else:
                        st.success("✅ Enhancement Complete!")
                        
                        quality_report = verify_enhancement(
                            st.session_state.resume_text,
                            enhanced_resume,
                            st.session_state.jd_text
                        )
                        
                        with st.expander("📊 Quality Report"):
                            st.code(quality_report)
                        
                        st.markdown("---")
                        st.markdown("### 📄 Enhanced Resume")
                        
                        enhanced_text = st.text_area(
                            "Review and customize",
                            enhanced_resume,
                            height=400
                        )
                        
                        st.markdown("---")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.download_button(
                                "📄 Download TXT",
                                data=enhanced_text if 'enhanced_text' in locals() else enhanced_resume,
                                file_name="resume_optimized.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        
                        with col2:
                            try:
                                pdf_buffer = create_professional_pdf(enhanced_text if 'enhanced_text' in locals() else enhanced_resume)
                                st.download_button(
                                    "📑 Download PDF",
                                    data=pdf_buffer,
                                    file_name="resume_optimized.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                            except Exception as e:
                                st.error(f"PDF generation error: {str(e)}")
        
        if 'resume_text' in st.session_state and 'jd_text' in st.session_state:
            st.markdown("---")
            st.markdown("### 🎯 Priority Keywords")
            
            critical_kw = extract_missing_critical_keywords(
                st.session_state.resume_text,
                st.session_state.jd_text,
                top_n=15
            )
            
            if critical_kw:
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                keywords_html = ""
                for i, kw in enumerate(critical_kw, 1):
                    keywords_html += f'<span class="keyword-pill">{i}. {kw}</span>'
                st.markdown(keywords_html, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("### 📚 Complete ATS Guide")
    
    with st.expander("🎯 Understanding ATS", expanded=True):
        st.markdown("""
        **Applicant Tracking Systems (ATS)** automatically scan, parse, and rank resumes.
        
        **Used by 98% of Fortune 500 companies** to:
        - Parse resume content
        - Extract keywords
        - Rank candidates
        - Filter applications
        
        **A 75%+ score means you'll pass most ATS filters successfully.**
        """)
    
    with st.expander("🔑 Keyword Optimization"):
        st.markdown("""
        **Success Strategies:**
        
        1. **Exact Matching**
           - Use JD phrases verbatim
           - Include full terms + acronyms
           - Add variations (JavaScript, JS, React.js)
        
        2. **Comprehensive Skills**
           - 40-60 keywords minimum
           - Categorize by type
           - Include all JD technologies
        
        3. **Enhanced Bullets**
           - Start with action verbs
           - 2-3 keywords each
           - Add metrics & numbers
        
        4. **Keyword-Rich Summary**
           - 6-10 JD keywords
           - Match job title
           - Include experience years
        """)
    
    with st.expander("📊 Score Interpretation"):
        st.markdown("""
        | Score | Status | Action |
        |-------|--------|--------|
        | 75-100% | Excellent | Apply now |
        | 60-74% | Good | Minor tweaks |
        | 45-59% | Average | Enhancement needed |
        | 0-44% | Poor | Complete rewrite |
        
        **Quick Wins:**
        - Add Skills section: +15-20%
        - Optimize summary: +10-15%
        - Enhance bullets: +10-15%
        - Add keywords: +20-30%
        """)
    
    with st.expander("✅ Formatting Best Practices"):
        st.markdown("""
        **Required:**
        - ✓ Standard section headers
        - ✓ Simple bullet points
        - ✓ Standard fonts
        - ✓ Single column
        - ✓ PDF or DOCX
        
        **Avoid:**
        - ✗ Tables/columns
        - ✗ Graphics/images
        - ✗ Headers/footers
        - ✗ Special characters
        - ✗ Keyword typos
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #F8FAFC 0%, #EDF2F7 100%); border-radius: 16px; margin-top: 3rem;">
    <p style="margin: 0; font-weight: 800; font-size: 1.2rem; background: linear-gradient(135deg, #0066FF, #00C6FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🎯 ResumeAI</p>
    <p style="margin: 0.5rem 0 0 0; color: #64748B; font-weight: 500;">Powered by Google Gemini AI • Built for Success</p>
</div>
""", unsafe_allow_html=True)
