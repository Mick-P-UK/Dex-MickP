# Bases Configuration Guide

**Using Obsidian Bases for Content Management**

This guide shows you how to set up database views in Obsidian using the Bases plugin to manage your content workflow.

---

## Quick Start

1. Install **Bases** plugin in Obsidian
2. Create a new Base pointing to `05-Areas/Writing_System/knowledge/`
3. Add columns from the YAML frontmatter fields
4. Create filtered views for different workflows

---

## Recommended Base Setups

### Base 1: Content Pipeline (Master View)

**Purpose:** See all content across all workflow stages

**Configuration:**
- **Folder:** `05-Areas/Writing_System/knowledge/`
- **Include subfolders:** Yes

**Columns to Add:**

| Column Name | Field | Type | Width |
|-------------|-------|------|-------|
| Title | `title` | Text | 300px |
| Status | `status` | Select | 100px |
| Destination | `destination` | Select | 150px |
| Division | `division` | Select | 100px |
| Target Audience | `target_audience` | Select | 120px |
| Created | `created` | Date | 100px |
| Published | `published` | Date | 100px |
| Priority | `priority` | Select | 80px |

**Select Field Options:**

- **Status:** draft, ready, published, archived
- **Destination:** diy-investors.com, diy-investors.ai, both, external
- **Division:** core, ai, personal
- **Target Audience:** inner_circle, plaza_group, ai_members, public, all
- **Priority:** high, normal, low

**Saved Views Within This Base:**

1. **All Content** - No filters
2. **DIY-Investors.com** - Filter: `destination` contains `diy-investors.com` OR `both`
3. **DIY-Investors.ai** - Filter: `destination` contains `diy-investors.ai` OR `both`
4. **Ready to Publish** - Filter: `status` = `ready`
5. **Published This Month** - Filter: `published` within last 30 days
6. **High Priority** - Filter: `priority` = `high`
7. **Needs Review** - Filter: `needs_review` = `true`

---

### Base 2: Ready to Publish Dashboard

**Purpose:** Quick view of content ready to go live

**Configuration:**
- **Folder:** `05-Areas/Writing_System/knowledge/2-Ready/`
- **Include subfolders:** No

**Columns:**

| Column Name | Field | Type |
|-------------|-------|------|
| Title | `title` | Text |
| Destination | `destination` | Select |
| Target Audience | `target_audience` | Select |
| Approved | `approved` | Date |
| Priority | `priority` | Select |

**Grouping:** Group by `destination`

**Sorting:** Priority (high to low), then Approved (newest first)

**What you see:** Content ready to publish, visually separated by destination

---

### Base 3: Editorial Calendar

**Purpose:** Timeline view of published content

**Configuration:**
- **Folder:** `05-Areas/Writing_System/knowledge/3-Published/`
- **View Mode:** Calendar (use `published` field as date)

**Columns:**

| Column Name | Field | Type |
|-------------|-------|------|
| Title | `title` | Text |
| Published | `published` | Date |
| Destination | `destination` | Select |
| Content Type | `content_type` | Select |
| URLs | `urls` | List |

**What you see:** Visual calendar showing publishing schedule

---

### Base 4: Repurposing Tracker

**Purpose:** Track which content has been repurposed

**Configuration:**
- **Folder:** `05-Areas/Writing_System/knowledge/3-Published/`

**Columns:**

| Column Name | Field | Type | Formula |
|-------------|-------|------|---------|
| Title | `title` | Text | - |
| Published | `published` | Date | - |
| Derivatives | `derivatives` | List | - |
| Derivative Count | - | Number | `length(derivatives)` |

**Filter:** `derivatives` is not empty

**Sorting:** Derivative Count (descending)

**What you see:** Which long-form pieces generated most repurposed content

---

### Base 5: Social Media Performance

**Purpose:** Track engagement on derivative content

**Configuration:**
- **Folder:** `05-Areas/Writing_System/knowledge/4-Derivatives/`

**Columns:**

| Column Name | Field | Type |
|-------------|-------|------|
| Title | `title` | Text |
| Platform | `platform` | Select |
| Likes | `engagement_likes` | Number |
| Shares | `engagement_shares` | Number |
| Comments | `engagement_comments` | Number |
| Published | `published` | Date |
| Parent | `derived_from` | Link |

**Filter:** `status` = `published`

**Sorting:** Likes (descending)

**What you see:** Top-performing social content

---

## Field Type Reference

Configure these field types in Bases for optimal filtering and sorting:

### Text Fields
- `title`
- `reviewer_notes`

### Select Fields (Single Choice)
- `status` → Options: draft, ready, published, archived
- `destination` → Options: diy-investors.com, diy-investors.ai, both, external
- `division` → Options: core, ai, personal
- `target_audience` → Options: inner_circle, plaza_group, ai_members, public, all
- `content_type` → Options: newsletter, article, social_post, email, video_script
- `category` → Options: education, market_commentary, strategy, ai_tools, portfolio_update
- `priority` → Options: high, normal, low
- `platform` → Options: linkedin, twitter, facebook, instagram, email

### Multi-Select Fields
- `topics`
- `published_to`

### Date Fields
- `created`
- `approved`
- `published`
- `archived`

### Number Fields
- `engagement_likes`
- `engagement_shares`
- `engagement_comments`
- `engagement_views`

### Checkbox Fields
- `needs_review`

### Link Fields
- `derived_from` (parent content link)

### List Fields
- `derivatives` (child content links)
- `urls`

---

## Common Workflows

### Workflow 1: Managing Drafts

**Base to use:** Content Pipeline (Master View)

**View:** Filter by `status` = `draft`

**Actions:**
- Review drafts
- Change `status` to `ready` when approved
- Add `approved` date
- Update `priority` if urgent

---

### Workflow 2: Publishing Content

**Base to use:** Ready to Publish Dashboard

**View:** Group by `destination`

**Actions:**
- See what's ready for diy-investors.com vs diy-investors.ai
- Publish content
- Update `published` date
- Add `urls` after publishing
- Move file from `2-Ready/` to `3-Published/`
- Change `status` to `published`

---

### Workflow 3: Planning Repurposing

**Base to use:** Repurposing Tracker

**View:** Filter by `derivatives` = empty (content not yet repurposed)

**Actions:**
- Identify published content that hasn't been repurposed
- Request derivative creation
- Track new derivatives in `derivatives` field

---

### Workflow 4: Tracking Performance

**Base to use:** Social Media Performance

**View:** Sort by `engagement_likes` descending

**Actions:**
- See top-performing social content
- Identify what resonates
- Update engagement numbers periodically
- Find patterns for future content

---

## Tips for Using Bases

### Tip 1: Use Grouping for Visual Organization

Group by `status` to see:
- Draft column
- Ready column
- Published column
- Archived column

Group by `destination` to see:
- diy-investors.com content
- diy-investors.ai content
- Both platforms content

### Tip 2: Create Custom Views for Different Contexts

Same Base, different saved views:
- **Morning view:** High priority + needs review
- **Publishing view:** Ready to publish + grouped by destination
- **Weekly review:** Published this week + engagement stats
- **Planning view:** Ideas + drafts + priority sorting

### Tip 3: Use Filters to Focus

**Common filters:**
- Show only high priority: `priority` = `high`
- Show only .com content: `destination` contains `diy-investors.com` OR `both`
- Show only .ai content: `destination` contains `diy-investors.ai` OR `both`
- Show recent: `created` within last 7 days
- Show needs attention: `needs_review` = `true`

### Tip 4: Update Metadata Directly in Bases

You can edit YAML fields directly in the Bases table view:
- Change status from draft → ready
- Add publication dates
- Update engagement numbers
- Mark for review

Changes save automatically to the markdown files.

---

## Example Base View: "This Week's Publishing"

**Configuration:**
- Filter: `status` = `ready` AND `priority` = `high`
- Group by: `destination`
- Sort: `approved` (newest first)

**Result:** High-priority content ready to publish, organized by destination

**Actions:**
- Review what's ready for .com
- Review what's ready for .ai
- Publish sequentially
- Update metadata as you go

---

## Maintenance

### Weekly
- Update engagement stats on published derivatives
- Mark old drafts for review or archiving
- Check repurposing tracker for new opportunities

### Monthly
- Archive old published content if replaced
- Review performance stats
- Clean up orphaned draft ideas

### Quarterly
- Analyze which destinations get most content
- Review category distribution
- Identify gaps in content topics

---

**Ready to set up your first Base?**

1. Open Obsidian
2. Install Bases plugin
3. Create Base #1: Content Pipeline (Master View)
4. Add columns from this guide
5. Start filtering and organizing!
