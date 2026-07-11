# Markdown to DOCX Conversion Guide

**For reviewing newsletter layout in Microsoft Word**

**Created:** 2026-02-07
**Status:** Pending review and decision

---

## The Problem

Newsletters are drafted in markdown (.md) but need to be reviewed in .docx format to:
- Check layout fits within 4 pages (A4)
- Verify headers and footers display correctly
- Ensure formatting matches newsletter template
- Review final appearance before publishing

---

## Three Options for Conversion

### Option 1: Use the Built-in DOCX Skill (Easiest)

**What it is:**
The `anthropic-docx` skill is already available in Dex. Claude can convert markdown to .docx on demand.

**How to use:**
```
You: "Convert the Three Pillars newsletter to .docx for layout review"
Claude: [Creates .docx file with your content]
```

Or invoke the skill:
```
/docx
```

**Pros:**
- [x] No setup required
- [x] Works immediately
- [x] Natural language requests
- [x] Can apply styling and formatting

**Cons:**
- [ ] Manual conversion each time
- [ ] May need to specify styling preferences repeatedly
- [ ] Not automated

**Best for:** Quick one-off conversions, testing, or occasional use

---

### Option 2: Pandoc with Newsletter Template (Most Control)

**What it is:**
Pandoc is a command-line tool that converts between document formats. You create a reference .docx template with your newsletter styling, and Pandoc applies it during conversion.

**Setup process:**

#### Step 1: Install Pandoc
```bash
# Windows
winget install pandoc

# Or download from: https://pandoc.org/installing.html
```

#### Step 2: Create Reference Template
1. Open your existing newsletter .docx in Word
2. Delete all content, keep only:
   - Page size (A4)
   - Margins
   - Headers and footers
   - Font styles
   - Heading styles
3. Save as `Newsletter-Template.docx` in Writing System folder

#### Step 3: Convert Markdown to DOCX
```bash
pandoc "1-Drafts/2026-02-07 - Three Pillars Newsletter.md" \
  -o "Newsletter-Preview.docx" \
  --reference-doc="Newsletter-Template.docx"
```

**Pros:**
- [x] Consistent styling every time
- [x] Uses YOUR exact newsletter template
- [x] One command converts with all formatting
- [x] Can be automated

**Cons:**
- [ ] Requires initial setup
- [ ] Command-line interface
- [ ] Need to maintain reference template

**Best for:** Regular newsletter production with consistent styling

---

### Option 3: Automated Workflow (Best Long-Term)

**What it is:**
A script that automatically converts markdown to .docx when you move files to `2-Ready/` folder.

**How it would work:**
1. You approve content in markdown
2. Move file to `2-Ready/`
3. Script detects file move
4. Auto-converts to .docx using Pandoc + your template
5. Saves .docx preview in same folder
6. You open .docx in Word to review layout

**Implementation options:**
- PowerShell script watching the folder
- Node.js script with file watcher
- Manual command you run after moving to Ready

**Pros:**
- [x] Fully automated
- [x] Consistent process
- [x] No manual conversion step
- [x] .docx preview always available

**Cons:**
- [ ] Requires scripting setup
- [ ] More complex to maintain
- [ ] Depends on Pandoc + template from Option 2

**Best for:** High-volume content production, established workflow

---

## Recommended Approach

**Start with Option 1** (DOCX skill)
- Test immediately
- See if it meets your needs
- Decide if you need more control

**Upgrade to Option 2** (Pandoc) if:
- You're converting regularly (weekly newsletters)
- You need consistent styling
- You want one-command conversion

**Consider Option 3** (Automation) if:
- You're producing a lot of content
- You want zero-friction workflow
- You're comfortable with scripting

---

## Additional Consideration: Metadata Tracking

Add fields to YAML frontmatter to track .docx previews:

```yaml
# Workflow
status: ready
docx_preview: true  # Has been converted and reviewed in Word
docx_preview_path: "2-Ready/2026-02-07 - Three Pillars Newsletter.docx"
docx_preview_date: 2026-02-08
page_count: 4  # Verified in Word
layout_approved: true
```

**Benefits:**
- Track which content has been reviewed in .docx format
- Know page count before publishing
- Confirm layout approval in workflow
- Can filter in Bases: "Show me Ready content that needs .docx review"

---

## Questions to Answer

Before deciding on an approach, consider:

1. **Frequency:** How often do you create newsletters?
   - Weekly/monthly -> Consider Pandoc setup
   - Occasional -> DOCX skill is fine

2. **Consistency:** Do you need identical styling every time?
   - Yes -> Pandoc with template
   - No -> DOCX skill

3. **Technical comfort:** Are you comfortable with command-line tools?
   - Yes -> Pandoc gives you control
   - No -> DOCX skill is easier

4. **Automation desire:** Do you want this to happen automatically?
   - Yes -> Build automation (Option 3)
   - No -> Manual conversion is fine

5. **Template complexity:** How complex is your newsletter template?
   - Simple -> DOCX skill can handle it
   - Complex (headers, footers, specific fonts) -> Pandoc template

---

## Next Steps

**Decision needed:**
1. Choose which option to try first
2. Test with Three Pillars newsletter
3. Evaluate results
4. Decide if current approach works or needs upgrading

**If choosing Pandoc:**
- Install Pandoc
- Create reference template from existing newsletter
- Test conversion
- Verify styling matches expectations

**If choosing DOCX skill:**
- Request conversion of Three Pillars newsletter
- Review output in Word
- Provide feedback on styling/formatting
- Decide if sufficient or need Pandoc

**If choosing automation:**
- Start with Pandoc setup (Option 2)
- Test manual conversion first
- Then build automation once manual process is solid

---

## Resources

- **Pandoc documentation:** https://pandoc.org/MANUAL.html
- **Pandoc reference docs:** https://pandoc.org/MANUAL.html#option--reference-doc
- **DOCX skill:** Already available in Dex, invoke with `/docx`

---

## Status: Awaiting Decision

**Created:** 2026-02-07 evening
**Review by:** 2026-02-08 morning
**Decision needed on:**
- Which option to try first
- Whether to set up Pandoc template
- Whether to add metadata tracking for .docx previews
