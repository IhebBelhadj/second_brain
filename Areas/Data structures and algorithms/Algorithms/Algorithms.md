---
type: subtopic
created: 2026-10-09
topic: Data structures and algorithms
tags: [subtopic, data-structures-and-algorithms]
---
# Algorithms

> What this covers: searching and sorting algorithms, and practice problems.

Part of [[Data structures and algorithms]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Breadth-first search]]: the queue invariant and shortest-path proof, path reconstruction, levels, multi-source, BFS over states, 0-1 BFS, bidirectional, bipartiteness
- [[Depth-first search]]: discovery/finish times, edge classification, directed vs undirected cycles, topological sort (DFS and Kahn), iterative DFS limits, traversal orders, components, bridges, SCC
- [[Merge sort]]: merge invariant and stability, recurrence and the Ω(n log n) lower bound, bottom-up and linked-list versions, counting inversions, k-way merge and external sorting, Timsort
- [[Arrays and strings problems]]: a 5-step method (input model → brute force → bottleneck → tool → edge cases) applied to CtCI chapter 1, with my versions' failures

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
