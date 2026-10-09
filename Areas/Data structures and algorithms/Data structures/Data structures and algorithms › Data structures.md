---
type: subtopic
created: 2026-10-09
topic: Data structures and algorithms
tags: [subtopic, data-structures-and-algorithms]
---
# Data structures and algorithms › Data structures

> What this covers: linked lists, hash tables, trees.

Part of [[Data structures and algorithms]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Linked list]]: cost model and cache locality, a method for rewiring pointers, sentinels (Linux `list_head`), reversal, two-pointer techniques with Floyd's proof, LRU cache, skip lists, and the bugs in my implementation
- [[Hash table]]: hashing vs compression, the hash/equality contract, chaining vs open addressing (probe math, tombstones), resizing and amortization, Python/Java/Swiss table internals, hash flooding, partitioning, the shared-bucket bug
- [[Binary search tree]]: the interval invariant, search/insert/delete with proofs, successor/floor/range/LCA, order statistics, height and rotations, AVL/red-black/B+ trees, BST vs hash table

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
