# Area guide: AI agents

**Index:** `AI agents.md` is the learning path (numbered sections, each assumes the ones above) with a one-line summary of every note and the planned notes as italic links. Read it for *what* a note covers; use this file for *where* it is.

**Scope:** working with AI coding agents as a systems engineer: context windows, splitting work across agents, and automating agent runs. Examples use **Claude Code** (the tool in use), but each note starts from the general problem (context, control of the loop, permissions).

## Folder map

```
AI agents/
├── AI agents.md                          topic index (the learning path)
├── Multi-agent pipeline.md               why a fresh agent per phase, PLAN.md/HANDOFF.md, dev/test split, fix loop, tips
├── Subagents.md                          agent definition files (.claude/agents/), model per role, model-driven loop
├── Workflow scripts.md                   script-driven loop: agent(), schema, phase(), args, resume, determinism rules
├── Headless Claude Code.md               claude -p in bash, --allowedTools, JSON schema output + jq, commits, cron
└── Subagents vs workflows vs headless.md who controls the loop, live view, resume, unattended: which to use
```

## Where a new note goes

| It's about… | Folder |
|---|---|
| Anything in this area (no subfolders yet) | Area root |

The planned notes (roadmap) are the italic `*[[…]]*` links in `AI agents.md`: when writing one, use that exact name so existing links resolve.
