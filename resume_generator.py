import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

def generate_enhanced_resume(resume_text, jd_text):
    """
    Generate a HIGHLY ENHANCED and ATS-optimized resume targeting 75-95% ATS match score.
    Uses aggressive keyword integration and strategic content enhancement.
    """
    
    prompt = f"""
You are an elite ATS resume optimizer with 15+ years of experience. Your mission is to transform this resume to achieve a MINIMUM 75% ATS match score, targeting 85-95%.

=== JOB DESCRIPTION ===
{jd_text}

=== CURRENT RESUME ===
{resume_text}

=== CRITICAL OPTIMIZATION REQUIREMENTS ===

**PHASE 1: DEEP KEYWORD EXTRACTION**
Extract and categorize ALL keywords from the JD:
- Technical skills (programming languages, frameworks, tools, technologies)
- Soft skills (leadership, communication, problem-solving)
- Industry terms and domain knowledge
- Action verbs and power words
- Certifications and methodologies
- Quantifiable metrics and KPIs

**PHASE 2: STRATEGIC INTEGRATION (This is KEY for 75%+ score)**

1. **ENHANCED PROFESSIONAL SUMMARY** (Top priority for ATS)
   - Open with a powerful headline using JD keywords
   - Include 3-4 sentences packed with JD terminology
   - Mirror the exact job title or similar variants
   - Mention years of experience matching JD requirements
   - Include 5-8 critical keywords from JD naturally
   
2. **COMPREHENSIVE SKILLS SECTION** (Massive ATS impact)
   - Create multiple skill categories: Technical Skills, Core Competencies, Tools & Technologies
   - List ALL relevant keywords from JD in appropriate categories
   - Include variations: "JavaScript" "JS" "ES6" "React.js" "ReactJS"
   - Add related technologies that support JD requirements
   - Format: Use commas or bullets for easy ATS parsing
   - Target: 40-60 keyword mentions in this section alone

3. **EXPERIENCE SECTION TRANSFORMATION**
   For EACH job entry:
   - Rewrite bullets to mirror JD language and action verbs
   - Start with strong verbs from JD (led, developed, architected, implemented, optimized)
   - Inject JD keywords naturally: "Developed Python-based machine learning models using TensorFlow"
   - Add metrics: "Improved performance by 40%" "Managed team of 8" "Reduced costs by $200K"
   - Expand each bullet from one line to 2-3 lines with more detail and keywords
   - Add 2-3 NEW relevant bullets per job that align with JD requirements
   - Include tools/technologies from JD in context

4. **PROJECT/ACHIEVEMENTS SECTION** (If applicable)
   - Highlight projects using JD technologies
   - Use JD terminology to describe technical implementations
   - Add metrics and business impact

5. **EDUCATION & CERTIFICATIONS**
   - Emphasize relevant degrees/certifications matching JD
   - Add relevant coursework if it matches JD requirements
   - Include GPA if strong (>3.5)

**PHASE 3: KEYWORD DENSITY OPTIMIZATION**
- Target density: 2-3% for critical keywords (appear 5-10 times naturally)
- Primary keywords should appear in: Summary, Skills, Experience (multiple times)
- Use natural variations to avoid keyword stuffing detection
- Integrate acronyms AND full terms: "API (Application Programming Interface)"

**PHASE 4: ATS-FRIENDLY FORMATTING**
- Use standard headers: PROFESSIONAL SUMMARY, TECHNICAL SKILLS, PROFESSIONAL EXPERIENCE, EDUCATION
- Simple bullet points (•)
- No tables, columns, or text boxes
- No headers/footers
- Standard date formats (MM/YYYY)
- No special characters or graphics

**PHASE 5: CONTENT EXPANSION RULES**
✅ DO:
- Expand and reframe existing experience to highlight JD-relevant aspects
- Add adjacent/related skills that logically extend from existing ones
- Use stronger action verbs and more descriptive language
- Add quantifiable achievements (even estimated ranges like "15-20%")
- Emphasize transferable skills matching JD requirements

❌ DO NOT:
- Fabricate completely unrelated experience
- Add skills from totally different domains
- Invent fake companies or roles
- Add false certifications

**CRITICAL SUCCESS METRICS**
Your enhanced resume MUST:
✓ Be 40-60% longer than original (more detail = more keywords)
✓ Include 80-90% of important keywords from JD
✓ Have keyword-rich summary (30-50 words with 6-10 JD keywords)
✓ Have expanded skills section (40+ relevant items)
✓ Have enhanced experience bullets (2-3 lines each, packed with keywords)
✓ Use variations of the same skill (Python, Python 3.x, Python programming)
✓ Include metrics in at least 60% of experience bullets

=== OUTPUT REQUIREMENTS ===
- Start IMMEDIATELY with the candidate's name (no preamble or explanations)
- Use professional formatting with clear section headers
- Make it substantially different and enhanced from original
- Ensure it reads naturally while being keyword-optimized
- Length: Aim for 600-900 words (approximately 1.5-2 pages)

REMEMBER: The difference between 50% and 75%+ ATS score is AGGRESSIVE keyword integration while maintaining readability. Be bold in enhancement!

Generate the enhanced resume now:
"""
    
    # Updated model list for 2024-2025 Gemini API
    model_priority = [
        "models/gemini-2.5-flash",      # Latest and fastest
        "models/gemini-flash-latest",   # Auto-updates to latest
        "models/gemini-2.5-pro",        # More powerful
        "models/gemini-2.0-flash",              # Stable pro version,        # Experimental 2.0 (if available)
    ]
    
    last_error = None
    
    for model_name in model_priority:
        try:
            print(f"🔄 Trying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.85,  # Balance creativity and consistency
                    max_output_tokens=8000,
                    top_p=0.95,
                    top_k=40
                )
            )
            
            enhanced = response.text.strip()
            
            # Validation checks
            if len(enhanced) < 100:
                print(f"⚠️ {model_name}: Output too short ({len(enhanced)} chars)")
                continue
                
            # Check for actual enhancement (should be significantly longer)
            if len(enhanced) < len(resume_text) * 0.8:
                print(f"⚠️ {model_name}: Insufficient enhancement (only {len(enhanced)} vs {len(resume_text)} chars)")
                continue
            
            # Success!
            print(f"✅ SUCCESS using {model_name}")
            print(f"📊 Original: {len(resume_text)} chars → Enhanced: {len(enhanced)} chars ({len(enhanced)/len(resume_text)*100:.0f}% of original)")
            
            # Add quality marker
            enhancement_ratio = len(enhanced) / len(resume_text)
            if enhancement_ratio >= 1.4:
                quality = "🌟 EXCELLENT"
            elif enhancement_ratio >= 1.2:
                quality = "✅ GOOD"
            else:
                quality = "⚠️ MODERATE"
            
            print(f"🎯 Enhancement Quality: {quality}")
            
            return enhanced
            
        except Exception as e:
            error_msg = str(e)
            last_error = e
            print(f"❌ {model_name} failed: {error_msg[:200]}")
            
            # Specific error handling
            if "quota" in error_msg.lower():
                print("💡 TIP: API quota exceeded. Wait a few minutes or upgrade your API plan.")
            elif "not found" in error_msg.lower() or "404" in error_msg:
                print(f"💡 TIP: Model {model_name} not available. Trying next...")
                continue
            elif "api key" in error_msg.lower():
                print("💡 TIP: Check your GEMINI_API_KEY in .env file")
                break
            
            continue
    
    # All models failed - provide helpful error message
    error_msg = f"""
╔════════════════════════════════════════════════════════════╗
║          ⚠️  RESUME ENHANCEMENT UNAVAILABLE                ║
╚════════════════════════════════════════════════════════════╝

🔴 ERROR: {str(last_error)[:150]}

📋 YOUR ORIGINAL RESUME:

{resume_text}

═══════════════════════════════════════════════════════════════

🔧 TROUBLESHOOTING STEPS:

1. ✅ VERIFY API KEY
   - Check your .env file has: GEMINI_API_KEY=your_key_here
   - Get a free key at: https://aistudio.google.com/app/apikey
   - Ensure no extra spaces or quotes around the key

2. 🔄 CHECK API QUOTA
   - Visit: https://aistudio.google.com/app/apikey
   - Free tier: 15 requests/minute, 1,500 requests/day
   - If exceeded, wait 1-2 minutes or upgrade

3. 🌐 VERIFY INTERNET CONNECTION
   - Ensure you have stable internet access
   - Try: ping google.com

4. 🔍 TEST YOUR SETUP
   - Run: python test_api.py
   - This will show which models work with your API key

═══════════════════════════════════════════════════════════════

💡 MANUAL ENHANCEMENT TIPS (For 75%+ ATS Score):

1. ADD KEYWORDS TO SKILLS:
   - Create "Technical Skills" section
   - List ALL technologies from job description
   - Include variations (JS, JavaScript, ES6)

2. REWRITE EXPERIENCE BULLETS:
   - Start with action verbs from JD
   - Add metrics (increased X by 40%)
   - Mirror JD language and terminology

3. ENHANCE SUMMARY:
   - Use exact job title or similar
   - Pack with 6-10 keywords from JD
   - Mention relevant experience years

4. ADD QUANTIFIABLE ACHIEVEMENTS:
   - "Reduced costs by $200K"
   - "Improved performance 50%"
   - "Managed team of 8 developers"

═══════════════════════════════════════════════════════════════
"""
    return error_msg


def verify_enhancement(original_resume, enhanced_resume, jd_text):
    """
    Verify enhancement quality and provide detailed metrics.
    Returns comprehensive quality report.
    """
    from ats_analyser import extract_all_terms, create_normalized_set
    
    # Extract terms
    jd_terms = extract_all_terms(jd_text)
    original_terms = extract_all_terms(original_resume)
    enhanced_terms = extract_all_terms(enhanced_resume)
    
    # Normalize for comparison
    jd_normalized = create_normalized_set(jd_terms)
    original_normalized = create_normalized_set(original_terms)
    enhanced_normalized = create_normalized_set(enhanced_terms)
    
    # Calculate matches
    original_matches = original_normalized.intersection(jd_normalized)
    enhanced_matches = enhanced_normalized.intersection(jd_normalized)
    
    # Calculate percentages
    original_match_pct = (len(original_matches) / len(jd_normalized)) * 100 if jd_normalized else 0
    enhanced_match_pct = (len(enhanced_matches) / len(jd_normalized)) * 100 if jd_normalized else 0
    
    improvement = len(enhanced_matches) - len(original_matches)
    improvement_pct = enhanced_match_pct - original_match_pct
    
    # Determine quality
    if enhanced_match_pct >= 75:
        quality_status = "🌟 EXCELLENT - Target Achieved!"
    elif enhanced_match_pct >= 60:
        quality_status = "✅ GOOD - Close to target"
    elif enhanced_match_pct >= 45:
        quality_status = "⚠️ MODERATE - Needs more keywords"
    else:
        quality_status = "❌ POOR - Major enhancement needed"
    
    quality_report = f"""
╔════════════════════════════════════════════════════════════╗
║              📊 ENHANCEMENT QUALITY REPORT                 ║
╚════════════════════════════════════════════════════════════╝

📈 KEYWORD MATCH ANALYSIS:
   Original Resume: {len(original_matches)}/{len(jd_normalized)} keywords ({original_match_pct:.1f}%)
   Enhanced Resume: {len(enhanced_matches)}/{len(jd_normalized)} keywords ({enhanced_match_pct:.1f}%)
   
   Improvement: +{improvement} keywords (+{improvement_pct:.1f}%)

📊 CONTENT ANALYSIS:
   Original Length: {len(original_resume)} characters
   Enhanced Length: {len(enhanced_resume)} characters
   Expansion: {(len(enhanced_resume)/len(original_resume))*100:.0f}%

🎯 QUALITY STATUS: {quality_status}

{"✅ This resume should score well on ATS systems!" if enhanced_match_pct >= 75 else ""}
{"💡 TIP: Consider adding more specific keywords from the job description." if enhanced_match_pct < 75 else ""}

═══════════════════════════════════════════════════════════════
"""
    
    return quality_report


def extract_missing_critical_keywords(resume_text, jd_text, top_n=15):
    """
    Extract the most critical missing keywords that should be added.
    Helps users manually enhance their resume.
    """
    from ats_analyser import extract_all_terms, create_normalized_set
    from collections import Counter
    import re
    
    jd_terms = extract_all_terms(jd_text)
    resume_terms = extract_all_terms(resume_text)
    
    jd_normalized = create_normalized_set(jd_terms)
    resume_normalized = create_normalized_set(resume_terms)
    
    # Find missing terms
    missing = jd_normalized - resume_normalized
    
    # Count frequency in JD (more frequent = more important)
    jd_text_lower = jd_text.lower()
    term_importance = {}
    
    for term in missing:
        # Count occurrences in JD
        count = jd_text_lower.count(term.lower())
        # Longer terms are often more specific/important
        length_bonus = len(term) / 10
        term_importance[term] = count + length_bonus
    
    # Sort by importance
    sorted_terms = sorted(term_importance.items(), key=lambda x: x[1], reverse=True)
    
    # Get top N critical keywords
    critical_keywords = [term for term, score in sorted_terms[:top_n]]
    
    return critical_keywords
