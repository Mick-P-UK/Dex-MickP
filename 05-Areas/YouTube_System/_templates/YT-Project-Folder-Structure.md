# YouTube Project Folder Structure Guide

This guide explains how to set up a new YouTube video project.

---

## Quick Start

1. **Choose channel and type:**
   - `diy-investors.com/YT-Longform/` or `diy-investors.ai/YT-Longform/`
   - For series: use `YT-Series/[Series Name]/`

2. **Create folder with naming convention:**
   ```
   YYYY-MM-DD - Video Title/
   ```
   Example: `2026-02-15 - Understanding P/E Ratios/`

3. **Create these subfolders:**
   ```
   research/
   scripts/
   assets/
   YT-Derivatives/
   ```

4. **Copy template:** Copy `YT-Project-Main.md` template and rename to `PROJECT.md`

5. **Customize frontmatter:** Update title, channel, status, target audience, etc.

---

## Complete Folder Structure

```
YYYY-MM-DD - Video Title/
|
+-- PROJECT.md                    # Main project file (required)
|   +-- YAML frontmatter         # Metadata and status tracking
|
+-- research/                     # Research phase
|   +-- notes.md                 # Research notes and findings
|   +-- sources.md               # Source links and references
|   +-- data.md                  # Statistics, charts, examples
|   +-- competitor-analysis.md   # What others have done on this topic
|
+-- scripts/                      # Scripting phase
|   +-- outline.md               # Initial outline
|   +-- v1-draft.md              # First full draft
|   +-- v2-reviewed.md           # After review/edits
|   +-- v3-final.md              # Final shooting script
|   +-- [Use script template]    # Copy from YT-Script-Template.md
|
+-- assets/                       # Production assets
|   +-- thumbnail-concepts.md    # Thumbnail ideas and variants
|   +-- b-roll-needed.md         # B-roll shot list
|   +-- graphics.md              # On-screen graphics needed
|   +-- music-notes.md           # Music choices
|   +-- final-files/             # Finished thumbnail, graphics
|       +-- thumbnail-v1.png
|       +-- thumbnail-v2.png
|       +-- thumbnail-final.png
|
+-- YT-Derivatives/               # Repurposed content
    +-- Short-1-[Topic].md       # YouTube Shorts (under 60 sec)
    +-- Short-2-[Topic].md
    +-- X-Clip-[Topic].md        # Social media clips for X/Twitter
    +-- LinkedIn-Clip-[Topic].md # LinkedIn clips
    +-- [Use derivative template] # Copy from YT-Derivative-Template.md
```

---

## File Purpose

### PROJECT.md
- **Single source of truth** for the video project
- Tracks production status, metadata, tasks
- Links to all related files and derivatives
- Contains YAML frontmatter for automation (future)

### research/
- Background research before scripting
- Source validation and fact-checking
- Example gathering
- Competitor analysis

### scripts/
- Script development from outline to final
- Version control (v1, v2, v3...)
- B-roll notes inline with script
- Final shooting script

### assets/
- Thumbnail concepts and designs
- B-roll shot lists
- On-screen graphics planning
- Music and sound effect notes
- Final production files

### YT-Derivatives/
- YouTube Shorts extracted from main video
- Social media clips (X, LinkedIn, Instagram)
- Standalone moments that work independently
- Tracks derivatives in PROJECT.md frontmatter

---

## Status Progression

As you work through the project, update `status:` in PROJECT.md:

1. **research** - Gathering sources, validating topic
2. **scripting** - Writing the script
3. **draft** - Script complete, ready for filming
4. **edited** - Filmed and edited
5. **final** - Ready to publish (thumbnail, SEO done)
6. **published** - Live on YouTube

---

## Workflow Tips

### Starting a New Project
1. Create folder structure
2. Start with research/notes.md
3. Copy PROJECT.md template and fill in frontmatter
4. Add to Content-Calendar.md
5. Create task in 03-Tasks/Tasks.md

### During Production
- Update status in PROJECT.md as you progress
- Keep scripts versioned (v1, v2, v3...)
- Document B-roll needs inline with script
- Save multiple thumbnail variants

### After Publishing
- Add YouTube URL to PROJECT.md
- Link published video in Content-Calendar.md
- Create derivatives (shorts, clips)
- Track analytics in PROJECT.md frontmatter

---

## Example: Real Project

```
diy-investors.com/YT-Longform/2026-02-15 - Understanding P/E Ratios/
|
+-- PROJECT.md
|   status: published
|   youtube_url: https://youtube.com/watch?v=ABC123
|
+-- research/
|   +-- notes.md (examples of P/E ratios from real stocks)
|   +-- sources.md (links to SEC filings, finance sites)
|
+-- scripts/
|   +-- outline.md (initial structure)
|   +-- v1-draft.md (first draft)
|   +-- v2-reviewed.md (after feedback)
|   +-- v3-final.md (shooting script with B-roll notes)
|
+-- assets/
|   +-- thumbnail-concepts.md (3 concepts tested)
|   +-- b-roll-needed.md (stock charts, calculator shots)
|   +-- graphics.md (P/E formula on-screen)
|   +-- final-files/
|       +-- thumbnail-final.png
|
+-- YT-Derivatives/
    +-- Short-1-PvsE-Formula.md (60-sec explainer)
    +-- Short-2-PvsE-Traps.md (common mistakes)
```

---

## Next Steps

1. **Create your first project folder** following this structure
2. **Copy PROJECT.md template** from `_templates/YT-Project-Main.md`
3. **Fill in frontmatter** with your video details
4. **Start researching!**

---

**See Also:**
- [[YouTube_System/[[README]]|YouTube System README]]
- [[YouTube_System/_templates/YT-Project-Main|PROJECT.md Template]]
- [[YouTube_System/_templates/YT-Script-Template|Script Template]]
