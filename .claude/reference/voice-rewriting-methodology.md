# Voice Rewriting Methodology - Mick's Voice DNA Application

**Created:** 2026-02-16
**Purpose:** Document the methodology for rewriting technical/academic documents into Mick's authentic voice
**Use Case:** Creating a skill for automated voice-based document rewriting

---

## Overview

This methodology rewrites formal, academic, or generic documents into Mick Pavey's authentic voice whilst preserving all technical accuracy, data points, and citations. It transforms educational/analytical content into peer-to-peer guidance that sounds like Mick explaining concepts to his DIY-Investors community.

---

## Required Context Profiles

The rewriting process requires three core context files from the Writing System:

### 1. Voice DNA (`05-Areas/Writing_System/context/core/voice-dna-mick.json`)
Contains:
- Core essence and worldview
- Emotional palette and range
- Communication style and thought progression
- Linguistic fingerprint (sentence architecture, vocabulary, rhetoric)
- Authenticity markers and quirks
- Voice boundaries (what Mick never/always sounds like)
- Illustrative moments showing quintessential voice

### 2. ICP Profile (`05-Areas/Writing_System/context/core/icp.json`)
Contains:
- Target audience (DIY investors)
- Pain points and aspirations
- Language patterns they use
- Objections and fears they have

### 3. Business Profile (`05-Areas/Writing_System/context/core/business-profile.json`)
Contains:
- DIY-Investors mission and offerings
- Brand positioning and philosophy
- Core principles (DYOR, Three Pillars, Portico Investing)
- What the brand stands for/against

---

## Voice Transformation Principles

### Core Voice DNA Elements to Apply

**1. Opening and Engagement:**
- Start with direct address: "Right, let's talk about..."
- Use conversational hooks: "Now, I'll be honest with you..."
- Position as peer, not expert: "Here's what I've found..."

**2. British English Throughout:**
- whilst (not while)
- favour (not favor)
- contextualised (not contextualized)
- colour, realise, centre
- "keen to hear" (not eager)
- "quite rightly"

**3. Sentence Architecture:**
- Mix lengths: medium declarative for facts, longer compound for analysis, short punchy for emphasis
- Parenthetical asides: "(though waived by HSBC)", "(at the time of writing)"
- Rhetorical questions: "Perhaps a time to be doing some profit taking?"
- Colon to introduce elaboration

**4. Signature Transitions:**
- "Meanwhile," - shift topics laterally
- "As ever," - return to familiar themes
- "Note that" - add important detail
- "In terms of" - categorize or specify
- "Coming to" - address specific points
- "Notwithstanding" - contrasts and complications
- "Coupled with that" - add layers
- "With that being said" - pivot after context

**5. Conviction Spectrum:**
- Confident: "as far as I'm concerned", "in my opinion", "quite rightly", "plain daft"
- Hedging: "at the time of writing", "seems to", "appears to", "perhaps", "might be"
- Temporal precision to avoid false certainty

**6. Thought Progression:**
- Data first, interpretation second
- Present facts before analysis
- Acknowledge complexity before simplification
- Multiple perspectives before stating position
- Specific examples before broader implications

**7. Closing Signatures:**
- End with DYOR philosophy: "As ever, do your own research."
- Sign-off: "With my best wishes, Mick Pavey" or "Best regards, Mick Pavey"

---

## Technical Preservation Requirements

### Must Preserve Exactly:

✅ **All numerical data:**
- Percentages to decimal points (70.30%, not "about 70%")
- Specific dates (31st December 2025, not "end of year")
- Financial figures (£10,867, not "around £11,000")
- Production volumes (226,000 PGM ounces)

✅ **All citations and references:**
- Keep numbered citations [1, 2, 3]
- Preserve complete reference list at end
- Maintain academic rigour through proper sourcing

✅ **Technical terminology:**
- Industry-specific terms (PGM, 4E vs 6E, UG2 reef, etc.)
- Financial metrics (P/E ratios, AISC, market cap)
- Explain when needed but don't avoid

✅ **Structural framework:**
- Keep methodological frameworks intact
- Preserve case study comparisons
- Maintain logical argument flow

---

## Transformation Examples

### Example 1: Academic Opening → Mick's Voice

**Before:**
> "The valuation of equity within the mining and extractive industries represents one of the most complex challenges in contemporary financial analysis."

**After:**
> "Right, let's talk about valuing mining companies. Specifically, those in the Platinum Group Metals (PGM) sector. Now, I'll be honest with you—this isn't straightforward stuff."

**Why:** Immediate engagement, conversational tone, acknowledges difficulty without academic distance.

---

### Example 2: Technical Explanation → Accessible but Precise

**Before:**
> "To overcome these analytical hurdles, a more robust and transparent approach for the sophisticated investor involves the calculation of best value per unit of currency through the lens of physical production leverage."

**After:**
> "So, how do we cut through all that? Well, I'm going to show you a dual-methodology approach that I reckon provides a far clearer picture: focusing on physical production leverage—essentially, how many ounces of metal your investment pound actually buys you at current valuations."

**Why:** Maintains technical concept but explains it conversationally. Uses "I reckon", "essentially" for warmth. Keeps precision with "investment pound".

---

### Example 3: Data Presentation → Data First, Warmth Second

**Before:**
> "For example, in the case of Tharisa plc, the utilization of a weighted average diluted share count of 304.8 million is recommended to ensure that valuation metrics reflect the true scope of the equity base."

**After:**
> "For example, with Tharisa plc, I'd use a weighted average diluted share count of 304.8 million to ensure valuation metrics reflect the true equity base."

**Why:** Same precision (304.8 million), but "I'd use" vs "is recommended" makes it personal guidance vs academic prescription.

---

### Example 4: Critical Point → British Understatement

**Before:**
> "Failing to normalize these figures would result in an artificial 25-30% undervaluation of 4E-reporting companies."

**After:**
> "Fail to normalise these figures and you'll artificially undervalue 4E-reporting companies by 25-30%."

**Why:** British spelling (normalise), direct address ("you'll"), keeps the critical warning but conversational.

---

## Document Generation Process

### Step 1: Extract Original Content
```python
from docx import Document
doc = Document(original_path)
for para in doc.paragraphs:
    print(para.text)
```

### Step 2: Load Context Profiles
Read all three JSON files:
- `voice-dna-mick.json`
- `icp.json`
- `business-profile.json`

### Step 3: Apply Voice Transformation
Rewrite following principles above, section by section:
1. Title → conversational, clear
2. Introduction → direct opening, engagement
3. Each section → data first, warm explanations
4. Conclusions → actionable takeaways + DYOR
5. Sign-off → Mick's standard closing

### Step 4: Generate .docx with docx-js
```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require('docx');

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      // Title, Heading1, Heading2 styles
    ]
  },
  sections: [{
    properties: {
      page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    children: [
      // Paragraphs with TextRun elements
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(output_path, buffer);
});
```

---

## Successful Test Case

**Original Document:**
`2026.02.16 - Strategic Dual Valuation Methodology_PGM's_Unformatted.docx` (40KB)

**Content Type:** Highly academic analysis of PGM mining company valuation using dual-methodology framework

**Transformation Applied:**
- ✅ Converted opening from academic to conversational
- ✅ Maintained all 190+ citations
- ✅ Preserved all numerical data (percentages, dates, figures)
- ✅ Kept technical terminology but explained in context
- ✅ Applied British English throughout
- ✅ Added Mick's signature transitions and phrases
- ✅ Ended with DYOR philosophy and standard sign-off

**Output Document:**
`2026.02.16 - Strategic Dual Valuation Methodology_PGM's_Mick's_Voice_v1.docx` (17KB)

**Result:**
Transformed from academic paper to peer-guidance document. Sounds like Mick explaining methodology to Inner Circle members—technical and data-driven, but warm, accessible, and focused on practical implementation.

---

## Quality Checklist

Before finalizing any voice rewrite, verify:

**Voice DNA:**
- [ ] Opens with direct, conversational hook
- [ ] Uses British English throughout
- [ ] Includes signature transitions (Meanwhile, As ever, Note that)
- [ ] Mixes sentence lengths appropriately
- [ ] Adds parenthetical asides for nuance
- [ ] Balances confidence with appropriate hedging
- [ ] Ends with DYOR + standard sign-off

**Technical Accuracy:**
- [ ] All numbers preserved exactly (to decimal points)
- [ ] All dates in British format (31st December 2025)
- [ ] All citations intact and numbered correctly
- [ ] All references preserved in bibliography
- [ ] Technical terminology maintained
- [ ] Structural framework preserved

**Audience Alignment:**
- [ ] Sounds like peer sharing, not expert lecturing
- [ ] Accessible to DIY investors (ICP)
- [ ] Reflects DIY-Investors brand philosophy
- [ ] Empowers reader to do own research
- [ ] Acknowledges complexity without drowning

**Document Quality:**
- [ ] Professional formatting (headings, spacing)
- [ ] Proper .docx structure
- [ ] Arial font throughout
- [ ] Appropriate visual hierarchy
- [ ] No formatting errors

---

## Files and Locations

**Context Profiles:**
- Voice DNA: `05-Areas/Writing_System/context/core/voice-dna-mick.json`
- ICP: `05-Areas/Writing_System/context/core/icp.json`
- Business Profile: `05-Areas/Writing_System/context/core/business-profile.json`

**Skills Directory:**
- `.claude/skills/` (for new voice-rewriting skill)

**Document Output:**
- Default: `05-Areas/Writing_System/knowledge/1-Drafts/`
- Naming: `YYYY.MM.DD - [Original Title]_Mick's_Voice_v1.docx`

**Dependencies:**
- Node.js with `docx` package (`npm install docx`)
- Python with `python-docx` (for extraction)

---

## Notes for Skill Creation

When converting this to a skill:

1. **Input Parameters:**
   - Source document path (must be .docx)
   - Output location (default to same folder)
   - Version number (default: v1)

2. **Process Flow:**
   - Load context profiles automatically
   - Extract original content
   - Apply voice transformation
   - Generate new .docx
   - Clean up temp files
   - Report success with file location

3. **Error Handling:**
   - Check docx module installed
   - Verify context profiles exist
   - Validate source document exists
   - Confirm output path writable

4. **User Confirmation:**
   - Show transformation summary
   - Preview key changes (opening, closing)
   - Confirm citations preserved
   - Report output file size and location

---

## Future Enhancements

Potential improvements for the skill:

- [ ] Add batch processing for multiple documents
- [ ] Include diff/comparison view (before/after)
- [ ] Support other input formats (PDF, markdown)
- [ ] Add voice intensity slider (more/less conversational)
- [ ] Generate transformation report with statistics
- [ ] Auto-detect document type and adjust approach
- [ ] Integration with newsletter/article writers

---

**End of Methodology Documentation**
