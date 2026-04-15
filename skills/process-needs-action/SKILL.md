# Skill: Process Needs Action Files

## Description
Processes all `.md` files in the `/Needs_Action` folder. Reads each file, determines what action is needed, creates a plan, and moves completed tasks to `/Done`.

## When to Use
- When the user asks you to "process pending tasks" or "check the inbox"
- When you detect new `.md` files in the `/Needs_Action` folder
- As part of the Ralph Wiggum loop for autonomous task completion

## Instructions

1. **Scan** the `/Needs_Action` folder for `.md` files.
2. **Read** each file and its frontmatter to understand the task type.
3. **Check** the `Company_Handbook.md` for rules and guidelines.
4. **Create a Plan.md** in `/Plans/` with checkboxes for multi-step tasks.
5. **Execute** the plan steps:
   - For **file drops**: review the content and suggest next steps.
   - For **emails**: draft a reply (do not send without approval).
   - For **payments**: ALWAYS create an approval request in `/Pending_Approval/`.
6. **Update** the `Dashboard.md` with recent activity.
7. **Move** completed task files to `/Done/`.
8. **Log** all actions in `/Logs/YYYY-MM-DD.json`.

## Rules
- **NEVER** send emails, payments, or external actions without approval.
- **ALWAYS** check `Company_Handbook.md` before making decisions.
- **ALWAYS** log every action you take.
- If unsure, create an approval request in `/Pending_Approval/`.

## Plan.md Template
```markdown
---
created: 2026-04-15T10:30:00Z
status: in_progress
source_file: FILENAME.md
---

# Plan: Brief Description

## Steps
- [x] Step 1 (completed)
- [ ] Step 2
- [ ] Step 3

## Approval Required
- [ ] Action description → `/Pending_Approval/ACTION_name.md`
```

## Completion Signal
When all tasks are processed, output:
```
<promise>TASK_COMPLETE</promise>
```
