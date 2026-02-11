from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
import io
import re

def create_professional_pdf(text):
    """
    Create a professional, ATS-friendly PDF resume
    """
    buffer = io.BytesIO()
    
    # Create document with standard margins
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        topMargin=0.75*inch, 
        bottomMargin=0.75*inch,
        leftMargin=0.75*inch, 
        rightMargin=0.75*inch
    )
    
    # Get default styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor('#2d3748'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=HexColor('#667eea'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=HexColor('#667eea'),
        borderPadding=3,
        leftIndent=0
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=HexColor('#2d3748'),
        spaceAfter=3,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        textColor=HexColor('#2d3748')
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=HexColor('#666666')
    )
    
    # Build story (content)
    story = []
    
    # Parse the text into sections
    lines = text.split('\n')
    current_section = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        if not line:
            continue
        
        # Detect name (usually first non-empty line or ALL CAPS)
        if i < 3 and (line.isupper() or len(line.split()) <= 4):
            story.append(Paragraph(line, title_style))
            story.append(Spacer(1, 0.1*inch))
            continue
        
        # Detect contact info (email, phone)
        if '@' in line or re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', line):
            story.append(Paragraph(line, contact_style))
            story.append(Spacer(1, 0.15*inch))
            continue
        
        # Detect section headers (ALL CAPS or common section names)
        section_keywords = [
            'SUMMARY', 'OBJECTIVE', 'EXPERIENCE', 'EDUCATION', 'SKILLS', 
            'PROJECTS', 'CERTIFICATIONS', 'ACHIEVEMENTS', 'PUBLICATIONS',
            'PROFESSIONAL EXPERIENCE', 'WORK EXPERIENCE', 'TECHNICAL SKILLS',
            'ABOUT ME', 'PROFILE', 'QUALIFICATIONS'
        ]
        
        if line.isupper() or any(keyword in line.upper() for keyword in section_keywords):
            if len(line) < 50:  # Section headers are usually short
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph(line, heading_style))
                current_section = line
                continue
        
        # Detect job titles or subheadings (bold text indicators)
        if '|' in line or (len(line) < 100 and current_section):
            story.append(Paragraph(f"<b>{line}</b>", subheading_style))
            continue
        
        # Detect bullet points
        if line.startswith('•') or line.startswith('-') or line.startswith('*'):
            clean_line = line.lstrip('•-* ')
            story.append(Paragraph(f"• {clean_line}", body_style))
            continue
        
        # Regular paragraph
        story.append(Paragraph(line, body_style))
    
    # Build PDF
    try:
        doc.build(story)
    except Exception as e:
        # Fallback: simple formatting if parsing fails
        story = []
        for line in lines:
            if line.strip():
                story.append(Paragraph(line, body_style))
                story.append(Spacer(1, 0.05*inch))
        doc.build(story)
    
    buffer.seek(0)
    return buffer


def create_simple_pdf(text):
    """
    Create a simple, clean PDF (fallback option)
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Split into paragraphs
    paragraphs = text.split('\n')
    
    for para in paragraphs:
        if para.strip():
            story.append(Paragraph(para, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
    