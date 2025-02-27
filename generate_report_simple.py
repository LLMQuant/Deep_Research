#!/usr/bin/env python3
"""
A simpler version of the PDF report generator that handles HTML tags better.
"""

import os
import re
import sys
import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, 
    Table, TableStyle, NextPageTemplate, PageTemplate, Frame
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import html
from bs4 import BeautifulSoup
from PIL import Image as PILImage
from reportlab.platypus.tableofcontents import TableOfContents

# Default font paths
PROJECT_FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "font", "STKaiti.ttf")
DEFAULT_FONT_PATH = PROJECT_FONT_PATH if os.path.exists(PROJECT_FONT_PATH) else "/System/Library/Fonts/STHeiti Light.ttc"
FONT_NAME = "HuawenKaiti"  # The name we'll use to refer to the font in the document

def register_font(font_path=None):
    """Register the font with ReportLab."""
    # Use provided font path or default
    path_to_use = font_path if font_path and os.path.exists(font_path) else DEFAULT_FONT_PATH
    
    if not os.path.exists(path_to_use):
        print(f"Warning: Font file not found at {path_to_use}. Using system default font.")
        return False
    
    try:
        pdfmetrics.registerFont(TTFont(FONT_NAME, path_to_use))
        print(f"Successfully registered font: {path_to_use}")
        return True
    except Exception as e:
        print(f"Error registering font: {e}")
        return False

# Define styles
def create_styles():
    """Create and return the styles for the document."""
    styles = getSampleStyleSheet()
    custom_styles = {
        'CustomTitle': ParagraphStyle(
            name='CustomTitle',
            fontName=FONT_NAME,
            fontSize=20,
            alignment=TA_CENTER,
            spaceAfter=12
        ),
        'CustomNormal': ParagraphStyle(
            name='CustomNormal',
            fontName=FONT_NAME,
            fontSize=11,
            leading=14,
            spaceAfter=6
        ),
        'CustomEnglish': ParagraphStyle(
            name='CustomEnglish',
            fontName=FONT_NAME,
            fontSize=11,
            leading=14,
            spaceAfter=6,
            textColor=colors.black
        ),
        'CustomHeading1': ParagraphStyle(
            name='CustomHeading1',
            fontName=FONT_NAME,
            fontSize=16,
            leading=18,
            spaceAfter=6,
            textColor=colors.darkblue,
            borderWidth=0,
            borderColor=colors.darkblue,
            borderPadding=5,
            borderRadius=2
        ),
        'CustomHeading1En': ParagraphStyle(
            name='CustomHeading1En',
            fontName=FONT_NAME,
            fontSize=16,
            leading=18,
            spaceAfter=10,
            textColor=colors.darkblue
        ),
        'CustomHeading2': ParagraphStyle(
            name='CustomHeading2',
            fontName=FONT_NAME,
            fontSize=14,
            leading=16,
            spaceAfter=6,
            textColor=colors.darkblue
        ),
        'CustomHeading2En': ParagraphStyle(
            name='CustomHeading2En',
            fontName=FONT_NAME,
            fontSize=14,
            leading=16,
            spaceAfter=10,
            textColor=colors.darkblue
        ),
        'CustomQuote': ParagraphStyle(
            name='CustomQuote',
            fontName=FONT_NAME,
            fontSize=11,
            leading=14,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=6,
            italics=True,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=5,
            borderRadius=2,
            backColor=colors.whitesmoke
        ),
        'CustomQuoteEn': ParagraphStyle(
            name='CustomQuoteEn',
            fontName=FONT_NAME,
            fontSize=11,
            leading=14,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10,
            italics=True,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=5,
            borderRadius=2,
            backColor=colors.whitesmoke
        ),
        'CustomFooter': ParagraphStyle(
            name='CustomFooter',
            fontName=FONT_NAME,
            fontSize=9,
            alignment=TA_CENTER
        ),
        'TOCHeading': ParagraphStyle(
            name='TOCHeading',
            fontName=FONT_NAME,
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=20
        ),
        'TOCEntry1': ParagraphStyle(
            name='TOCEntry1',
            fontName=FONT_NAME,
            fontSize=12,
            leading=16,
            spaceAfter=6
        ),
        'TOCEntry2': ParagraphStyle(
            name='TOCEntry2',
            fontName=FONT_NAME,
            fontSize=10,
            leading=14,
            leftIndent=20,
            spaceAfter=6
        ),
        'SectionTitle': ParagraphStyle(
            name='SectionTitle',
            fontName=FONT_NAME,
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.darkblue,
            borderWidth=0,
            borderPadding=10,
            borderRadius=5
        ),
        'FinancialHighlight': ParagraphStyle(
            name='FinancialHighlight',
            fontName=FONT_NAME,
            fontSize=11,
            leading=14,
            spaceAfter=6,
            textColor=colors.black,
            backColor=colors.lightgrey,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=5,
            borderRadius=2
        ),
        'FinancialHighlightEn': ParagraphStyle(
            name='FinancialHighlightEn',
            fontName=FONT_NAME,
            fontSize=11,
            leading=14,
            spaceAfter=6,
            textColor=colors.black,
            backColor=colors.lightgrey,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=5,
            borderRadius=2
        ),
        'ExecutiveSummary': ParagraphStyle(
            name='ExecutiveSummary',
            fontName=FONT_NAME,
            fontSize=11,
            leading=14,
            spaceAfter=6,
            textColor=colors.black,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=10,
            borderRadius=2
        ),
        'ExecutiveSummaryEn': ParagraphStyle(
            name='ExecutiveSummaryEn',
            fontName=FONT_NAME,
            fontSize=11,
            leading=14,
            spaceAfter=6,
            textColor=colors.black,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=10,
            borderRadius=2
        ),
        'Disclaimer': ParagraphStyle(
            name='Disclaimer',
            fontName=FONT_NAME,
            fontSize=8,
            leading=10,
            spaceAfter=6,
            textColor=colors.darkgrey,
            alignment=TA_CENTER
        )
    }

    # Add custom styles to the stylesheet
    for style_name, style in custom_styles.items():
        styles.add(style)
    
    return styles

# Custom flowable for page numbers
class PageNumberFlowable(Flowable):
    def __init__(self, page_size=A4):
        Flowable.__init__(self)
        self.page_size = page_size
        self.width = page_size[0]
        self.height = 20

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setFont(FONT_NAME, 9)
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.drawCentredString(self.width / 2, 0, text)
        canvas.restoreState()

# Simple translation dictionary
translations = {
    "苹果": "Apple",
    "财年": "Fiscal Year",
    "第一季度": "First Quarter",
    "财报会议": "Financial Report Meeting",
    "公司": "Company",
    "创纪录的收入": "Record Revenue",
    "美元": "USD",
    "同比增长": "Year-over-Year Growth",
    "美洲": "Americas",
    "欧洲": "Europe",
    "日本": "Japan",
    "亚太地区": "Asia Pacific",
    "历史新高": "All-Time High",
    "新兴市场": "Emerging Markets",
    "显著的收入增长": "Significant Revenue Growth",
    "尤其是": "Especially in",
    "拉丁美洲": "Latin America",
    "中东": "Middle East",
    "南亚": "South Asia",
    "蒂姆·库克": "Tim Cook",
    "产品表现": "Product Performance",
    "可穿戴设备": "Wearables",
    "家居": "Home",
    "配件": "Accessories",
    "服务业务": "Services Business",
    "继续吸引观众": "Continues to Attract Viewers",
    "获得了": "Received",
    "超过": "Over",
    "提名": "Nominations",
    "奖项": "Awards",
    "未来展望": "Future Outlook",
    "计划": "Plans",
    "在沙特阿拉伯开设旗舰店": "to Open a Flagship Store in Saudi Arabia",
    "继续在印度等新兴市场扩展业务": "Continue to Expand Business in Emerging Markets like India",
    "推出更多语言版本": "Launch More Language Versions of",
    "包括": "Including",
    "法语": "French",
    "德语": "German",
    "意大利语": "Italian",
    "我们将继续投资于创新和变革性工具": "We Will Continue to Invest in Innovative and Transformative Tools",
    "以帮助用户在日常生活中受益": "to Help Users Benefit in Their Daily Lives",
    "财务状况": "Financial Condition",
    "毛利率": "Gross Margin",
    "净收入": "Net Income",
    "向股东返还": "Returned to Shareholders",
}

def translate_text(text):
    """Simple word-by-word translation."""
    result = text
    for cn, en in translations.items():
        result = result.replace(cn, en)
    return result

def clean_html(text):
    """Clean HTML text to make it safe for ReportLab."""
    # Replace problematic characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text

def add_page_header(canvas, doc):
    """Add logo and title to each page."""
    # Skip for the first page (cover page) and TOC page
    if doc.page == 1 or doc.page == 2:
        return
        
    canvas.saveState()
    
    # Add logo - only specify width to maintain aspect ratio
    logo_path = "/Users/haoxue/LLMQuant_report/logo-short.png"
    
    # Get image dimensions using PIL
    try:
        with PILImage.open(logo_path) as img:
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height
    except Exception as e:
        print(f"Warning: Could not determine logo aspect ratio: {e}")
        aspect_ratio = 3  # Fallback aspect ratio (typical for logos)
    
    logo_width = 1.5*inch
    logo_height = logo_width / aspect_ratio
    
    # Position the logo at the top of the page
    # The y-coordinate is calculated as: page height - top margin - logo height
    canvas.drawImage(logo_path, 1*inch, doc.height + 0.5*inch, 
                    width=logo_width, height=logo_height, preserveAspectRatio=True)
    
    # Add title next to the logo
    canvas.setFont(FONT_NAME, 12)
    canvas.drawString(3*inch, doc.height + 0.25*inch, "LLMQuant Financial Report")
    
    # Add date on the right side of the header
    canvas.setFont(FONT_NAME, 9)
    canvas.drawRightString(doc.width + 1*inch - 0.5*inch, doc.height + 0.25*inch, "February 2024")
    
    # Add page number
    canvas.setFont(FONT_NAME, 9)
    page_num = canvas.getPageNumber()
    canvas.drawRightString(doc.width + 1*inch - 0.5*inch, 0.5*inch, f"Page {page_num}")
    
    # Add horizontal line below the header
    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(1*inch, doc.height - 0.2*inch, doc.width + 1*inch - 0.5*inch, doc.height - 0.2*inch)
    canvas.line(1*inch, 0.8*inch, doc.width + 1*inch - 0.5*inch, 0.8*inch)
    
    # Add footer with disclaimer
    canvas.setFont(FONT_NAME, 7)
    canvas.setFillColor(colors.darkgrey)
    canvas.drawCentredString(doc.width / 2 + 1*inch, 0.3*inch, "Confidential - For internal use only. LLMQuant © 2024")
    
    canvas.restoreState()

def add_toc_header(canvas, doc):
    """Add header for table of contents page."""
    canvas.saveState()
    
    # Add logo - only specify width to maintain aspect ratio
    logo_path = "/Users/haoxue/LLMQuant_report/logo-short.png"
    
    # Get image dimensions using PIL
    try:
        with PILImage.open(logo_path) as img:
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height
    except Exception as e:
        print(f"Warning: Could not determine logo aspect ratio: {e}")
        aspect_ratio = 3  # Fallback aspect ratio (typical for logos)
    
    logo_width = 1.5*inch
    logo_height = logo_width / aspect_ratio
    
    # Position the logo at the top of the page
    canvas.drawImage(logo_path, 1*inch, doc.height + 0.5*inch, 
                    width=logo_width, height=logo_height, preserveAspectRatio=True)
    
    # Add title next to the logo
    canvas.setFont(FONT_NAME, 12)
    canvas.drawString(3*inch, doc.height + 0.25*inch, "LLMQuant Financial Report")
    
    # Add date on the right side of the header
    canvas.setFont(FONT_NAME, 9)
    canvas.drawRightString(doc.width + 1*inch - 0.5*inch, doc.height + 0.25*inch, "February 2024")
    
    # Add page number
    canvas.setFont(FONT_NAME, 9)
    page_num = canvas.getPageNumber()
    canvas.drawRightString(doc.width + 1*inch - 0.5*inch, 0.5*inch, f"Page {page_num}")
    
    # Add horizontal line below the header
    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(1*inch, doc.height - 0.2*inch, doc.width + 1*inch - 0.5*inch, doc.height - 0.2*inch)
    canvas.line(1*inch, 0.8*inch, doc.width + 1*inch - 0.5*inch, 0.8*inch)
    
    # Add footer with disclaimer
    canvas.setFont(FONT_NAME, 7)
    canvas.setFillColor(colors.darkgrey)
    canvas.drawCentredString(doc.width / 2 + 1*inch, 0.3*inch, "Confidential - For internal use only. LLMQuant © 2024")
    
    canvas.restoreState()

def generate_pdf(input_md_path, output_pdf_path, font_path=None):
    """Generate a PDF report from markdown content."""
    # Register the font
    if not register_font(font_path):
        print("Warning: Using default font as fallback.")
    
    # Create styles
    styles = create_styles()
    
    # Read markdown content
    with open(input_md_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=1*inch,
        rightMargin=1*inch,
        topMargin=1*inch,  # Reduced top margin to accommodate the header
        bottomMargin=1*inch
    )
    
    # Create story (content)
    story = []
    
    # Add cover page with proper aspect ratio
    cover_logo_path = "/Users/haoxue/LLMQuant_report/logo-b.png"
    
    # Get image dimensions using PIL
    try:
        with PILImage.open(cover_logo_path) as img:
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height
    except Exception as e:
        print(f"Warning: Could not determine cover logo aspect ratio: {e}")
        aspect_ratio = 2  # Fallback aspect ratio
    
    cover_width = 4*inch
    cover_height = cover_width / aspect_ratio
    
    cover_logo = Image(cover_logo_path, width=cover_width, height=cover_height)
    cover_logo.hAlign = 'CENTER'
    
    story.append(cover_logo)
    story.append(Spacer(1, 1*inch))
    
    title_text = "LLMQuant Financial Report"
    story.append(Paragraph(title_text, styles['CustomTitle']))
    story.append(Spacer(1, 0.5*inch))
    
    subtitle_text = "Quarterly Financial Analysis"
    story.append(Paragraph(subtitle_text, styles['CustomHeading2']))
    story.append(Spacer(1, 0.5*inch))
    
    # Add fiscal period
    fiscal_text = "Fiscal Year 2025 - First Quarter"
    story.append(Paragraph(fiscal_text, styles['CustomHeading2']))
    story.append(Spacer(1, 1.5*inch))
    
    date_text = "February 2024"
    story.append(Paragraph(date_text, styles['CustomNormal']))
    
    # Add confidentiality notice
    story.append(Spacer(1, 1*inch))
    confidential_text = "CONFIDENTIAL - FOR INTERNAL USE ONLY"
    story.append(Paragraph(confidential_text, styles['Disclaimer']))
    
    # Add page break after cover
    story.append(PageBreak())
    
    # Add Table of Contents
    toc = TableOfContents()
    toc.levelStyles = [
        styles['TOCEntry1'],
        styles['TOCEntry2'],
    ]
    
    story.append(Paragraph("Table of Contents", styles['TOCHeading']))
    story.append(Spacer(1, 0.2*inch))
    story.append(toc)
    story.append(PageBreak())
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content)
    
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Create lists to store English and Chinese content separately
    english_content = []
    chinese_content = []
    
    # Add Executive Summary for English section
    english_content.append(Paragraph("Executive Summary", styles['CustomHeading1En']))
    english_content.append(Spacer(1, 0.2*inch))
    
    executive_summary_en = """
    Apple Inc. has delivered exceptional financial results for the first quarter of fiscal year 2025, 
    achieving record revenue of $124.3 billion USD, representing a 4% year-over-year growth. 
    The company has demonstrated strong performance across all geographic segments, with record-breaking 
    revenue in the Americas, Europe, Japan, and Asia Pacific regions. Emerging markets have shown 
    particularly impressive growth, especially in Latin America, the Middle East, and South Asia.
    """
    
    english_content.append(Paragraph(executive_summary_en.strip(), styles['ExecutiveSummaryEn']))
    english_content.append(Spacer(1, 0.3*inch))
    
    # Add Financial Highlights for English section
    english_content.append(Paragraph("Financial Highlights", styles['CustomHeading2En']))
    english_content.append(Spacer(1, 0.2*inch))
    
    financial_highlights_en = [
        "• Record quarterly revenue of $124.3 billion USD, up 4% year-over-year",
        "• iPhone revenue: $69.1 billion USD, reaching all-time highs in multiple markets",
        "• Mac revenue: $9.0 billion USD, up 16% year-over-year",
        "• iPad revenue: $8.1 billion USD, up 15% year-over-year",
        "• Services revenue: $26.3 billion USD, an all-time high with 14% year-over-year growth",
        "• Gross margin: 46.9%",
        "• Net income: $36.3 billion USD",
        "• Over $30 billion USD returned to shareholders"
    ]
    
    for highlight in financial_highlights_en:
        english_content.append(Paragraph(highlight, styles['FinancialHighlightEn']))
        english_content.append(Spacer(1, 0.1*inch))
    
    english_content.append(Spacer(1, 0.2*inch))
    
    # Add Executive Summary for Chinese section
    chinese_content.append(Paragraph("执行摘要", styles['CustomHeading1']))
    chinese_content.append(Spacer(1, 0.2*inch))
    
    executive_summary_cn = """
    苹果公司在2025财年第一季度取得了卓越的财务业绩，实现了1243亿美元的创纪录收入，同比增长4%。
    公司在所有地区都表现强劲，在美洲、欧洲、日本和亚太地区的收入均创下历史新高。
    新兴市场表现尤为突出，特别是在拉丁美洲、中东和南亚地区。
    """
    
    chinese_content.append(Paragraph(executive_summary_cn.strip(), styles['ExecutiveSummary']))
    chinese_content.append(Spacer(1, 0.3*inch))
    
    # Add Financial Highlights for Chinese section
    chinese_content.append(Paragraph("财务亮点", styles['CustomHeading2']))
    chinese_content.append(Spacer(1, 0.2*inch))
    
    financial_highlights_cn = [
        "• 季度收入创纪录，达1243亿美元，同比增长4%",
        "• iPhone收入：691亿美元，在多个市场创下历史新高",
        "• Mac收入：90亿美元，同比增长16%",
        "• iPad收入：81亿美元，同比增长15%",
        "• 服务业务收入：263亿美元，创历史新高，同比增长14%",
        "• 毛利率：46.9%",
        "• 净收入：363亿美元",
        "• 向股东返还超过300亿美元"
    ]
    
    for highlight in financial_highlights_cn:
        chinese_content.append(Paragraph(highlight, styles['FinancialHighlight']))
        chinese_content.append(Spacer(1, 0.1*inch))
    
    chinese_content.append(Spacer(1, 0.2*inch))
    
    # Process each element for English content
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul']):
        if element.name in ['h1', 'h2', 'h3']:
            # Headers
            text = clean_html(element.get_text())
            english_text = translate_text(text)
            
            # Determine header level and style
            if element.name == 'h1':
                style_name = 'CustomHeading1En'
                level = 0
            else:
                style_name = 'CustomHeading2En'
                level = 1
            
            # Add bookmark for TOC
            bookmark_name = f"section-en-{len(english_content)}"
            
            # Add English header with bookmark
            para = Paragraph(english_text, styles[style_name])
            english_content.append(para)
            
            # Add to TOC
            toc.addEntry(level, english_text, bookmark_name)
            
            # Add some space after headers
            english_content.append(Spacer(1, 0.2*inch))
            
        elif element.name == 'p':
            # Paragraphs
            text = clean_html(element.get_text())
            english_text = translate_text(text)
            
            # Determine if this is a quote
            if element.find('em'):
                style_name = 'CustomQuoteEn'
            else:
                style_name = 'CustomEnglish'
            
            # Add English paragraph
            english_content.append(Paragraph(english_text, styles[style_name]))
            english_content.append(Spacer(1, 0.2*inch))
            
        elif element.name == 'ul':
            # Lists
            for li in element.find_all('li'):
                text = clean_html(li.get_text())
                english_text = f"• {translate_text(text)}"
                
                # Add English list item
                english_content.append(Paragraph(english_text, styles['CustomEnglish']))
                english_content.append(Spacer(1, 0.1*inch))
            
            # Add extra space after the list
            english_content.append(Spacer(1, 0.1*inch))
    
    # Process each element for Chinese content
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul']):
        if element.name in ['h1', 'h2', 'h3']:
            # Headers
            text = clean_html(element.get_text())
            
            # Determine header level and style
            if element.name == 'h1':
                style_name = 'CustomHeading1'
                level = 0
            else:
                style_name = 'CustomHeading2'
                level = 1
            
            # Add bookmark for TOC
            bookmark_name = f"section-cn-{len(chinese_content)}"
            
            # Add Chinese header with bookmark
            para = Paragraph(text, styles[style_name])
            chinese_content.append(para)
            
            # Add some space after headers
            chinese_content.append(Spacer(1, 0.2*inch))
            
        elif element.name == 'p':
            # Paragraphs
            text = clean_html(element.get_text())
            
            # Determine if this is a quote
            if element.find('em'):
                style_name = 'CustomQuote'
            else:
                style_name = 'CustomNormal'
            
            # Add Chinese paragraph
            chinese_content.append(Paragraph(text, styles[style_name]))
            chinese_content.append(Spacer(1, 0.2*inch))
            
        elif element.name == 'ul':
            # Lists
            for li in element.find_all('li'):
                text = f"• {clean_html(li.get_text())}"
                
                # Add Chinese list item
                chinese_content.append(Paragraph(text, styles['CustomNormal']))
                chinese_content.append(Spacer(1, 0.1*inch))
            
            # Add extra space after the list
            chinese_content.append(Spacer(1, 0.1*inch))
    
    # Add English content section title
    story.append(Paragraph("English Version", styles['SectionTitle']))
    story.append(Spacer(1, 0.3*inch))
    
    # Add all English content
    story.extend(english_content)
    
    # Add page break before Chinese content
    story.append(PageBreak())
    
    # Add Chinese content section title
    story.append(Paragraph("中文版", styles['SectionTitle']))
    story.append(Spacer(1, 0.3*inch))
    
    # Add all Chinese content
    story.extend(chinese_content)
    
    # Build PDF with custom page layout
    doc.build(story, onFirstPage=add_page_header, onLaterPages=add_page_header)
    
    print(f"PDF report generated successfully: {output_pdf_path}")

if __name__ == "__main__":
    input_md_path = "/Users/haoxue/LLMQuant_report/input.md"
    output_pdf_path = "/Users/haoxue/LLMQuant_report/output/LLMQuant_Report.pdf"
    
    # Check if a custom font path is provided as a command-line argument
    font_path = None
    if len(sys.argv) > 1:
        font_path = sys.argv[1]
        if not os.path.exists(font_path):
            print(f"Warning: Font file not found at {font_path}. Will use default font.")
            font_path = None
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    
    generate_pdf(input_md_path, output_pdf_path, font_path) 