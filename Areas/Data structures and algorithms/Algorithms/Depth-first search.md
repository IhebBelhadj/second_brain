---
type: concept
created: 2026-10-02
topic: Data structures and algorithms
confidence: 1
tags: [dsa, algorithms, graphs, dfs, trees]
aliases: [DFS, Tree traversal, Pre-order traversal, In-order traversal, Post-order traversal, Topological order, Cycle detection]
---
# Depth-first search

> [!abstract] In one sentence
> Depth-first search follows one path as deep as it can, then **backtracks** to the most recent node with unexplored edges, using the call stack or an explicit LIFO stack, in **O(V + E)**. What makes DFS more than "a traversal" is the **structure it records**: each node has a discovery time and a finish time, and the moment a node *finishes* (after all its descendants) is what powers cycle detection, topological sorting, strongly connected components, bridges, and every post-order computation on trees.

## 1. Recursive DFS and the timestamps

```python
def dfs_all(graph):
    WHITE, GRAY, BLACK = 0, 1, 2          # unvisited / on the current path / finished
    state = {u: WHITE for u in graph}
    tin, tout, clock = {}, {}, [0]

    def visit(u):
        state[u] = GRAY
        tin[u] = clock[0]; clock[0] += 1
        for v in graph[u]:
            if state[v] == WHITE:
                visit(v)
        state[u] = BLACK
        tout[u] = clock[0]; clock[0] += 1

    for u in graph:                        # every component
        if state[u] == WHITE:
            visit(u)
    return tin, tout
```

- **Discovery** (`tin`): when the node turns gray, i.e. enters the recursion stack
- **Finish** (`tout`): when all its descendants are done and it turns black

**Parenthesis structure**: for any two nodes u, v, the intervals `[tin, tout]` are either nested (one is a descendant of the other in the DFS tree) or disjoint. Never partially overlapping. That's what makes the edge classification below sound.

Cost: each node turns gray and black once, each edge is examined once from its tail: **O(V + E)**. Memory: the recursion depth, up to V on a long path (Python's limit is ~1000, see [[Recursion]]).

## 2. Edge classification

When DFS at u examines an edge u → v, the state of v says what kind of edge it is:

| v's state | Edge type | Meaning |
|---|---|---|
| WHITE | **Tree edge** | v is discovered through u |
| GRAY | **Back edge** | v is an ancestor still on the stack: **a cycle** |
| BLACK, `tin[u] < tin[v]` | **Forward edge** | v is an already-finished descendant |
| BLACK, `tin[v] < tin[u]` | **Cross edge** | v is in another, finished branch |

**A directed graph has a cycle iff DFS finds a back edge.** A plain visited set can't tell a back edge (cycle) from a cross or forward edge (two paths merging), which is why directed cycle detection needs the **three** states.

In an **undirected** graph only tree and back edges exist, and every edge appears in both directions, so the edge back to the **parent** must be ignored: a cycle is an edge to an already-visited node **other than the parent**.

```python
def has_cycle_undirected(graph):
    seen = set()
    def visit(u, parent):
        seen.add(u)
        for v in graph[u]:
            if v == parent:
                continue
            if v in seen or visit(v, u):
                return True
        return False
    return any(u not in seen and visit(u, None) for u in graph)
```

(With parallel edges between the same pair, skip the parent **edge** by edge ID instead of by node.)

## 3. Topological sort

A topological order of a DAG lists every node before all nodes it points to (every task after its prerequisites). **Reverse finish order** is one: when u finishes, everything reachable from u has already finished, so u must come before them.

```python
def topological_order(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    state = {u: WHITE for u in graph}
    order = []
    def visit(u):
        state[u] = GRAY
        for v in graph[u]:
            if state[v] == GRAY:
                raise ValueError("cycle: no topological order")
            if state[v] == WHITE:
                visit(v)
        state[u] = BLACK
        order.append(u)                    # post-order
    for u in graph:
        if state[u] == WHITE:
            visit(u)
    return order[::-1]
```

Dressing example (`shirt → tie → jacket`, `pants → shoes`, `pants → jacket`, `socks → shoes`) gives `socks, pants, shoes, shirt, tie, jacket`: every arrow points forward.

The BFS alternative, **Kahn's algorithm**: repeatedly output a node with in-degree 0 and decrement its successors' in-degrees. If nodes remain with nonzero in-degree, there's a cycle. It's iterative (no recursion limit) and naturally gives "layers" of tasks that can run in parallel. More in *[[Topological sort]]*.

## 4. Iterative DFS

Recursion depth is a real limit in Python, so production DFS is often iterative. The simple correct version pushes neighbors and checks `visited` **when popping**:

```python
def dfs_iterative(graph, start):
    visited, order = set(), []
    stack = [start]
    while stack:
        u = stack.pop()
        if u in visited:
            continue                       # a node can be pushed several times
        visited.add(u)
        order.append(u)
        for v in reversed(graph.get(u, ())):   # reversed → same order as recursive
            if v not in visited:
                stack.append(v)
    return order
```

The stack can hold O(E) entries (a node pushed once per incoming edge). For pre-order traversal that's fine. For algorithms that need **finish times** (topological sort, SCC, bridges), this version isn't enough: a node finishes when all its children are done, so the stack must hold `(node, iterator over its neighbors)` frames and only pop a node when its iterator is exhausted, exactly what the call stack does.

## 5. Tree traversals

On a tree there are no cycles, so no visited set. The three depth-first orders differ only in **when the node is handled relative to its subtrees**, and the choice follows from what the computation needs:

| Order | Sequence | Use it when the node needs… | Examples |
|---|---|---|---|
| **Pre-order** | node, left, right | …information **from its ancestors** (passed down) | Copy/serialize a tree, print a directory listing, pass depth or bounds down ([[Binary search tree]] validation) |
| **In-order** | left, node, right | …to be between its subtrees in **sorted** order | BST sorted output, k-th smallest |
| **Post-order** | left, right, node | …results **from its children** (returned up) | Height, size, diameter, freeing memory, `du` (directory size = sum of children), evaluating expression trees |

For the BST from 4, 2, 6, 1, 3, 5, 7: pre-order 4 2 1 3 6 5 7, in-order 1 2 3 4 5 6 7, post-order 1 3 2 5 7 6 4.

Iterative in-order (useful for BST iterators that yield one key at a time):

```python
def inorder_iterative(root):
    out, stack, node = [], [], root
    while stack or node:
        while node:                        # go as far left as possible
            stack.append(node)
            node = node.left
        node = stack.pop()                 # leftmost unvisited
        out.append(node.key)
        node = node.right                  # then its right subtree
    return out
```

## 6. What else DFS solves

| Problem | DFS idea | Cost |
|---|---|---|
| **Connected components** (undirected) / flood fill / counting islands | One DFS per unvisited node, each marks one component | O(V + E) |
| **Path existence** between s and t | DFS from s, stop at t (any path, not the shortest) | O(V + E) |
| **Bridges and articulation points** (edges/nodes whose removal disconnects the graph) | `low[u]` = smallest `tin` reachable from u's subtree with one back edge. Tree edge u → v is a bridge iff `low[v] > tin[u]` | O(V + E) |
| **Strongly connected components** (directed) | Tarjan (low-link, one pass) or Kosaraju (DFS, then DFS on the reversed graph in decreasing finish order) | O(V + E) |
| **Backtracking** (permutations, sudoku, n-queens) | DFS over an implicit tree of choices ([[Recursion]]) | Size of the search tree |

Counting islands on `["110", "100", "011"]` gives 2. Bridges on a triangle 1-2-3 with a tail 3-4-5 are (3, 4) and (4, 5): the triangle's edges each lie on a cycle, the tail's don't.

```python
def bridges(graph):
    tin, low, out, clock = {}, {}, [], [0]
    def dfs(u, parent):
        tin[u] = low[u] = clock[0]; clock[0] += 1
        for v in graph[u]:
            if v == parent:
                continue
            if v in tin:                           # back edge
                low[u] = min(low[u], tin[v])
            else:                                  # tree edge
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:                # v's subtree can't climb above u
                    out.append((u, v))
    for u in graph:
        if u not in tin:
            dfs(u, None)
    return out
```

Bridges and articulation points are literally "single points of failure" in a network topology.

## 7. DFS vs BFS

| | DFS | [[Breadth-first search]] |
|---|---|---|
| Frontier structure | Stack (LIFO) | Queue (FIFO) |
| Order | Deep first, backtrack | By distance |
| Shortest paths (unweighted) | No | **Yes** |
| Memory | O(depth) recursion (+ visited) | O(width of the widest level) |
| Finish times, ancestor/descendant structure | **Yes** (cycles, topo sort, SCC, bridges) | No |
| Infinite or huge implicit graphs | Can dive forever down one branch (use depth limits / iterative deepening) | Finds shallow solutions first |

## 8. In systems

- **Dependency resolution and build ordering**: make, Bazel, package managers, Terraform's resource graph, systemd units: topological order, and cycle detection to report circular dependencies
- **Deadlock detection**: a cycle in the wait-for graph between transactions or threads (databases check this and abort one victim)
- **Garbage collection**: mark phase from the roots (mark-and-sweep is typically DFS with an explicit mark stack)
- **Filesystem walks**: `find`, `du`, `rm -r` (post-order: children before the directory)
- **Network resilience**: bridges and articulation points are links/routers whose failure partitions the network. Loop detection in layer 2 topologies is the problem [[Spanning Tree]] solves

## 9. Bugs in my implementations

I wrote iterative DFS twice. The first version:

```python
while call_stack:
    node = call_stack.pop()
    if node in visited: pass       # never skips, and nothing is ever added to visited
    print(node)
    for neighbor in graph[node]:
        call_stack.append(neighbor)
```

The second version (marks on push):

```python
while len(stack) > 0:
    current = stack.pop()
    print(current)
    for neighbor in g[current]:
        if neighbor in visited: pass   # still pushes it below
        visited.add(neighbor)
        stack.append(neighbor)
```

| Version | Bug | Effect | Fix |
|---|---|---|---|
| First | `pass` instead of `continue`, and `visited.add` never called | Every pop is processed: duplicates on DAGs (a node reachable by two paths is printed twice), **infinite loop** on any cycle | `continue`, then `visited.add(node)` |
| Second | `pass` instead of `continue` | Visited neighbors are pushed again: duplicates, infinite loop on cycles | `continue` (or push only `if v not in visited`) |
| Recursive | `graph[node]` with a node that has no key | `KeyError` on nodes that only appear as neighbors | `graph.get(node, ())` |

Marking on push (second version), once fixed, visits every node but not always in true depth-first order: a node can be claimed by an early push before a deeper path reaches it. Harmless for traversal, wrong for anything that depends on DFS structure (finish times, back edges).

## Practice

> [!example]- Directed graph `a → b, b → c, c → a, c → d`. Which edge does DFS from a classify as a back edge?
> c → a: when DFS at c examines a, a is gray (still on the path a, b, c). That back edge proves the cycle a → b → c → a.

> [!example]- Topological order of `A → C, B → C, C → D, B → E` by reverse finish order, visiting nodes in the order A, B, C, D, E.
> DFS(A): C, then D. D finishes, C finishes, A finishes. DFS(B): C done, E finishes, B finishes. Finish order D, C, A, E, B → reversed: B, E, A, C, D.

> [!example]- Why does undirected cycle detection skip the parent, and directed detection need three colors?
> Undirected: each edge appears both ways, so the edge back to the parent would look like a cycle. Directed: reaching a finished (black) node just means two paths merge; only reaching a node still on the current path (gray) is a cycle.

> [!example]- Which traversal computes the size of every subtree, and why?
> Post-order: a node's size is 1 + its children's sizes, which must be computed first.

> [!example]- In a network graph, how do I find links whose failure splits the network?
> Bridges via DFS low-link values: tree edge u → v is a bridge iff low[v] > tin[u], i.e. nothing in v's subtree has a back edge reaching u or above.

## Related
- Counterpart:: [[Breadth-first search]]
- Built with:: [[Recursion]], *[[Stacks and queues]]*, [[Hash table]] (visited/state maps)
- Trees:: [[Binary search tree]]
- Next:: *[[Topological sort]]*, *[[Backtracking]]*, *[[Graph representations]]*
- Systems:: [[Spanning Tree]]
- Area:: [[Data structures and algorithms]]

## Flashcards
#flashcards

DFS cost? :: O(V + E) time, O(depth) recursion memory
What do discovery and finish times record? :: When a node enters the recursion stack and when all its descendants are done
Parenthesis property of DFS intervals? :: Two nodes' [tin, tout] intervals are nested (ancestor/descendant) or disjoint, never overlapping
Tree, back, forward, cross edges? :: Tree: to a white node. Back: to a gray ancestor. Forward: to a black descendant. Cross: to a black node in another branch
When does a directed graph have a cycle? :: Iff DFS finds a back edge (to a gray node)
Why isn't a visited set enough for directed cycle detection? :: Reaching a finished node can be two paths merging, not a cycle
Undirected cycle detection rule? :: An edge to an already-visited node other than the parent
How does DFS give a topological order? :: Reverse of the finish order
What is Kahn's algorithm? :: Topological sort by repeatedly removing in-degree-0 nodes; leftovers mean a cycle
Why can't the simple iterative DFS compute finish times? :: It pops a node before its children are done; finish times need (node, neighbor iterator) frames
Pre-order, in-order, post-order: when to use each? :: Pre: info flows down from ancestors. In: sorted order of a BST. Post: results flow up from children
What is a bridge? :: An edge whose removal disconnects the graph: tree edge u→v with low[v] > tin[u]
Two algorithms for strongly connected components? :: Tarjan (low-link, one DFS) and Kosaraju (DFS, then DFS on the reversed graph by decreasing finish time)
DFS vs BFS memory? :: DFS: O(depth). BFS: O(widest level)
In iterative DFS, what must the visited check do? :: continue, not pass
