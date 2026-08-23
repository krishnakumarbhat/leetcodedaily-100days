"""
=====================================================================
LeetCode 206 : Reverse Linked List                             (Easy)
https://leetcode.com/problems/reverse-linked-list/
Category   : Linked List
---------------------------------------------------------------------
PROBLEM
    Given the head of a singly linked list, reverse the list and
    return the new head:
        n0 → n1 → n2 → … → nk   becomes   nk → … → n2 → n1 → n0
---------------------------------------------------------------------
INTUITION
    Reversing means rewriting every node's `next` to point at its
    PREVIOUS node. The only trap: overwriting cur.next destroys the
    rest of the chain, so the successor must be cached first.
    (save-next, flip, slide) is the whole algorithm.
---------------------------------------------------------------------
APPROACH 1 — Iterative, 3 sliding pointers (BEST)
    prev=None, cur=head. Loop: nxt=cur.next (cache), cur.next=prev
    (flip), prev=cur, cur=nxt (slide). cur==None → prev is the new
    head. Every arrow flipped exactly once.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Recursive
    Reverse the tail first (recursion returns the new head), then
    wire head.next.next = head and head.next = None. The call stack
    does the "remember the successor" job.
    Time  Complexity : O(n)   Space Complexity : O(n) (stack)
---------------------------------------------------------------------
REAL LIFE
    • LRU caches (0146), hash-table buckets (separate chaining) and
      intrusive allocators all rewrite next pointers this way.
    • "Undo stack" traversal lists in editors: reversing a chain of
      revisions is the same flip.
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
    dummy = ListNode()                    # sentinel removes the empty-case
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
# APPROACH 1 : Iterative with 3 sliding pointers (best)
# =====================================================================
class Solution_Iterative:
    """
    Purpose : Reverse a linked list in place, O(1) extra memory.
    Inputs  : head — first node of the list to reverse.
    Output  : The NEW head (the old last node).
    """

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev: Optional[ListNode] = None   # already-reversed part; new list's end
        cur = head                        # node we are about to flip

        while cur is not None:
            nxt = cur.next                # THE CACHE: save successor first
            cur.next = prev               # THE FLIP: point at previous node
            prev = cur                    # THE SLIDE: advance both pointers
            cur = nxt

        return prev                       # cur fell off → prev is the new head


# =====================================================================
# APPROACH 2 : Recursive — the call stack remembers the successor
# =====================================================================
class Solution_Recursive:
    """
    Purpose : Reverse a linked list recursively.
    Inputs  : head — first node of the list (or sub-list) to reverse.
    Output  : The NEW head of the reversed (sub-)list.
    Note    : O(n) time but O(n) recursion-stack space.
    """

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head                   # empty or 1 node → already reversed

        new_head = self.reverseList(head.next)  # reverse the TAIL first
        head.next.next = head             # old successor points back at head
        head.next = None                  # head becomes the new tail
        return new_head                   # new head bubbles up unchanged


# =====================================================================
# BENCHMARK — both approaches, 3 tests, time + peak memory
# =====================================================================
if __name__ == "__main__":
    tests: list[list[int]] = [
        [1, 2, 3, 4, 5],                  # classic 5-node reverse
        [7],                              # single node → unchanged
        [],                               # empty list → None head
    ]
    expected: list[list[int]] = [
        [5, 4, 3, 2, 1],
        [7],
        [],
    ]

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok1 = all(
        to_list(Solution_Iterative().reverseList(build_list(t))) == e
        for t, e in zip(tests, expected)
    )
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok2 = all(
        to_list(Solution_Recursive().reverseList(build_list(t))) == e
        for t, e in zip(tests, expected)
    )
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"0206 Reverse Linked List")
    print(f"Approach 1 (iterative) : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (recursive) : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches reversed all 3 tests correctly."
          if ok1 and ok2 else "FAIL : at least one test produced a wrong list.")
