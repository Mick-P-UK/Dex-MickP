#!/usr/bin/env python3
"""
Convert S&P 500 Weekend Market Report from Markdown to PDF
with professional formatting
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)
from reportlab.lib import colors
import re
from datetime import datetime

def parse_markdown(md_file):
    """Parse markdown file and extract content."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    return content

def markdown_to_flowables(content, styles):
    """Convert markdown content to ReportLab flowables."""
    flowables = []

    lines = content.split('\n')
    i = 0
    current_paragraph = []
    in_table = False
    table_data = []

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines unless we're building a paragraph
        if not line:
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                flowables.append(Paragraph(para_text, styles['Normal']))
                flowables.append(Spacer(1, 6))
                current_paragraph = []
            i += 1
            continue

        # Title (# S&P 500...)
        if line.startswith('# '):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                flowables.append(Paragraph(para_text, styles['Normal']))
                current_paragraph = []
            title_text = line[2:].strip()
            flowables.append(Paragraph(title_text, styles['Title']))
            flowables.append(Spacer(1, 12))
            i += 1
            continue

        # H2 headers (## )
        if line.startswith('## '):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                flowables.append(Paragraph(para_text, styles['Normal']))
                current_paragraph = []
            header_text = line[3:].strip()
            flowables.append(Spacer(1, 12))
            flowables.append(Paragraph(header_text, styles['Heading1']))
            flowables.append(Spacer(1, 6))
            i += 1
            continue

        # Bold headers within sections (**Text**)
        if line.startswith('**') and line.endswith('**') and len(line) < 100:
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                flowables.append(Paragraph(para_text, styles['Normal']))
                current_paragraph = []
            bold_text = line[2:-2].strip()
            flowables.append(Spacer(1, 8))
            flowables.append(Paragraph(f"<b>{bold_text}</b>", styles['Heading2']))
            flowables.append(Spacer(1, 4))
            i += 1
            continue

        # Horizontal rules
        if line.startswith('---'):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                flowables.append(Paragraph(para_text, styles['Normal']))
                current_paragraph = []
            flowables.append(Spacer(1, 12))
            i += 1
            continue

        # Tables
        if '|' in line and not in_table:
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                flowables.append(Paragraph(para_text, styles['Normal']))
                current_paragraph = []
            in_table = True
            table_data = []

        if in_table:
            if '|' in line:
                # Skip separator lines
                if re.match(r'^\|[\s\-:|]+\|$', line):
                    i += 1
                    continue
                # Parse table row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                table_data.append(cells)
                i += 1
                continue
            else:
                # End of table
                if table_data:
                    table = Table(table_data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 9),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        ('TOPPADDING', (0, 0), (-1, 0), 8),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ]))
                    flowables.append(table)
                    flowables.append(Spacer(1, 12))
                    table_data = []
                in_table = False
                continue

        # Bullet points
        if line.startswith('- '):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                flowables.append(Paragraph(para_text, styles['Normal']))
                current_paragraph = []
            bullet_text = line[2:].strip()
            # Convert markdown bold to reportlab
            bullet_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', bullet_text)
            flowables.append(Paragraph(f"- {bullet_text}", styles['Bullet']))
            i += 1
            continue

        # Regular text - accumulate into paragraph
        # Convert markdown formatting
        line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)  # Bold
        line = re.sub(r'\[(.+?)\]', r'[\1]', line)  # Stock tickers

        current_paragraph.append(line)
        i += 1

    # Don't forget last paragraph
    if current_paragraph:
        para_text = ' '.join(current_paragraph)
        flowables.append(Paragraph(para_text, styles['Normal']))

    return flowables

def create_pdf(md_file, output_file):
    """Create PDF from markdown file."""

    # Set up the document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )

    # Create custom styles
    styles = getSampleStyleSheet()

    # Modify existing Title style
    styles['Title'].fontSize = 20
    styles['Title'].textColor = colors.HexColor('#1a1a1a')
    styles['Title'].spaceAfter = 6
    styles['Title'].alignment = TA_CENTER
    styles['Title'].fontName = 'Helvetica-Bold'

    # Modify existing Heading1 for major sections
    styles['Heading1'].fontSize = 14
    styles['Heading1'].textColor = colors.HexColor('#2c3e50')
    styles['Heading1'].spaceAfter = 6
    styles['Heading1'].spaceBefore = 12
    styles['Heading1'].fontName = 'Helvetica-Bold'

    # Modify existing Heading2 for subsections
    styles['Heading2'].fontSize = 11
    styles['Heading2'].textColor = colors.HexColor('#34495e')
    styles['Heading2'].spaceAfter = 4
    styles['Heading2'].spaceBefore = 8
    styles['Heading2'].fontName = 'Helvetica-Bold'

    # Modify Normal text
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 14
    styles['Normal'].alignment = TA_JUSTIFY
    styles['Normal'].fontName = 'Helvetica'

    # Modify Bullet points style if it exists, otherwise add it
    if 'Bullet' in styles:
        styles['Bullet'].fontSize = 10
        styles['Bullet'].leading = 14
        styles['Bullet'].leftIndent = 20
        styles['Bullet'].fontName = 'Helvetica'
    else:
        styles.add(ParagraphStyle(
            name='Bullet',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            leftIndent=20,
            fontName='Helvetica'
        ))

    # Parse markdown and build flowables
    content = parse_markdown(md_file)
    flowables = markdown_to_flowables(content, styles)

    # Build PDF
    doc.build(flowables)
    print(f"PDF created successfully: {output_file}")

if __name__ == "__main__":
    md_file = "2026.02.01 - SP500 Weekend Market Report.md"
    output_file = "2026.02.01 - SP500 Weekend Market Report.pdf"

    create_pdf(md_file, output_file)
