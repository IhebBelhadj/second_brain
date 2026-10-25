---
type: concept
created: 2026-10-25
topic: AI agents
confidence: 1
tags: [ai-agents, claude-code, automation, bash]
aliases: [claude -p, Claude Code print mode, Headless agents]
---
# Headless Claude Code

> [!abstract] In one sentence
> `claude -p "prompt"` runs one agent **non-interactively** as its own process and exits, so a bash script can loop over a plan calling it once per agent: a clean context is guaranteed (new process each time), it uses my logged-in subscription, and it can run unattended from cron, as long as every tool the agents need is allowed up front.

## Build-up

### The problem
[[Subagents]] and [[Workflow scripts]] both need an open Claude Code session: I start them, and they run while the session is there. For an overnight run, or a job cron starts at 2 a.m., there's no session and no one at the keyboard.

### One process per agent
`claude -p` ("print" mode) takes a prompt, runs the agent to the end, prints the result and exits. Each call is a **separate process**, so nothing carries over between calls: the clean context per phase of a [[Multi-agent pipeline]] comes for free. No API (Application Programming Interface) key is needed; it uses the subscription I'm logged in with.

### The script

```bash
#!/usr/bin/env bash
set -euo pipefail
PLAN=PLAN.md
N=$(grep -c '^## Phase' "$PLAN")          # PLAN.md uses "## Phase 1: ..." headings
TOOLS='Read,Edit,Write,Glob,Grep,Bash(npm test:*),Bash(git diff:*)'
SCHEMA='{"type":"object","properties":{"pass":{"type":"boolean"},"failures":{"type":"string"}},"required":["pass","failures"]}'

for i in $(seq 1 "$N"); do
  feedback=""
  for try in 0 1 2; do
    claude -p --model opus --allowedTools "$TOOLS" \
      "Implement Phase $i of $PLAN. Read HANDOFF.md first. ${feedback:+Fix these test failures: $feedback.} \
       When done, rewrite HANDOFF.md for the next phase (state, files, decisions, open issues)."

    out=$(claude -p --model sonnet --allowedTools "$TOOLS" --output-format json --json-schema "$SCHEMA" \
      "Phase $i of $PLAN was just implemented (see HANDOFF.md). Write/extend its tests, run the suite, report.")
    pass=$(jq -r '.structured_output.pass' <<<"$out")
    [[ $pass == true ]] && break
    feedback=$(jq -r '.structured_output.failures' <<<"$out")
  done
  [[ $pass == true ]] || { echo "Phase $i failing, stopping"; exit 1; }
  git add -A && git commit -qm "phase $i: $(grep -m1 "^## Phase $i" "$PLAN")"
done
```

### Walking through it
1. **`set -euo pipefail`**: stop on any failed command, unset variable or failed pipe stage, instead of carrying on with half a result
2. **Count the phases** with `grep -c '^## Phase'`: the plan must use `## Phase 1: …` headings, since bash can't "understand" the plan the way an agent can
3. **`TOOLS`**: the exact tools allowed. `Bash(npm test:*)` allows only commands starting with `npm test`, not any shell command
4. **`SCHEMA`**: the JSON (JavaScript Object Notation) shape the tester must answer with, `{pass, failures}`
5. **Per phase, up to 3 tries** (`try in 0 1 2` = the first attempt + 2 fixes):
   - dev with `--model opus`. `${feedback:+…}` adds "Fix these test failures: …" **only** when `feedback` is non-empty
   - tester with `--model sonnet --output-format json --json-schema "$SCHEMA"`: the output is JSON with the structured answer under `.structured_output`
   - `jq -r '.structured_output.pass'` pulls out `true`/`false`; on `true`, `break`; otherwise the failures become the next dev's `feedback`
6. **Still failing after the tries** → print and `exit 1` (cron mail or a log will show it)
7. **Passing** → `git commit` with the phase heading as the message: a checkpoint per phase, which is also how this script "resumes": rerun from the last committed phase

## Permissions matter here

In `-p` mode, **any tool I haven't allowed is denied silently**: the agent can't ask me, because nobody is there. An agent that needs `npm test` without `Bash(npm test:*)` in the list just can't run the tests, and may report something misleading instead of failing loudly.

So `--allowedTools` should list **exactly** what each agent needs (my test command, `git diff`), no more. Avoid `--dangerously-skip-permissions` (which allows everything) unless the script runs inside a container or VM (virtual machine) that it can't damage.

## Easy to get wrong
- An unlisted tool is denied **without any prompt or error to me**
- The plan's headings must match the `grep` pattern, or `N` is 0 and nothing runs
- The structured answer is under `.structured_output`, not at the top of the JSON
- `--dangerously-skip-permissions` only inside a container or VM
- There's no live view: only logs and the commits

## Related
- Used for:: [[Multi-agent pipeline]]
- Differs from:: [[Workflow scripts]] (needs a session, has resume and a live view), [[Subagents]]
- Compared in:: [[Subagents vs workflows vs headless]]
- Area:: [[AI agents]]

## Flashcards
#flashcards

What does claude -p do? :: Runs one agent non-interactively with the given prompt, prints the result and exits
Why does claude -p guarantee a clean context per phase? :: Each call is a separate process
Does a claude -p script need an API key? :: No, it uses the logged-in subscription
What happens to a tool not in --allowedTools in -p mode? :: It's denied silently, the agent can't ask
What does Bash(npm test:*) in --allowedTools allow? :: Only shell commands starting with npm test
How do you get a structured verdict from claude -p? :: --output-format json --json-schema '<schema>', then read .structured_output with jq
When is --dangerously-skip-permissions acceptable? :: Only inside a container or VM
How does the bash script get checkpoints and a way to resume? :: A git commit after every passing phase
What does ${feedback:+text} do in bash? :: Expands to text only if feedback is set and non-empty
