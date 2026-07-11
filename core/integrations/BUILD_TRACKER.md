# Productivity Integrations Build Tracker

**Orchestrator:** Sub-agent coordination via TODOs
**Status:** [green] Building in Parallel
**Started:** 2026-02-04

---

## Build Progress

### Notion Integration
- [ ] Test `@notionhq/notion-mcp-server` package
- [x] Create `/integrate-notion` skill [x]
- [x] Create detection helper (check existing config) [x]
- [x] Create setup helper (guided flow) [x]
- [x] Hook into `/meeting-prep` [x]
- [x] Hook into person pages (template updated) [x]
- [x] Add to onboarding flow [x]

### Slack Integration
- [ ] Test `@kazuph/mcp-slack` package
- [x] Create `/integrate-slack` skill [x]
- [x] Create detection helper (check existing config) [x]
- [x] Create setup helper (guided flow) [x]
- [x] Hook into `/meeting-prep` [x]
- [x] Hook into person pages (template updated) [x]
- [x] Add to onboarding flow [x]

### Google Integration
- [ ] Test `mcp-google` package
- [x] Create `/integrate-google` skill [x]
- [x] Create detection helper (check existing config) [x]
- [x] Create setup helper (OAuth walkthrough) [x]
- [x] Hook into `/meeting-prep` [x]
- [x] Hook into person pages (template updated) [x]
- [x] Add to onboarding flow [x]

### Onboarding Integration
- [x] Add "What tools do you use?" step to onboarding [x]
- [x] Create integration orchestrator [x]
- [ ] Update onboarding MCP validation

### Update Flow (Existing Users)
- [x] Add integration detection to `/dex-update` [x]
- [x] Create comparison view for existing configs [x]
- [x] Allow keep/replace/skip choice [x]

---

## Architecture

```
User Flow:
+-------------------------------------------------------------+
| Onboarding Step: "What productivity tools do you use?"      |
| [ ] Notion  [ ] Slack  [ ] Google Workspace  [ ] None/Later |
+-------------------------------------------------------------+
                           |
         +-----------------+-----------------+
         v                 v                 v
    /integrate-notion  /integrate-slack  /integrate-google
         |                 |                 |
         +-----------------+-----------------+
                           v
              System/integrations/config.yaml
              (tracks which integrations are active)
```

```
Existing User Flow (/dex-update):
+-------------------------------------------------------------+
| "We've added productivity integrations!"                     |
|                                                              |
| Detected in your config:                                    |
| [x] notion-mcp-server (v1.2.0)                               |
|                                                              |
| Dex recommends: @notionhq/notion-mcp-server (v2.1.0)       |
| Benefits: Official, better maintained, more features        |
|                                                              |
| [Keep existing] [Try Dex version] [Skip for now]           |
+-------------------------------------------------------------+
```

---

## File Locations

| Component | Location |
|-----------|----------|
| Integration modules | `core/integrations/{notion,slack,google}/` |
| Skills | `.claude/skills/integrations/` |
| User config | `System/integrations/config.yaml` |
| Detection helper | `core/integrations/detect.py` |
| Onboarding step | `.claude/flows/onboarding.md` (new step) |
