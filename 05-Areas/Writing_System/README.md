# Writing System

**Your AI co-writer powered by voice DNA, ICP, and business profile**

This system helps you create high-quality content that sounds like you and resonates with your target audience.

**Enhanced with:**
- [x] Complete content workflow (Ideas -> Draft -> Ready -> Published -> Derivatives)
- [x] Destination tracking (diy-investors.com vs diy-investors.ai)
- [x] Content repurposing framework
- [x] Obsidian Bases integration for database views

---

## Content Workflow Overview

```
0-Ideas/        -> Messy thoughts, outlines, writing brainstorms
1-Drafts/       -> Formal drafts from AI or you
2-Ready/        -> Approved content ready to publish
3-Published/    -> Published parent content (newsletters, articles)
4-Derivatives/  -> Repurposed content (social posts, snippets)
Archive/        -> Retired content
```

**See:** `Bases Configuration Guide.md` for Obsidian database setup

---

## Quick Start

### Writing Skills Available

Use these skills with the `/` command:

| Skill | Purpose | Command |
|-------|---------|---------|
| **Thought Leadership** | Value-packed newsletters (800-1,500 words) | `/thought-leadership` |
| **Substack Note** | High-performing short notes | `/substack-note` |
| **Content Extraction** | Extract ideas from long-form content | `/content-extraction` |
| **Social Media Bios** | Platform-specific bio generation | `/social-media-bio-generator` |

### Writing Agents Available

Specialized agents for complex writing tasks (use with Task tool):

| Agent | Purpose | Use When |
|-------|---------|----------|
| **article-writer** | Long-form articles | Need deep, researched content |
| **newsletter-writer** | Email newsletters | Regular audience communication |
| **researcher-agent** | Research and synthesis | Gathering insights for content |

---

## Complete Workflow

### Stage 0: Ideation (0-Ideas/)

**When:** You have messy thoughts or want to plan content

**Process:**
1. Brain dump ideas to `0-Ideas/[Topic] brainstorm.md`
2. Structure into outline when ready
3. Request AI draft from outline

**Example:**
```
You: "I have some thoughts on the Three Pillars in 0-Ideas/"
Cedric: [Reads outline, creates draft in 1-Drafts/]
```

---

### Stage 1: Drafting (1-Drafts/)

**When:** AI creates formal draft or you write one

**Process:**
1. Draft saved with metadata (destination, division, topics)
2. You review and edit
3. When satisfied, change `status` to `ready`
4. Add `approved` date
5. Move to `2-Ready/`

**Metadata tracking:**
- Destination: diy-investors.com, diy-investors.ai, both
- Division: core, ai, personal
- Target audience: inner_circle, plaza_group, ai_members, public

---

### Stage 2: Ready to Publish (2-Ready/)

**When:** Content is approved and waiting to go live

**Process:**
1. Content sits here until you publish
2. Use Bases to filter by destination
3. Publish when ready
4. Update `published` date and `urls`
5. Change `status` to `published`
6. Move to `3-Published/`

---

### Stage 3: Published (3-Published/)

**When:** Content is live

**Process:**
1. Parent content lives here
2. Track where published (`published_to`)
3. Track URLs
4. Becomes seed for derivative content

---

### Stage 4: Repurposing (4-Derivatives/)

**When:** You want to extract social posts, snippets from published content

**Process:**
1. Request derivatives from published piece
2. AI creates folder: `4-Derivatives/[Parent Title]/`
3. Multiple derivative files created, each tracking parent
4. Publish derivatives, track engagement

**Example:**
```
You: "Extract 3 LinkedIn posts from the Three Pillars newsletter"
Cedric: [Creates 3 posts in 4-Derivatives/2026-02-07 - Three Pillars/]
```

---

## System Components

### 1. Context Profiles (`context/core/`)

Your writing foundation - always loaded before creating content:

| Profile | Contains | Purpose |
|---------|----------|---------|
| **voice-dna-mick.json** | Tone, style, phrases, boundaries | Sound like you |
| **icp.json** | Audience pain points, language, aspirations | Speak to their problems |
| **business-profile.json** | Offerings, positioning, methodology | Integrate CTAs naturally |

### 2. Knowledge Base (`knowledge/`)

**Published Content** (`knowledge/content/`)
- Past newsletters, letters, and polished work
- Reference for topics already covered
- Examples of your authentic voice

**Drafts** (`knowledge/drafts/`)
- Work in progress
- Current projects being developed

### 3. Templates (`_templates/`)

Reusable note structures for consistency.

---

## How to Use This System

### Before Writing Anything

1. **Pick the right skill** - Newsletter? Article? Social post?
2. **The system auto-loads context** - Voice DNA, ICP, and business profile inject automatically
3. **Reference past work** - Check `/knowledge/content/` for similar topics

### Writing Workflow

```
You: "/thought-leadership about [topic]"
Claude: [Reads voice-dna-mick.json, icp.json, business-profile.json]
Claude: [Produces newsletter in your voice, for your audience]
```

### What Gets Loaded Automatically

When you use any writing skill:
- [x] Your voice DNA (how you sound)
- [x] Your ICP (who you write for)
- [x] Your business profile (what you offer)

**You don't need to remind me** - the system handles context injection.

---

## Content Profile Summary

### Your Voice
*Loaded from: `context/core/voice-dna-mick.json`*

Your unique tone, communication style, signature phrases, and voice boundaries are captured here. Every piece of content matches this voice automatically.

### Your Audience
*Loaded from: `context/core/icp.json`*

Your Ideal Customer Profile defines who you write for, what they struggle with, what they want, and how they talk. Content speaks directly to their pain points in their language.

### Your Business
*Loaded from: `context/core/business-profile.json`*

Your offerings, positioning, and methodology ensure CTAs and positioning statements align with your business goals.

---

## Tips for Best Results

1. **Trust the context** - You don't need to explain your voice every time
2. **Reference past work** - Say "similar to my January newsletter" to guide style
3. **Be specific** - "Newsletter about investment risk" works better than "write something"
4. **Iterate naturally** - Give feedback like you would to a human co-writer

---

## Updating Your Profiles

To update your voice, audience, or business context:

1. Edit the relevant JSON file in `context/core/`
2. Changes apply immediately to all future content
3. Templates in `context/core/` show the expected structure

---

## Integration with Dex

This Writing System integrates with Dex workflows:

- **Daily Plan** - Block time for content creation
- **Tasks** - "Write newsletter" -> auto-suggests `/thought-leadership`
- **Projects** - Content series tracked as projects
- **Person Pages** - Write for specific people in your network

---

**Questions?** Just ask naturally: "How do I write a LinkedIn post?" or "What's my voice DNA?"
