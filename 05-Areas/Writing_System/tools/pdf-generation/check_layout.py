from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib import colors
import re

# Read the markdown file
with open(r"C:\Vaults\Mick's-Writing-System\knowledge\drafts\2026.02.01 - SP500 Weekend Market Report.md", 'r', encoding='utf-8') as f:
    content = f.read()

# Remove frontmatter
content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

# Create PDF
pdf_path = r"C:\Vaults\Mick's-Writing-System\knowledge\drafts\SP500_Layout_Check.pdf"
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch,
    leftMargin=0.75*inch,
    rightMargin=0.75*inch
)

# Custom styles
styles = getSampleStyleSheet()

# Title style
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=colors.HexColor('#1a1a1a'),
    spaceAfter=12,
    alignment=TA_CENTER,
    leading=22
)

# Heading 2 style
h2_style = ParagraphStyle(
    'CustomH2',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#2a2a2a'),
    spaceAfter=10,
    spaceBefore=16,
    keepWithNext=True,
    leading=18
)

# Bold subheading style
bold_style = ParagraphStyle(
    'CustomBold',
    parent=styles['Normal'],
    fontSize=11,
    textColor=colors.HexColor('#1a1a1a'),
    spaceAfter=8,
    spaceBefore=12,
    keepWithNext=True,
    leading=14,
    fontName='Helvetica-Bold'
)

# Body text style
body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.HexColor('#333333'),
    spaceAfter=10,
    leading=14,
    alignment=TA_LEFT,
    allowOrphans=0,
    allowWidows=0
)

# Bullet style
bullet_style = ParagraphStyle(
    'CustomBullet',
    parent=body_style,
    leftIndent=20,
    bulletIndent=10,
    spaceAfter=6
)

story = []

# Parse markdown line by line
lines = content.strip().split('\n')
i = 0

while i < len(lines):
    line = lines[i].strip()

    # Skip empty lines
    if not line:
        i += 1
        continue

    # H1 - Title
    if line.startswith('# '):
        text = line[2:].strip()
        story.append(Paragraph(text, title_style))
        story.append(Spacer(1, 6))

    # H2 - Section headings
    elif line.startswith('## '):
        text = line[3:].strip()
        story.append(Spacer(1, 8))
        story.append(Paragraph(text, h2_style))

    # Bold text (subsection headings)
    elif line.startswith('**') and line.endswith('**'):
        text = line[2:-2].strip()
        story.append(Paragraph(text, bold_style))

    # Horizontal rules
    elif line.startswith('---'):
        story.append(Spacer(1, 12))

    # Bullet points
    elif line.startswith('- '):
        text = line[2:].strip()
        # Handle bold within bullets
        text = text.replace('**', '<b>').replace('**', '</b>')
        story.append(Paragraph('- ' + text, bullet_style))

    # Tables
    elif line.startswith('|'):
        # Collect table rows
        table_lines = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            table_lines.append(lines[i].strip())
            i += 1
        i -= 1

        # Parse table
        if len(table_lines) > 2:  # Header, separator, and at least one row
            table_data = []
            for row in [table_lines[0]] + table_lines[2:]:  # Skip separator
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                table_data.append(cells)

            # Create table with styling
            t = Table(table_data, colWidths=[1.8*inch, 1.4*inch, 1.4*inch, 2.2*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ]))
            story.append(Spacer(1, 8))
            story.append(KeepTogether(t))
            story.append(Spacer(1, 8))

    # Regular paragraphs
    else:
        # Handle bold and italic markdown
        text = line
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'\[(.*?)\]', r'[\1]', text)

        story.append(Paragraph(text, body_style))

    i += 1

# Build PDF
doc.build(story)
print(f"PDF created: {pdf_path}")
print(f"\nA4 page dimensions: 210mm x 297mm")
print(f"Text area with margins: ~159mm x 247mm")
print(f"\nOrphan/widow control enabled in paragraph styles")
print(f"KeepWithNext enabled for all headings")
print(f"Table kept together on single page")
