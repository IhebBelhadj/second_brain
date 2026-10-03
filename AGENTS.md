# Second brain: guide for agents

An **Obsidian vault** of study notes. The owner is working toward **systems engineer**; the **AWS certification** is the current milestone, not the end goal. Notes are written in the owner's voice (first person) as learning material with flashcards.

**Don't read the vault from scratch.** Use the lookup order below and open only what the task needs.

## Lookup order

1. **This file**: layout and conventions
2. **The area guide** `Areas/<Area>/AGENTS.md`: which folder holds what, and the file name of every note in the area
3. **The topic index** `Areas/<Area>/<Area>.md`: every note with a one-line summary, in reading order. It's also what the owner uses to study, so it's always kept up to date
4. **Search, don't browse**. Notes also answer to their `aliases:` (e.g. `[[OSI model]]` opens `Network layers.md`):
   ```bash
   grep -rl --include='*.md' -i "^aliases:.*\bNAT\b" Areas      # find a note by alias
   grep -rn --include='*.md' "^## " "Areas/Networking/DNS/DNS.md"  # a note's section headings, before reading it all
   grep -rln --include='*.md' "\[\[VPN\]\]" Areas               # who links to a note (impact of a change)
   ```

## Vault layout

| Folder | Holds | State |
|---|---|---|
| `Home.md` | Dashboard: Dataview queries (weakest notes, inbox, projects, topics). Don't hand-edit the queries | |
| `How this works.md` | The owner's own manual for the system: folders, templates, properties. Read it before restructuring anything | |
| `Areas/` | Subjects built up over time, **one folder per subject** with a topic index | **Where almost everything is**: `Networking/`, `AWS/`, `Storage/`, `Messaging/`, `Containers/`, `Data structures and algorithms/` |
| `Inbox/` | Undecided captures | Nearly empty |
| `Journal/` | Daily/weekly notes | Empty |
| `Notes/` | The owner's own ideas | Empty |
| `Projects/` | Things with a deadline | Empty |
| `Resources/` | Books, courses, articles (other people's material) | Empty |
| `Archive/` | Finished or abandoned | Empty |
| `Templates/` | Templater templates (`<% tp.… %>` syntax). **Never put real notes here**, and keep the `<% %>` tags intact | |
| `Attachments/` | Images embedded with `![[file.png]]`. `Excalidraw/` for drawings | |
| `.obsidian/` | Obsidian config and plugins. Don't touch unless asked | |
| `.claude/scripts/` | Agent tooling (hidden from Obsidian) | |

### Areas right now

| Area | Guide | Index | Scope |
|---|---|---|---|
| Networking | `Areas/Networking/AGENTS.md` | `Areas/Networking/Networking.md` | **Vendor-neutral** networking as a systems engineer needs it: layers, L2, L3, DNS, security, proxies/LB, VPNs. Ordered as a learning path |
| AWS | `Areas/AWS/AGENTS.md` | `Areas/AWS/AWS.md` | AWS services for the certification, and how the Networking concepts map onto AWS products |
| Storage | `Areas/Storage/AGENTS.md` | `Areas/Storage/Storage.md` | **Vendor-neutral** storage: block/file/object, filesystems, RAID, network storage, backups, distributed storage. Ordered as a learning path. Mostly a roadmap so far |
| Messaging | `Areas/Messaging/AGENTS.md` | `Areas/Messaging/Messaging.md` | **Vendor-neutral** messaging: queues, pub/sub, event streaming (Kafka), delivery guarantees, event-driven patterns. Ordered as a learning path. Mostly a roadmap so far |
| Containers | `Areas/Containers/AGENTS.md` | `Areas/Containers/Containers.md` | **Vendor-neutral** containers: building, tagging and shipping images, running containers, internals, orchestration. AWS container services (ECS, Fargate, ECR) stay in the AWS area and are linked from the index |
| Data structures and algorithms | `Areas/Data structures and algorithms/AGENTS.md` | `Areas/Data structures and algorithms/Data structures and algorithms.md` | Data structures, algorithms, techniques and practice problems, with Python code. Ordered as a learning path |

A new subject gets its own `Areas/<Subject>/` folder with an index note `<Subject>.md` (type `topic`, from `Templates/Topic.md`), its own `AGENTS.md` and `CLAUDE.md`, and a row in the table above.

## Note conventions

**Frontmatter** (every note under `Areas/`):
```yaml
---
type: concept        # concept | compare | procedure | note | topic | event | person | source | practice | mistake
created: 2026-09-27  # YYYY-MM-DD
topic: Networking    # = the area's index note name. Drives the index's "Weakest first" query
confidence: 1        # 1 (can't explain it) → 5 (could teach it). The OWNER rates this: new notes start at 1, never raise it for them.
                     # Only on types whose template has it (not note/procedure/topic): check Templates/<Type>.md
tags: [networking, dns]
aliases: [DNS records, dig]   # optional: other names people link with
---
```

**Names and links:**
- The file name **is** the note's title and its link target: `[[Load balancing]]`. File names must be **unique across the vault** (links don't include folders)
- Aliases must not match another note's name or alias
- Section links `[[DNS#Caching and TTL]]` match the heading text exactly. **Keep headings plain** (no `*emphasis*` or links in headings), and grep for `[[Note#Old heading` before renaming a heading
- A link to a note that doesn't exist yet is written in italics, `*[[IPv6]]*`: it marks a **planned** note (a roadmap item), not a broken link
- In tables, escape the pipe in aliased links: `[[IPsec and IKE\|IPsec]]`
- **Never refer to files outside the vault** (code directories, paths like `~/projects/…`, `.py` file names): Obsidian can't open them and the note stops being self-contained. Quote the relevant code inline instead

**Structure of a knowledge note** (a default, not a mold: pick what the topic needs. A technique or problem-solving note like [[Recursion]] is organized around *how to solve*):
1. `> [!abstract] In one sentence` callout
2. **Build-up**: start from the **situation and the problem**, the way a person would explain it: a concrete scenario (named hosts, real-looking IPs from the documentation ranges `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, or private ranges), each stage fixing the previous one's problem
3. **Misconceptions are never the opener.** Don't start a note with a "Common misconceptions" section: it reads like a template, not like a person explaining. Correct a wrong mental model **where it naturally bites**, inside the build-up (a short `> [!warning]` or a sentence at the stage where it causes the problem), or in a short section **after** the build-up when there are several worth collecting. Only real, common ones. Frame them neutrally, **never as the owner's past** (no "The misconceptions I had", "I thought…", "I mixed them up for weeks"): invented memories don't help studying
4. **Advanced problems**: real failure modes, their symptoms, and the fix
5. For cloud-applicable topics, a section on how a cloud (AWS) does it **at the end**, never as the frame of a Networking note
6. Optional **Practice** with collapsed answers: `> [!example]- Question` + answer lines
7. `## Easy to get wrong` bullets
8. `## Related` with Dataview inline fields: `- Depends on:: [[X]], [[Y]]`
9. `## Flashcards`, then `#flashcards` on its own line, then one card per line: `Question? :: Answer` (the Spaced Repetition plugin reads this exact syntax)

Older notes still open with "Common misconceptions": leave them unless the owner asks for a rewrite, but don't copy that shape into new notes.

**Style:**
- Plain and human. First person is fine for the scenario and advice ("I add a queue", "what I'd do"), but don't invent what the owner thought, felt or did in the past. Explain *why*, not just *what*
- **Mermaid** for anything with branches, sequences or several boxes (flowcharts, sequence diagrams). No ASCII art for complex diagrams. Colours only through `classDef` with explicit text colours, so the diagram stays readable in light and dark themes
- Tables for comparisons. Callouts: `[!abstract]`, `[!tip]`, `[!warning]`, `[!info]`, `[!note]`, `[!example]-`, `[!question]`
- Keep Networking notes vendor-neutral. Put AWS specifics in the AWS area and link across

## When adding or changing notes

1. Put the note in the right `Areas/<Area>/<folder>/` (see the area guide). Folders say what a note is *for*, and the `topic` property says what it's *about*
2. Fill in the frontmatter above
3. Add it to the **topic index** (right section, one-line summary). If it fills a planned `*[[X]]*` item, replace that item
4. Add its file name to the **area guide's** folder map
5. Link it from the closest existing notes (their `## Related`), and link back
6. Run the checker and fix what it reports:
   ```bash
   python3 .claude/scripts/vault_check.py
   ```
   It reports unresolved links, broken `#heading` links, duplicate names/aliases, missing frontmatter, and notes missing from their area index or guide. Planned italic links are listed but aren't errors
7. **Don't commit.** The obsidian-git plugin commits automatically ("vault backup: <date>"). Only use git if the owner asks

Mermaid can't be rendered in this environment (no browser): check syntax carefully and tell the owner to look at new diagrams in Obsidian.
