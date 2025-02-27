import os
import re
import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, 
    Table, TableStyle, Frame, PageTemplate, NextPageTemplate
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from html.parser import HTMLParser
import jieba
import re

# Register the font
font_path = "/System/Library/Fonts/STHeiti Light.ttc"  # Path to Huawen Kaiti font on macOS
pdfmetrics.registerFont(TTFont("HuawenKaiti", font_path))

# Define styles
styles = getSampleStyleSheet()
custom_styles = {
    'CustomTitle': ParagraphStyle(
        name='CustomTitle',
        fontName='HuawenKaiti',
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=12
    ),
    'CustomNormal': ParagraphStyle(
        name='CustomNormal',
        fontName='HuawenKaiti',
        fontSize=12,
        leading=14,
        spaceAfter=6
    ),
    'CustomHeading1': ParagraphStyle(
        name='CustomHeading1',
        fontName='HuawenKaiti',
        fontSize=16,
        leading=18,
        spaceAfter=6
    ),
    'CustomHeading2': ParagraphStyle(
        name='CustomHeading2',
        fontName='HuawenKaiti',
        fontSize=14,
        leading=16,
        spaceAfter=6
    ),
    'CustomQuote': ParagraphStyle(
        name='CustomQuote',
        fontName='HuawenKaiti',
        fontSize=12,
        leading=14,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=6,
        italics=True
    ),
    'CustomFooter': ParagraphStyle(
        name='CustomFooter',
        fontName='HuawenKaiti',
        fontSize=10,
        alignment=TA_CENTER
    )
}

# Add custom styles to the stylesheet
for style_name, style in custom_styles.items():
    styles.add(style)

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
        canvas.setFont('HuawenKaiti', 10)
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.drawCentredString(self.width / 2, 0, text)
        canvas.restoreState()

# Function to translate Chinese text to English
def translate_chinese_to_english(text):
    # This is a simplified translation dictionary
    # In a real application, you would use a proper translation API or service
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
    
    # Simple word-by-word translation
    for cn, en in translations.items():
        text = text.replace(cn, en)
    
    return text

# Function to create a bilingual paragraph
def create_bilingual_paragraph(chinese_text, style):
    english_text = translate_chinese_to_english(chinese_text)
    return [
        Paragraph(chinese_text, style),
        Paragraph(english_text, style),
        Spacer(1, 0.2*inch)
    ]

# Function to parse markdown and convert to ReportLab flowables
def markdown_to_flowables(md_text):
    # Convert markdown to HTML
    html = markdown.markdown(md_text)
    
    # Split HTML by tags to process each element
    elements = re.findall(r'<[^>]+>.*?</[^>]+>|[^<]+', html)
    
    flowables = []
    
    for element in elements:
        # Skip empty elements
        if element.strip() == '':
            continue
            
        # Headers
        if element.startswith('<h1>'):
            text = element[4:-5]
            flowables.extend(create_bilingual_paragraph(text, styles['CustomHeading1']))
        elif element.startswith('<h2>'):
            text = element[4:-5]
            flowables.extend(create_bilingual_paragraph(text, styles['CustomHeading2']))
        elif element.startswith('<h3>'):
            text = element[4:-5]
            flowables.extend(create_bilingual_paragraph(text, styles['CustomHeading2']))
            
        # Paragraphs
        elif element.startswith('<p>'):
            text = element[3:-4]
            # Check if it's a quote
            if '<em>' in text and '</em>' in text:
                text = text.replace('<em>', '').replace('</em>', '')
                flowables.extend(create_bilingual_paragraph(text, styles['CustomQuote']))
            else:
                flowables.extend(create_bilingual_paragraph(text, styles['CustomNormal']))
                
        # Lists
        elif element.startswith('<ul>'):
            # Process list items
            list_items = re.findall(r'<li>(.*?)</li>', element)
            for item in list_items:
                bullet_text = f"• {item}"
                flowables.extend(create_bilingual_paragraph(bullet_text, styles['CustomNormal']))
                
        # Other elements (plain text)
        elif not element.startswith('<'):
            if element.strip():
                flowables.extend(create_bilingual_paragraph(element, styles['CustomNormal']))
    
    return flowables

# Function to add logo and title to each page
def add_page_header(canvas, doc):
    # Skip for the first page (cover page)
    if doc.page == 1:
        return
        
    canvas.saveState()
    
    # Add logo
    logo_path = "/Users/haoxue/LLMQuant_report/logo-short.png"
    canvas.drawImage(logo_path, 1*inch, doc.height - 1*inch, width=1.5*inch, height=0.5*inch)
    
    # Add title
    canvas.setFont('HuawenKaiti', 14)
    canvas.drawString(3*inch, doc.height - 0.75*inch, "LLMQuant Report")
    
    canvas.restoreState()

# Main function to generate the PDF
def generate_pdf(input_md_path, output_pdf_path):
    # Read markdown content
    with open(input_md_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=1*inch,
        rightMargin=1*inch,
        topMargin=1.5*inch,
        bottomMargin=1*inch
    )
    
    # Create story (content)
    story = []
    
    # Add cover page
    cover_logo_path = "/Users/haoxue/LLMQuant_report/logo-b.png"
    cover_logo = Image(cover_logo_path, width=4*inch, height=2*inch)
    cover_logo.hAlign = 'CENTER'
    
    story.append(cover_logo)
    story.append(Spacer(1, 1*inch))
    
    title_text = "LLMQuant Report"
    story.append(Paragraph(title_text, styles['CustomTitle']))
    story.append(Spacer(1, 0.5*inch))
    
    subtitle_text = "Bilingual Financial Report"
    story.append(Paragraph(subtitle_text, styles['CustomHeading2']))
    story.append(Spacer(1, 2*inch))
    
    date_text = "February 2024"
    story.append(Paragraph(date_text, styles['CustomNormal']))
    
    # Add page break after cover
    story.append(PageBreak())
    
    # Convert markdown to flowables and add to story
    flowables = markdown_to_flowables(md_content)
    story.extend(flowables)
    
    # Add page numbers to each page
    for i in range(len(story)):
        if isinstance(story[i], PageBreak) or i == len(story) - 1:
            story.insert(i, Spacer(1, 0.5*inch))
            story.insert(i+1, PageNumberFlowable())
            i += 2
    
    # Build PDF with custom page layout
    doc.build(story, onFirstPage=add_page_header, onLaterPages=add_page_header)

if __name__ == "__main__":
    input_md_path = "/Users/haoxue/LLMQuant_report/input.md"
    output_pdf_path = "/Users/haoxue/LLMQuant_report/LLMQuant_Report.pdf"
    
    generate_pdf(input_md_path, output_pdf_path)
    print(f"PDF report generated successfully: {output_pdf_path}") 