---
type: concept
created: 2026-10-25
topic: AI agents
confidence: 1
tags: [ai-agents, claude-code, automation]
aliases: [Claude Code workflows, Workflow script, implement-plan workflow]
---
# Workflow scripts

> [!abstract] In one sentence
> A **workflow** is a small JavaScript file, run inside Claude Code, in which **my code decides the order of steps**, not the model: each `agent()` call starts a fresh agent, a schema turns its answer into data the script can branch on, and only what the script `return`s reaches my main session.

## Build-up

### The problem
With [[Subagents]], the loop of a [[Multi-agent pipeline]] lives in a prompt: "dev, then tester, retry at most twice". The model follows it most of the time, but it can skip a step or decide the failures "don't matter", and every summary still piles up in the main context. I want the loop to be **code**: a `for` over the phases and a retry counter that can't be argued with.

### The pieces a script uses

| Piece | What it does | Why it's needed |
|---|---|---|
| `export const meta = {…}` | Name, one-line description, the phases shown in progress | Identifies the workflow; must be a plain literal |
| `args` | The input passed when the workflow is run (`args.plan`) | Same script, different plan files |
| `agent(prompt, opts)` | Starts a **fresh** agent and waits for its result | Each call is a clean context |
| `opts.model`, `opts.effort` | Which model, how hard it thinks | Opus for dev, Sonnet + low effort for simple parsing |
| `opts.schema` | A JSON (JavaScript Object Notation) schema the answer must match | The result is an object (`{pass, failures}`), not prose the script would have to guess at |
| `opts.label` | Name shown for that agent in the progress view | Tell `dev 2 (fix 1)` from `test 2` |
| `phase(title)` | Starts a progress group | One group per plan phase |
| `log(text)` | A line in the progress view | Say why the run stopped |
| `return` | The workflow's result | **The only thing my main session sees** |

### The script

Saved as `.claude/workflows/implement-plan.js`:

```js
export const meta = {
  name: 'implement-plan',
  description: 'Implement a plan phase by phase: Opus builds, Sonnet tests, HANDOFF.md between phases',
  phases: [{ title: 'Read plan' }],
}

const PLAN = args?.plan ?? 'PLAN.md'
const HANDOFF = args?.handoff ?? 'HANDOFF.md'
const MAX_FIXES = 2

const PHASES = { type: 'object', required: ['phases'], properties: {
  phases: { type: 'array', items: { type: 'object', required: ['title', 'task'],
    properties: { title: { type: 'string' }, task: { type: 'string' } } } } } }
const TEST = { type: 'object', required: ['pass', 'failures'], properties: {
  pass: { type: 'boolean' }, failures: { type: 'string' } } }

phase('Read plan')
const { phases } = await agent(
  `Read ${PLAN}. Return its phases in order: a title and the full text of each.`,
  { model: 'sonnet', effort: 'low', schema: PHASES })

const report = []
for (const [i, p] of phases.entries()) {
  phase(`${i + 1}. ${p.title}`)                 // one progress group per plan phase
  let feedback = '', result = null
  for (let attempt = 0; attempt <= MAX_FIXES; attempt++) {
    // fresh Opus agent every time: its only memory is the plan + HANDOFF.md
    await agent(
      `Implement phase ${i + 1} of ${PLAN}: ${p.title}\n\n${p.task}\n\n` +
      `Read ${HANDOFF} first if it exists. ` +
      (feedback ? `The tester reported these failures; fix them:\n${feedback}\n\n` : '') +
      `When done, rewrite ${HANDOFF} for the next agent: current state, files touched, ` +
      `decisions and why, open issues. Under 300 lines.`,
      { model: 'opus', label: `dev ${i + 1}${attempt ? ` (fix ${attempt})` : ''}` })
    // fresh Sonnet agent, structured verdict so the script can branch on it
    result = await agent(
      `Phase ${i + 1} of ${PLAN} (${p.title}) was just implemented; ${HANDOFF} describes it. ` +
      `Write or extend its tests, run the whole suite, report. Do not change non-test code.`,
      { model: 'sonnet', label: `test ${i + 1}`, schema: TEST })
    if (result?.pass) break
    feedback = result?.failures ?? 'the tester crashed'
  }
  report.push({ phase: p.title, pass: !!result?.pass, failures: result?.pass ? '' : feedback })
  if (!result?.pass) { log(`Phase ${i + 1} still failing after ${MAX_FIXES} fixes, stopping`); break }
}
return report   // the only thing your main session sees
```

### Walking through it
1. **Read the plan** with a cheap agent (Sonnet, low effort). The `PHASES` schema forces the answer into `{phases: [{title, task}]}`, so the script gets a real array to loop over instead of parsing text
2. **For each phase**, open a progress group, then up to `1 + MAX_FIXES` = 3 attempts:
   - a **fresh Opus** dev agent, told the phase, told to read `HANDOFF.md`, and (from the second attempt) given the tester's failures
   - a **fresh Sonnet** tester, whose answer must match `TEST` = `{pass: boolean, failures: string}`
   - `result.pass` true → stop retrying; otherwise the failures become the next dev's `feedback`. `?? 'the tester crashed'` covers a tester that returned nothing
3. **Record** each phase in `report`; if a phase still fails after 2 fixes, `log` why and stop the whole run
4. **Return** `report`: a short list like `[{phase, pass, failures}]`. That's all my session's context receives, however much work the agents did

The loop logic (`for`, `attempt <= MAX_FIXES`, `break`) is plain JavaScript: the model can't skip it.

### Running it
In a session: *"run the implement-plan workflow with plan PLAN.md"*. Type `/workflows` to watch progress live (the phases and labels from the script show up there). Workflows only run when I ask for one explicitly, since they can start many agents.

## Things to know

- **The script can't read or write files itself; only the agents can.** It's an orchestrator, not a program with disk access. That's why the **agents** write `HANDOFF.md`, and why the plan is read by an agent rather than by the script
- **`Date.now()` and `Math.random()` aren't allowed.** They would break **resume**: if a run dies at phase 3, rerunning it reuses the cached results of the `agent()` calls that already finished (phases 1–2) instead of redoing them. A cached result is matched by its prompt and options, so the script must produce the **same** calls on a rerun; a timestamp or random number in a prompt would make every call look new. Resume is done from the same Claude Code session, using the failed run's ID
- **The fix loop is capped** at 2 retries per phase, so a failing phase can't burn through the usage limits
- **`meta` is a pure literal**: no variables or function calls inside it

## Easy to get wrong
- Only the `return` value reaches the main session, not the agents' output
- Without a `schema`, an agent answers in prose and `result.pass` doesn't exist
- The script itself has no file access; agents do the reading and writing
- Anything non-deterministic in prompts breaks resume

## Related
- Used for:: [[Multi-agent pipeline]]
- Differs from:: [[Subagents]] (model drives the loop), [[Headless Claude Code]] (no session at all)
- Compared in:: [[Subagents vs workflows vs headless]]
- Area:: [[AI agents]]

## Flashcards
#flashcards

What is a Claude Code workflow? :: A JavaScript script in which code, not the model, decides the order of agent steps
Where do saved workflows live? :: .claude/workflows/<name>.js
What does each agent() call start? :: A fresh agent with an empty context
Why pass a schema to agent()? :: So the answer is structured data (e.g. {pass, failures}) the script can branch on
What part of a workflow reaches the main session? :: Only what the script returns
How do you watch a workflow run? :: /workflows
Can a workflow script read files? :: No, only its agents can. That's why agents write HANDOFF.md
Why are Date.now() and Math.random() banned in workflows? :: They'd change the prompts on a rerun, so resume couldn't reuse cached agent results
What does resume do? :: Reruns a failed workflow reusing the cached results of agent() calls that already completed
How is the fix loop bounded in the script? :: A for loop with attempt <= MAX_FIXES (2), then the run stops
