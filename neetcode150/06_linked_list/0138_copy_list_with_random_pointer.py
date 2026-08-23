"""
=====================================================================
LeetCode 138 : Copy List with Random Pointer                 (Medium)
https://leetcode.com/problems/copy-list-with-random-pointer/
Category   : Linked List
---------------------------------------------------------------------
PROBLEM
    A list has TWO pointers per node: `next` and `random` (any node
    of the list, or None). Build a DEEP COPY — new nodes, identical
    values, random pointers into the NEW list.
---------------------------------------------------------------------
INTUITION
    The hard part is remapping random pointers: old-node → new-node.
    Either record the mapping explicitly (hash map) or make it
    IMPLICIT by physically pairing every old node with its clone
    (interleaving) — then cloneOf(old->random) is always the node
    right beside it.
---------------------------------------------------------------------
APPROACH 1 — Interleaving / weave — O(1) space (BEST)
    Pass 1: insert a clone after every node (old→new→old→new…).
    Pass 2: clone.random = old.random.next (the clone beside it).
    Pass 3: unweave: restore old.next, chain the clones.
    Time  Complexity : O(n)   Space Complexity : O(1) extra
---------------------------------------------------------------------
APPROACH 2 — Hash map old → new
    Pass 1: create all clones, record old→new. Pass 2: wire next
    and random through the map.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Copy-on-write caches and serialization of graph-like objects
      (document object models, game worlds) — deep copying graphs
      with cross-links uses exactly this remapping problem.
    • "Undo" snapshots that must clone object graphs.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import Optional


class Node:
    """Random-pointer list node: val, next, random."""

    def __init__(self, val: int = 0, next: Optional["Node"] = None,
                 random: Optional["Node"] = None) -> None:
        self.val = val
        self.next = next
        self.random = random


# =====================================================================
# APPROACH 1 : Interleaving — clone woven beside each original (best)
# =====================================================================
class Solution_Interleave:
    """
    Purpose : Deep-copy a random-pointer list using O(1) extra space.
    Inputs  : head — first node of the original list.
    Output  : Head of the deep copy (identical values + random).
    """

    def copyRandomList(self, head: Optional[Node]) -> Optional[Node]:
        if head is None:
            return None

        # PASS 1 — weave: old → NEW → old → NEW → …
        cur = head
        while cur is not None:
            cur.next = Node(cur.val, cur.next)   # clone born beside it
            cur = cur.next.next                  # jump to next old node

        # PASS 2 — random wiring: clone's random = old.random's clone,
        # and the clone of any node lives at node.next.
        cur = head
        while cur is not None:
            if cur.next is not None:
                cur.next.random = cur.random.next if cur.random is not None else None
            cur = cur.next.next

        # PASS 3 — unweave: restore old chain, chain up the clones.
        copy_head = head.next
        cur = head
        while cur is not None:
            clone = cur.next
            cur.next = clone.next if clone is not None else None   # restore old
            if clone is not None:
                clone.next = clone.next.next if clone.next is not None else None
            cur = cur.next
        return copy_head


# =====================================================================
# APPROACH 2 : Hash map old node → new node
# =====================================================================
class Solution_HashMap:
    """
    Purpose : Deep-copy a random-pointer list with a hash map.
    Inputs  : head — first node of the original list.
    Output  : Head of the deep copy.
    """

    def copyRandomList(self, head: Optional[Node]) -> Optional[Node]:
        if head is None:
            return None

        # Pass 1: create every clone; record old → clone mapping.
        old_to_new: dict[Node, Node] = {}
        cur = head
        while cur is not None:
            old_to_new[cur] = Node(cur.val)
            cur = cur.next

        # Pass 2: wire next + random through the map (O(1) each).
        cur = head
        while cur is not None:
            clone = old_to_new[cur]
            clone.next = old_to_new[cur.next] if cur.next is not None else None
            clone.random = old_to_new[cur.random] if cur.random is not None else None
            cur = cur.next

        return old_to_new[head]


# =====================================================================
# BENCHMARK — 3 tests, both approaches, time + peak memory
# =====================================================================
if __name__ == "__main__":
    # (values, random target OFFSET per node, -1 = None)
    tests: list[tuple[list[int], list[int]]] = [
        ([7, 13, 11, 10, 1], [-1, 0, 4, 2, 0]),
        ([1, 2, 3], [2, 0, 1]),
        ([42], [-1]),
    ]

    def make_list(values: list[int], random_idx: list[int]) -> tuple[list[Node], Node]:
        """Build a random-pointer list; return (node_array, head)."""
        nodes = [Node(v) for v in values]
        for i, n in enumerate(nodes):
            n.next = nodes[i + 1] if i + 1 < len(nodes) else None
            n.random = nodes[random_idx[i]] if random_idx[i] >= 0 else None
        return nodes, nodes[0]

    def verify(orig: list[Node], copy: Optional[Node], random_idx: list[int]) -> bool:
        """Values equal, random OFFSETS equal, and no shared nodes.
        Random targets live in the COPY, so the position map is built
        by walking the copy chain itself."""
        pos: dict[Node, int] = {}
        i = 0
        c = copy
        while c is not None:
            pos[c] = i
            i += 1
            c = c.next
        c = copy
        for idx, o in enumerate(orig):
            if c is None or o is c:               # SHARED node → not deep
                return False
            if o.val != c.val:
                return False
            got = -1 if c.random is None else pos.get(c.random, -999)
            if got != random_idx[idx]:
                return False
            c = c.next
        return c is None

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok1 = True
    for values, ridx in tests:
        nodes, head = make_list(values, ridx)
        copy = Solution_Interleave().copyRandomList(head)
        ok1 = verify(nodes, copy, ridx) and ok1
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok2 = True
    for values, ridx in tests:
        nodes, head = make_list(values, ridx)
        copy = Solution_HashMap().copyRandomList(head)
        ok2 = verify(nodes, copy, ridx) and ok2
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("0138 Copy List with Random Pointer")
    print(f"Approach 1 (interleave) : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (hash map)   : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches produced deep copies with correct random pointers."
          if ok1 and ok2 else "FAIL : at least one copy was wrong or shared nodes.")
