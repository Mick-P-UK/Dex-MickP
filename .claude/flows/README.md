# Flows: The Setup Experience That Doesn't Suck

**Purpose:** Guided wizards that configure complex features through conversation, not documentation. You answer questions, Dex builds your system.

**Why flows exist:** Setting up systems is cognitively expensive. "Here's 47 configuration options, good luck" doesn't work. Flows turn setup into conversation.

---

## What Are Flows?

**Flows** are interactive wizards that adapt to your answers and configure your system automatically. Think of it like having an expert guide you through setup rather than reading 20 pages of docs and hoping you didn't miss something.

**The Dex philosophy:** No forced learning. Progressive disclosure. Start shallow, go deep as you get curious. Flows embody this - they ask the minimum required questions and handle the complexity automatically.

### How Flows Work

**Example: Onboarding a New User**

```
1. Welcome message
2. Q: "What's your role?"
   -> User selects "Product Manager"
3. Q: "Company size?"
   -> User selects "50-200"
4. Q: "Enable quarterly planning?"
   -> User selects "Yes"
5. [Flow creates PM-specific folders]
6. [Flow generates strategic pillars]
7. [Flow sets up templates]
8. "Setup complete! Run /daily-plan to start."
```

### Key Characteristics

**Sequential:** Each step builds on the previous one
**Interactive:** Pauses for user input at decision points
**Branching:** Different paths based on user choices
**One-time:** Typically for setup or configuration (not daily use)

### Flows vs Skills vs Agents

| Aspect | Flows | Skills | Agents |
|--------|-------|--------|--------|
| **Interaction** | Multi-step wizard with branching | Single invocation | Autonomous (no user input) |
| **Frequency** | One-time or rare | Repeatable daily/weekly | As needed |
| **Purpose** | Setup and configuration | Execute workflows | Background analysis |
| **Example** | Onboarding wizard | `/daily-plan` | `project-health` scan |
| **User input** | Multiple questions throughout | Optional at start | None during execution |

### When to Use Each

**Use a Flow when:**
- [x] Setting up system for the first time
- [x] Configuring a complex feature with multiple options
- [x] Guiding unfamiliar users through a process
- [x] Decisions affect what happens next (branching)

**Use a Skill when:**
- [x] Repeatable daily/weekly command
- [x] Linear workflow without complex branching
- [x] User explicitly invokes with `/command`

**Use an Agent when:**
- [x] Autonomous background work
- [x] No user interaction needed
- [x] Multi-step analysis returning a summary

---

## What Goes Here

Flow definition files (`.md` format) that:
- Guide users through multi-step processes
- Require user decisions at key points
- Create or configure system components
- Onboard new users or features

## When to Use

Create a flow when:
- **Sequential steps** - Process has a clear progression with dependencies
- **User input required** - Decisions or information needed at each step
- **One-time setup** - Configuring system components or integrations
- **Teaching moment** - Explaining concepts while building

Don't use flows for:
- Autonomous tasks (use agents instead)
- Simple single-step operations (use skills)
- Routine daily operations (use skills)

## Structure

Flows typically include:
- Clear step-by-step instructions
- Decision points and branching logic
- Validation of prerequisites
- File creation or configuration
- Confirmation of success

## Examples in Dex

- **onboarding.md** - First-time setup that adapts to 31 roles
  - PM? Gets sprint planning, user story templates, roadmap structure
  - CFO? Gets financial planning, board prep, metrics dashboards
  - One conversation, fully configured system

Future flows might include:
- Career ladder setup (map your progression path)
- Integration wizards (Slack, Notion, CRM connections)
- Team rollout (configure Dex for your entire team with shared conventions)

## Related

- **Skills** (`.claude/skills/`) - Simple user commands
- **Agents** - Autonomous multi-step tasks (invoked via Task tool)
