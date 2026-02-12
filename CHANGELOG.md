# Changelog

All notable changes to Dex will be documented in this file.

**For users:** Each entry explains what was frustrating before, what's different now, and why you'll care.

---

## [Unreleased]

### 🔒 API Key Security Requirements (Hard-Baked)

**What was missing:** No explicit guidance on where to store API keys and credentials when integrating external services (MCPs, cloud APIs, databases). This created risk of accidentally committing secrets to GitHub.

**What's different now:** Hard security requirement added to CLAUDE.md - **ALL API keys, tokens, and credentials MUST be stored in `.env` file (gitignored), NEVER in config files.**

**The rules:**
- ✅ Store secrets in `.env` (gitignored)
- ✅ Reference via `${VAR_NAME}` in configs
- ✅ Never hardcode keys in `.mcp.json`, docs, scripts, or commits
- ✅ Defense-in-depth: even gitignored configs use references
- ❌ Stop immediately if hardcoded key detected

**Why you'll care:** Your API keys and credentials will never accidentally end up on GitHub. Following this pattern is mandatory for all external integrations (YouTube, OpenAI, databases, OAuth tokens, webhook secrets, etc.).

**Technical details:** Added "Security & API Keys (CRITICAL - NON-NEGOTIABLE)" section to CLAUDE.md → Core Behaviors. This is now enforced behavior, not optional guidance.

---

### ⏰ Time-Based Greeting Enforcement

**What was frustrating:** Cedric would greet with "Good morning/afternoon/evening" without actually checking the current time first. This led to incorrect greetings (saying "morning" when it was actually evening) and broke the time-aware personalization.

**What's different now:** Time verification is now **mandatory** in the Session Start Protocol. Before greeting at the start of any session, Cedric must:
1. Check current UTC time programmatically
2. Calculate London (Europe/London) timezone
3. Use the appropriate greeting based on actual time:
   - Before 12:00: "Good morning, Mick"
   - 12:00-18:00: "Good afternoon, Mick"
   - After 18:00: "Good evening, Mick"

**Why you'll care:** Every session now starts with a correctly time-aware greeting. No more "morning" when it's evening. Small detail, but it makes interactions feel more natural and shows that the system is paying attention.

**Technical details:** Added Step 2 to Session Start Protocol in CLAUDE.md. Time verification is now part of the "REQUIRED at every session start - no exceptions" enforcement layer, not just a descriptive guideline.

---

### 🛡️ Date Verification Safeguards

**What was frustrating:** Date-based files (daily plans, reviews, weekly syntheses) could be created with incorrect dates if the system assumed dates instead of verifying them. This caused confusion, duplicate files, and broken workflows.

**What's different now:** All date-based routines now verify the current date programmatically before creating any files. This includes:
- `/daily-plan` - Verifies today's date and day of week
- `/review` and `/daily-review` - Verifies date before creating review files
- `/week-plan` and `/week-review` - Calculates Monday of the week correctly from actual date
- `/quarter-plan` and `/quarter-review` - Calculates current quarter correctly based on user's Q1 start month
- `/journal` - Verifies date for daily and weekly journal entries

**Why you'll care:** No more wrong dates, no more duplicate files, no more confusion about which day/week/quarter you're working with. The system always uses the correct date, calculated from your system clock, not assumptions.

**Technical details:** Added Step 0: Date Verification (CRITICAL) to all date-based skills. See CLAUDE.md → File Conventions → Date Verification for the full guidelines.

**Skill creation safeguards:** Both `/create-skill` and `/anthropic-skill-creator` now include date verification checklists. When creating new skills, if dates are involved, the date verification step is automatically required. This prevents future date errors in newly created skills.

---

## [1.3.0] - 2026-02-05

### 🔬 X-Ray: Understand What's Actually Happening (and Make Dex Your Own)

From the start, Dex was built to do two things: help you get organised, and help you understand AI. X-Ray delivers on that second promise.

**How to use it:** Type `/xray` followed by whatever you want to understand. That's it.

- `/xray How does the Career MCP server work?`
- `/xray How is the daily-plan command working?`
- `/xray What just happened in this conversation?`
- `/xray How did Dex know to pull that person page?`

Dex will show you exactly what happened — which files were read and why, which tools fired, how context was loaded — and connect it all to the AI concepts behind it. It generates diagrams, walks you through the building blocks, and ties everything back to your actual vault and your actual actions.

**Deep-dive modes** (type these exactly as shown):
- `/xray ai` — First principles: context windows, tokens, statelessness, tools
- `/xray dex` — The full architecture: CLAUDE.md, hooks, MCPs, skills, vault structure
- `/xray boot` — How a Dex session starts up, step by step
- `/xray extend` — How to customise: edit CLAUDE.md, create skills, write hooks, build MCPs

**Why this matters:** There are plenty of great courses out there that teach AI proficiency. But I passionately believe the best way to learn AI is to build with it. There's nothing more personal than building your own knowledge system through something like Dex — and being able to see what's actually happening as you go. X-Ray opens the black box. You stop being a passive user and start understanding the mechanics, which means you can extend, customise, and make Dex genuinely yours. That's always been the goal: educate and elevate.

---

### 🔌 Connect Your Productivity Stack (Notion, Slack, Google Workspace)

Your work lives across multiple tools. Now Dex can reach into them, so your meeting prep, person pages, and daily planning pull from everywhere — not just your vault.

1. **Notion** (`/integrate-notion`) — Search your workspace, pull relevant docs into meeting prep, link shared content to person pages. 2 min setup.

2. **Slack** (`/integrate-slack`) — Ask "What did Sarah say about the Q1 budget?" and get an answer. Meeting prep includes recent Slack context with attendees. Person pages show communication history. 3 min setup.

3. **Google Workspace** (`/integrate-google`) — Gmail threads surface in person pages. Email context with meeting attendees during prep. 5 min setup.

**Where you'll notice it:**
- `/meeting-prep` pulls from all enabled integrations automatically
- Person pages gain an Integration Context section
- If you already have these MCPs configured, Dex detects them and offers to keep, upgrade, or skip

Each integration has a guided setup command that walks you through it step by step.

---

### 🤖 AI Model Flexibility: Work Cheaper or Work Offline

Until now, Dex needed Claude and an internet connection. That's no longer the case.

1. **Budget Cloud Mode** — Use models like Kimi K2.5 or DeepSeek for routine tasks. Save 80-97% on API costs. Quality is solid for daily planning, summaries, and task management.

2. **Offline Mode** — Download an open-source AI model to your machine. Works on planes, trains, cafés with terrible wifi. Completely free, runs locally.

3. **Smart Routing** — Let Dex pick the right model automatically. Claude for complex work, budget models for everyday tasks, local model when you're offline.

**New commands:**
- `/ai-setup` — Guided setup that handles the technical bits for you
- `/ai-status` — Check what's configured and how much credit you have left

---

### 📊 Help Improve Dex (Optional Analytics)

I'd genuinely appreciate your help making Dex better. This release adds optional, privacy-first analytics — it tells me which features you use, not what you do with them.

**What gets shared (if you opt in):**
- Which built-in features you use (e.g., "ran /daily-plan")
- That's it. No content, no names, no notes, no conversations. Ever.

**What's never shared:**
- Custom skills or MCPs you create
- Anything you write or manage
- Who you meet with or what you discuss

Dex will ask you once — during onboarding or your next planning session:

> "Help improve Dex? [Yes, happy to help] / [No thanks]"

Say yes and you help me see what's working. Say no and nothing changes. Either way, thank you for using Dex.

---

### ⚡ Calendar Queries: 30x Faster

Calendar queries used to take 30 seconds. Now they take under a second.

**What was wrong:** The old approach loaded your entire calendar history into memory, then filtered. For a busy work calendar, that meant thousands of events churning through every time you asked "what's on today?" — plus ghost events from weeks ago leaking into results.

**What's fixed:** Dex now uses Apple's native EventKit framework, which queries the calendar database directly. Only the events you asked for come back, instantly.

**One-time setup:** Run `/calendar-setup` after updating to grant the permission. Skip it and calendar still works (just slower, using the old method).

---

### 🎯 Smart Pillar Inference for Tasks

Creating a task used to mean a back-and-forth: you'd say "Remind me to prep for the Acme demo" and Dex would ask which pillar it belongs to. Now Dex figures it out:

- "Prep demo for Acme Corp" → **Deal Support**
- "Write blog post about AI" → **Thought Leadership**
- "Review beta feedback" → **Product Feedback**

It confirms with a quick one-liner and you move on. If it guesses wrong, just tell it — easy override.

**Customisation:** Edit `System/pillars.yaml` to add your own keywords for better inference, or adjust the behaviour in your CLAUDE.md.

---

### 🐛 Bug Fix: Hardcoded Paths

Several scripts contained paths hardcoded to my machine. Your core workflows (`/daily-plan`, `/review`, task management, meeting processing) were unaffected, but `/dex-obsidian-setup` and background automation scripts wouldn't work on other setups.

**Fixed:** All paths now resolve dynamically. Internal development scripts that shouldn't have been distributed have been removed.

Thank you to the community members who reported these. Your feedback makes Dex better for everyone.

---

## [1.2.0] - 2026-02-03

### 🧠 Planning Intelligence: Your System Now Thinks Ahead

**What's this about?**

Until now, daily and weekly planning showed you information — your tasks, calendar, priorities. But you had to connect the dots yourself. 

Now Dex actively thinks ahead and surfaces things you might have missed.

This is the biggest upgrade to Dex's intelligence since launch. Based on feedback from early users, we've rebuilt the planning skills to be proactive rather than passive. Dex now does the mental work of connecting your calendar to your tasks, tracking your commitments, and warning you when things are slipping — so you can focus on actually doing the work.

---

**Midweek Awareness**

**Before:** You'd set weekly priorities on Monday, then forget about them until Friday's review. By then it's too late — Priority 3 never got touched.

**Now:** When you run `/daily-plan` midweek, Dex knows where you stand:

> "It's Wednesday. You've completed 1 of 3 weekly priorities. Priority 2 is in progress (2 of 5 tasks done). Priority 3 hasn't been touched yet — you have 2 days left."

**Result:** Course-correct while there's still time. No more end-of-week surprises.

---

**Meeting Intelligence**

**Before:** You'd see "Acme call" on your calendar and have to manually check: what's the status of that project? Any outstanding tasks? What did we discuss last time?

**Now:** For each meeting, Dex automatically connects the dots:

> "You have the Acme call Thursday. Looking at that project: the proposal is still in draft, and you owe Sarah the pricing section. Want to block time for prep?"

**Result:** Walk into every meeting prepared. Related tasks and project status surface automatically.

---

**Commitment Tracking**

**Before:** You'd say "I'll get back to you Wednesday" in a meeting, write it in your notes... and forget. It lived in a meeting note you never looked at again.

**Now:** Dex scans your meeting notes for things you said you'd do:

> "You told Mike you'd get back to him by Wednesday. That's today."

**Result:** Keep your promises. Nothing slips through because it was buried in notes.

---

**Smart Scheduling**

**Before:** All tasks were equal. A 3-hour strategy doc and a 5-minute email sat on the same list with no guidance on when to tackle them.

**Now:** Dex classifies tasks by effort and matches them to your calendar:

> "You have a 3-hour block Wednesday morning — perfect for 'Write Q1 strategy doc' (deep work). Thursday is stacked with meetings — good for quick tasks only."

It even warns you when you have more deep work than available focus time.

**Result:** Stop fighting your calendar. Know which tasks fit which days.

---

**Intelligent Priority Suggestions**

**Before:** `/week-plan` asked "What are your priorities?" and waited. You had to figure it out yourself.

**Now:** Dex suggests priorities based on your goals, task backlog, and calendar shape:

> "Based on your goals, tasks, and calendar, I suggest:
> 1. Complete pricing proposal — Goal 1 needs this for milestone 3
> 2. Customer interviews — Goal 2 hasn't had activity in 3 weeks
> 3. Follow up on Acme — You committed to Sarah by Friday"

You still decide. But now you have a thinking partner who's done the analysis.

**Result:** Start each week with intelligent suggestions, not a blank page.

---

**Concrete Progress (Not Fake Percentages)**

**Before:** "Goal X is at 55%." What does that even mean? Percentages feel precise but communicate nothing.

**Now:** "Goal X: 3 of 5 milestones complete. This week you finished the pricing page and scheduled the customer interviews."

**Result:** Weekly reviews that actually show what you accomplished and what's left.

---

**How it works (under the hood):**

Six new capabilities power the intelligence:

| What Dex can now do | Why it matters |
|---------------------|----------------|
| Check your week's progress | Knows which priorities are on track vs slipping |
| Understand meeting context | Connects each meeting to related projects and people |
| Find your commitments | Scans notes for promises you made and when they're due |
| Judge task effort | Knows a strategy doc needs focus time, an email doesn't |
| Read your calendar shape | Sees which days have deep work time vs meeting chaos |
| Match tasks to time | Suggests what to work on based on available blocks |

**What to try:**

- Run `/daily-plan` on a Wednesday — see midweek awareness in action
- Check `/week-plan` — get intelligent priority suggestions instead of a blank page
- Before a big meeting, run `/meeting-prep` — watch it pull together everything relevant

---

## [1.1.0] - 2026-02-03

### 🎉 Personalize Dex Without Losing Your Changes

**What's this about?**

Many of you have been making Dex your own — adding personal instructions, connecting your own tools like Gmail or Notion, tweaking how things work. That's exactly what Dex is designed for.

But until now, there was a tension: when I release updates to Dex with new features and improvements, your personal changes could get overwritten. Some people avoided updating to protect their setup. Others updated and had to redo their customizations.

This release fixes that. Your personalizations and my updates now work together.

---

**What stays protected:**

**Your personal instructions**

If you've added notes to yourself in the CLAUDE.md file — reminders about how you like things done, specific workflows, preferences — those are now protected. Put them between the clearly marked `USER_EXTENSIONS` section, and they'll never be touched by updates.

**Your connected tools**

If you've connected Dex to other apps (like your email, calendar, or note-taking tools), those connections are now protected too. When you add a tool, Dex automatically names it in a way that keeps it safe from updates.

**New command: `/dex-add-mcp`** — When you want to connect a new tool, just run this command. It handles the technical bits and makes sure your connection is protected. No config files to edit.

---

**What happens when there's a conflict?**

Sometimes my updates will change a file that you've also changed. When that happens, Dex now guides you through it with simple choices:

- **"Keep my version"** — Your changes stay, skip this part of the update
- **"Use the new version"** — Take the update, replace your changes
- **"Keep both"** — Dex will keep both versions so nothing is lost

No technical knowledge needed. Dex explains what changed and why, then you decide.

---

**Why this matters**

I want you to make Dex truly yours. And I want to keep improving it with new features you'll find useful. Now both can happen. Update whenever you like, knowing your personal setup is safe.

---

### 🔄 Background Meeting Sync (Granola Users)

**Before:** To get your Granola meetings into Dex, you had to manually run `/process-meetings`. Each time, you'd wait for it to process, then continue your work. Easy to forget, tedious when you remembered.

**Now:** A background job syncs your meetings from Granola every 30 minutes automatically. One-time setup, then it just runs.

**To enable:** Run `.scripts/meeting-intel/install-automation.sh`

**Result:** Your meeting notes are always current. When you run `/daily-plan` or look up a person, their recent meetings are already there — no manual step needed.

---

### ✨ Prompt Improvement Works Everywhere

**Before:** The `/prompt-improver` command required extra configuration. In some setups, it just didn't work.

**Now:** It automatically uses whatever AI is available — no special configuration needed.

**Result:** Prompt improvement just works, regardless of your setup.

---

### 🚀 Easier First-Time Setup

**Before:** New users sometimes hit confusing error messages during setup, with no clear guidance on what to do next.

**Now:**
- Clear error messages explain exactly what's wrong and how to fix it
- Requirements are checked upfront with step-by-step instructions
- Fewer manual steps to get everything working

**Result:** New users get up and running faster with less frustration.

---

## [1.0.0] - 2026-01-25

### 📦 Initial Release

Dex is your AI-powered personal knowledge system. It helps you organize your professional life — meetings, projects, people, ideas, and tasks — with an AI assistant that learns how you work.

**Core features:**
- **Daily planning** (`/daily-plan`) — Start each day with clear priorities
- **Meeting capture** — Extract action items, update person pages automatically
- **Task management** — Track what matters with smart prioritization
- **Person pages** — Remember context about everyone you work with
- **Project tracking** — Keep initiatives moving forward
- **Weekly and quarterly reviews** — Reflect and improve systematically

**Requires:** Cursor IDE with Claude, Python 3.10+, Node.js
