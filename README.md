# FTEs-Personal-AI-Employee — Bronze Tier

> **Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

This repository implements the **Bronze Tier** of the Personal AI Employee Hackathon — a foundation for building an autonomous AI agent powered by Qwen Code and Obsidian.

---

## What is Bronze Tier?

Bronze Tier is the **Minimum Viable Deliverable** — a working foundation with:

- ✅ Obsidian vault with `Dashboard.md` and `Company_Handbook.md`
- ✅ One working Watcher script (filesystem monitoring)
- ✅ Qwen Code reading from and writing to the vault
- ✅ Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`
- ✅ AI functionality implemented as Agent Skills

---

## Directory Structure

```
FTEs-Personal-AI-Employee/
├── Dashboard.md                    # Real-time status dashboard
├── Company_Handbook.md             # Rules of engagement for the AI
├── Business_Goals.md               # Business targets and metrics
├── orchestrator.py                 # Master process that ties everything together
├── requirements.txt                # Python dependencies
├── .env.example                    # Credentials template (copy to .env)
├── .gitignore
│
├── Inbox/                          # Drop files here for processing
├── Needs_Action/                   # Watchers create .md files here
├── Done/                           # Completed tasks moved here
├── Plans/                          # Claude Code creates Plan.md files here
├── Pending_Approval/               # Approval requests for sensitive actions
├── Approved/                       # Move files here to approve actions
├── Rejected/                       # Quarantined/corrupted files
├── Logs/                           # Daily JSON logs (YYYY-MM-DD.json)
├── Accounting/                     # Financial records
├── Briefings/                      # CEO briefings (weekly audit output)
│
├── watchers/
│   ├── base_watcher.py             # Abstract base class for all watchers
│   └── filesystem_watcher.py       # Working watcher — monitors Inbox/
│
└── skills/
    └── process-needs-action/
        └── SKILL.md                # Claude Code skill for processing tasks
```

---

## Setup Instructions

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.13+ | Watcher scripts & orchestrator |
| Qwen Code | Active session | Reasoning engine |
| Obsidian | v1.10.6+ (free) | Vault GUI & knowledge base |

### Step 1: Install Python Dependencies

```bash
cd FTEs-Personal-AI-Employee
pip install -r requirements.txt
```

### Step 2: Set Up Environment (Optional)

```bash
cp .env.example .env
# Edit .env with your credentials when you add Gmail/WhatsApp watchers
```

### Step 3: Open in Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Select the `FTEs-Personal-AI-Employee` directory
4. You should see `Dashboard.md`, `Company_Handbook.md`, and `Business_Goals.md`

### Step 4: Start the Filesystem Watcher

```bash
python watchers/filesystem_watcher.py
```

This monitors the `Inbox/` folder. Drop any file into `Inbox/` and the watcher will:
1. Copy it to `Needs_Action/`
2. Create a `.md` metadata file alongside it

### Step 5: Start the Orchestrator (in a separate terminal)

```bash
python orchestrator.py --dry-run
```

The orchestrator:
- Scans `Needs_Action/` for new files
- Logs all activity to `Logs/`
- Moves completed tasks to `Done/`
- Updates `Dashboard.md`

> **`--dry-run`** mode: Logs actions without modifying files. Remove this flag for production use.

### Step 6: Point Qwen Code at the Vault

Open Qwen Code in this directory and you can ask:
- "Check the Needs_Action folder and process any pending tasks."
- "Update the dashboard with current status."
- "Review the Company Handbook and suggest improvements."

---

## How It Works

### The Perception → Reasoning → Action Loop

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  PERCEPTION  │────▶│  REASONING   │────▶│    ACTION    │
│              │     │              │     │              │
│ Filesystem   │     │  Qwen Code   │     │  Orchestrator│
│ Watcher      │     │  (you run    │     │  + Skills    │
│ monitors     │     │  interactively)     │  (file move, │
│ Inbox/       │     │              │     │  log, plan)  │
└──────────────┘     └──────────────┘     └──────────────┘
```

1. **Perception**: `filesystem_watcher.py` detects new files in `Inbox/` → creates `.md` action files in `Needs_Action/`.
2. **Reasoning**: You run Qwen Code and ask it to process pending tasks. It reads action files, consults `Company_Handbook.md`, and creates plans.
3. **Action**: The orchestrator (or Qwen directly) moves files, updates the dashboard, and logs everything.

---

## Testing the Setup

### Quick Test

```bash
# 1. Start the filesystem watcher (terminal 1)
python watchers/filesystem_watcher.py

# 2. Drop a test file into Inbox (terminal 2)
echo "This is a test document" > Inbox/test_document.txt

# 3. Watch the watcher create action files in Needs_Action/
dir Needs_Action

# 4. Start the orchestrator (terminal 3)
python orchestrator.py --dry-run
```

You should see:
- `Needs_Action/FILE_20260415_..._test_document.txt` (copied file)
- `Needs_Action/FILE_20260415_..._test_document.txt.md` (metadata)
- Logs in `Logs/YYYY-MM-DD.json`

---

## Next Steps (Silver Tier Upgrades)

- [ ] Add Gmail Watcher (Google API integration)
- [ ] Add WhatsApp Watcher (Playwright web automation)
- [ ] Set up MCP servers for external actions (email send, browser automation)
- [ ] Implement Human-in-the-Loop approval workflow
- [ ] Add scheduling via cron or Task Scheduler
- [ ] Create Claude Code reasoning loop that generates Plan.md files

---

## Security Notes

- **NEVER** commit `.env` files or credentials to git.
- **ALWAYS** use `--dry-run` during development.
- **REVIEW** all actions in `Logs/` regularly.
- **ROTATE** credentials monthly or after any suspected breach.

See `Company_Handbook.md` for detailed security rules.

---

## Troubleshooting

### Watcher not starting
```bash
pip install watchdog
python watchers/filesystem_watcher.py --vault .
```

### Orchestrator not finding files
Make sure files have `.md` extension and are in `Needs_Action/`.

### Claude Code not seeing vault files
Run Qwen Code from the repository root directory.

---

## License

This project is part of the Panaversity AI Employee Hackathon.

## Links

- [Hackathon Blueprint (full document)](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Qwen Code](https://qwenlm.github.io/)
- [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Panaversity YouTube](https://www.youtube.com/@panaversity)
