# YouTube Content Management System

**Last Updated:** 2026-02-08

A project-based YouTube content system that manages video creation, publishing, and derivatives across both DIY-Investors channels.

---

## System Philosophy

**Each YouTube video is a PROJECT** with:
- Its own folder containing all assets (research, scripts, thumbnails, B-roll notes)
- Clear production phases tracked via YAML frontmatter
- Associated tasks auto-linked in Tasks.md
- Derivatives (shorts, clips) organized under the parent project
- Reusable context from the Writing System (voice DNA, ICP, business profile)

---

## Directory Structure

```
YouTube_System/
├── README.md                          # This file
├── Content-Calendar.md                # Monthly planning across channels
│
├── context/
│   ├── channel-configs/               # Channel-specific settings
│   │   ├── diy-investors-com.yaml    # Main channel config
│   │   └── diy-investors-ai.yaml     # AI channel config
│   └── shared/                        # Symlink to Writing_System/context/core/
│       ├── voice-dna-mick.json       # (reused from Writing System)
│       ├── icp.json                  # (reused from Writing System)
│       └── business-profile.json     # (reused from Writing System)
│
├── _templates/                        # Project creation templates
│   ├── YT-Project-Folder-Structure.md
│   ├── YT-Project-Main.md
│   ├── YT-Script-Template.md
│   └── YT-Derivative-Template.md
│
├── diy-investors.com/
│   ├── YT-Longform/                  # Full-length videos (8-12 min)
│   └── YT-Series/                    # Multi-part series
│
└── diy-investors.ai/
    ├── YT-Longform/                  # Full-length videos (10-15 min)
    └── YT-Series/                    # Multi-part series
```

---

## Creating a New Video Project

### Step 1: Choose Channel and Type

**Channel:**
- `diy-investors.com/` - Educational content, market analysis, Q&A
- `diy-investors.ai/` - AI tools, demos, automation strategies

**Type:**
- `YT-Longform/` - Standalone videos
- `YT-Series/` - Multi-episode series

### Step 2: Create Project Folder

**Naming convention:** `YYYY-MM-DD - Video Title/`

Example: `2026-02-09 - Three Pillars of DIY Investing/`

**Folder structure:**
```
2026-02-09 - Three Pillars of DIY Investing/
├── PROJECT.md                 # Main project file (see template)
├── research/
│   ├── notes.md              # Research notes
│   └── sources.md            # Sources and references
├── scripts/
│   ├── v1-draft.md           # Initial script
│   ├── v2-reviewed.md        # After review
│   └── v3-final.md           # Final shooting script
├── assets/
│   ├── thumbnail-concepts.md # Thumbnail ideas
│   ├── b-roll-needed.md      # B-roll shot list
│   └── graphics.md           # On-screen graphics notes
└── YT-Derivatives/
    ├── Short-1-[Topic].md    # YouTube Shorts
    └── X-Clip-[Topic].md     # Social media clips
```

### Step 3: Use PROJECT.md Template

Copy `_templates/YT-Project-Main.md` and customize:

**Key frontmatter fields:**
- `status` - Current production phase (see Status Workflow below)
- `channel` - Which channel this belongs to
- `pillar` - Strategic pillar alignment
- `target_audience` - From ICP (inner_circle, plaza_group, ai_members, public)
- `planned_publish_date` - Target publication date

### Step 4: Link to Content Calendar

Add the project to `Content-Calendar.md` under the appropriate month.

---

## Status Workflow

Projects move through these phases:

### 1. Research
- Gathering sources, examples, data
- Validating topic fit for audience
- Checking competition/existing content

**Tasks created:** None yet

### 2. Scripting
- Writing initial script draft
- Adding B-roll notes
- Planning visual elements

**Tasks created:** "Write script for [video title]"

### 3. Draft
- Script reviewed and refined
- Ready for filming

**Tasks created:** "Review script for [video title]"

### 4. Edited
- Video filmed
- Rough cut complete
- Thumbnail designed

**Tasks created:**
- "Film [video title]"
- "Edit [video title]"

### 5. Final
- Final edit approved
- Thumbnail finalized
- SEO metadata written (title, description, tags)
- Ready to upload

**Tasks created:** "Create thumbnail for [video title]"

### 6. Published
- Uploaded to YouTube
- Scheduled or live
- Analytics tracking begins

**Tasks created:** "Upload and publish [video title]"

---

## Channel Guidelines

### DIY-Investors.com Channel

**Posting frequency:** Weekly (Sundays)
**Video length:** 8-12 minutes
**Audience:** Inner Circle, Plaza Group, Public

**Content mix:**
- 60% Educational (fundamental/technical analysis tutorials)
- 30% Market Analysis (current market commentary)
- 10% Q&A (answering community questions)

**Style:** Clear, educational, actionable advice

**See:** `context/channel-configs/diy-investors-com.yaml` for complete guidelines

### DIY-Investors.ai Channel

**Posting frequency:** Bi-weekly (every 2 weeks)
**Video length:** 10-15 minutes
**Audience:** AI Members, Inner Circle, Plaza Group, Public

**Content mix:**
- 50% AI Tools Demos (step-by-step walkthroughs)
- 30% AI Strategy (how to integrate AI into investing workflow)
- 20% Case Studies (real examples of AI-powered research)

**Style:** Tech-forward, screen-heavy, practical demonstrations

**See:** `context/channel-configs/diy-investors-ai.yaml` for complete guidelines

---

## Task Integration

### Current (Manual)

When you change a video's status in PROJECT.md:
1. Manually create corresponding task in `03-Tasks/Tasks.md`
2. Link task ID in PROJECT.md frontmatter under `tasks:`
3. Reference project folder in task description

### Future (Automated) - Phase 5

Status changes will automatically trigger task creation:
- `research → scripting`: Create "Write script" task
- `scripting → draft`: Create "Review script" task
- `draft → edited`: Create "Film" and "Edit" tasks
- `edited → final`: Create "Create thumbnail" task
- `final → published`: Create "Upload and publish" task

Tasks will be auto-assigned to the correct pillar based on channel.

---

## Derivatives Workflow

### Creating YouTube Shorts from Longform

1. Identify 2-3 standalone moments from the main video
2. Create derivative files in `YT-Derivatives/` folder
3. Use template: `_templates/YT-Derivative-Template.md`
4. Track in PROJECT.md under `derivatives:` section

**Naming:** `Short-[Number]-[Topic].md`

Example: `Short-1-Fundamental-Analysis.md`

### Creating Social Media Clips

1. Extract punchy soundbites (30-60 seconds)
2. Create derivative file in `YT-Derivatives/`
3. Tag with platform (X, LinkedIn, Instagram)

**Naming:** `[Platform]-Clip-[Topic].md`

Example: `X-Clip-Market-Makers.md`

### Tracking Derivatives

Update PROJECT.md frontmatter:
```yaml
derivatives_created: 3
derivatives_published: 2
derivatives:
  - YT-Derivatives/Short-1-Fundamental-Analysis.md
  - YT-Derivatives/Short-2-Technical-Analysis.md
  - YT-Derivatives/X-Clip-Market-Makers.md
```

---

## Content Calendar Integration

### Monthly Planning

1. Open `Content-Calendar.md`
2. Add planned videos to appropriate month
3. Balance content across both channels
4. Consider topic seasonality (earnings season, year-end, etc.)

### Weekly Integration

During `/week-plan`:
- Check upcoming videos from Content Calendar
- Create tasks for videos entering production
- Link video projects to weekly priorities

During `/daily-plan`:
- Surface video production tasks based on status
- Suggest next steps for in-progress videos

---

## Context Reuse

### Shared Context Profiles

The `context/shared/` folder is a symlink to `05-Areas/Writing_System/context/core/`, giving you access to:

1. **Voice DNA** (`voice-dna-mick.json`)
   - Tone, style, phrases
   - Do Your Own Research (DYOR) philosophy
   - Writing boundaries and patterns

2. **ICP** (`icp.json`)
   - Target audience pain points
   - Language preferences
   - Aspirations and goals

3. **Business Profile** (`business-profile.json`)
   - Offerings and pricing
   - Positioning and frameworks
   - Three Pillars methodology

### Using Context in Scripts

When writing scripts, reference these profiles to ensure:
- Consistent voice across written and video content
- Audience-appropriate language and examples
- Alignment with business positioning

---

## Best Practices

### Thumbnail Strategy
- Design 2-3 thumbnail concepts before filming
- Test with target audience if possible
- Use high contrast, bold text, person visible
- Match channel branding guidelines

### Script Writing
- Start with hook (first 10 seconds critical)
- Use pattern interrupts every 60-90 seconds
- Include clear call-to-action at end
- Add B-roll notes inline with script

### SEO Optimization
- Research keywords before writing title
- Front-load keywords in title and description
- Use 5-10 relevant tags
- Write first sentence of description for search results

### Production Efficiency
- Batch filming when possible (same setup/lighting)
- Record multiple takes of key moments
- Capture extra B-roll for future videos
- Keep project folders organized throughout

---

## Analytics Tracking (Future)

Project frontmatter includes `analytics:` section for tracking:
- Views
- Watch time
- Engagement (likes, comments)
- Click-through rate (CTR)
- Average view duration

**Note:** Analytics integration coming in Phase 6.

---

## Getting Help

**Templates:** See `_templates/` folder for project structure examples
**Channel configs:** See `context/channel-configs/` for style guidelines
**Questions:** Ask Cedric "How do I [task] in YouTube System?"

---

## Changelog

**2026-02-08** - Initial YouTube System created
- Project-based structure with channel separation
- Status workflow with future task automation
- Shared context profiles from Writing System
- Templates and content calendar
