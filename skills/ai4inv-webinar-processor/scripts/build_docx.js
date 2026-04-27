/**
 * ai4inv-webinar-processor: Word Document Builder
 * 
 * Usage: Set the PARAMS block below, then run:
 *   node build_docx.js
 *
 * The skill reads this file, fills in PARAMS from the current month's data,
 * writes it to /tmp/build_webinar_guide.js, and runs it.
 */

// ─── PARAMS (filled by skill at runtime) ────────────────────────────────────
const MONTH_NAME    = "{{MONTH_NAME}}";       // e.g. "February 2026"
const WEBINAR_DATE  = "{{WEBINAR_DATE}}";     // e.g. "25 February 2026"
const OUTPUT_PATH   = "{{OUTPUT_PATH}}";      // full Windows path for the .docx

// Section content - skill fills these from the NotebookLM query response
const SECTIONS = {{SECTIONS_JSON}};
// Expected structure:
// [
//   { heading: "1.  Introduction and Objectives", body: ["para1", "para2", ...], checkboxes: [], bullets: [] },
//   { heading: "2.  ...", body: [...], checkboxes: [...], bullets: [...] },
//   ...
// ]
// ────────────────────────────────────────────────────────────────────────────

const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
        BorderStyle, LevelFormat, PageNumber, Header, Footer } =
  require('/tmp/docx_work/node_modules/docx');
const fs = require('fs');

// ── Helpers ──────────────────────────────────────────────────────────────────
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text, bold: true, font: "Arial", size: 32, color: "1F4E79" })]
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text, bold: true, font: "Arial", size: 28, color: "2E75B6" })]
  });
}
function body(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun({ text, font: "Arial", size: 24, ...opts })]
  });
}
function checkbox(text) {
  return new Paragraph({
    spacing: { after: 80 },
    indent: { left: 360 },
    children: [new TextRun({ text: "□  " + text, font: "Arial", size: 24 })]
  });
}
function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text, font: "Arial", size: 24 })]
  });
}
function spacer() {
  return new Paragraph({ spacing: { after: 160 }, children: [new TextRun("")] });
}
function rule() {
  return new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } },
    spacing: { after: 160 },
    children: [new TextRun("")]
  });
}

// ── Build section children from structured data ───────────────────────────────
function buildSection(section) {
  const children = [];
  children.push(h1(section.heading));
  if (section.intro) children.push(body(section.intro));
  for (const para of (section.body || [])) {
    if (para.startsWith("##")) {
      children.push(h2(para.replace(/^##\s*/, "")));
    } else {
      children.push(body(para));
    }
  }
  if ((section.bullets || []).length > 0) {
    children.push(spacer());
    for (const b of section.bullets) children.push(bullet(b));
  }
  if ((section.checkboxes || []).length > 0) {
    children.push(spacer());
    for (const c of section.checkboxes) children.push(checkbox(c));
  }
  children.push(rule());
  return children;
}

// ── Document ─────────────────────────────────────────────────────────────────
const allChildren = [
  // Title block
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [
    new TextRun({ text: "AI for Investors", font: "Arial", size: 52, bold: true, color: "1F4E79" })
  ]}),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [
    new TextRun({ text: MONTH_NAME + " Webinar  |  User Guide", font: "Arial", size: 32, color: "2E75B6" })
  ]}),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [
    new TextRun({ text: WEBINAR_DATE + "  |  DIY-Investors.ai Membership", font: "Arial", size: 22, color: "999999" })
  ]}),
  rule(),
];

// Add all sections
for (const section of SECTIONS) {
  for (const child of buildSection(section)) allChildren.push(child);
}

// Footer note
allChildren.push(
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [
    new TextRun({ text: "DIY-Investors.ai  |  AI for Investors Webinar Series", font: "Arial", size: 18, color: "999999" })
  ]}),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [
    new TextRun({ text: "User guide generated from webinar audio via Google NotebookLM", font: "Arial", size: 18, color: "BBBBBB" })
  ]})
);

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "•",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
    }]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: "1F4E79" },
        paragraph: { spacing: { before: 320, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "2E75B6" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    properties: {
      page: { size: { width: 11906, height: 16838 },
              margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } },
        children: [new TextRun({
          text: "DIY-Investors.ai  |  AI for Investors Webinar Series  |  " + MONTH_NAME,
          font: "Arial", size: 18, color: "666666"
        })]
      })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        border: { top: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } },
        alignment: AlignmentType.RIGHT,
        children: [
          new TextRun({ text: "Page ", font: "Arial", size: 18, color: "666666" }),
          new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: "666666" }),
          new TextRun({ text: " of ", font: "Arial", size: 18, color: "666666" }),
          new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Arial", size: 18, color: "666666" }),
        ]
      })] })
    },
    children: allChildren
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUTPUT_PATH, buffer);
  console.log("SUCCESS: " + OUTPUT_PATH + " (" + Math.round(buffer.length/1024) + "KB)");
}).catch(e => { console.error("ERROR: " + e.message); process.exit(1); });
