// Week Plan Print - Base Document Generator
// Usage: Populate the WEEK_DATA array below with events from calendar fetch,
// then run: node generate_week_doc.js
// Output: week_plan_[DATE_RANGE].docx

const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, BorderStyle, WidthType, ShadingType } = require('docx');
const fs = require('fs');

// CONFIG
const OUTPUT_FILE = "/home/claude/week_plan_OUTPUT.docx";
const DATE_RANGE_LABEL = "1 - 8 March 2026"; // Update each week
const GENERATED_DATE = "Sunday 1 March 2026";  // Update each week

// COLOUR TOKENS
const DARK_BLUE    = "1F3864";
const MID_BLUE     = "2E5FA3";
const LIGHT_GREY   = "F2F2F2";
const WHITE        = "FFFFFF";
const TEXT_DARK    = "1A1A1A";
const NOTE_GREY    = "888888";
const FOOTER_GREY  = "AAAAAA";
const HEADER_DIM   = "CCDDEE";
const BORDER_COL   = "CCCCCC";

// WEEK DATA
// Populate this array from the calendar fetch. Each day is an object:
// { day: "SUNDAY", date: "1 March 2026", isToday: true, isHighlight: false, highlightNote: null,
//   events: [ { time: "11:00am", title: "Julia (Coffee) @ 92KW", note: null }, ... ] }
//
// isToday: true for today's date (renders mid-blue header)
// isHighlight: true for major event days like webinar (also mid-blue + note in header)
// highlightNote: short string appended to header e.g. "- WEBINAR DAY"

const WEEK_DATA = [
  // REPLACE THIS WITH LIVE CALENDAR DATA
  {
    day: "SUNDAY", date: "1 March 2026", isToday: true, isHighlight: false, highlightNote: null,
    events: [
      { time: "7:15am",  title: "Ditty Box Publishing payments check", note: null },
      { time: "11:00am", title: "Julia (Coffee) @ 92KW", note: null },
      { time: "5:30pm",  title: "To Bewdley", note: null },
      { time: "6:00pm",  title: "Csaba Dance Class", note: null },
    ]
  },
  // Add remaining days here...
];

// BORDER HELPERS
const cellBorder  = { style: BorderStyle.SINGLE, size: 1, color: BORDER_COL };
const cellBorders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };
const noBorder    = { style: BorderStyle.NONE, size: 0, color: WHITE };
const noBorders   = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

// ROW BUILDERS
function dayHeader(dayName, dateStr, isHighlight, highlightNote) {
  const headerText = isHighlight && highlightNote
    ? dayName + "  -  " + highlightNote
    : dayName;
  return new TableRow({
    children: [new TableCell({
      columnSpan: 2,
      borders: cellBorders,
      shading: { fill: isHighlight ? MID_BLUE : DARK_BLUE, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 160, right: 160 },
      children: [new Paragraph({ children: [
        new TextRun({ text: headerText, bold: true, color: WHITE, size: 22, font: "Arial" }),
        new TextRun({ text: "  " + dateStr, color: HEADER_DIM, size: 20, font: "Arial" }),
      ]})]
    })]
  });
}

function eventRow(time, title, note, shade) {
  return new TableRow({
    children: [
      new TableCell({
        borders: cellBorders,
        shading: { fill: shade ? LIGHT_GREY : WHITE, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 160, right: 100 },
        width: { size: 1800, type: WidthType.DXA },
        children: [new Paragraph({ children: [
          new TextRun({ text: time, color: MID_BLUE, size: 18, font: "Arial", bold: true })
        ]})]
      }),
      new TableCell({
        borders: cellBorders,
        shading: { fill: shade ? LIGHT_GREY : WHITE, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 100, right: 160 },
        width: { size: 7160, type: WidthType.DXA },
        children: [new Paragraph({ children: [
          new TextRun({ text: title, color: TEXT_DARK, size: 18, font: "Arial" }),
          ...(note ? [new TextRun({ text: "  " + note, color: NOTE_GREY, size: 16, font: "Arial", italics: true })] : [])
        ]})]
      })
    ]
  });
}

function noEventsRow() {
  return eventRow("", "No events scheduled", null, false);
}

function spacerRow() {
  return new TableRow({
    children: [new TableCell({
      columnSpan: 2, borders: noBorders,
      margins: { top: 30, bottom: 30, left: 0, right: 0 },
      children: [new Paragraph({ children: [new TextRun({ text: "" })] })]
    })]
  });
}

// BUILD TABLE ROWS
const tableRows = [];
WEEK_DATA.forEach((dayData, dayIndex) => {
  tableRows.push(dayHeader(dayData.day, dayData.date, dayData.isToday || dayData.isHighlight, dayData.highlightNote));
  if (dayData.events.length === 0) {
    tableRows.push(noEventsRow());
  } else {
    dayData.events.forEach((ev, i) => {
      tableRows.push(eventRow(ev.time, ev.title, ev.note, i % 2 !== 0));
    });
  }
  if (dayIndex < WEEK_DATA.length - 1) tableRows.push(spacerRow());
});

// BUILD DOCUMENT
const doc = new Document({
  styles: { default: { document: { run: { font: "Arial", size: 20 } } } },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 720, right: 720, bottom: 720, left: 720 }
      }
    },
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 120 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: DARK_BLUE, space: 4 } },
        children: [
          new TextRun({ text: "WEEKLY PLANNER", bold: true, size: 36, color: DARK_BLUE, font: "Arial" }),
          new TextRun({ text: "     |     ", color: "CCCCCC", size: 28 }),
          new TextRun({ text: DATE_RANGE_LABEL, size: 28, color: MID_BLUE, font: "Arial" }),
        ]
      }),
      new Paragraph({ children: [new TextRun({ text: "" })], spacing: { before: 0, after: 80 } }),
      new Table({
        width: { size: 8960, type: WidthType.DXA },
        columnWidths: [1800, 7160],
        rows: tableRows
      }),
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        spacing: { before: 120, after: 0 },
        children: [
          new TextRun({ text: "Generated by Cedric  |  DIY Investors PAIDA  |  ", color: FOOTER_GREY, size: 14, italics: true, font: "Arial" }),
          new TextRun({ text: GENERATED_DATE, color: FOOTER_GREY, size: 14, font: "Arial" }),
        ]
      })
    ]
  }]
});

// WRITE FILE
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUTPUT_FILE, buffer);
  console.log("Done: " + OUTPUT_FILE);
});
