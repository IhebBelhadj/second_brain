---
type: subtopic
created: 2026-10-09
topic: Data structures and algorithms
tags: [subtopic, data-structures-and-algorithms]
---
# Data structures and algorithms › Foundations

> What this covers: what everything else builds on: recursion, stack and heap memory, number bases.

Part of [[Data structures and algorithms]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Recursion]]: how to solve recursive problems. My 5-step method made precise (induction, termination), designing the function's parameters, how many calls (linear, divide and conquer, choices), the combine for count/exists/best/list, base cases, cost from the recursion tree, memoization, backtracking and pruning, worked examples, debugging
- [[Stack and heap]]: how long a value must live decides where it lives. Lifetime vs virtual address vs physical frame, C's storage durations, why calls use a stack (frames, the stack pointer, LIFO), recursion and the 8 MiB limit (depth and big local arrays), why a heap (outliving the call, run-time sizes), pointer vs pointee, what survives a return and ownership, a table of C declarations (static, globals, BSS, char s[] vs char *s), costs side by side, Python/Java/Go (references, escape analysis), heap memory vs the heap data structure, and lifetime bugs (dangling pointers, use after free, double free, leaks, stack smashing and canaries)
- [[Number base conversion]]: positional notation, division and Horner's rule, regrouping bits, fractions and why 0.1 isn't exact, two's complement and overflow, bit operations, endianness and network byte order

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
