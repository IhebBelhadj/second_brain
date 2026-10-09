---
type: concept
created: 2026-10-02
topic: Data structures and algorithms
subtopic: Data structures and algorithms › Algorithms and problems
confidence: 1
tags: [dsa, algorithms, graphs, bfs]
aliases: [BFS, Level-order traversal, Multi-source BFS, Bidirectional BFS, 0-1 BFS]
---
# Breadth-first search

> [!abstract] In one sentence
> Breadth-first search explores a graph from a source in **increasing order of distance** (number of edges), using a FIFO queue and a visited set, in **O(V + E)**. That ordering is the whole point: the first time BFS reaches a node, it has found a **shortest path** to it in an unweighted graph, and the same machinery extends to many sources at once, to weights of 0 and 1, to searching from both ends, and to graphs whose "nodes" are states of a puzzle.

## 1. The algorithm and its invariant

```python
from collections import deque

def bfs(graph, source):
    dist = {source: 0}
    parent = {source: None}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in graph.get(u, ()):
            if v not in dist:              # discovered for the first time
                dist[v] = dist[u] + 1
                parent[v] = u
                queue.append(v)            # mark on enqueue
    return dist, parent
```

**Invariant**: at any moment, the queue holds nodes whose distances are **non-decreasing from front to back** and span **at most two consecutive values** (d and d + 1). Nodes leave the queue in order of distance, so they are processed level by level.

**Why the first discovery is a shortest path**: suppose v is first discovered from u, so `dist[v] = dist[u] + 1`. Any other path to v ends with an edge from some w with `dist[w] ≥ dist[u]` (w is processed after u, or at the same level), so it's no shorter. Formally by induction on distance: all nodes at distance k are dequeued before any node at distance k + 1, and each discovers its undiscovered neighbors at k + 1.

**Why mark on enqueue, not on dequeue**: a node with several neighbors in the current level would be enqueued once per neighbor. The result is still correct, but the queue can grow to O(E) instead of O(V), and every duplicate is processed again.

**Cost**: each node enqueued and dequeued once (O(V)), each adjacency list scanned once (O(E) total, or 2E for undirected): **O(V + E)** with adjacency lists, **O(V²)** with an adjacency matrix (scanning a row costs V). Memory O(V) for `dist`, `parent` and the queue, which can hold an entire level: on a wide graph, the frontier is the memory cost.

### Reconstructing the path

`parent` forms a **BFS tree** rooted at the source; walking it backward from a target gives a shortest path:

```python
def path_to(parent, target):
    if target not in parent:
        return None                       # unreachable
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]
```

### Level-by-level processing

When the answer is "how many rounds" (minutes until everything is infected, the depth of a tree, nodes per level), process one level per outer iteration:

```python
level = 0
while queue:
    for _ in range(len(queue)):           # exactly the nodes of this level
        u = queue.popleft()
        ...                               # enqueue neighbors (next level)
    level += 1
```

## 2. Variants

### Multi-source BFS

Distance from each cell to the **nearest** of several sources (nearest exit, nearest server, fire spreading from several points): put **all sources in the queue at distance 0** at the start. Equivalent to adding a virtual super-source connected to every source, and still O(V + E), instead of one BFS per source.

```python
def nearest_source(grid):                 # 'S' sources, '#' walls, '.' free
    R, C = len(grid), len(grid[0])
    dist = [[None] * C for _ in range(R)]
    q = deque()
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#" and dist[nr][nc] is None:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist
```

On `["S..", "##.", "S.."]` → `[[0,1,2],[–,–,3],[0,1,2]]`. Grids are graphs whose neighbors are computed on the fly, no adjacency list needed.

### BFS over states (implicit graphs)

When the problem has more than a position, the **node is the whole state**: `(row, col, keys_held)`, `(position, remaining_wall_breaks)`, a board configuration, a word in a word ladder. BFS over states finds the fewest moves; the visited set holds states. The cost is O(number of reachable states × moves per state), so the design question is how small the state can be made.

### 0-1 BFS

Edges of weight 0 or 1 (free moves vs paid moves, "turning costs 1, going straight costs 0"): use a **deque**, push weight-0 neighbors to the **front** and weight-1 neighbors to the **back**. The deque keeps the two-consecutive-distances invariant, giving shortest paths in O(V + E) without a priority queue. A node can be improved after discovery, so it relaxes `dist` instead of using a plain visited set:

```python
def zero_one_bfs(graph, s):              # graph[u] = [(v, w)] with w in {0, 1}
    dist = {s: 0}
    dq = deque([s])
    while dq:
        u = dq.popleft()
        for v, w in graph[u]:
            if dist[u] + w < dist.get(v, float("inf")):
                dist[v] = dist[u] + w
                (dq.appendleft if w == 0 else dq.append)(v)
    return dist
```

General non-negative weights need *[[Dijkstra's algorithm]]* (BFS with a priority queue keyed by distance).

### Bidirectional BFS

Searching from both the source and the target and stopping when the frontiers meet explores about **2·b^(d/2)** nodes instead of **b^d** (b = branching factor, d = distance). With b = 10 and d = 6: ~2,000 vs 1,000,000. Expand the **smaller** frontier each round. Needs the target known in advance and edges traversable backward (undirected, or a reverse graph).

### Bipartiteness (2-coloring)

A graph is bipartite iff it has no odd cycle. BFS colors each node opposite to its parent; an edge between two same-colored nodes proves an odd cycle. Run from every uncolored node to cover all components.

```python
def is_bipartite(graph):
    color = {}
    for s in graph:
        if s in color:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True
```

A 4-cycle is bipartite, a triangle isn't.

## 3. Choosing BFS

| Question | Tool |
|---|---|
| Fewest edges / moves / hops, unweighted | **BFS** |
| Nearest of many sources | **Multi-source BFS** |
| Weights 0/1 | **0-1 BFS** |
| Non-negative weights | Dijkstra |
| Negative weights | Bellman-Ford |
| Any path, reachability, cycles, topological order, components with low memory on wide graphs | [[Depth-first search]] |
| Level structure (tree level order, "rounds") | BFS with level loop |

## 4. Where BFS appears in systems

- **Fewest hops** between machines or routers, degrees of separation, minimum number of transfers
- **Flooding and broadcast**: a switch flooding an unknown destination, a gossip protocol, an [[OSPF]] link-state advertisement all spread in BFS-like waves. On a graph with cycles, flooding without a "seen" rule never stops, which is why switched networks need [[Spanning Tree]] and routing protocols use sequence numbers
- **Shortest paths in link-state routing** (OSPF, IS-IS) are Dijkstra, the weighted generalization ([[Routing tables]])
- **Web crawlers** (frontier queue, depth limit), **garbage collectors** (Cheney's copying collector is a BFS over live objects), **peer discovery**, **dependency layers**

## 5. Notes on my implementation

My BFS marks visited on enqueue (correct) but used a plain list and skipped nodes missing from the dict:

```python
current_node = queue.pop(0)
if current_node not in graph: continue
```

- `list.pop(0)` shifts every remaining element: O(n) per dequeue, O(V²) overall. `deque.popleft()` is O(1)
- A node that appears only as a neighbor (no key in the dict) is marked visited but never processed: with `{1: [2]}`, BFS from 1 never visits 2. `graph.get(u, ())` treats it as a node with no out-edges

## Practice

> [!example]- Graph `A: [B, C], B: [D], C: [D, E], D: [F], E: [F], F: []`. BFS distances from A, and the path to F found through `parent`?
> A 0, B 1, C 1, D 2, E 2, F 3. D is discovered from B (B is dequeued before C), F from D: path A → B → D → F.

> [!example]- Minimum minutes for rot to spread to all oranges on a grid, from several rotten ones.
> Multi-source BFS with every rotten orange at distance 0, level-by-level; the answer is the last level reached, or −1 if a fresh orange is never reached.

> [!example]- Shortest path on a grid where you may break at most one wall. What's the node?
> `(row, col, walls_broken)` with walls_broken ∈ {0, 1}: BFS over 2·R·C states.

> [!example]- Why does bidirectional BFS help, and what does it need?
> Two searches of depth d/2 explore about 2·b^(d/2) nodes instead of b^d. It needs a known target and backward-traversable edges.

> [!example]- Moving straight costs 0, turning costs 1. Fewest turns from S to E?
> 0-1 BFS over states `(cell, direction)`: continuing straight is a weight-0 edge (deque front), changing direction weight 1 (back).

## Related
- Counterpart:: [[Depth-first search]]
- Data structures:: *[[Stacks and queues]]*, [[Hash table]] (dist/parent maps)
- On trees:: [[Binary search tree]] (level-order traversal)
- Next:: *[[Dijkstra's algorithm]]*, *[[Graph representations]]*
- Systems:: [[Spanning Tree]], [[Routing tables]]
- Area:: [[Data structures and algorithms]]

## Flashcards
#flashcards

BFS invariant on the queue? :: Distances are non-decreasing front to back and span at most two consecutive values
Why is BFS's first discovery a shortest path? :: Nodes are processed in order of distance, so a node is first reached from a node at the smallest possible distance
BFS cost with adjacency lists vs matrix? :: O(V + E) vs O(V²)
Why mark visited on enqueue? :: Otherwise a node is enqueued once per discovering neighbor (queue up to O(E), duplicate work)
How to reconstruct the shortest path? :: Store parent[v] on discovery, walk back from the target, reverse
How to process BFS level by level? :: Inner loop over len(queue) nodes per level
What is multi-source BFS? :: All sources start in the queue at distance 0: distance to the nearest source in one O(V + E) pass
What is BFS over states? :: Nodes are full states (position + extra info like keys or remaining breaks), visited holds states
How does 0-1 BFS work? :: A deque: weight-0 edges to the front, weight-1 edges to the back, relaxing distances
Benefit of bidirectional BFS? :: About 2·b^(d/2) nodes explored instead of b^d
How does BFS test bipartiteness? :: 2-color by levels; an edge between same colors means an odd cycle
Shortest paths with non-negative weights? :: Dijkstra (BFS with a priority queue)
Why is list.pop(0) wrong for a BFS queue in Python? :: O(n) per dequeue; deque.popleft() is O(1)
