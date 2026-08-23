"""
=====================================================================
LeetCode 25 : Reverse Nodes in k-Group                        (Hard)
https://leetcode.com/problems/reverse-nodes-in-k-group/
Category   : Linked List
---------------------------------------------------------------------
PROBLEM
    Reverse the nodes of a list k AT A TIME; the leftover tail
    (fewer than k nodes) stays as it is.
        1→2→3→4→5, k=2  →  2→1→4→3→5
        1→2→3→4→5, k=3  →  3→2→1→4→5
---------------------------------------------------------------------
INTUITION
    Cut the list into k-node blocks; each block is reversed with the
    exact prev/cur flip from 0206, then the blocks are sewn back
    together: block tail → next block head. A dummy node carries the
    pointer to the first group's new head.
---------------------------------------------------------------------
APPROACH 1 — Iterative, dummy + anchored segment flips (BEST)
    Peek k nodes ahead (fewer → stop, tail untouched); flip exactly
    k nodes after cursor; sew tail→next-group and cursor→new-head;
    cursor jumps to the block's old head (now its tail).
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Recursive per group
    Reverse first k nodes; recurse on the remainder; sew this
    group's tail to the next group's reversed head.
    Time  Complexity : O(n)   Space Complexity : O(n/k) stack
---------------------------------------------------------------------
REAL LIFE
    • Block-wise transforms of page chains (pagination caches).
    • Batch reordering in distributed queues: reverse chunks of
      k records at a time, sew the stream back.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import Optional


class ListNode:
    """Minimal singly linked list node used by every test below."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def build_list(values: list[int]) -> Optional[ListNode]:
    """Turn a Python list into a linked list; returns the head."""
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> list[int]:
    """Walk a linked list back into a Python list (for verification)."""
    out: list[int] = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


# =====================================================================
# APPROACH 1 : Iterative — dummy head + anchored segment flips (best)
# =====================================================================
class Solution_Iterative:
    """
    Purpose : Reverse the list in groups of exactly k nodes.
    Inputs  : head — first node of the list; k — group size ≥ 1.
    Output  : Head of the regrouped list (leftover tail unmodified).
    """

    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)         # uniform sewing for group #1
        cursor: Optional[ListNode] = dummy   # node BEFORE current group

        while True:
            # Peek: does a full k-node group remain after cursor?
            probe = cursor
            for _ in range(k):
                probe = probe.next if probe else None
                if probe is None:
                    return dummy.next    # leftover tail stays as-is

            old_head = cursor.next        # becomes the group's TAIL
            prev: Optional[ListNode] = cursor   # flip target starts here
            cur = cursor.next             # first node to flip

            # Flip exactly k nodes (bounded 0206 flip).
            for _ in range(k):
                nxt = cur.next if cur else None   # CACHE successor
                if cur is not None:
                    cur.next = prev               # flip the arrow
                prev = cur
                cur = nxt

            # Sew: old_head (group tail) → next group; cursor → new head.
            if old_head is not None:
                old_head.next = cur
            if cursor is not None:
                cursor.next = prev
            cursor = old_head             # next group starts here


# =====================================================================
# APPROACH 2 : Recursive — reverse first group, recurse on the rest
# =====================================================================
class Solution_Recursive:
    """
    Purpose : Reverse the list in groups of exactly k nodes.
    Inputs  : head — first node of the list; k — group size ≥ 1.
    Output  : Head of the regrouped list.
    Note    : O(n/k) recursion depth.
    """

    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # Probe: are there k nodes from here?
        probe = head
        for _ in range(k):
            if probe is None:
                return head              # fewer than k → keep as-is
            probe = probe.next

        # Reverse exactly k nodes (bounded flip).
        prev: Optional[ListNode] = None
        cur = head
        for _ in range(k):
            nxt = cur.next if cur else None
            if cur is not None:
                cur.next = prev
            prev = cur
            cur = nxt

        # head is now the group's TAIL → point it at the next
        # group's reversed head (recursion).
        if head is not None:
            head.next = self.reverseKGroup(cur, k)
        return prev                      # new head of this group


# =====================================================================
# BENCHMARK — 3 tests, both approaches, time + peak memory
# =====================================================================
if __name__ == "__main__":
    tests: list[tuple[list[int], int]] = [
        ([1, 2, 3, 4, 5], 2),
        ([1, 2, 3, 4, 5], 3),
        ([1, 2], 2),
    ]
    expected: list[list[int]] = [
        [2, 1, 4, 3, 5],
        [3, 2, 1, 4, 5],
        [2, 1],
    ]

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok1 = all(
        to_list(Solution_Iterative().reverseKGroup(build_list(v), k)) == e
        for (v, k), e in zip(tests, expected)
    )
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok2 = all(
        to_list(Solution_Recursive().reverseKGroup(build_list(v), k)) == e
        for (v, k), e in zip(tests, expected)
    )
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("0025 Reverse Nodes in k-Group")
    print(f"Approach 1 (iterative) : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (recursive) : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches regrouped all 3 tests correctly."
          if ok1 and ok2 else "FAIL : at least one test produced a wrong list.")
