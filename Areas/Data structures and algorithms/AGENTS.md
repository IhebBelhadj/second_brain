# Area guide: Data structures and algorithms

**Index:** `Data structures and algorithms.md` is the learning path (8 numbered sections) with a one-line summary of every note and the planned notes as italic links. Read it for *what* a note covers; use this file for *where* it is.

**Scope:** data structures, algorithms, techniques and practice problems, language-agnostic in concept, with Python code. The owner practices in a code directory **outside the vault**. Notes may document real bugs from that code, but must be **self-contained**: quote the relevant snippet inline and never mention file names, paths or the directory, since nothing outside the vault can be linked or opened from Obsidian. Each note ends with where the structure appears in real systems, linking to Networking/Messaging/Storage notes.

## Folder map

```
Data structures and algorithms/
├── Data structures and algorithms.md   topic index (the learning path)
├── Foundations/
│   ├── Recursion.md                    problem-solving guide: function design, number of calls, combine, cost, memo, backtracking
│   └── Number base conversion.md       division/Horner, hex/octal by bit groups, systems uses
├── Data structures/
│   ├── Linked list.md                  singly/doubly/circular, two pointers, dummy head, bugs in my implementation
│   ├── Hash table.md                   collisions, load factor, resizing, the shared-bucket bug
│   └── Binary search tree.md           insert/search/delete, traversals, balance
├── Algorithms/
│   ├── Breadth-first search.md         queue, shortest paths, grids
│   ├── Depth-first search.md           recursion/stack, tree traversals, cycles, bugs in my iterative DFS
│   └── Merge sort.md                   merge, stability, external sort, bugs in my merge
└── Problems/
    └── Arrays and strings problems.md  CtCI ch. 1 (permutation, URLify, palindrome permutation, one away)
```

## Sub-topics

Every note in this area has `subtopic: <index name>` in its frontmatter, and is linked from that sub-topic index (`type: subtopic`, tag `subtopic`). The area index `Data structures and algorithms.md` links every sub-topic index in its "Sub-topics" section.

| Sub-topic index | Lives in | Covers |
|---|---|---|
| `Data structures and algorithms › Foundations.md` | `Foundations/` | what everything else builds on: recursion, number bases |
| `Data structures and algorithms › Data structures.md` | `Data structures/` | linked lists, hash tables, trees |
| `Data structures and algorithms › Algorithms and problems.md` | `Algorithms/` | searching and sorting algorithms, and practice problems |

A new note gets the `subtopic` of the folder it goes in (notes at the area root: see the table), and a line in that sub-topic index as well as in `Data structures and algorithms.md`.

## Where a new note goes

| It's about… | Folder |
|---|---|
| Cost analysis, recursion, bits, number representation (section 1) | `Foundations/` |
| A data structure (sections 2–4) | `Data structures/` |
| An algorithm: traversal, sort, search, shortest path (sections 5–6) | `Algorithms/` |
| A technique: two pointers, backtracking, DP (section 7) | `Foundations/` (or a `Techniques/` folder once 2+ notes) |
| A set of practice problems (section 8) | `Problems/`, one note per book chapter or theme |

The planned notes (roadmap) are the italic `*[[…]]*` links in the index: when writing one, use that exact name so existing links resolve. Notes follow the vault structure, plus a "Bugs in my implementation" section when the owner's code for that topic has real bugs.
