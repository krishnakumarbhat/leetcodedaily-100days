"""
=====================================================================
LeetCode 21 : Merge Two Sorted Lists                            (Easy)
https://leetcode.com/problems/merge-two-sorted-lists/
Category   : Linked List
---------------------------------------------------------------------
PROBLEM
    Merge two SORTED linked lists into ONE sorted list.
        1→2→4  merged with  1→3→4  gives  1→1→2→3→4→4
---------------------------------------------------------------------
INTUITION
    Both lists are sorted, so the smallest remaining node is always
    the smaller of the two current heads. Peel that smaller head off
    and append it to the result chain — a merge, not a re-sort.
---------------------------------------------------------------------
APPROACH 1 — Iterative with a dummy head (BEST)
    dummy = sentinel before the result head → no "first append?"
    branch. While both lists live, attach the smaller head; then
    splice the leftover chain with one pointer assignment.
    Time  Complexity : O(n + m)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Recursive
    Empty list → the other list IS the answer. Otherwise the smaller
    head leads and its tail merges with the other list recursively.
    Time  Complexity : O(n + m)   Space Complexity : O(n + m) stack
---------------------------------------------------------------------
REAL LIFE
    • Merge step of merge sort (the classic sort of linked lists).
    • Database query planners merge sorted index runs exactly this way.
    • K-way merge (problem 0023) generalizes it with a heap.
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
# APPROACH 1 : Iterative merge with a dummy head (best)
# =====================================================================
class Solution_DummyNode:
    """
    Purpose : Merge two sorted lists into one sorted list, in place.
    Inputs  : l1, l2 — heads of two ascending singly linked lists.
    Output  : Head of the merged ascending list (O(1) extra space).
    """

    def mergeTwoLists(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()                # sentinel: no first-append branch
        tail = dummy                      # tail of the result chain

        while l1 is not None and l2 is not None:
            if l1.val <= l2.val:
                tail.next = l1            # l1's head wins this round
                l1 = l1.next
            else:
                tail.next = l2            # l2's head wins
                l2 = l2.next
            tail = tail.next              # result chain grows

        # Leftover shortcut: splice the whole remaining chain.
        tail.next = l1 if l1 is not None else l2
        return dummy.next


# =====================================================================
# APPROACH 2 : Recursive merge
# =====================================================================
class Solution_Recursive:
    """
    Purpose : Merge two sorted lists recursively.
    Inputs  : l1, l2 — heads of two ascending singly linked lists.
    Output  : Head of the merged ascending list.
    Note    : O(n + m) time, O(n + m) recursion-stack space.
    """

    def mergeTwoLists(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        if l1 is None:
            return l2                     # empty → the other list IS the result
        if l2 is None:
            return l1
        if l1.val <= l2.val:
            l1.next = self.mergeTwoLists(l1.next, l2)   # l1 leads
            return l1
        l2.next = self.mergeTwoLists(l1, l2.next)       # l2 leads
        return l2


# =====================================================================
# BENCHMARK — 3 tests, both approaches, time + peak memory
# =====================================================================
if __name__ == "__main__":
    tests_a: list[list[int]] = [[1, 2, 4], [], [5]]
    tests_b: list[list[int]] = [[1, 3, 4], [1, 2], []]
    expected: list[list[int]] = [[1, 1, 2, 3, 4, 4], [1, 2], [5]]

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok1 = all(
        to_list(Solution_DummyNode().mergeTwoLists(build_list(a), build_list(b))) == e
        for a, b, e in zip(tests_a, tests_b, expected)
    )
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok2 = all(
        to_list(Solution_Recursive().mergeTwoLists(build_list(a), build_list(b))) == e
        for a, b, e in zip(tests_a, tests_b, expected)
    )
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("0021 Merge Two Sorted Lists")
    print(f"Approach 1 (dummy node) : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (recursive)  : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches merged all 3 tests correctly."
          if ok1 and ok2 else "FAIL : at least one test produced a wrong list.")
