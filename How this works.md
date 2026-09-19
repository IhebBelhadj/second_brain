---
type: guide
tags: []
---
# How this works

[[Home]] is the dashboard. Everything else is these seven folders.

## Folders

| Folder        | What goes in                                                  |
| ------------- | ------------------------------------------------------------- |
| **Inbox**     | Anything you haven't decided about yet. Empty it weekly.      |
| **Journal**   | Daily and weekly notes. A log, not storage.                   |
| **Notes**     | Your own thinking. One idea per note.                         |
| **Projects**  | Things with a deadline and a finish line.                     |
| **Areas**     | Ongoing subjects you're building up — one folder per subject. |
| **Resources** | Other people's stuff: books, courses, articles, videos.       |
| **Archive**   | Finished or abandoned. Out of sight, still searchable.        |

Plus `Templates` and `Attachments` — plumbing, ignore them.

**Folders say what something is *for*. Tags and links say what it's *about*.** Don't build folder trees by subject — put the subject in the `topic` property instead.

## Where do I put it?

Ask in order, stop at the first yes:

1. Not sure yet? → **Inbox**
2. A record of today/this week? → **Journal**
3. Someone else's material? → **Resources**
4. Has a deadline and a finish line? → **Projects**
5. A subject you're building up over time? → **Areas**
6. Your own idea? → **Notes**
7. Over? → **Archive**

## Templates

Creating a note in a folder applies its template automatically.

**Knowledge — pick by the *shape* of the thing, not the subject:**

| Template | For | Works for |
|---|---|---|
| **Concept** | An idea, term, theory, model or tool | *Opportunity cost · Mercantilism · Hash table · Sonata form* |
| **Event** | Something that happened at a time | *The Treaty of Westphalia · The 2008 crash · A product launch* |
| **Person** | Someone worth knowing about | *Keynes · Bismarck · an author you're reading* |
| **Procedure** | How to do something, step by step | *Filing taxes · Deriving a proof · Proofing bread* |
| **Compare** | Two or more things side by side | *Stocks vs bonds · Rome vs Carthage · REST vs GraphQL* |
| **Note** | An idea of your own that fits no box | Anything |

**Working:**

| Template | For |
|---|---|
| **Source** | A book, course, article or video |
| **Topic** | The index page for a subject |
| **Project** | Something with a deadline |
| **Daily** / **Weekly** | The journal and the review |
| **Practice** | A practice test, problem set or exercise session |
| **Mistake** | Something you got wrong |

Insert one manually with `Alt+T` or `<Space>t`.

> [!tip] Don't agonise
> If two templates could fit, take either. **Concept** is the safe default — it handles most things. You can always add a section.

## The two properties that matter

```yaml
topic: <subject>    # what subject this belongs to
confidence: 1       # 1 = can't explain it, 5 = could teach it
```

`topic` groups your notes — set it to whatever you're studying, and a **Topic** note of the same name collects them automatically.

`confidence` is what drives everything. [[Home]] sorts your study queue by it, lowest first. Rate honestly and you never have to decide what to study next.

## Using it for a subject

Works the same whether the subject is a certification, a period of history, personal finance, or a language.

1. Make `Areas/<Subject>/` and a **Topic** note called `<Subject>`.
2. Set `topic: <Subject>` in every note about it.
3. Write notes as you learn, picking the template by shape. Rate `confidence`.
4. Books and courses go in **Resources** with the same `topic`. Pull what matters out into your own notes — a source note that produces nothing taught you nothing.
5. Log practice sessions with **Practice**, and give every real gap its own **Mistake** note.
6. Weekly: empty the inbox, run the **Weekly** review, look at what's still confidence 1–2.

**What that looks like across subjects:**

| Studying | Areas folder | Typical notes |
|---|---|---|
| A cloud certification | `Areas/Cloud/` | Concept per service, Compare for "X vs Y", Practice after each test |
| The French Revolution | `Areas/French Revolution/` | Event per turning point, Person per figure, Compare for competing factions |
| Personal finance | `Areas/Finance/` | Concept per instrument, Procedure for "rebalance a portfolio", Compare for account types |
| A language | `Areas/German/` | Concept per grammar rule, Procedure for conjugation, heavy flashcard use |

The folders, properties and dashboard never change. Only the templates you reach for do.

## Flashcards

Anywhere in a note:

```
#flashcards

Question :: Answer
```

Review them with `Alt+R`. Keep them in the note they came from — the context is the point.

## Callouts

```markdown
> [!abstract] Summary
> [!tip] Rule of thumb
> [!warning] Gotcha
> [!question] Unresolved
```

## Habits

- **Daily** — capture, don't file.
- **Weekly** — inbox to zero, run the review.
- **Monthly** — archive what's finished.

Getting the folder slightly wrong costs nothing. Forgetting to link the note costs you the note.
