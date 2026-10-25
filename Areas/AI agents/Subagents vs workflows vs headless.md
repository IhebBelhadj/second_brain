---
type: compare
created: 2026-10-25
topic: AI agents
confidence: 1
tags: [ai-agents, claude-code, compare]
aliases: [Subagents vs workflows, Workflow vs claude -p]
---
# Subagents vs workflows vs headless

> [!abstract] The short answer
> All three give each phase of a [[Multi-agent pipeline]] a clean context. The difference is **who controls the loop** and **whether a session must be open**: subagents (the model drives, easiest), a workflow script (my code drives, inside a session, with resume and a live view), or `claude -p` in bash (my code drives, no session, can run from cron). Workflow at the computer, `claude -p` overnight.

## Side by side

| | [[Subagents]] | [[Workflow scripts\|Workflow]] | [[Headless Claude Code\|claude -p script]] |
|---|---|---|---|
| Who controls the loop | the model | your script | your script |
| Clean context per phase | yes | yes | yes, a new process each time |
| Main context grows? | slowly (each summary) | no (only the `return`) | no session at all |
| Watch it live | yes | `/workflows` | logs only |
| Resume after a crash | no | yes, built in | you add it (git commits per phase) |
| Runs unattended / from cron | no | needs a session | yes |
| Permissions | asks me as usual | asks me as usual | must be listed up front (`--allowedTools`), otherwise denied silently |
| Setup | two agent files + a sentence | a JavaScript file | a bash script |

## What they share
- A fresh agent per dev and test step
- The same `PLAN.md` / `HANDOFF.md` format: the plan in, the handoff between phases
- Opus for dev, Sonnet for testing, a capped fix loop

## Where they actually differ
- **Control**: with subagents the loop is a request to the model, which can skip or improvise. The other two make it code
- **Presence**: subagents and workflows need an open session; `claude -p` doesn't
- **Recovery**: a workflow reuses finished steps after a crash; a bash script only has its commits to restart from

## If you have to choose
- Trying it once, want to watch every step, nothing to learn → **subagents**
- At my computer, want a fixed loop, progress view and resume → **workflow**
- Overnight or from cron, nobody watching → **`claude -p` script**

Recommendation: the **workflow** while at the computer and the **`claude -p` script** for overnight or cron runs, with the same `PLAN.md` / `HANDOFF.md` format for both so a plan works in either.

## Related
- Compares:: [[Subagents]], [[Workflow scripts]], [[Headless Claude Code]]
- Idea behind them:: [[Multi-agent pipeline]]
- Area:: [[AI agents]]

## Flashcards
#flashcards

Which of subagents / workflow / claude -p lets the model control the loop? :: Subagents
Which option has built-in resume after a crash? :: The workflow script
Which option can run from cron with no session? :: The claude -p bash script
How does the claude -p script get resume? :: You add it yourself, via a git commit per passing phase
Recommended setup at the computer vs overnight? :: Workflow at the computer, claude -p script overnight or from cron
What stays the same across all three? :: Fresh agent per step, PLAN.md/HANDOFF.md, Opus dev + Sonnet test, capped fixes
