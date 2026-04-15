# FTEs-Personal-AI-Employee

## Project Overview

This repository documents and guides the construction of a **Personal AI Employee** (also called a Digital FTE - Full-Time Equivalent). It is a local-first, agent-driven automation system powered by **Claude Code** as the reasoning engine and **Obsidian** as the local Markdown dashboard and memory store.

The system is designed to proactively manage personal and business affairs 24/7 by combining:

* **Claude Code** – the "Brain" that reasons, plans, and executes multi-step tasks.
* **Obsidian Vault** – the "Memory / GUI" that stores all state, tasks, and reports as local Markdown.
* **Watcher Scripts** – lightweight Python scripts that monitor Gmail, WhatsApp, filesystems, etc., and create actionable `.md` files in an `Inbox` / `Needs_Action` folder.
* **MCP (Model Context Protocol) Servers** – the "Hands" that interact with external systems (email, browsers, calendars, social media, payment portals, Odoo ERP, etc.).
* **Ralph Wiggum Loop** – a Claude Code Stop-hook pattern that keeps the agent iterating until a task is marked complete.

This is primarily an **educational / hackathon project** originating from the Panaversity community. It provides architectural blueprints, tiered deliverables (Bronze → Platinum), and reference patterns for building autonomous AI agents that communicate via files rather than APIs.

---

## Directory Structure

```
FTEs-Personal-AI-Employee/
├── .gitattributes
├── skills-lock.json
├── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md
├── QWEN.md                          # This file
├── .qwen/
│   └── skills/
│       └── browsing-with-playwright/
│           ├── SKILL.md
│           ├── references/
│           │   └── playwright-tools.md
│           └── scripts/
│               ├── mcp-client.py
│               ├── start-server.sh
│               ├── stop-server.sh
│               └── verify.py
└── (git-ignored files, e.g., .git/)
```

---

## Key Files

| File | Description |
|------|-------------|
| `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md` | The master blueprint. Contains architecture, watcher patterns, MCP configuration, Ralph Wiggum loop, tiered deliverables, CEO briefing templates, and deployment guidance. |
| `skills-lock.json` | Tracks installed Claude Code Agent Skills (currently includes `browsing-with-playwright` from `bilalmk/todo_correct`). |
| `.qwen/skills/browsing-with-playwright/` | An installed skill enabling browser automation via Playwright. Includes SKILL.md, reference docs, and helper scripts for MCP server lifecycle. |
| `.gitattributes` | Normalizes line endings (`* text=auto`). |

---

## Architecture Summary

The system follows a **Perception → Reasoning → Action** loop:

1. **Perception (Watchers):** Python sentinel scripts continuously monitor email (Gmail API), WhatsApp (Playwright web automation), filesystems (watchdog), etc. New items are saved as `.md` files in `/Needs_Action`.
2. **Reasoning (Claude Code):** Claude reads the action files, consults `Business_Goals.md` and `Company_Handbook.md`, creates `Plan.md` files with checkboxes, and decides what to do.
3. **Action (MCP Servers):** Claude invokes MCP servers to send emails, navigate browsers, schedule calendar events, post to social media, draft payments in Odoo, etc.
4. **Human-in-the-Loop (HITL):** For sensitive actions (payments, sends), Claude writes an approval request to `/Pending_Approval`. The user moves it to `/Approved` to authorize execution.
5. **Persistence (Ralph Wiggum Loop):** A Stop hook prevents Claude from exiting until the task file appears in `/Done`, enabling autonomous multi-step completion.

### Cross-Domain / Cloud-Native (Platinum Tier)

* **Cloud VM** runs watchers + orchestrator 24/7 (draft-only actions).
* **Local machine** owns approvals, WhatsApp sessions, banking, and final send/post.
* **Synced Vault** via Git or Syncthing communicates through `/Needs_Action/<domain>/`, `/In_Progress/<agent>/`, `/Pending_Approval/<domain>/`, and `/Updates/`.
* **Claim-by-move rule** prevents double-work; secrets (`.env`, tokens, sessions) never sync.

---

## Building and Running

This project does not contain traditional application source code. Instead, it is a **blueprint / vault repository** that you set up on your local machine. Below are the typical setup and run commands:

### Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.13+ |
| Node.js | v24+ LTS |
| Claude Code | Active subscription (or free Gemini API via router) |
| Obsidian | v1.10.6+ |
| GitHub Desktop | Latest |

### Initial Setup

```bash
# 1. Clone or open this repo
cd FTEs-Personal-AI-Employee

# 2. Create an Obsidian vault pointed at this directory (or a subfolder)

# 3. Set up Python venv (if building watcher scripts)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt  # Create this as you add dependencies

# 4. Configure MCP servers in Claude Code (~/.config/claude-code/mcp.json)
# See the main hackathon doc for examples.
```

### Running Watchers

```bash
# Example: run a Gmail watcher
python watchers/gmail_watcher.py

# Example: run a WhatsApp watcher (uses Playwright)
python watchers/whatsapp_watcher.py
```

### Starting Claude Code

```bash
# Point Claude Code at your Obsidian vault
claude --vault ./ObsidianVault

# Or use the Ralph Wiggum loop for autonomous tasks
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

### Scheduling (e.g., Monday Morning CEO Briefing)

```bash
# Linux/Mac cron example
0 8 * * 1 claude --prompt "Generate the Monday Morning CEO Briefing from /Vault/Accounting/ and /Vault/Tasks/"

# Windows Task Scheduler: create a weekly task pointing to a .bat or .ps1 script.
```

---

## Development Conventions

* **File-based communication:** All inter-component communication happens via Markdown files with YAML frontmatter. No shared databases or message queues.
* **Single-writer rule:** `Dashboard.md` is only written by the local orchestrator to prevent merge conflicts.
* **Claim-by-move:** Agents claim tasks by moving them into `/In_Progress/<agent>/`. Other agents must ignore files already claimed.
* **Secrets isolation:** `.env`, API keys, browser sessions, and banking credentials are never committed or synced across machines.
* **Human-in-the-loop:** Sensitive actions (payments, posts, emails) must go through `/Pending_Approval/` → `/Approved/` → execute pattern.

---

## Tiered Deliverables (Hackathon)

| Tier | Scope |
|------|-------|
| **Bronze** | Obsidian vault with `Dashboard.md` + `Company_Handbook.md`, one watcher, basic folder structure, Claude reading/writing to vault. |
| **Silver** | Multiple watchers, LinkedIn auto-posting, Claude Plan.md creation, one MCP server, HITL approval, basic scheduling. |
| **Gold** | Full cross-domain integration, Odoo Community accounting via MCP, social media integrations (FB, IG, X), weekly audit + CEO briefing, Ralph Wiggum loop, comprehensive audit logging. |
| **Platinum** | Always-on Cloud VM + Local Executive, work-zone specialization (Cloud drafts, Local approves), synced vault via Git/Syncthing, Odoo on Cloud VM with HTTPS + backups, A2A upgrade (Phase 2). |

---

## Useful Links

* [Claude Code Docs](https://claude.com/product/claude-code)
* [Claude Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
* [Ralph Wiggum Plugin](https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum)
* [MCP-ODoo-Adv](https://github.com/AlanOgic/mcp-odoo-adv)
* [Oracle Cloud Free VMs](https://www.oracle.com/cloud/free/)
* [Panaversity YouTube](https://www.youtube.com/@panaversity)
* Research Meeting (Wednesdays 10:00 PM PKT): [Zoom](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1)

---

## Notes for Qwen

When working in this repository:

* **Do not create or modify actual vault content** (e.g., `Dashboard.md`, `Company_Handbook.md`) unless explicitly requested. These are user-managed files.
* **When generating watcher scripts or MCP configs**, follow the patterns in the main hackathon document.
* **Prefer file-based, Markdown-first designs** consistent with the project's architecture.
* **Respect secrets isolation**: never hardcode credentials; always use environment variables or `.env` files excluded from git.
