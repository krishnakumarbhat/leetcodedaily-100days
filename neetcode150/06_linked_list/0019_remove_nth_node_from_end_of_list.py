"""
=====================================================================
LeetCode 19 : Remove Nth Node From End of List               (Medium)
https://leetcode.com/problems/remove-nth-node-from-end-of-list/
Category   : Linked List
---------------------------------------------------------------------
PROBLEM
    Remove the n-th node counting from the END (1-indexed) of a
    singly linked list; return the head.
        1→2→3→4→5, n=2  →  1→2→3→5
---------------------------------------------------------------------
INTUITION
    "n-th from the end" = "n steps before the null at the end".
    Two pointers holding a measuring stick of length n: when the
    right one reaches None, the left one is at the node BEFORE
    the victim. Deleting = skipping (pointer surgery).
---------------------------------------------------------------------
APPROACH 1 — One pass: dummy + fixed-gap two pointers (BEST)
    right walks n steps ahead; both slide until right hits None;
    left.next is the victim; left.next = left.next.next deletes.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Two passes: count, then delete
    Pass 1 counts L nodes; victim is node (L − n + 1) from start;
    walk to its predecessor and skip it.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
REAL LIFE
    • Ring buffers keep a read pointer K bytes behind a write
      pointer — the same fixed-gap window.
    • "Undo N steps" trackers and sliding-window log tails.
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
# APPROACH 1 : One pass — dummy + fixed-gap two pointers (best)
# =====================================================================
class Solution_OnePass:
    """
    Purpose : Delete the n-th node from the end in a single walk.
    Inputs  : head — first node of the list; n — 1-indexed distance
                    from the end (guaranteed ≤ list length).
    Output  : Head of the list with the target node removed.
    """

    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)         # absorbs the delete-head case
        left: Optional[ListNode] = dummy
        right: Optional[ListNode] = dummy

        # Stretch the measuring stick: right jumps n steps first.
        for _ in range(n):
            right = right.next if right else None

        # Slide: gap stays n; right at None → left before the victim.
        while right is not None and right.next is not None:
            left = left.next if left else None
            right = right.next

        # Pointer surgery: bridge over the victim.
        if left is not None and left.next is not None:
            left.next = left.next.next

        return dummy.next


# =====================================================================
# APPROACH 2 : Two passes — count the length, then delete
# =====================================================================
class Solution_TwoPass:
    """
    Purpose : Delete the n-th node from the end using two walks.
    Inputs  : head — first node of the list; n — 1-indexed distance
                    from the end.
    Output  : Head of the list with the target node removed.
    """

    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # Pass 1: measure the total length L.
        length = 0
        cur = head
        while cur is not None:
            length += 1
            cur = cur.next

        # Victim is (L − n + 1)-th from start; walk to its
        # predecessor: the (L − n)-th node. Dummy handles n == L.
        dummy = ListNode(0, head)
        cur = dummy
        for _ in range(length - n):
            cur = cur.next if cur else None

        if cur is not None and cur.next is not None:
            cur.next = cur.next.next       # skip the victim

        return dummy.next


# =====================================================================
# BENCHMARK — 3 tests, both approaches, time + peak memory
# =====================================================================
if __name__ == "__main__":
    tests: list[tuple[list[int], int]] = [
        ([1, 2, 3, 4, 5], 2),
        ([1], 1),
        ([1, 2], 2),
    ]
    expected: list[list[int]] = [[1, 2, 3, 5], [], [2]]

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok1 = all(
        to_list(Solution_OnePass().removeNthFromEnd(build_list(v), n)) == e
        for (v, n), e in zip(tests, expected)
    )
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok2 = all(
        to_list(Solution_TwoPass().removeNthFromEnd(build_list(v), n)) == e
        for (v, n), e in zip(tests, expected)
    )
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("0019 Remove Nth Node From End of List")
    print(f"Approach 1 (one pass) : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (two pass) : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches removed the right node on all 3 tests."
          if ok1 and ok2 else "FAIL : at least one test produced a wrong list.")
